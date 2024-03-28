from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def home():
    return render_template("index.html")

@app.route('/assignments.html')
def assignments():
    return render_template("assignments.html")

@app.route('/calendar.html')
def calendar():
    return render_template("calendar.html")

@app.route('/content.html')
def content():
    return render_template("content.html")

@app.route('/feedback.html')
def feedback():
    return render_template("feedback.html")

@app.route('/labs.html')
def labs():
    return render_template("labs.html")

@app.route('/team.html')
def team():
    return render_template("team.html")

if __name__ == '__main__':
    app.run(debug=True)