#!/usr/bin/env python

# Try to fetch local offices from legislator websites

# * html2text the whole thing
# * look for zips
# * try to work backwards to parse the rest of the data

from urllib.request import urlopen
from utils import load_data
import re
from bs4 import BeautifulSoup

def run():
  current = load_data("legislators-current.yaml")
  i = 0
  for m in current:
    if i > 2:
      continue

    last_term = m['terms'][-1]
    if last_term['url'] != '':
      print("url is %s" % last_term['url'])

      # finding a url
      # search the base page first, lots of reps have locations in their footer
      # if not found, search links on the page for anything that contains offices and search those pages

      searchURLForOffices(last_term['url'])


    i += 1

def searchURLForOffices(url):
  html = urlopen(url).read()
  soup = BeautifulSoup(html, features="html.parser")
  for script in soup(["script", "style"]):
    script.extract()
  text = soup.get_text()
  # break into lines and remove leading and trailing space on each
  lines = list(line.strip() for line in text.splitlines())
  chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

  zip_code_pattern = re.compile(r'\b\d{5}\b')

  j = 0
  for line in chunks:
    if re.search(zip_code_pattern, line):
      possibleAddressLines(lines[j-3:j+3])
    j += 1

def possibleAddressLines(lines):
  print(lines)



if __name__ == '__main__':
  run()