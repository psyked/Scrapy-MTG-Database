This project uses the Python 'Scrapy' library to harvest data about cards for Magic: The Gathering and save them locally in a JSON format.

To begin, you will need to install the Scrapy library, with the command:

    easy_install scrapy

Execute crawl with the following command:

    scrapy crawl cards -o items.json -t json