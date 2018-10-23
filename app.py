from flask import Flask, render_template, flash, request
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import names

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        
        # the new phrase in the input box is assigned a variable
        new_input = request.form['new_input']
        
        # start of algorithm
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
                
        final_pos = float(pos)/len(words)
        final_neg = float(neg)/len(words)
        # end of algorithm
        
        return render_template('index3.html', new_input = new_input, final_pos = final_pos, final_neg = final_neg)


    return render_template('index3.html', count = None)

if __name__ == "__main__":
    app.run(host='localhost', debug = True) # Start the app