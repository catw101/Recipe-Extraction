from flask import Flask, request, render_template
from bs4 import BeautifulSoup
import requests, sys, importlib, re
from urllib.request import Request, urlopen
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy

app = Flask(__name__)

importlib.reload(sys)
sys.getdefaultencoding()
nlp = spacy.load('en_core_web_sm') 
excluded_tags = {"VERB", "ADJ"}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        #specific to this link at the moment
        #page = requests.get("https://thecinnaman.com/blog/malaweh-with-scallion-cheddar-cheese")
        ingredients = []
        page = requests.get(request.form["link"])
        #print(page.content)  
        soup = BeautifulSoup(page.content, 'html.parser')
        #print(soup.prettify())
        ing = soup.find("h3", text="ingredients:")
        ing = ing.findNext("ul").find_all("li")
        for elem in ing:
            #print(elem.find("p").text) #prints out the ingredients
            ingredients.append(elem.find("p").text)
        for ingredient in ingredients:
            ingredient = re.sub(r'\d+', '', ingredient)
            ingredient = ingredient.split("(", 1)[0]
            new_ing = []
            for token in nlp(ingredient):
                if token.pos_ not in excluded_tags:
                    new_ing.append(token.text) 
                    ingredient = " ".join(new_ing)
            text_token = word_tokenize(ingredient)
            tokens_without_sw = [word for word in text_token if not word in stopwords.words()]
            for token in tokens_without_sw:
                if len(token) < 3:
                    tokens_without_sw.remove(token)
            print(tokens_without_sw)
        return render_template("ingredients.html")
        # link = request.form["link"] 
        # response = requests.get(link, headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
        # source = response.content
        # soup = BeautifulSoup(source, "lxml")
        # #return "Link " + link

    return render_template("index.html")

@app.route("/ingredients")
def link_route(): 
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
