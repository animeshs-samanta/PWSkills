# Import necessary libraries
from flask import Flask, render_template
import requests

# Create a Flask app
app = Flask(__name__)

# The Dog API URL
api_url = 'https://api.thedogapi.com/v1/images/search'

# Define the route for the home page
@app.route('/')
def home():
    # Make a request to The Dog API
    response = requests.get(api_url)
    if response.status_code == 200:
        dog_data = response.json()
        dog_image_url = dog_data[0]['url']
    else:
        dog_image_url = "Error fetching dog image."

    return render_template('index.html', dog_image_url=dog_image_url)

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
