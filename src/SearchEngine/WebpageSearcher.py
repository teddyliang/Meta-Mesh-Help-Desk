# The WebSearcher class is a model that allows users to create a searchable
# database of specific websites. It uses a combination of webscraping and manually
# typed key words to search through the links. Basically like google but only with
# the links you allow.
#
# To use,
#
#   1. Start with instantiating a WebSearcher object, eg: searcher = WebpageSearcher()
#   2. Add any amount of links you want to search, eg: searcher.add_link('http://www.google', keyword='google')
#   3. Once you have added all the links, you can run the search() method, eg: searcher.search('google')


import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Error message from browser when webscraping fails
ERROR_MESSAGE = "Acceptable ! appropriate representation requested resource could found server . error generated Mod_Security ."
# Determines how much the key words matter when searching links
KEYWORD_WEIGHT = 2
# Determines how many results should be returned
SEARCH_LIST_LEN = 5


class WebpageSearcher:
    def __init__(self):
        self.links = []

    def add_link(self, link, keywords=""):
        # webscrape the link
        try:
            processed_link = preprocess_webpage(link)
        except:
            return False

        self.links.append([processed_link, link, preprocess_text(keywords)])
        # Check for Errors
        if (processed_link is None or processed_link == ERROR_MESSAGE or processed_link == ''):
            return False

        return True

    def search(self, query):
        # Use natural language processing to process the query
        processed_query = preprocess_text(query)

        if (processed_query is None or processed_query == ''):
            return []

        # Calculate the similarity between the processed query and each link
        similarities = {}
        for link in self.links:
            processed_link = link[0]
            keywords = link[2]
            similarity = (calculate_similarity(processed_query, processed_link) + calculate_similarity(processed_query, keywords) * KEYWORD_WEIGHT)
            if (similarity > 0):
                similarities[link[1]] = similarity

        # Find the link with the highest similarity
        sorted_links = sorted(similarities, key=similarities.get, reverse=True)

        # Return the most similar link
        return sorted_links[:min(len(sorted_links), SEARCH_LIST_LEN)]


def preprocess_text(text):
    # Tokenize the text into words
    words = nltk.word_tokenize(text)

    # Remove stopwords
    stopwords_list = stopwords.words('english')
    filtered_words = [word for word in words if word.lower() not in stopwords_list]

    # Lemmatize the words
    lemmatizer = WordNetLemmatizer()
    lemmed_words = [lemmatizer.lemmatize(word) for word in filtered_words]

    # Rejoin the words into a single string
    preprocessed_text = " ".join(lemmed_words)
    return preprocessed_text


def preprocess_webpage(url):
    # Scrape the webpage
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Extract the visible text from the webpage
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    webpage_text = u" ".join(t.strip() for t in visible_texts)

    # Preprocess the webpage text
    preprocessed_webpage = preprocess_text(webpage_text)

    return preprocessed_webpage


def calculate_similarity(query, subject):
    # Create a TfidfVectorizer object and fit it to the query and subject
    vectorizer = TfidfVectorizer()
    vectorizer.fit([query, subject])

    # Calculate the cosine similarity between the query and subject vectors
    similarity = cosine_similarity(vectorizer.transform([query]), vectorizer.transform([subject]))[0][0]

    return similarity


def tag_visible(element):
    # Ignore invisible elements (e.g. scripts, styles)
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    return True
