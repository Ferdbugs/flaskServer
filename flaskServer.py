import flask

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def handle_request():
        performance = (flask.request.form['performance'])
        difficulty = (flask.request.form['difficulty'])
        print(performance)
        print(difficulty)
        return "Hello"

app.run(host="0.0.0.0", port=5000, debug=True)
