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

################
# database
################
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL', '') 
# or "sqlite:///db/toxicwatch_db_v2.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)

# does not work in heroku
class site_inputs(db.Model):
    __tablename__ = 'site_inputs'
    id = db.Column(db.Serial, primary_key=True, autoincrement=True)
    new_input = db.Column(db.Text)
    naivebayes_pos = db.Column(db.Integer)
    naivebayes_neg = db.Column(db.Integer)
    naivebayes_neu = db.Column(db.Integer)
    vader_composite = db.Column(db.Integer)
    vader_pos = db.Column(db.Integer)
    vader_neu = db.Column(db.Integer)
    vader_neg = db.Column(db.Integer)
    vader_toxic = db.Column(db.Text)

#################
# flask routes
#################

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        
        # the new phrase in the input box is assigned a variable
        new_input = request.form['new_input']
        
        ### START A-Model -- Naive Bayes processing
        def word_feats(words):
            return dict([(word, True) for word in words])

        positive_vocab = [ 'awesome', 'outstanding', 'fantastic', 'terrific', 'good', 'nice', 'great', ':)', 'congratulations', 'fun']
        negative_vocab = [ 'bad', 'terrible','useless', 'hate', 'horrible', 'fuck','bloody','asshole','fucker', 'jew', 'stupid','cunt','shit', 'faggot', 'dick', 'pussy', 'gay', 'nazi', 'cocksucker', 'bitch', 'motherfucking','rape']
        neutral_vocab = [ 'i', 'it', 'movie','the','sound','was','is','actors','did','know','words','not', 'crap','sorry']
        discard_vocab = ['I', 'i', 'it', 'the', 'would', 'should', 'could', ]
        toxic_vocab = ['fuck', 'shit', 'suck', 'like', 'bitch', 'ass', 'stupid', 'stop', 'wikipedia']
        severe_vocab = ['fuck', 'bitch', 'suck', 'shit', 'ass', 'asshole', 'dick', 'faggot', 'cunt']
        obscene_vocab = ['fuck','shit','suck','bitch','ass','asshole', 'faggot', 'dick', 'cunt']
        threat_vocab = ['kill', 'die','fuck','ass','hope','shit','rape','death','bitch']
        insult_vocab = ['fuck','bitch','shit','suck','ass', 'asshole','faggot','stupid','idiot']
        identity_vocab =['fuck','gay','faggot','nigger','shit','bitch','ass','like','jew']

        positive_features = [(word_feats(pos), 'pos') for pos in positive_vocab]
        negative_features = [(word_feats(neg), 'neg') for neg in negative_vocab]
        neutral_features = [(word_feats(neu), 'neu') for neu in neutral_vocab]
        discard_features = [(word_feats(dis),'dis') for dis in discard_vocab]
        toxic_features = [(word_feats(tox),'tox') for tox in toxic_vocab]
        severe_features = [(word_feats(sev),'sev') for sev in severe_vocab]
        obscene_features = [(word_feats(obs),'obs') for obs in obscene_vocab]
        threat_features = [(word_feats(thr),'thr') for thr in threat_vocab]
        insult_features = [(word_feats(ins),'ins') for ins in insult_vocab]
        identity_features = [(word_feats(ide),'ide') for ide in identity_vocab]
        
        train_set = negative_features + positive_features + neutral_features + discard_features + toxic_features + severe_features + obscene_features + threat_features + insult_features + identity_features
        
        classifier = NaiveBayesClassifier.train(train_set)
        
#         train1 = "resources/train_sentiment.csv"
        train1 = "https://s3.us-east-2.amazonaws.com/toxicwatch/train_sentiment.csv"
        train_df = pd.read_csv(train1, encoding="ISO-8859-1")
        
        
        comments1 = train_df['comment_text']
        
        # Predict
        neg = 0
        pos = 0
        neu = 0
        tox = 0
        sev = 0
        obs = 0
        thr = 0
        ins = 0
        ide = 0

        positive = []
        negative = []
        neutral = []
        toxic = []
        severe = []
        obscene = []
        threat = []
        insult = []
        identity = []

        #comments = comments1.lower()
        #.split(' ')
        lowercase_input = new_input.lower()
        words = lowercase_input
#         words = comments1 
        
        for word in words:

            # print(word)
            classResult = classifier.classify(word_feats(word))
            if classResult == 'neg':
#                 print(word, 'found neg')
                neg = neg + 1
                #negative.append('neg')
            if classResult == 'pos':
#                 print(word, 'found pos')
                pos = pos + 1
                #positive.append('pos')
            if classResult == 'neu':
#                 print(word, 'found neu')
                neu = neu + 1
                #neutral.append('neu')
            if classResult == 'tox':
#                 print(word, 'found toxic')
                tox = tox + 1
            if classResult == 'sev':
#                 print(word, 'found severe')
                sev = sev + 1
            if classResult == 'obs':
#                 print(word, 'found obscene')
                obs = obs + 1
            if classResult == 'thr':
#                 print(word, 'found threat')
                thr == thr + 1
            if classResult == 'ide':
#                 print(word, 'found identity')
                ide == ide + 1
                
#         a_final_pos = float(pos)/len(words)
#         a_final_neg = float(neg)/len(words)
#         a_final_neu = float(neu)/len(words)
#         a_final_tox = float(tox)/len(words)
#         a_final_sev = float(sev)/len(words)
#         a_final_obs = float(obs)/len(words)
#         a_final_thr = float(thr)/len(words)
#         a_final_ide = float(ide)/len(words)

        # 10/25/18 PROBLEM: everything from a_final_tox to a_final_ide displays 0 all the time. why?        
        a_final_pos = pos
        a_final_neg = neg
        a_final_neu = neu
        a_final_tox = tox
        a_final_sev = sev
        a_final_obs = obs
        a_final_thr = thr
        a_final_ide = ide
        ### END A-Model
               
        ### START J-Model -- VADER Sentiment Analysis
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
            is_toxic = "Not Toxic!"
            is_toxic_db = "non-toxic"
        elif compound < 0: 
            is_toxic = "Yes!"
            is_toxic_db = "toxic"
        else:
            is_toxic = "Too neutral to tell!"
            is_toxic_db = "neutral"
        
        ### END J-Model
        
        # START R-Model
            # Machine Learning to be placed here
        # END R-Model
        
        #does not work in heroku
        db_dict = {'new_input': new_input,
                 'naivebayes_pos': a_final_pos,
                 'naivebayes_neg': a_final_neg,
                 'naivebayes_neu': a_final_neu,
                 'vader_composite': j_final_comp,
                 'vader_pos': j_final_pos,
                 'vader_neu': j_final_neu,
                 'vader_neg': j_final_neg,
                 'vader_toxic': is_toxic_db
                }
        
        new_info = site_inputs(**db_dict)
        db.session.add(new_info)
        db.session.commit()
        
        return render_template('index.html', 
                               new_input = new_input, 
                               a_final_pos = a_final_pos, 
                               a_final_neg = a_final_neg, 
                               a_final_neu = a_final_neu, 
                               a_final_tox = a_final_tox, 
                               a_final_sev = a_final_sev, 
                               a_final_obs = a_final_obs, 
                               a_final_thr = a_final_thr, 
                               a_final_ide = a_final_ide, 
                               j_final_comp = j_final_comp, 
                               j_final_pos = j_final_pos, 
                               j_final_neu = j_final_neu, 
                               j_final_neg = j_final_neg, 
                               is_toxic = is_toxic)


    return render_template('index.html', count = None)

@app.route("/about")
def about():
    """Return the about page."""
    return render_template("about.html")

@app.route("/models")
def models():
    """Return the models page."""
    return render_template("models.html")

@app.route("/research")
def research():
    """Return the research page."""
    return render_template("research.html")

@app.route("/data")
def data():
    """Return the data page."""
    return render_template("data.html")

@app.route("/roadmap")
def roadmap():
    """Return the roadmap page."""
    return render_template("roadmap.html")


if __name__ == "__main__":
#     app.run(host='localhost', debug = True) # Start the app
    app.run(debug=True)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True