import random
from pprint import pprint
from bs4 import BeautifulSoup as bs

from souphelper import soup
from character import scrapeCharacter

BASE_URL = "https://simpsons.fandom.com"

def isCharactersPage(page:bs):
    """True if the BeautifulSoup object represents a characters page"""
    return page.find(id="firstHeading").string.strip() == "Characters"

def charactersURLs(charactersPage:bs):
    """Return a list of all links of possible characters pages"""
    if not isCharactersPage(charactersPage):
        raise ValueError("Soup received is not a characters page")
    
    # reduce search space considering only the right section of the page
    charactersSection = charactersPage.find_all(class_="category-page__members")[0]
    characters = charactersSection.find_all(class_="category-page__member")
    # iterate character elements to find all links
    links = []
    for character in characters:
        # this are relative links
        links.append(BASE_URL + character.a["href"])
    return links

def charactersNextURL(charactersPage:bs):
    """Return the url for the next characters page, None if this is the last page"""
    if not isCharactersPage(charactersPage):
        raise ValueError("Soup received is not a characters page")
    
    # .find() returns None if can't find anything
    nextButton = charactersPage.find(class_="category-page__pagination-next")
    if nextButton:
        return str(nextButton["href"])
    else:
        return None

def scrapeCharactersPage(url:str, test=False):
    """Returns a list of characters given a characters page (page containing a list of characters)"""
    characters = []
    charactersPage = soup(url)
    nextCharactersPageURL = charactersNextURL(charactersPage)
    if test:
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
