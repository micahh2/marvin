#https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srsearch=poop

import urllib.request
import urllib.parse
from urllib.error import *
import json
from .searchprovider import SearchProvider
from .searchresult import SearchResult

class WikipediaSearchProvider(SearchProvider):
    """Search for info about topics on wikipedia sets."""

    @property
    def title(self):
        return "Wikipedia Results"

    def routine(self, query):
        """Overiding the parents routine to search using the wikipedia.org"""

        success = True
        reply = ""

        try:
            url = "https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srsearch="+urllib.parse.quote_plus(query)
            page = urllib.request.urlopen(url, timeout=2.5)
            jdata = json.loads(page.read().decode('utf-8'))
            for i in jdata["query"]["search"]:
                reply += i["title"] + " : "+ i["snippet"] + "<div class=\"clear space\"></div>"

        except (URLError,KeyError) as e:
            reply = "Failed to connect: " + str(e)
            success = False

        if reply == "":
            success = False

        self.result = SearchResult(reply, confidence=success)
