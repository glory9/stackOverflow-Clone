from SearchEngine import get_top_questions
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("results.html")


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['query']
        words = search_query.split(" ")
        keywords = [word for word in words if len(word) > 2]
        if len(keywords) > 5:
            keywords = keywords[:5]

        matches = get_top_questions(keywords)

        return jsonify({'questions': matches})


if __name__ == "__main__":
    app.run(debug=True)