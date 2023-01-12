import random
from pprint import pprint
import time

from characters import scrapeCharactersPage
from character import scrapeCharacter
import export

START_PAGE = "https://simpsons.fandom.com/wiki/Category:Characters"

TEST = True # scrape some random characters
CHARACTER_TEST_URL = None # scrape only this if not None

def scrapeCharacters(startPage = START_PAGE):
    """Returns the list of all characters of the wiki"""
    characters = []
    charactersPages = []
    charactersPageURL = startPage
    while charactersPageURL:
        charactersPages.append(charactersPageURL)
        print("Characters page " + str(len(charactersPages)) + " (" + charactersPageURL + ")")
        pageCharacters, charactersPageURL = scrapeCharactersPage(charactersPageURL, test=TEST)
        characters.extend(pageCharacters)
        if TEST and random.random() < 0.2:
            charactersPageURL = None
    return characters, charactersPages

#s = bs("<div> ciao, <br/> io <a href='/aaa'> </a> sono Luca </div>", "html.parser")
#root = s.div
#printSoupContent(root)
##removeLinebreaks(p, replaceWith='<br>')
#handleLinks(root)
#handleLinebreaks(root)
#mergeStringElements(root)
#printSoupContent(root)

if __name__ == "__main__":
    if CHARACTER_TEST_URL:
        print("Testing single character " + CHARACTER_TEST_URL)
        pprint(scrapeCharacter(CHARACTER_TEST_URL), sort_dicts=False)
    else:
        # scrape
        startScrapingTime = time.time()
        characters, _ = scrapeCharacters()
        scrapingTime = time.time() - startScrapingTime
        print("Scraping completed in " + str(int(scrapingTime/60)) + " min (" + str(scrapingTime) + " sec)")
        # export
        startExportTime = time.time()
        filename = export.CSV_FILE_NAME + ("-test" if TEST else "")
        print("Now exporting to " + filename + "." + export.CSV_FILE_EXTENSION)
        export.writeCsv(characters, filename=filename)
        exportTime = time.time() - startExportTime
        print("Export completed in " + str(int(exportTime/60)) + " min (" + str(exportTime) + " sec)")
        # total
        totalTime = time.time() - startScrapingTime
        print("Number of character scraped: " + str(len(characters)))
        print("Finished in " + str(int(totalTime/60)) + " min (" + str(totalTime) + " sec)")
