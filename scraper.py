import random
from pprint import pprint
import time

from souphelper import soup
from characters import charactersURLs, charactersNextURL
from character import characterAttrs
from characterexeptions import exceptions
import export

START_PAGE = "https://simpsons.fandom.com/wiki/Category:Characters"

TEST = False # scrape some random characters
CHARACTER_TEST_URL = None # scrape only this if not None

def scrapeCharacter(url:str):
    """Returns a character dictionary given the url to that character page, or returns None if the scraping failed"""
    if url.find("User:") != -1:
        return None
    if url.find("Category:") != -1:
        return None
    if url in exceptions:
        return None
    characterPage = soup(url)
    character = characterAttrs(characterPage, url=url)
    return character

def scrapeCharactersPage(url:str):
    """Returns a list of characters given a characters page (page containing a list of characters)"""
    characters = []
    charactersPage = soup(url)
    nextCharactersPageURL = charactersNextURL(charactersPage)
    if TEST:
        characterURL = random.choice(charactersURLs(charactersPage))
        print("Testing", characterURL)
        character = scrapeCharacter(characterURL)
        pprint(character, sort_dicts=False)
        if character: # don't append if character is None
            characters.append(character)
    else:
        for characterURL in charactersURLs(charactersPage):
            print("  Scraping character", characterURL)
            character = scrapeCharacter(characterURL)
            if character: # don't append if character is None
                characters.append(character)
    return characters, nextCharactersPageURL

def scrapeCharacters(startPage = START_PAGE):
    """Returns the list of all characters of the wiki"""
    characters = []
    charactersPages = []
    charactersPageURL = startPage
    while charactersPageURL:
        charactersPages.append(charactersPageURL)
        print("Characters page " + str(len(charactersPages)) + " (" + charactersPageURL + ")")
        pageCharacters, charactersPageURL = scrapeCharactersPage(charactersPageURL)
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
        print("now exporting to " + export.CSV_FILE_NAME)
        if TEST:
            export.writeCsv(characters, filename=export.CSV_FILE_NAME+"-test")
        else:
            export.writeCsv(characters)
        exportTime = time.time() - startExportTime
        print("Export completed in " + str(int(exportTime/60)) + " min (" + str(exportTime) + " sec)")
        # total
        totalTime = time.time() - startScrapingTime
        print("Number of character scraped: " + str(len(characters)))
        print("Finished in " + str(int(totalTime/60)) + " min (" + str(totalTime) + " sec)")
