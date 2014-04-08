Looking for MTG cards data?
===========================
- The output for this set of scripts is included in the `output` folder.
- A better source for this information might be: http://mtgjson.com/

Introduction
============

This project uses the Python 'Scrapy' library to harvest data about cards for Magic: The Gathering and save them locally in a JSON format, along with previews of the card images.

Prerequisites
-------------

To begin, you will need Python 2.7 installed, and will need to install the Scrapy library, which you can install with the command:

    easy_install scrapy

### Windows
If you're on Windows, you might find it tough to install all the required libraries, without Visual Studio 2008. Luckily, you can find pre-built packages for Windows at [http://www.lfd.uci.edu/~gohlke/pythonlibs/#libxml-python](http://www.lfd.uci.edu/~gohlke/pythonlibs/#libxml-python)

### Mac
If you're on Mac, installing `libxml` is still an absolute PITA. But it's possible. 

Running the Project
-------------------
Once Scrapy is installed and running correctly on your machine, you can execute a crawl with the following command:

    scrapy crawl cards -o ../output/data/items.json -t json

This will go off and spider the hardcoded URLs for card data, output the results in JSON format under the `output/data/items.json` file. Images associated with the cards are saved under the images directory, with the MD5 hash of the image used as the filename.

Output
------
A saved copy of the output from the project is available in the `output` branch and/or the `output` folder.
