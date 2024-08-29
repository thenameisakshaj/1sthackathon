from flask import Flask, render_template, request
import requests
from xml.etree import ElementTree as ET

app = Flask(_name_)

# API URLs and Keys
NEWS_API_URL = 'https://newsapi.org/v2/everything'
NEWS_API_KEY = 'YOUR_NEWS_API_KEY'  # Get from https://newsapi.org

RESEARCH_API_URL = 'http://export.arxiv.org/api/query'  # No API key needed for arXiv
BLOG_API_URL = 'https://api.rss2json.com/v1/api.json?rss_url=https://medium.com/feed/tag/'  # No API key required

# Function to fetch blogs, research papers, and news articles
def fetch_results(topic):
    # Fetch Blogs from Medium via RSS to JSON API
    blog_response = requests.get(f'{BLOG_API_URL}{topic}')
    blogs = blog_response.json() if blog_response.status_code == 200 else None

    # Fetch Research Papers from arXiv
    research_response = requests.get(f'{RESEARCH_API_URL}?search_query={topic}&start=0&max_results=5')
    research_papers = research_response.text if research_response.status_code == 200 else None

    # Fetch News Articles from NewsAPI
    news_response = requests.get(f'{NEWS_API_URL}?q={topic}&apiKey={NEWS_API_KEY}')
    news_articles = news_response.json() if news_response.status_code == 200 else None

    # Parsing arXiv XML for research papers
    research_data = []
    if research_papers:
        root = ET.fromstring(research_papers)
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://www.w3.org/2005/Atom}title').text
            link = entry.find('{http://www.w3.org/2005/Atom}id').text
            research_data.append({'title': title, 'url': link})

    return blogs, research_data, news_articles

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        topic = request.form.get('topic')
        blogs, research_papers, news_articles = fetch_results(topic)
        return render_template('index.html', blogs=blogs, research_papers=research_papers, news_articles=news_articles, topic=topic)
    return render_template('index.html')

if _name_ == '_main_':
    app.run(debug=True)