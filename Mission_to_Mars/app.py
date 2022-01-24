from flask import Flask, render_template
import pymongo
from scrape_mars import scrape 

app = Flask(__name__)

# Setup connection to mongodb
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# connect to mongo db and collection
db = client.mission_to_mars
mars_facts = db.mars_facts

@app.route("/scrape")
def scraping():
    # calling for scrape function from scrape_mars
    data = scrape
    mars_facts.insert(data)

@app.route("/")
def index():
    mars = list(mars_facts.find())
    return render_template("index.html" , mars=mars)

if __name__ == "__main__":
    app.run(debug=True)