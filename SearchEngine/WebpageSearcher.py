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

ERROR_MESSAGE = "Acceptable ! appropriate representation requested resource could found server . error generated Mod_Security ."
KEYWORD_WIEGHT = 2
SEARCH_LIST_LEN = 1


class WebpageSearcher:
    def __init__(self):
        self.links = []

    def add_link(self, link, keywords=""):
        # webscrape the link
        processed_link = preprocess_webpage(link)

        # Check for Errors
        if (processed_link == ERROR_MESSAGE or processed_link == None or processed_link == ''):
            return False, processed_link
        
        self.links.append([processed_link, link, preprocess_text(keywords)])
        return True, processed_link

    def search(self, query):
        # Use natural language processing to process the query
        processed_query = preprocess_text(query)

        # Calculate the similarity between the processed query and each link
        similarities = {}
        for link in self.links:
            processed_link = link[0]
            keywords = link[2]
            similarity = (calculate_similarity(processed_query, processed_link) +
                        calculate_similarity(processed_query, keywords) * KEYWORD_WIEGHT)
            if (similarity > 0):
                similarities[link[1]] = similarity

        if len(similarities) == 0:
            return "no result"

        # Find the link with the highest similarity
        sorted_links = sorted(similarities, key=similarities.get, reverse=True)
        most_similar_link = sorted_links[0]

        # Return the most similar link
        if len(sorted_links) > SEARCH_LIST_LEN:
            return sorted_links[:SEARCH_LIST_LEN]
        else:
            return sorted_links

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
