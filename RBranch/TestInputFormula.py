
# coding: utf-8

# In[29]:
#Raymond M. Chan - Linear Regression Toxicity NLP


def hashPredict(testVar,testToxic):

	# testVar = input("Input sentence without special characters and in all lowercase (IE !,.,?,$,@).")

	# testToxic = input("Input 0 if you think it's not toxic, 1 if you think what you said is toxic")


	# In[30]:


	testToxic=int(testToxic)
	# type(testToxic)


	# In[31]:


	from pyspark import SparkFiles
	import pandas as pd
	import hashlib
	df = pd.read_csv("Resources/CleanedToxicTrainFinal.csv")
	# df.tail()


	# In[32]:
	print("Appending Please Wait!. . . \n")

	df=df.append({'id':'test', 'comment_text':testVar,'toxic':testToxic}, ignore_index=True)
	# df.tail()

	print("Appended!\n")

	# In[33]:
	print("Stop Words Removal Please Wait!. . . \n")

	from nltk.corpus import stopwords
	import nltk
	nltk.download('stopwords')
	stop = stopwords.words('english')
	# type(df)
	df['comment_text'] = df['comment_text'].str.lower().str.split()
	df['comment_text'] = df['comment_text'].apply(lambda x: [item for item in x if item not in stop])
	# df.tail()

	print("Stop Words Removed!\n")

	# In[34]:
	print("Hashing Please Wait!. . . \n")

	import hashlib
	for index, row in df.iterrows():
	#         print(index)
	        sent = ''
	        for item in row['comment_text']:
	            sent +=item
	#         print(sent)
	        temp1 = hashlib.md5(sent.encode('utf-8'))
	        temp2 = int(temp1.hexdigest(),16)
	        df.loc[index,'hash'] = temp2


	# In[35]:
	print("Hashed! Phew that took awhile!\n")

	df.tail()


	# In[36]:
	print("Modeling Please Wait!. . . \n")

	import matplotlib.pyplot as plt
	import numpy as np
	import pandas as pd

	from sklearn.linear_model import LinearRegression
	model = LinearRegression()
	model

	# Assign X (data) and y (target)
	X = df["hash"]
	y = df["toxic"]
	print(X.shape, y.shape)


	# In[37]:


	from sklearn.model_selection import train_test_split

	X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1, stratify=y)


	# In[38]:


	X=X.reshape(-1, 1)
	y=y.reshape(-1, 1)
	model.fit(X, y)
	print(model)


	# In[39]:

	print(' ________MODEL_RESULTS_DATA___________ \n')
	print('Weight coefficients: ', model.coef_)
	print('y-axis intercept: ', model.intercept_) 
	print(' ____________________________________\n')

	# In[40]:


	predictions = model.predict(X)
	print(f"True output: {y[0]}")
	print(f"Predicted output: {predictions[0]}")
	print(f"Prediction Error: {predictions[0]-y[0]}")
	print(' ______________________________________ \n')

	# In[41]:


	from sklearn.metrics import mean_squared_error, r2_score
	# Score the prediction with mse and r2
	mse = mean_squared_error(y, predictions)
	r2 = r2_score(y, predictions)

	print(f"Mean Squared Error (MSE): {mse}")
	print(f"R-squared (R2 ): {r2}")
	print(' _______________________________________ \n')

	# In[42]:


	data=np.column_stack([predictions,y,predictions-y]);
	temp=pd.DataFrame(data,columns=["Predicted", "Actual", "Error"])


	# In[49]:


	temp.tail()


	# In[51]:


	output=temp.iloc[-1,:]


	# In[55]:


	predictedOutput=output[0]
	actualOutput=output[1]
	errorOutput=output[2]


	if(round(predictedOutput)==0):
	    result='That is not Toxic, keep it up! :)'
	else: 
	    result='That is Toxic cut that out! >:('


	return result



testinput1 = input("Please input sentence without special characters and in all lowercase (IE !,.,?,$,@):\n")
testinput2 = input("Input 0 if you think it's not toxic, 1 if you think what you said is toxic: \n")

print(hashPredict(testinput1,testinput2))

