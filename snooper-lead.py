#!/usr/bin/env python3
from urllib.request import urlopen, Request
import urllib.error
from bs4 import BeautifulSoup
import argparse
import ssl
import re
import os

pages = set()

def scrape_data(url):
    global pages
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        # Connect to source URL
        context = ssl.SSLContext()
        req = Request(url, headers={'User-Agent': user_agent}, method='GET')
        html = urlopen(req, context=context).read()
        bsObj = BeautifulSoup(html, 'lxml')
        print("Checking for Emails...")

        for link in bsObj.findAll("a", href=re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")):
            if 'href' in link.attrs:
                if link.attrs['href'] not in pages:
                    newPage = link.attrs['href']
                    # Connect to all links one by one
                    req1 = Request(newPage, headers={'User-Agent': user_agent}, method='GET')
                    html1 = urlopen(req1, context=context).read()
                    bsObj1 = BeautifulSoup(html1, 'lxml').get_text()
                    # Find Emails in those links
                    match = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", bsObj1)
                    convert = "\n".join(str(x) for x in match)  # Convert list to string

                    if convert is not None and convert.split("\n") != ['']:  # remove whitespaces
                        # add to email.txt
                        with open("emails.txt", "a+") as f:
                            f.write(convert + "\n")

    # if any error happens
    except urllib.error.HTTPError as e:
        print(f"[!] HTTP Error [!]\n[?] Error Code: {e.code} [?]")

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--url", help="Usage: python findmail.py --url=https://www.example.com/", type=scrape_data)
        args = parser.parse_args()
        # remove duplicates
        openmail = open("emails.txt", "r").readlines()
        openmail_set = set(openmail)
        cleanmail = open("emails.txt", "w")

        for line in openmail_set:
            cleanmail.write(line)
        if os.path.isfile("emails.txt"):
            print("\n[+] Emails Saved on: " + os.getcwd())
        else:
            pass
    except Exception as e:
        print("Error:", e)
