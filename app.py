from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    mars_info_dict = mongo.db.mars_info_dict.find_one()

    # Return template and data
    return render_template("index.html", mars_info_dict=mars_info_dict)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    
    # Run the scrape function
    mars_info_dict = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_info_dict.update({}, mars_info_dict, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)