from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find record of data from the mongo database
    mars_information = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mission=mars_information)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape_():

    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Insert the record - ERROR HERE
    mongo.db.collection.update_one({}, {"$set": mars_data}, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)