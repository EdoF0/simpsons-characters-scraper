from warnings import warn
from bs4 import BeautifulSoup as bs

from souphelper import *
from characterexceptions import exceptions

STR_SEPARATOR = ","

def name(characterInfobox:bs):
    """Get character name from infobox"""
    if characterInfobox:
        titleTag = characterInfobox.find("h2")
        if titleTag:
            # some characters has part of the name in italic when referencing something (https://simpsons.fandom.com/wiki/%27%27People_Who_Look_Like_Things%27%27_host)
            handleItalic(titleTag)
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

genderImgNames = {
    "Male.png": "male",
    "Female.png": "female",
    "Nonbinary.png": "nonbinary", # (https://simpsons.fandom.com/wiki/Dubya_Spuckler)
    "Unknown.png": "unknown"
}
def gender(characterInfobox:bs):
    """Get character gender from infobox"""
    if characterInfobox:
        genderTag = characterInfobox.find(attrs={"data-source": "sex"})
        if not genderTag:
            # if sex is not found, try with gender (for rare pages like https://simpsons.fandom.com/wiki/Always_Comes_in_Second)
            genderTag = characterInfobox.find(attrs={"data-source": "gender"})
        if genderTag:
            genderContent = genderTag.div
            # gender is displayed through an image with alt attribute same as image name
            # but in rare cases, there is no image (https://simpsons.fandom.com/wiki/Al_Sneed)
            if genderContent.string:
                # if the string property exists, there is no other status
                # lower because genderImgNames values are all lower
                return str(genderContent.string).strip().lower()
            # a character was found with only the secondary gender inside a paragraph (https://simpsons.fandom.com/wiki/Homeland_Security_Agents)
            # so don't stop if there is not the first image
            gender = None
            if genderContent.a:
                # possibilities in genderImgNames
                gender = genderImgNames[genderContent.a.img["alt"]]
            # in rare cases, some characters have multiple genders (https://simpsons.fandom.com/wiki/3_Little_Pigs) (https://simpsons.fandom.com/wiki/Lady_Duff)
            genderContent.a.decompose()
            handleP(genderContent)
            if genderContent.a:
                gender = gender + "," + genderImgNames[genderContent.a.img["alt"]]
            return gender
    return None

statusImgNames = {
    "Alive.png": "alive",
    "Deceased.png": "deceased",
    "Unknown.png": "unknown",
    "Fictional.jpg": "fictional"
}
def _handleStatusTag(statusTag:bs):
    status = None
    fictional = False
    if statusTag:
        statusContent = statusTag.div
        # status is displayed through an image with alt attribute same as image name
        # but in rare cases, there is no image (https://simpsons.fandom.com/wiki/Charlene_Bouvier)
        if statusContent.string:
            # if the string property exists, there is no other status
            # lower because statusImgNames values are all lower
            return str(statusContent.string).strip().lower(), fictional
        # possibilities in statusImgNames
        status = statusImgNames[statusContent.a.img["alt"]]
        # some characters have 2 statuses, but it seems that the one of the two is always fictional (https://simpsons.fandom.com/wiki/Burns%27_Alien (fictional second)) (https://simpsons.fandom.com/wiki/Amy_Wong (fictional first)) (https://simpsons.fandom.com/wiki/Mao (only Fictional))
        # so this function will return the real status, and a boolean indicating if this character is fictional
        if status == "fictional":
            status = None
            fictional = True
        # handle two statuses
        statusContent.a.decompose()
        handleP(statusContent)
        if statusContent.a and statusContent.a.img:
            # if there is another status
            # statusContent.a.img check is necessary for rare cases (https://simpsons.fandom.com/wiki/Tracey_Ullman_Homer)
            status2 = statusImgNames[statusContent.a.img["alt"]]
            if status2 == "fictional":
                fictional = True
            else:
                if status:
                    # for rare cases (https://simpsons.fandom.com/wiki/Mario) (https://simpsons.fandom.com/wiki/Mickey_Mouse_(Character))
                    status = status + STR_SEPARATOR + status2
                else:
                    status = status2
    return status, fictional
def status(characterInfobox:bs):
    """Get character status from infobox, the second returned value represents if the character is fictional"""
    if characterInfobox:
        statusTag1 = characterInfobox.find(attrs={"data-source": "status"})
        # some rare characters have also "other statuses" (https://simpsons.fandom.com/wiki/Myrna_Bellamy)
        statusTag2 = characterInfobox.find(attrs={"data-source": "other statuses"})
        status1, fictional1 = _handleStatusTag(statusTag1)
        status2, fictional2 = _handleStatusTag(statusTag2)
        status = None
        fictional = fictional1 or fictional2
        if status1 and status2:
            status = status1 + STR_SEPARATOR + status2
        elif status1:
            status = status1
        elif status2:
            status = status2
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
            # sometimes there are small tags explaining the alias context (https://simpsons.fandom.com/wiki/Abraham_Lincoln)
            # remove the context, keep aliases only
            handleSmall(aliasContent, extract=False)
            # there are also cite notes (https://simpsons.fandom.com/wiki/Demogorgon)
            handleSups(aliasContent)
            # in rare cases there are links (https://simpsons.fandom.com/wiki/Charles_Montgomery_Burns)
            handleLinks(aliasContent)
            # multiple jobs
            handleLinebreaks(aliasContent, STR_SEPARATOR)
            if aliasContent.string:
                return str(aliasContent.string).strip()
            else:
                warn('alias parsing failed for ' + str(aliasContent) + '"')
    return None

def hairColor(characterInfobox:bs):
    """Get character hair color from infobox"""
    if characterInfobox:
        hairColorTag = characterInfobox.find(attrs={"data-source": "hair"})
        if hairColorTag:
            hairColorContent = hairColorTag.div
            # some characters dos not have only direct text inside, but also paragraphs (https://simpsons.fandom.com/wiki/Homeland_Security_Agents)
            handleP(hairColorContent)
            # some characters has 2 hair colors (or characteristics) separated by line breaks (https://simpsons.fandom.com/wiki/First_Lady_Admiral)
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
            # some rare characters have context descriptions for the job in small tags (https://simpsons.fandom.com/wiki/Carol_Berrera)
            # remove the context, keep job only
            handleSmall(jobContent, extract=False)
            # different jobs are separated by line breaks (https://simpsons.fandom.com/wiki/Elvis_Presley) (https://simpsons.fandom.com/wiki/Chief_Inspector)
            handleLinebreaks(jobContent, STR_SEPARATOR)
            if jobContent.string:
                return str(jobContent.string).strip()
            else:
                warn('job parsing failed for ' + str(jobContent) + '"')
    return None

def firstAppearance(characterInfobox:bs):
    """Get character first appearance episode name from infobox"""
    if characterInfobox:
        firstAppearanceTag = characterInfobox.find(attrs={"data-source": "appearance"})
        if firstAppearanceTag:
            # firstAppearanceTag contains a link to an episode
            # or, in rare cases, the title only (https://simpsons.fandom.com/wiki/Amy_Wong)
            if firstAppearanceTag.div.a:
                return str(firstAppearanceTag.div.a["title"]).strip()
            else:
                return str(firstAppearanceTag.div.string).strip()
    return None

def firstMentioned(characterInfobox:bs):
    """Get character first mentioned episode name from infobox"""
    if characterInfobox:
        firstMentionedTag = characterInfobox.find(attrs={"data-source": "mentioned"})
        if firstMentionedTag:
            # firstMentionedTag contains a link to an episode
            # or, in rare cases, the title only inside a span or not (https://simpsons.fandom.com/wiki/The_Collector (inside a span)) (https://simpsons.fandom.com/wiki/Burns%27_Vampire_Minions (no span))
            if firstMentionedTag.div.a:
                return str(firstMentionedTag.div.a["title"]).strip()
            elif firstMentionedTag.div.span:
                return str(firstMentionedTag.div.span.string).strip()
            else:
                return str(firstMentionedTag.div.string).strip()
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
            # some rare characters have <strong> elements for particular voice actors (https://simpsons.fandom.com/wiki/Regis_Philbin)
            handleStrong(voiceContent)
            # some characters have a voice actor with a dedicated page, meaning wrapped by an <a> tag
            handleLinks(voiceContent)
            # some rare characters have context descriptions for the voice actor in small tags (https://simpsons.fandom.com/wiki/Carol_Berrera)
            # remove the context, keep voice actors only
            handleSmall(voiceContent, extract=False)
            # a character with italic tags was found (https://simpsons.fandom.com/wiki/Charles_Montgomery_Burns)
            handleItalic(voiceContent)
            # remove also cite notes (https://simpsons.fandom.com/wiki/Blake_(Dad_Behavior))
            handleSups(voiceContent)
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
        "known as": characterPage.find(id="firstHeading").string.strip(),
        "full name": name(infobox),
        "image url": image(infobox),
        "age": age(infobox),
        "species": species(infobox),
        "gender": gender(infobox),
        "status": state,
        "fictional": fictional,
        "alias": alias(infobox),
        "hair color": hairColor(infobox),
        "color": color(infobox),
        "birth country": birthCountry(infobox),
        # TODO owner (https://simpsons.fandom.com/wiki/Bluella)
        "job": job(infobox),
        # TODO related to (https://simpsons.fandom.com/wiki/Ingrid_Schedeen) (https://simpsons.fandom.com/wiki/Charles_Montgomery_Burns)
        "first appearance": firstAppearance(infobox),
        "first mentioned": firstMentioned(infobox),
        "voice": voice(infobox)
    }

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
