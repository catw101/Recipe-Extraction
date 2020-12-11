from flask import Flask, request, render_template, redirect, url_for
from bs4 import BeautifulSoup
import requests, sys, importlib, re
from urllib.request import Request, urlopen
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from googlesearch import search
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
        new_ingredients = []
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
            #print(tokens_without_sw)
            tokens_without_sw = " ".join(tokens_without_sw)
            new_ingredients.append(tokens_without_sw)
        #return redirect(url_for("ingredients", new_list = new_ingredients, len = len(new_ingredients)))
        #return redirect(url_for("ingredients", new_list = new_ingredients))
        return render_template("ingredients.html", new_list = new_ingredients)
        # link = request.form["link"] 
        # response = requests.get(link, headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
        # source = response.content
        # soup = BeautifulSoup(source, "lxml") 
        # #return "Link " + link
    return render_template("index.html")

@app.route("/test_ingredients", methods=["GET", "POST"]) 
def test_ingredients():
    if request.method == "POST":
        # gets checked items in the list
        checked = request.form.getlist("check")
        sites_list = []
        print(checked)
        for i in range(0, len(checked)-1):
            for j in search (checked[i]+checked[-1],  tld='com', lang='en', tbs='0', safe='off', num=1, start=0, stop=1, country='', extra_params=None, user_agent=None):
                print(j)
                sites_list.append(j)
        return render_template("sites.html", sites_list=sites_list)
    return render_template("test_ingredients.html") 

if __name__ == "__main__":
    app.run(debug=True) 
