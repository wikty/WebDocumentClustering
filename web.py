import json
import requests
from flask import Flask, Response, jsonify, request
from flask import send_from_directory, render_template, redirect, url_for
import classify

app = Flask(__name__)

def bing_api(q):
	url = 'https://api.cognitive.microsoft.com/bing/v5.0/search'
	key1 = '9f8921c7d658477dac16545bc114e2f5'
	key2 = '6c82dfe0f7e2477b8cfaf7d13e3a6012'
	headers = {
		'Ocp-Apim-Subscription-Key': key1,
		'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM;'
	}
	params = {
		'q': str(q),
		'responseFilter': 'webpages',
		'count': 50,
		'mkt': 'en-US'
	}
	l = []
	r = requests.get(url, params, headers=headers)
	result = r.json()
	for item in result['webPages']['value']:
		t = {
			'name': item['name'],
			'displayUrl': item['displayUrl'],
			'snippet': item['snippet'],
			'url': item['url'],
			'id': item['id'].split('.')[-1]
		}
		l.append(t)
	return l

# @app.route("/h5/js/<path:path>")
# def send_js(path):
# 	return send_from_directory('js', path)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/q")
def q(query=None):
	query = request.args.get('query')
	removenode = request.args.get('query')
	if query:
		l = bing_api(query)
		if removenode:
			checked = "checked"
			categories = classify.get_categories(l, True)
		else:
			checked = ""
			categories = classify.get_categories(l, False)
		return render_template('results.html', categories=categories, oldquery=query, checked=checked)
	return redirect(url_for('index'))

@app.route("/raw", methods=['GET'])
def api():
	l = bing_api('http protocol')
	for t in l:
		filename = 'data/test'+t['id']+'.txt'
		with open(filename, 'w', encoding='utf-8') as f:
			f.write(json.dumps(t))
	response = jsonify(l)
	return response

if __name__ == '__main':
	app.run()