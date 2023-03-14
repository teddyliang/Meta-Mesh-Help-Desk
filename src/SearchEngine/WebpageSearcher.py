import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from rake_nltk import Rake
from bs4 import BeautifulSoup
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

TOP_N_KEYWORDS = 4

class WebpageSearcher:
    def __init__(self):
        self.links = []

    def add_link(self, link):
        self.links.append(link)

    def search(self, query):
        # Use natural language processing to process the query
        processed_query = preprocess_text(query)

        # Calculate the similarity between the processed query and each link
        similarities = {}
        for link in self.links:
            processed_link = preprocess_webpage(link)
            link_keywords = get_keywords(processed_link)
            similarity = calculate_similarity(processed_query, processed_link)
            similarities[(link, link_keywords)] = similarity

        # Find the link with the highest similarity
        sorted_links_with_keywords = sorted(similarities, key=similarities.get, reverse=True)
        most_similar_link_with_keywords = sorted_links_with_keywords[0]
        print("###############", most_similar_link_with_keywords)

        # Return the most similar link, or "no result" if no matching link is found
        if similarities[most_similar_link_with_keywords] == 0:
            return "no result", ""
        else:
            # Get keywords as string
            return most_similar_link_with_keywords

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

def calculate_similarity(query, webpage):
    # Create a TfidfVectorizer object and fit it to the query and webpage
    vectorizer = TfidfVectorizer()
    vectorizer.fit([query, webpage])

    # Calculate the cosine similarity between the query and webpage vectors
    similarity = cosine_similarity(vectorizer.transform([query]), vectorizer.transform([webpage]))[0][0]

    return similarity

def tag_visible(element):
    # Ignore invisible elements (e.g. scripts, styles)
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    return True

def get_keywords(query):
    # Create rake object to extract the top keywords from query
    rake_object = Rake()
    rake_object.extract_keywords_from_text(query)
    top_keywords = rake_object.get_ranked_phrases()[:TOP_N_KEYWORDS]

    # Return top keywords as string separated by commas
    print("!!!!!", top_keywords)
    return ', '.join(top_keywords)

