# pip install --upgrade youtube-dl

from __future__ import unicode_literals
import youtube_dl
from bs4 import BeautifulSoup
import sys
import re
import time
import datetime


def geturls(filename) -> set:
    """Fetch all YT links from the footnotes of a LibreOffice created html document"""
    urls = set()
    with open(filename) as doc:
        soup = BeautifulSoup(doc, 'html.parser')
        footnotes = soup.find_all("div", id=re.compile("^sdfootnote[0-9]+$"))
        yt = re.compile("youtu\.?be")
        for fn in footnotes:
            for link in fn.find_all("a", href=yt):
                urls.add(link["href"])
    return urls


def check(url) -> bool:
    """Test if YT video is up"""
    ydl_opts = {'ignoreerrors': False, 'no_warnings': True, 'quiet': False}
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=False)
        return True
    except Exception:
        return False


if len(sys.argv) < 2:
    print("Usage: checker <html file>")
else:
    urls = geturls(sys.argv[1])
    bugs = 0
    maxbugs = 10
    override = False
    s, p, bs, bp = 1.1, 5, 5, 15 # Sleep times for single, playlist, bad s, bad p
    with open("errors.log", "w") as logfile:
        logfile.write(str(datetime.datetime.now()) + "\n\n")
        for url in urls:
            if not check(url):
                if "list=" in url:
                    time.sleep(bp)
                else:
                    time.sleep(bs)
                if not check(url):
                    logfile.write(f"{url}\n")
                    bugs = bugs + 1
                    if not override and bugs >= maxbugs:
                        print(f"{bugs} bad links. Keep going?")
                        ans = input()
                        if not ( ans == "y" or ans == "Y" ):
                            exit()
                        else:
                            override = True
            if "list=" in url:
                time.sleep(p)
            else:
                time.sleep(s)

        if bugs > 0:
            logfile.write("\n")
        logfile.write(f"Checked {len(urls)} links, found {bugs} error")
        if bugs == 0:
            logfile.write("s :)")
        elif bugs > 1:
            logfile.write("s")
        logfile.write("\n")
