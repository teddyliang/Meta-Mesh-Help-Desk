'''
The WebSearcher class is a model that allows users to create a searchable
database of specific websites. It uses a combination of webscraping and manually
typed key words to search through the links. Operates similar to Google but with a user-defined
corpus.

To use,
    1. Start with instantiating a WebSearcher object, eg: searcher = WebpageSearcher()
    2. Add any amount of links you want to search, eg: searcher.add_link('http://www.google', keyword='google')
    3. Once you have added all the links, you can run the search() method, eg: searcher.search('google')
'''

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup
import requests
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from helpdesk_app.models import AnswerResource
from django.db.utils import OperationalError

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Error message from browser when webscraping fails
ERROR_MESSAGE = "Acceptable ! appropriate representation requested resource could found server . error generated Mod_Security ."
# Determines how much the key words matter when searching links
KEYWORD_WEIGHT = 2
# Determines how many results should be returned
SEARCH_LIST_LEN = 5
# There are two methods of finding search results, use the tags matching built-in functionality or cosine similarity developed
# in this class, this variable determines which method to use. (In development for now)
USE_TAGS = False
# Used for regex cleaning of input, all non-alphanumeric characters are removed expected these, the underlying algorithm for getting
# search results has trouble with some characters so most most non-alphanumberic characters are remoed
CHARACTERS_TO_KEEP_LIST = " ?!@#$%&()."


class WebpageSearcher:
    def __init__(self):
        try:
            self.links = AnswerResource.objects.all()

            for link in self.links:
                try:
                    link.content = preprocess_webpage(link.url)
                    link.save()
                except:
                    '''could not webscrape the link'''
                    pass
        except OperationalError:
            # When first initializing views.py, it's possible that the database doesn't exist yet.
            # In these cases, Django will throw an OperationalError when trying to init the WebpageSearcher as
            # the call to AnswerResource will be invalid. In these cases, it's fine to pass.
            pass

    def update_search_engine(self):
        # Webscrape the link
        self.links = AnswerResource.objects.all()

        for link in self.links:
            try:
                link.content = preprocess_webpage(link.url)
                link.save()
            except:
                '''could not webscrape the link'''
                pass

    def search(self, query, category_object):
        # Use natural language processing to process the query
        processed_query = preprocess_text(query)
        if (processed_query is None or processed_query == ''):
            return []

        # Use the tags similarity method to find the best match
        if USE_TAGS:
            # Techncial limitation: we need to create an object to be able to compare it to other objects with similar tags
            comparable = AnswerResource()
            comparable.tags = processed_query
            comparable.url = "https://amazon.com/"
            comparable.save()

            sorted_links = comparable.tags.similar_objects()
            if len(sorted_links) == 0:
                return []

        else:
            # Calculate the similarity between the processed query and each link
            similarities = {}
            for link in self.links:
                processed_link = link.content
                keywords = " ".join(link.tags.names())
                similarity = (calculate_similarity(processed_query, processed_link) + calculate_similarity(processed_query, keywords) * KEYWORD_WEIGHT)
                if (similarity > 0):
                    similarities[link] = similarity

            if len(similarities) == 0:
                return []

            # Find the link with the highest similarity
            sorted_links = sorted(similarities, key=similarities.get, reverse=True)

        # Filter by category, if applicable
        if category_object is not None:
            sorted_links = [resource for resource in sorted_links if category_object in list(resource.categories.all())]

        # Return the most similar link
        return sorted_links[:min(SEARCH_LIST_LEN, len(sorted_links))]


def preprocess_text(text):
    # clean input with regex
    text = re.sub(r'[^\w' + CHARACTERS_TO_KEEP_LIST + ']', '', text)

    # Tokenize the text into words
    words = nltk.word_tokenize(text)
    # Remove stopwords
    stopwords_list = stopwords.words('english')

    # add all singlular charcters to stopwords list
    for i in range(33, 127):
        stopwords_list.append(chr(i))

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
