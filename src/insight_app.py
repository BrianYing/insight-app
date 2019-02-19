import json
import urllib.request
from bs4 import BeautifulSoup

from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)


class Data:
    def __init__(self, price, trend, summary, article, transcript):
        self.price = price
        self.trend = trend
        self.summary = summary
        self.article = article
        self.transcript = transcript

    def get_price(self):
        return self.price

    def get_trend(self):
        return self.trend

    def get_summary(self):
        return self.summary

    def get_article(self):
        return self.article

    def get_transcript(self):
        return self.transcript


def getAddress(company):

    target_page = "https://www.nasdaq.com/symbol/" + company + "/call-transcripts"
    page = urllib.request.urlopen(target_page)

    soup = BeautifulSoup(page, 'html.parser')

    # transcript address
    addresses = soup.find_all('a', href=True)
    for address in addresses:
        address = address['href']
        if address[:5] == '/aspx':
            return address


def getCall(address):

    quote_page = "https://www.nasdaq.com/" + address
    page = urllib.request.urlopen(quote_page)

    soup = BeautifulSoup(page, 'html.parser')

    transcript = {}
    # time
    call_time = {}
    time = soup.select('#SAarticle > p:nth-child(3)')[0].text.strip()
    call_time["time"] = time
    transcript["time"] = call_time

    # participants
    participants = soup.select('#SAarticle > p')
    p_map = {}
    i = 4
    while participants[i].text.strip() != 'Presentation':
        participant = participants[i].text.strip()
        if participant != 'Conference Call Participants':
            p_map[str(i)] = participant
        i = i + 1
    transcript["participants"] = p_map

    # longest
    max_sp = {}
    speakers = soup.find_all('strong')
    max_len = 0
    i = 0
    while speakers[i].text.strip() != 'Compare to:':
        i = i + 1

    i = i + 1
    max_speaker = speakers[i].text.strip()
    while speakers[i].text.strip() != 'Nasdaq.com':
        speech_len = len(speakers[i].findNext().text.strip())
        if speech_len > max_len:
            max_len = speech_len
            max_speaker = speakers[i].text.strip()
        i = i + 1
    max_sp["max_speaker"] = max_speaker
    transcript['max_speaker'] = max_sp
    return transcript


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

    # call transcript
    address = getAddress(company)
    transcript = getCall(address)

    return Data(stock_price, stock_trend, summary_dict, article_dict, transcript)


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
                "news": data.article,
                "trans": data.transcript
            }
            return jsonify(res)
        return "No place information is given"


if __name__ == '__main__':
    app.run(debug=True)
