from warnings import warn
from bs4 import BeautifulSoup as bs

from souphelper import *

STR_SEPARATOR = ","

def name(characterInfobox:bs):
    """Get character name from infobox"""
    if characterInfobox:
        titleTag = characterInfobox.find("h2")
        if titleTag:
            return str(titleTag.string).strip()
    return None

def image(characterInfobox:bs):
    """Get character image url from infobox"""
    if characterInfobox:
        imageTag = characterInfobox.figure
        if imageTag:
            return imageTag.a.img["src"]
    return None

def age(characterInfobox:bs):
    """Get character age from infobox"""
    if characterInfobox:
        ageTag = characterInfobox.find(attrs={"data-source": "age"})
        if ageTag:
            age = None
            # ageTag div has directly a number inside (https://simpsons.fandom.com/wiki/Charlene_Bouvier)
            ageStr = str(ageTag.div.string).strip()
            # or the age + "years old" (https://simpsons.fandom.com/wiki/Adam_Simpson)
            if ageStr.endswith("years old"):
                ageStr = (ageStr[:-9]).strip()
            # sometimes there is no age (in the same page) (https://simpsons.fandom.com/wiki/Burns%27_Alien)
            try:
                age = int(ageStr)
            except ValueError:
                # parsing failed
                warn('cannot get age number from string "' + str(ageTag.div) + '"')
            return age
    return None

def species(characterInfobox:bs):
    """Get character species from infobox"""
    # this is a rare attribute not for human characters (https://simpsons.fandom.com/wiki/Bluella)
    if characterInfobox:
        speciesTag = characterInfobox.find(attrs={"data-source": "species"})
        if speciesTag:
            return str(speciesTag.div.string).strip().lower()
    return None

sexImgNames = {
    "Male.png": "male",
    "Female.png": "female",
    "Unknown.png": "unknown"
}
def sex(characterInfobox:bs):
    """Get character sex from infobox"""
    if characterInfobox:
        sexTag = characterInfobox.find(attrs={"data-source": "sex"})
        if not sexTag:
            # if sex is not found, try with gender (for rare pages like https://simpsons.fandom.com/wiki/Always_Comes_in_Second)
            sexTag = characterInfobox.find(attrs={"data-source": "gender"})
        if sexTag:
            sexContent = sexTag.div
            # sex is displayed through an image with alt attribute same as image name
            # possibilities in sexImgNames
            sex = sexImgNames[sexContent.a.img["alt"]]
            # in rare cases, some characters have multiple genders (https://simpsons.fandom.com/wiki/3_Little_Pigs) (https://simpsons.fandom.com/wiki/Lady_Duff)
            sexContent.a.decompose()
            handleP(sexContent)
            if sexContent.a:
                sex = sex + "," + sexImgNames[sexContent.a.img["alt"]]
            return sex
    return None

statusImgNames = {
    "Alive.png": "alive",
    "Deceased.png": "deceased",
    "Unknown.png": "unknown",
    "Fictional.jpg": "fictional"
}
def status(characterInfobox:bs):
    """Get character status from infobox, the second returned value represents if the character is fictional"""
    if characterInfobox:
        statusTag = characterInfobox.find(attrs={"data-source": "status"})
        if statusTag:
            statusContent = statusTag.div
            # status is displayed through an image with alt attribute same as image name
            # but in rare cases, there is no image (https://simpsons.fandom.com/wiki/Charlene_Bouvier)
            if statusContent.string:
                # lower because statusImgNames values are all lower
                return str(statusTag.div.string).strip().lower(), False
            # possibilities in statusImgNames
            status = statusImgNames[statusContent.a.img["alt"]]
            fictional = False
            # some characters have 2 statuses, but it seems that the one of the two is always fictional (https://simpsons.fandom.com/wiki/Amy_Wong) (https://simpsons.fandom.com/wiki/Mao (only Fictional))
            # so this function will return the real status, and a boolean indicating if this character is fictional
            if status == "fictional":
                status = None
                fictional = True
            # handle two statuses
            statusContent.a.decompose()
            handleP(statusContent)
            if statusContent.a:
                if fictional:
                    status = statusImgNames[statusContent.a.img["alt"]]
                else:
                    fictional = statusImgNames[statusContent.a.img["alt"]] == "fictional"
                    if not fictional:
                        warn("two statuses not fictional found")
            return status, fictional
    return None, False

def alias(characterInfobox:bs):
    """Get character aliases from infobox"""
    if characterInfobox:
        aliasTag = characterInfobox.find(attrs={"data-source": "alias"})
        if aliasTag:
            aliasContent = aliasTag.div
            # aliasContent has directly a name inside (https://simpsons.fandom.com/wiki/Adam_Simpson)
            # but sometimes it has paragraphs containing other aliases (https://simpsons.fandom.com/wiki/Elvis_Presley)
            handleP(aliasContent)
            handleLinebreaks(aliasContent, STR_SEPARATOR)
            return str(aliasContent.string).strip()
    return None

def hairColor(characterInfobox:bs):
    """Get character hair color from infobox"""
    if characterInfobox:
        hairColorTag = characterInfobox.find(attrs={"data-source": "hair"})
        if hairColorTag:
            hairColorContent = hairColorTag.div
            # some rare characters has 2 hair colors (or characteristics) separated by line breaks (https://simpsons.fandom.com/wiki/First_Lady_Admiral)
            handleLinebreaks(hairColorContent, STR_SEPARATOR)
            # hair color is made lowercase for uniformity and human error fixing (case error only)
            return str(hairColorContent.string).strip().lower()
    return None

def color(characterInfobox:bs):
    """Get character color from infobox"""
    # this is a rare attribute not for human characters (https://simpsons.fandom.com/wiki/Bluella)
    if characterInfobox:
        colorTag = characterInfobox.find(attrs={"data-source": "color"})
        if colorTag:
            return str(colorTag.div.string).strip().lower()
    return None

def birthCountry(characterInfobox:bs):
    """Get character birth country from infobox"""
    if characterInfobox:
        birthCountryTag = characterInfobox.find(attrs={"data-source": "country of birth"})
        if birthCountryTag:
            birthCountryContent = birthCountryTag.div
            return str(birthCountryContent.string).strip()
    return None

def job(characterInfobox:bs):
    """Get character job(s) from infobox"""
    if characterInfobox:
        jobTag = characterInfobox.find(attrs={"data-source": "job"})
        if jobTag:
            jobContent = jobTag.div
            # jobContent has directly a job inside
            # but sometimes it has paragraphs containing other jobs (https://simpsons.fandom.com/wiki/Elvis_Presley)
            handleP(jobContent)
            # and sometimes jobs contain some links to the job place (https://simpsons.fandom.com/wiki/Chief_Inspector)
            handleLinks(jobContent)
            # different jobs are separated by line breaks (https://simpsons.fandom.com/wiki/Elvis_Presley) (https://simpsons.fandom.com/wiki/Chief_Inspector)
            handleLinebreaks(jobContent, STR_SEPARATOR)
            return str(jobContent.string).strip()
    return None

def firstAppearance(characterInfobox:bs):
    """Get character first appearance episode name from infobox"""
    if characterInfobox:
        firstAppearanceTag = characterInfobox.find(attrs={"data-source": "appearance"})
        if firstAppearanceTag:
            # firstAppearanceTag contains a link to an episode
            # or, in rare cases, the title only (https://simpsons.fandom.com/wiki/Amy_Wong)
            if firstAppearanceTag.div.a:
                return firstAppearanceTag.div.a["title"].strip()
            else:
                return firstAppearanceTag.div.string
    return None

def firstMentioned(characterInfobox:bs):
    """Get character first mentioned episode name from infobox"""
    if characterInfobox:
        firstMentionedTag = characterInfobox.find(attrs={"data-source": "mentioned"})
        if firstMentionedTag:
            # firstMentionedTag contains a link to an episode
            return firstMentionedTag.div.a["title"].strip()
    return None

def voice(characterInfobox:bs):
    """Get character voice actor(s) from infobox"""
    if characterInfobox:
        voiceTag = characterInfobox.find(attrs={"data-source": "voiced by"})
        if voiceTag:
            voiceContent = voiceTag.div
            # some rare characters have the multiple voice actors inside paragraphs (https://simpsons.fandom.com/wiki/Mother_Bear)
            handleP(voiceContent)
            # some rare characters have <span> elements inside voice description (https://simpsons.fandom.com/wiki/Mother_Bear)
            handleSpan(voiceContent)
            # some characters have a voice actor with a dedicated page, meaning wrapped by an <a> tag
            handleLinks(voiceContent)
            # some rare characters are voiced by multiple voice actors separated by line breaks (https://simpsons.fandom.com/wiki/Kumiko_Albertson)
            handleLinebreaks(voiceContent, STR_SEPARATOR)
            return voiceContent.string.strip()
    return None

def characterAttrs(characterPage:bs, **moreAttributes):
    """Get all character attributes"""
    infobox = characterPage.find(class_="portable-infobox")
    state, fictional = status(infobox)
    return {
        **moreAttributes,
        "title": characterPage.find(id="firstHeading").string.strip(),
        "name": name(infobox),
        "image": image(infobox),
        "age": age(infobox),
        "species": species(infobox),
        "sex": sex(infobox),
        "status": state,
        "fictional": fictional,
        "alias": alias(infobox),
        "hair color": hairColor(infobox),
        "color": color(infobox),
        "birth country": birthCountry(infobox),
        # TODO owner (https://simpsons.fandom.com/wiki/Bluella)
        "job": job(infobox),
        # TODO related to (https://simpsons.fandom.com/wiki/Ingrid_Schedeen)
        "first appearance": firstAppearance(infobox),
        "first mentioned": firstMentioned(infobox),
        "voice": voice(infobox)
    }
