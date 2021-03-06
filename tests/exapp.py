from flask import Flask, request, render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        link = request.form["link"]
        site = requests.get(link)
        source = site.content
        soup = BeautifulSoup(source, "lxml")
        print(link)
        return "Link " + link

    return render_template("index.html")
@app.route("/link")
def link_route():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
