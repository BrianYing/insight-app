# from flask import Flask, jsonify, make_response, request, abort
#
# app = Flask(__name__, static_url_path='/public/')
#
# tasks = [
#     {
#         'id': 1,
#         'title': u'Buy groceries',
#         'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
#         'done': False
#     },
#     {
#         'id': 2,
#         'title': u'Learn Python',
#         'description': u'Need to find a good Python tutorial on the web',
#         'done': False
#     }
# ]
#
#
# @app.route('/')
# def root():
#     return app.send_static_file('index.html')
#
#
# @app.route('/todo/api/tasks', methods=['GET'])
# def getTasks():
#     return jsonify({'tasks': tasks})
#
#
# @app.route('/todo/api/addTask', methods=['POST'])
# def add_task():
#     if request.json['title'] == "":
#         abort(400)
#     task = {
#         'id': tasks[-1]['id'] + 1,
#         'title': request.json['title'],
#         'description': request.json.get('description', ""),
#         'done': False
#     }
#     tasks.append(task)
#     return jsonify({'tasks': tasks}), 201
#
#
# @app.route('/todo/api/deleteTask', methods=['POST'])
# def delete_task():
#     task_id = request.json['id']
#     for task in tasks:
#         if task['id'] == task_id:
#             tasks.remove(task)
#             return jsonify({'tasks': tasks}), 201
#
#
# # 404
# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)
#
#
# if __name__ == '__main__':
#     app.run(debug=True)


import urllib.request
from bs4 import BeautifulSoup

from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


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
    stock_price = soup.select('#qwidget_lastsale')
    stock_price = stock_price[0].text.strip()  # strip() is used to remove starting and trailing

    # stock_trend
    if soup.find('div', {'class': 'arrow-green'}):
        stock_trend = 'Trending Up'
    else:
        stock_trend = 'Trending Down'

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
            return jsonify(data.summary)
            # return data.price
        return "No place information is given"


if __name__ == '__main__':
    app.run(debug=True)


# if __name__ == '__main__':
#     comp = 'oxy'
#     # comp = 'gasx'
#
#     data = parse(comp)
#     print(data.price)
