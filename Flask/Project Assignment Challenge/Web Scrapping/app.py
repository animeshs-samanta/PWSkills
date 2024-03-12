from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests

app=Flask(__name__)

def scrape_youtube(query):
    url=f"https://www.youtube.com/results?search_query={query}"
    response=requests.get(url)
    soup=BeautifulSoup(response.text,'html.parser')
    video_titles=[title.text for title in soup.select('.yt-lockup-title a')]
    return video_titles

def scrape_amazon(query):
    url=f"https://www.amazon.com/s/?field-keywords={query}"
    response=requests.get(url)
    soup=BeautifulSoup(response.text,'html.parser')
    product_titles=[title.text for title in soup.select('.s-title-instructions h2 span')]
    return product_titles

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search/<query>')
def search(query):
    youtube_results=scrape_youtube(query)
    amazon_results=scrape_amazon(query)
    return render_template('results.html',query=query,youtube_results=youtube_results,amazon_results=amazon_results)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000)
    