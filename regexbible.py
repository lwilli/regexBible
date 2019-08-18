import json
from flask import Flask, render_template, request, jsonify
from parse_json_bible import regex_search_bibles

app = Flask(__name__, template_folder='./templates')

ERROR_TEMPLATE = "search_results_error.html"
RESULTS_TEMPLATE = "search_results.html"

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/search")
def search():
    regex = request.args.get('regex')
    translations_to_search = json.loads(request.args.get('versions'))

    if len(translations_to_search) == 0:
        return render_template(ERROR_TEMPLATE, error="Please select a translation to search.")
    elif regex.strip() == "":
        return render_template(ERROR_TEMPLATE, error="Please enter something to search.")

    # get regex results
    results = regex_search_bibles(translations_to_search, regex)

    if results:
        return render_template(RESULTS_TEMPLATE, search_results=results, result_count=len(results))
    else:
        return render_template(ERROR_TEMPLATE, error="Your search did not match any verses in the translations " + ", ".join(translations_to_search) + ".")


if __name__ == "__main__":
    app.run(host='0.0.0.0')