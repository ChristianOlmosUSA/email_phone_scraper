import requests
from bs4 import BeautifulSoup
import requests
import json
import csv

# website url links
urls=''

# load website URLs
with open('websites.txt','r') as f:
    for line in f.read():
        urls += line

# convert string to list of URLSs
urls = list(filter(None, urls.split('\n')))

# loop over URLs
for url in urls:
    print(url)
