# Some characters contain human errors that makes the scraper throw errors.
# Here is a list of all characters that, for the actual scraper status, should be avoided.

exceptions = {
    "https://simpsons.fandom.com/wiki/Abraham_The_Thief", # human error: relations inside other statuses
    "https://simpsons.fandom.com/wiki/Aunt_Edith", # human error: gender and status swapped
    "https://simpsons.fandom.com/wiki/Banker", # human error: status data error
    "https://simpsons.fandom.com/wiki/Blue-eyed_wife", # syntax: gender and status images not inside a link
    "https://simpsons.fandom.com/wiki/Brian_McGee", # human error: job is the fictional status image
}