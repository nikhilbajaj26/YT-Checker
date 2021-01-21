# YT URL Checker
Python script to check the footnotes of LibreOffice-exported HTML document for dead youtube links using youtube-dl

## Requirements
Python (duh)
```
pip install beautifulsoup4
pip install [--upgrade] youtube-dl
```

## Usage
I made this to check the links in the footnotes of a google doc (export to .odt), but you can start from any document readable by LibreOffice writer with youtube links in the footnotes.
1. Open document with [LibreOffice Writer](https://www.libreoffice.org/)
2. File > Send to > Create HTML
3. Run checker.py in same directory. 

The script writes any bad links to errors.log. After 10 errors, the program will ask for confirmation before continuing (just as a sanity check, since this may indicate youtube-dl is out of date or some other problem unrelated to the links themselves.) Script will attempt all bad links twice, with a pause between attempts, in order to reduce the number of false positives.
