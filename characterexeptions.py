# Some characters contain human errors that makes the scraper throw errors.
# Here is a list of all characters that, for the actual scraper status, should be avoided.

exceptions = {
    "https://simpsons.fandom.com/wiki/Abraham_The_Thief", # human error: relations inside other statuses
    "https://simpsons.fandom.com/wiki/Aunt_Edith", # human error: gender and status swapped
    "https://simpsons.fandom.com/wiki/Banker", # human error: status data error
    "https://simpsons.fandom.com/wiki/Blue-eyed_wife", # syntax: gender and status images not inside a link
    "https://simpsons.fandom.com/wiki/Brian_McGee", # human error: job is the fictional status image
    "https://simpsons.fandom.com/wiki/Cocoa_Beanie", # human error: gender is the fictional status image
    "https://simpsons.fandom.com/wiki/Dick_Tufeld", # semantic: he is a guest voice, not a character
    "https://simpsons.fandom.com/wiki/Nuclear_Employee_1_(Who_Shot_Mr._Burns?)", # availability: response status 301 (moved permanently) then 404 (not found)
    "https://simpsons.fandom.com/wiki/Nuclear_Employee_2_(Who_Shot_Mr._Burns?)", # availability: response status 301 (moved permanently) then 404 (not found)
    "https://simpsons.fandom.com/wiki/Nuclear_Employee_3_(Who_Shot_Mr._Burns?)", # availability: response status 301 (moved permanently) then 404 (not found)
    "https://simpsons.fandom.com/wiki/Pa_(How_Munched_Is_That_Birdie_in_the_Window?)", # availability: response status 301 (moved permanently) then 404 (not found)
    "https://simpsons.fandom.com/wiki/Patrolman_1", # human error: status deceased image inside alias section
    "https://simpsons.fandom.com/wiki/Vivienne_Saint_Germain", # human error: species and age inside other statuses
    "https://simpsons.fandom.com/wiki/Rhinos", # human error: first episode appearance is a description
}
