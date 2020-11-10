from flask import Flask, request, render_template
from bs4 import BeautifulSoup
import requests, sys, importlib
from urllib.request import Request, urlopen

app = Flask(__name__)

importlib.reload(sys)
sys.getdefaultencoding()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        link = request.form["link"]
        response = requests.get(link, headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
        source = response.content
        soup = BeautifulSoup(source, "lxml")
        print(soup)
        #return "Link " + link
        ingredients = ""
        tag = soup.find_all('div', {'class': 'entry clearfix'})
        print(tag)
        #ingredients = ingredients + "\n" + tag.find('ul')
        #print(ingredients)

    return render_template("index.html")
@app.route("/link")
def link_route(): 
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
