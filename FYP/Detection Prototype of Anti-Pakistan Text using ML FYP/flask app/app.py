import pickle
import re
import string

import pandas as pd
from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect

sentiment_analyzer_model = pickle.load(
    open(r'E:\Deploying Models updated (2)\Deploying Models updated\Deploying Models\flask app\my_model.pkl', 'rb'))


def cleanText(x):
    x = x.encode('ascii', 'ignore').decode()  # remove emojis
    x = re.sub(r'https*\S+', '', x)  # remove urls
    x = re.sub(r'@\S+', '', x)  # remove mentions
    x = re.sub(r'#\S+', '', x)  # remove hashtags
    x = re.sub(r'\'w+', '', x)
    return x


def preporocess(tweet):
    tweet = [t for t in tweet if t not in string.digits]  # removing digits
    tweet = ''.join(tweet)
    tweet = [t for t in tweet if t not in string.punctuation]  # removing punctuations
    return ''.join(tweet)


app = Flask(__name__)


@app.route('/')
def index():
    # render home.html and when get started button press redirect to /home
    return render_template("index.html")


@app.route('/svm')
def svm():
    return render_template("services.html")


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/s_t', methods=["GET", "POST"])
def s_t():
    if request.method == "POST":
        f = request.files['file']
        limit = int(request.form['limit'])
        f.save(f.filename)
        # f.load(f.filename)
        data = pd.read_csv(f.filename)
        #  data['tweet']=data['tweet'].apply(cleanText)  # cleaning the text using cleanText function , removing hashes , mentions emojis and urls etc
        data['tweet'] = data['tweet'].apply(
            preporocess)  # preprocessing the tweets removing stopwords , punctuations , digits
        data['tweet'] = data['tweet'].apply(lambda x: x.strip())  # removing spaces in the begining of the tweet
        data['tweet'] = data['tweet'].dropna()

        # return f.filename + "file" + str(len(data)) + "<p>" + str( data['tweet'][:10]) + "</p>"
        # preds=[]
        # pred.append(sentiment_analyzer_model.predict([data['tweet'][i]]))
        # for i in range(limit):
        preds = sentiment_analyzer_model.predict(data['tweet'][:limit])

        # result={'tweet':data['tweet'][:limit] ,'prediction':pred}
        result = {}

        for i, j, k in zip(data['tweet'][:limit], preds, data['username'][:limit]):
            if j == 1.0:
                result[i] = ('Anti Pakistan', k)
            else:
                result[i] = ('Not Anti Pakistan', k)
        return render_template("result.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)

