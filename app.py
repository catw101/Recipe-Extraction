from flask import Flask, request, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        link = request.form['link']
        site = requests.get(link)
        source = site.content
        soup = BeautifulSoup(source, 'lxml')
        print(soup)
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
