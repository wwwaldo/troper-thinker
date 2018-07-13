#!/usr/bin/python3
import sys
import urllib
from bs4 import BeautifulSoup

filename = "tropes.txt"
if len(sys.argv) > 1:  
    filename = sys.argv[1]

html_plaintext = urllib.request.urlopen("https://tvtropes.org/pmwiki/pagelist_having_pagetype_in_namespace.php?n=Main&t=trope").read()
soup = BeautifulSoup(html_plaintext, 'html.parser')
table = soup.find('table')

with open(filename, "w") as file:
    file.write("\n".join([link.attrs["href"].strip() for link in table.find_all('a')]))
    
    print("Trope URLs written to " + filename)

