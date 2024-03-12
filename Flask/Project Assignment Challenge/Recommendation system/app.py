from flask import Flask, render_template, request

app = Flask(__name__)

content_data = {
    'movie1': ['action', 'thriller'],
    'movie2': ['comedy', 'romance'],
    'movie3': ['action', 'drama'],
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_preferences = request.form.getlist('preferences')
    recommended_content = get_recommendations(user_preferences)
    return render_template('recommendations.html', recommendations=recommended_content)

def get_recommendations(user_preferences):
    recommended_content = []
    for content, genres in content_data.items():
        if any(genre in user_preferences for genre in genres):
            recommended_content.append(content)
    return recommended_content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
