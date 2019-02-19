import json
import urllib.request
from bs4 import BeautifulSoup

from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

class Data:
    def __init__(self, price, trend, summary, article):
        self.price = price
        self.trend = trend
        self.summary = summary
        self.article = article

    def get_price(self):
        return self.price

    def get_trend(self):
        return self.trend

    def get_summary(self):
        return self.summary

    def get_article(self):
        return self.article


def parse(company):

    quote_page = 'https://www.nasdaq.com/symbol/' + company
    page = urllib.request.urlopen(quote_page)

    soup = BeautifulSoup(page, 'html.parser')

    # stock_price
    stock_price = {}
    price = soup.select('#qwidget_lastsale')
    price = price[0].text.strip()  # strip() is used to remove starting and trailing
    stock_price["price"] = price

    # stock_trend
    stock_trend = {}
    if soup.find('div', {'class': 'arrow-green'}):
        stock_trend["trend"] = 'Trending Up'
    else:
        stock_trend["trend"] = 'Trending Down'

    # summary
    summary_dict = {}
    summary = soup.find('div', {'class': 'row overview-results relativeP'})
    table = summary.find_all('div', {'class': 'table-row'})
    for cell in table:
        info = cell.find_all('div', {'class': 'table-cell'})
        key = info[0].text.strip()
        val = info[1].text.strip()
        summary_dict[key] = val

    # articles
    article_dict = {}
    articles = soup.find('div', {'id': 'CompanyNewsCommentary'})
    a_list = articles.find_all('li')
    for li in a_list:
        title = li.find_all('a')[0].text.strip()
        url = li.find_all('a')[0].get('href')
        article_dict[title] = url

    return Data(stock_price, stock_trend, summary_dict, article_dict)


@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'GET':
        place = request.args.get('place', None)
        if place:
            data = parse(place)
            # res = data.summary
            res = {
                "stock_price": data.price,
                "stock_trend": data.trend,
                "summary": data.summary,
                "news": data.article
            }
            return jsonify(res)
        return "No place information is given"


if __name__ == '__main__':
    app.run(debug=True)
