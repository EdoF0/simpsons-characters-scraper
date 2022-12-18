import random
from pprint import pprint

from souphelper import soup
from characters import charactersURLs, charactersNextURL
from character import characterAttrs

START_PAGE = "https://simpsons.fandom.com/wiki/Category:Characters"

TEST = True # scrape some random characters
CHARACTER_TEST_URL = None # scrape only this if not None

def scrapeCharacter(url:str):
    """Returns a character dictionary given the url to that character page, or returns None if the scraping failed"""
    if url.find("User:") != -1:
        return None
    if url.find("Category:") != -1:
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
        characters.append(character)
    else:
        for characterURL in charactersURLs(charactersPage):
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
        if TEST:
            scrapeCharacters()
