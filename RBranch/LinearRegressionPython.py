#RayM.Chan - Linear Regression Model

#First, we create the model using the Sklearn LinearRegression model.
from sklearn.linear_model import LinearRegression
model = LinearRegression()

#Next, we fit the model to our data using the fit method.

%matplotlib inline
import matplotlib.pyplot as plt
import pandas as pd
import os
voice = pd.read_csv(os.path.join('Resources', 'FINALhashedcsv.csv'))
voice.head()

# Assign X (data) and y (target)
X = voice["hash"]
y = voice["toxic"]
# print(X.shape, y.shape)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1, stratify=y)

#Reshape and fit the model
X=X.reshape(-1, 1)
y=y.reshape(-1, 1)
model.fit(X, y)

#We can view the coefficients and intercept of the line from the coef_ and intercept_ attributes. Note that the _ suffix indicates that the attribute is available after model is fit to the data (trained).

print('Weight coefficients: ', model.coef_)
print('y-axis intercept: ', model.intercept_) 


#We can use our model to make predictions.

predictions = model.predict(X)
print(f"True output: {y[0]}")
print(f"Predicted output: {predictions[0]}")
print(f"Prediction Error: {predictions[0]-y[0]}")

# Score the prediction with mse and r2
from sklearn.metrics import mean_squared_error, r2_score
mse = mean_squared_error(y, predictions)
r2 = r2_score(y, predictions)

print(f"Mean Squared Error (MSE): {mse}")
print(f"R-squared (R2 ): {r2}")

#Get the Model Score
model.score(X, y)

#Combine the Prediction Arrays into a dataframe
data=np.column_stack([predictions,y,predictions-y]);
temp=pd.DataFrame(data,columns=["Predicted", "Actual", "Error"])