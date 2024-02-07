import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import json
import time
import ssl
import sys


conn = sqlite3.connect('yelp.sqlite')
cur = conn.cursor()

# Do some setup
cur.executescript('''
DROP TABLE IF EXISTS Business;

CREATE TABLE Business (
    id     TEXT UNIQUE,
    name   TEXT,
    categories  TEXT,
    open        INTEGER,
    stars   INTEGER
);
''')


# file selection - not necessary
fname = input('Enter file name: ')
if len(fname) < 1:
    fname = 'yelp_academic_dataset_business.json'
count = 0

# JSON Parsing
json_data = []
with open(fname) as f:
    for line in f:
        try:
            entry = json.loads(line)
            json_data.append(entry)
        except json.JSONDecodeError as e:
             print(f"Error decoding JSON: {e}")
             continue

for entry in json_data:
    if count > 100:
         print('Retrieved 100 Businesses')
         break
    
    id = entry.get("business_id")
    name = entry.get("name")
    categories = entry.get("categories")
    open = entry.get("is_open")
    stars = entry.get("stars")

    print((name))

    cur.execute('''INSERT OR IGNORE INTO Business (id, name, categories, open, stars)
        VALUES ( ? , ? , ? , ? , ?)''', ( id, name, categories, open, stars) )

    count = count + 1

    conn.commit()
