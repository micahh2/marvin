import urllib.request
import urllib.parse
from urllib.error import *
import json
from .searchprovider import SearchProvider
from .searchresult import SearchResult

class DataGovSearchProvider(SearchProvider):
    """Search for data sets."""

    @property
    def title(self):
        return "Data.Gov Results"

    def routine(self, query):
        """Overiding the parents routine to search using the data.gov"""

        success = True
        reply = ""

        try:
            url = "http://catalog.data.gov/api/3/action/resource_search?query=description:"+urllib.parse.quote_plus(query)
            page = urllib.request.urlopen(url, timeout=5.5)
            jdata = json.loads(page.read().decode('utf-8'))
            if jdata["success"]:
                for i in jdata["result"]["results"]:
                    if i["url"].strip() != "":
                        reply += i["name"] + " : "+ i["url"] + "<div class=\"clear space\"></div>"

        except (URLError,KeyError) as e:
            reply = "Failed to connect: " + str(e)
            success = False

        if reply == "":
            success = False

        self.result = SearchResult(reply, confidence=success)
