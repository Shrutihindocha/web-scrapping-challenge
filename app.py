from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape 

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars_facts.find_one()
    return render_template("index.html" , mars=mars)

@app.route("/scrape")
def scraping():
    # calling for scrape function from scrape_mars
    mars_facts = mongo.db.mars_facts
    data = scrape()
    mars_facts.update({}, data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)