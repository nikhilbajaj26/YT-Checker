# pip install --upgrade youtube-dl
# Check if body matches footnotes.

from __future__ import unicode_literals
import youtube_dl
from bs4 import BeautifulSoup
import sys
import re
import time
import datetime
from collections import defaultdict

"List of body urls vs footnote urls per footnote section"
def geturls(filename):
    """Fetch all YT links from the footnotes and body of a LibreOffice html document"""
    urls = defaultdict(lambda: [[],[], [], []])
    with open(filename) as doc:
        soup = BeautifulSoup(doc, 'html.parser')
        # Footnotes
        footnotes = soup.find_all("div", id=re.compile("^sdfootnote[0-9]+$"))
        yt = re.compile("youtu\.?be")
        for fn in footnotes:
            num = int("".join(filter(str.isdigit, fn["id"])))
            for link in fn.find_all("a", href=yt):
                urls[num][1].append(link["href"])
                urls[num][3].append(link.string)
        # Bodyodyody
        anc = re.compile("^sdfootnote[0-9]+anc$")
        bodyend = soup.find_all("a", class_="sdfootnoteanc")[-1]
        links = bodyend.find_all_previous("a", href=yt)
        for link in links[::-1]:
            fn = link.find_next("a", class_="sdfootnoteanc")
            num = int("".join(filter(str.isdigit, fn["name"])))
            urls[num][0].append(link["href"])
            urls[num][2].append(link.string)
    return urls


def getids(url):
    """Get id/ids from a YT link"""
    ydl_opts = {'ignoreerrors': False, 'no_warnings': True, 'quiet': False}
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=False)
            if "entries" in result:
                return [ i["id"] for i in result["entries"] ]
            else:
                return [ result["id"] ]
    except Exception:
        print(f"Error: failed to extract info from {url}")
        input()



def check(num, entry: list):
    """Test if body videos match footnotes"""
    ydl_opts = {'ignoreerrors': False, 'no_warnings': True, 'quiet': False}
    bodyids, footids = [], []
    for url in entry[0]:
        bodyids.extend(getids(url))
        time.sleep(4)
    for url in entry[1]:
        footids.extend(getids(url))
        time.sleep(4)
    if bodyids != footids:
        bodyset = set(bodyids)
        footset = set(footids)
        if bodyset != footset:
            return [bodyset.difference(footset), footset.difference(bodyset)]
        else:
            print(f"{num} {entry[2]}: Order mismatch")
            input("Press enter to continue")



if len(sys.argv) < 2:
    print("Usage: discrep.py <html file>")
else:
    urls = geturls(sys.argv[1])
    for num in urls:
        if urls[num][0] != urls[num][1]:
            if set(urls[num][0]).issubset(set(urls[num][1])):
                pass # print(urls[num])
            else:
                delta = check(num, urls[num])
                if delta:
                    print(f"Discrepancy w/ {num} {urls[num][2]}")
                    print(delta)
                    input("Press enter to continue")
                else:
                    print(f"{num} {urls[num][2]} is ok")
                time.sleep(4)



    #print(urls)

# Bach sonatas, bach vcs, mozart vcs, brandenburgs, orch suites