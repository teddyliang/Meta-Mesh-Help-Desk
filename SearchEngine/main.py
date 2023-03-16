from WebpageSearcher import WebpageSearcher

def main():
    # Create a new WebpageSearcher object
    searcher = WebpageSearcher()

    # Add some links to the database
    searcher.add_link("https://techboomers.com/", keywords="computers, tech, old people")
    searcher.add_link("https://seniornet.org/", keywords="computers")
    searcher.add_link("https://www.bbcgoodfood.com/recipes/easy-vanilla-cake", keywords="baking")
    searcher.add_link("https://www.delish.com/cooking/recipe-ideas/a27081036/easy-homemade-vanilla-cake-recipe/", keywords="soccer")

    # Get input from the user
    while True:
        query = input("Please enter a query (or 'q' to quit): ")
        if query == 'q':
            break

        # Search for the query and print the most relevant URL
        url = searcher.search(query)
        if url is None:
            print("No relevant URLs found.")
        else:
            print("The most relevant URL for the query '{}' is: {}".format(query, url))

if __name__ == "__main__":
    main()
