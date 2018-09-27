import json
import re

import requests
import html2text

"""Gets a joke from www.witz-des-tages.de and sends it"""
# Regex pattern to extract the url from the joke
pattern = re.compile(r'<td class="joke_title"><a href=.(.+\/)\?tc')

# Example: http://www.witz-des-tages.de/top-witze/seite/2/
source_url = 'http://www.witz-des-tages.de/top-witze/seite/'

list_of_joke_urls = list()

for i in range(2):
    url_for_download = source_url + str(i)

    # Extracting the URLs of the jokes
    r = requests.get(url_for_download)
    list_of_joke_urls += (pattern.findall(str(r.text)))


# Extracting the paragraphs, we need the first two! (Title and the actual text)
joke_pattern_title = re.compile(r'"title entry-title">(.+)<\/h\d>')

# Creating a dictionary to save the joke content in json later
joke_dict = dict()
joke_dict['jokes'] = []

h = html2text.HTML2Text()
# Run through every single joke url
for joke_url in list_of_joke_urls:
    # Requesting the web page with the actual joke
    r = requests.get(joke_url)

    data = str(r.text)
    # Extracting the title and the joke text.
    joke_title = joke_pattern_title.findall(data)
    joke_text = data[data.find('<p>'):data.find(
        '<span class="hreview-aggregate">')]

    # Adding the joke to the dictionary
    joke_dict['jokes'].append({
        'Titel': h.handle(joke_title[0]).rstrip('\n'),
        'Text': h.handle(joke_text).rstrip('\n').strip('\n')
    })

# See https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
# Saving to the data file
with open('data.json', 'w') as outfile:
    json.dump(joke_dict, outfile)
