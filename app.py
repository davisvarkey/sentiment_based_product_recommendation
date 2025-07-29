from email import header
from operator import index
from flask import Flask, request, render_template, jsonify
from model import SentimentRecommenderModel


app = Flask(__name__)

sentiment_model = SentimentRecommenderModel()


@app.route('/')
def home():
    return render_template('index.html', active_tab='recommendation')


@app.route('/predict', methods=['POST'])
def prediction():
    # get user from the html form
    user = request.form['userName']
    # get active tab from form
    active_tab = request.form.get('active_tab', 'recommendation')
    # convert text to lowercase
    user = user.lower()
    items = sentiment_model.getSentimentRecommendations(user)

    if(not(items is None)):
        print(f"retrieving items....{len(items)}")
        print(items)
        # data=[items.to_html(classes="table-striped table-hover", header="true",index=False)
        return render_template("index.html", column_names=items.columns.values, row_data=list(items.values.tolist()), zip=zip, active_tab=active_tab)
    else:
        return render_template("index.html", message="User Name doesn't exists, No product recommendations at this point of time!", active_tab=active_tab)


@app.route('/predictSentiment', methods=['POST'])
def predict_sentiment():
    # get the review text from the html form
    review_text = request.form["reviewText"]
    # get active tab from form
    active_tab = request.form.get('active_tab', 'sentiment')
    print(review_text)
    pred_sentiment = sentiment_model.classify_sentiment(review_text)
    print(pred_sentiment)
    return render_template("index.html", sentiment=pred_sentiment, active_tab=active_tab)


if __name__ == '__main__':
    app.run()
