from flask import Flask, render_template, redirect
from flask_pymongo import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# set database (used this first time to create db)
db=client.mars_db


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_results = db.mars_results.find()

    # Return template and data
    return render_template("index.html", mars_results=mars_results)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # drop any data that is already in database
    db.mars_data.drop()
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    db.mars_data.insert_one(mars_data)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)



