import os

# data science dependencies
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# ML dependencies
import nltk
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import names
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# flask dependencies
from flask import Flask, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#################
# flask routes
#################

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        
        # the new phrase in the input box is assigned a variable
        new_input = request.form['new_input']
        
        ### START A-Model
        def word_feats(words):
            return dict([(word, True) for word in words])

        positive_vocab = [ 'awesome', 'outstanding', 'fantastic', 'terrific', 'good', 'nice', 'great', ':)' ]
        negative_vocab = [ 'bad', 'terrible','useless', 'hate', 'horrible', ':(' , 'fuck','bloody','asshole','fucker']
        neutral_vocab = [ 'i', 'it', 'movie','the','sound','was','is','actors','did','know','words','not' ]
        discard_vocab = ['I', 'i', 'it']

        positive_features = [(word_feats(pos), 'pos') for pos in positive_vocab]
        negative_features = [(word_feats(neg), 'neg') for neg in negative_vocab]
        neutral_features = [(word_feats(neu), 'neu') for neu in neutral_vocab]
        discard_features = [(word_feats(dis),'dis') for dis in discard_vocab]
        
        train_set = negative_features + positive_features + neutral_features + discard_features
        
        classifier = NaiveBayesClassifier.train(train_set) 
        
        neg = 0
        pos = 0
        neu = 0
        lowercase_input = new_input.lower()
        words = lowercase_input.split(' ')
        
        for word in words:

            # print(word)
            classResult = classifier.classify(word_feats(word))
            if classResult == 'neg':
                print(word, 'found neg')
                neg = neg + 1
            if classResult == 'pos':
                print(word, 'found pos')
                pos = pos + 1
            if classResult == 'neu':
                print(word, 'found neu')
                neu = neu + 1
                
        a_final_pos = float(pos)/len(words)
        a_final_neg = float(neg)/len(words)
        ### END A-Model
               
        ### START J-Model Analyzing
        analyzer = SentimentIntensityAnalyzer()
        
        # Variables for holding sentiments
        compound_list = []
        positive_list = []
        negative_list = []
        neutral_list = []
        results = []
        # Run Vader Sentiment Analysis on Each of the comments

        # Run Vader Analysis on each Sample
        results = analyzer.polarity_scores(new_input)
        compound = results["compound"]
        pos = results["pos"]
        neu = results["neu"]
        neg = results["neg"]
        compound_list.append(compound)
        positive_list.append(pos)
        negative_list.append(neg)
        neutral_list.append(neu)

        # Print Samples and Analysis
        print(new_input)
        print("Compound Score:", compound)
        print("Positive Score:", pos)
        print("Neutral Score:", neu)
        print("Negative Score: ", neg)
            
        j_final_comp = compound
        j_final_pos = pos
        j_final_neu = neu
        j_final_neg = neg
        
        if compound > 0:
            is_toxic = "Nope!"
        elif compound < 0: 
            is_toxic = "Yes!"
        else:
            is_toxic = "Too neutral to tell!"
        
        ### END J-Model
        
        # START R-Model
        
        # END R-Model
        
        return render_template('index3.html', 
                               new_input = new_input, 
                               a_final_pos = a_final_pos, 
                               a_final_neg = a_final_neg,
                               j_final_comp = j_final_comp,
                               j_final_pos = j_final_pos, 
                               j_final_neu = j_final_neu, 
                               j_final_neg = j_final_neg,
                               is_toxic = is_toxic
                              )


    return render_template('index3.html', count = None)

if __name__ == "__main__":
    app.run(host='localhost', debug = True) # Start the app