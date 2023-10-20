# Toxicwatch

## Purpose

Toxicwatch aims to save the world from the toxicity that is prevalent throughout the online community. Starting with a fixed data set, our goal is to train a machine to monitor and determine toxicity levels of user comments across numerous platforms of internet communication.


The objective of Toxicwatch was to make an API that uses a Machine Learning model to categorize a newly input phrase as 'toxic' or 'non-toxic.' The dataset we used was from the [Kaggle Toxic Comment Classification Challenge](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge). 

This dataset included Wikipedia comments that were categorized into one of several categories related to toxicity and severity.

Our goal was to use this dataset to train a Machine Learning model by using Natural Language Processing techniques to assign values to the dataset's phrases and having it return whether or not a newly input phrase is toxic or non-toxic. 

With one variable (Hash Values) we chose to go with the Linear Regression Model, because we expected to use a continuously updating model to train. The objective is to use the hash values to determine of pattern of toxicity within comments.

Our mission is to help make the internet a safer place for all!

## Tools Used

* Jupyter Notebook
* NLTK
* VADER Sentiment Analysis
* Scikit-learn
* SQLite
* SQLAlchemy
* Flask
* HTML5
* CSS
* Heroku
* Heroku PostgreSQL

The original conception of Toxicwatch was inspired by [Perspective API](http://perspectiveapi.com/#/), a project created by Jigsaw, an Alphabet Inc. subsidiary.

## Results

Our website was deployed on Heroku: [Toxicwatch](https://toxicwatch.herokuapp.com) (expired in Jan. 2023)

As of Version 1.0 (October 25, 2018), the website does not apply a Machine Learning model to a sentence. It does, however, make a Naive Bayes Classification and VADER Sentiment Analysis.

It also stores all text entered into a PostgreSQL database provided by Heroku, privately accessible by this project's administrators on [Heroku Dataclips](https://dataclips.heroku.com/clips). Please don't submit any personal information into our Heroku site!

## Presentation
Project members were Jason, Raymond, Joe, and Christine.

Project presentation was delivered on Thursday, October 25, 2018.
