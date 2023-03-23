# Test file for Search Engine, Please run whenever modifying the WebpageSearcher.py file

from WebpageSearcher import WebpageSearcher

searcher = WebpageSearcher()


def main():

    # Add some links to the database
    assert searcher.add_link("https://techboomers.com/", keywords="computers, tech, old people")
    assert searcher.add_link("https://www.bbcgoodfood.com/recipes/easy-vanilla-cake", keywords="baking")
    assert searcher.add_link("https://ruwix.com/the-rubiks-cube/how-to-solve-the-rubiks-cube-blindfolded-tutorial/", keywords="soccer")
    assert not searcher.add_link("https://seniornet.org/", keywords="computers")
    assert not searcher.add_link("https://skjfnljeqbf", keywords="")

    # check_webscraping()
    check_keywords()
    check_extraneous_inputs()

    print("All tests passed!")


# Checks if the webscraping is working
def check_webscraping():
    assert searcher.search("online")[0] == "https://techboomers.com/"
    assert searcher.search("entertainment")[0] == "https://techboomers.com/"
    assert searcher.search("recipes")[0] == "https://www.bbcgoodfood.com/recipes/easy-vanilla-cake"
    assert searcher.search("vanilla")[0] == "https://www.bbcgoodfood.com/recipes/easy-vanilla-cake"
    assert searcher.search("rubiks cube")[0] == "https://ruwix.com/the-rubiks-cube/how-to-solve-the-rubiks-cube-blindfolded-tutorial/"
    assert searcher.search("algorithm")[0] == "https://ruwix.com/the-rubiks-cube/how-to-solve-the-rubiks-cube-blindfolded-tutorial/"


# checks if the keywords are working
def check_keywords():
    assert searcher.search("tech")[0] == "https://techboomers.com/"
    assert searcher.search("old people")[0] == "https://techboomers.com/"
    assert searcher.search("baking")[0] == "https://www.bbcgoodfood.com/recipes/easy-vanilla-cake"
    assert searcher.search("soccer")[0] == "https://ruwix.com/the-rubiks-cube/how-to-solve-the-rubiks-cube-blindfolded-tutorial/"


# checks if the extraneous inputs cause errors
def check_extraneous_inputs():
    assert searcher.search("")[0] == "no result"
    assert searcher.search("i32754ct894.//,ko5vhi3cuh")[0] == "no result"
    assert searcher.search("3287vt49t829d35__239rh98347rbc4ejgnw/.rc,';lvnt,")[0] == "no result"


if __name__ == "__main__":
    main()
