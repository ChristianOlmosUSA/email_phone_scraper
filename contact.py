# from: https://www.youtube.com/watch?v=qdFvlo0dxfg
# Go to the homepage
# download it
# regex search it for phones & emails
# search for 'a'/href tag with 'contactus' and repeat the regex for the contac page
import requests
from bs4 import BeautifulSoup
import requests
import json
import csv
import re

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
    res = requests.get(url)
    print('crawled base URL')

    # parse response
    content = BeautifulSoup(res.text, 'lxml')

    # extract contact data
    emails_home = re.findall('(\w+@\w+\.\w+\.\w+)', content.get_text())
    phones_home = re.findall('(\d{3,4} \d{3,4} \d{3,4})', content.get_text())
    print('\n Emails (home page): ', emails_home)
    print('\n Phones (home page): ', phones_home)

    # create a data structure to store contacts
    contacts = {
        'WEBSITE': res.url,
        'emails_home': ', '.join(emails_home),
        'phones_home': ', '.join(phones_home),
        'emails_contact':'',
        'phones_contact': ''
        }

    # Extract contact link ## HOW TO FIND A LINK
    try:
        contact = content.find('a', text=re.compile('contact', re.IGNORECASE))['href']
        print(res.url, contact)         #see 20.5mins
        if 'http' in contact:
            print('URL is OK')
            contact_url = contact
        else: 
            print('URL is not OK')
            contact_url = res.url[0:-1]+ contact
            print(contact_url)

        # Crawling contact URL recursively
        res_contact = requests.get(contact_url)
        contact_content=BeautifulSoup(res_contact.text, 'lxml').get_text()
        print('crawled contact URL:',res_contact.url)

        # extract contact data
        emails_contact = re.findall('(\w+@\w+\.\w+\.\w+)', contact_content)
        phones_contact = re.findall('(\d{3,4} \d{3,4} \d{3,4})', contact_content)

        print('\n Emails (contact page): ',  emails_contact)
        print('\n Phones (contact page): ', phones_contact)

        # append additional contacts data
        contacts['emails_contact'] = ', '.join(emails_contact)
        contacts['phones_contact'] = ', '.join(phones_contact)

    except Exception as e:
        print(e)

    print(json.dumps(contact, indent=2)) # print to screen, nicely

    # store data to CSV file
    projectname = 'contacts.csv'
    with open(projectname, 'a') as f:
        # create CSV write
        writer = csv.DictWriter(f, fieldnames=contacts.keys())

        # write headers
        writer.writeheader()    # actually you need to check the csv is empty, so this only works the first time lol

        # append row to the CSV
        writer.writerow(contacts)