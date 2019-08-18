import json
from flask import Flask, render_template, request, jsonify
from parse_json_bible import regex_search_bibles

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/search")
def search():
    regex = request.args.get('regex')
    translations_to_search = json.loads(request.args.get('versions'))

    # get regex results
    results = regex_search_bibles(translations_to_search, regex)

    if len(translations_to_search) == 0:
    	return "<div>Please select a translation to search.</div>"
    elif results:
        return render_template('search_results.html', search_results=results, result_count=len(results))
    else:
        return "<div>Your search did not match any verses in the translations " + ", ".join(translations_to_search) + ".</div>"