This project uses the Python 'Scrapy' library to harvest data about cards for Magic: The Gathering and save them locally in a JSON format, along with previews of the card images.

To begin, you will need Python 2.7 installed, and will need to install the Scrapy library, which you can install with the command:

    easy_install scrapy

If you're on Windows, you might find it tough to install all the required libraries, without Visual Studio 2008. Luckily, you can find pre-built packages for Windows at [http://www.lfd.uci.edu/~gohlke/pythonlibs/#libxml-python](http://www.lfd.uci.edu/~gohlke/pythonlibs/#libxml-python)

You can execute a crawl with the following command:

    scrapy crawl cards -o items.json -t json