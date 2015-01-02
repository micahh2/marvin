#!/usr/bin/python3
import csv
import io
from flask import Flask, request, jsonify
from searchproviders.duckduckgo import *
from searchproviders.sympyeval import *
from searchproviders.datagov import *
from searchproviders.wikipedia import *

app = Flask(__name__)

place = 0
history = [""]


#Setup search providers
#ddg = DuckDuckGoSearchProvider()
dg = DataGovSearchProvider()
sp = SymPySearchProvider()
wiki = WikipediaSearchProvider()

def gethistory( num=1):
    if len(history) > place+num and place+num >= 0:
        rval = history[place+num-1]
        place+=num
        entry.delete(0, END)
        entry.insert(0, rval)
    return

def addhistory(query=""):
    history[:0] = [query]
    place=0
    return

def up(event):
    if place == 0 and entry.get() != "":
        addhistory(entry.get())
    gethistory(num=1)
    return

def down(event):
    gethistory(num=-1)
    return

def loadhistory():
    with open("history.csv", newline="") as csvfile:
        hist = csv.reader(csvfile, delimiter=';', quotechar="\"")
        for i in hist:
            for j in i:
                addhistory(j)
    return

def writehistory(self):
    with open("history.csv", 'w', newline="") as csvfile:
        histwrite = csv.writer(csvfile, delimiter=';', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        for i in reversed(history):
            if i != "":
                histwrite.writerow([i])
    return

def quitProgram(self):
    """Quit the program closing any threads"""
    writehistory()

def geturl(sub_url):
    """Returns the suburl"""
    return "" + sub_url

@app.route(geturl("/"), methods=["GET"])
def index():
    """Welcome to edward."""
    return app.send_static_file('index.html')

@app.route(geturl("/query"), methods=["GET", "POST"])
def evaluate():
    q = ""
    if request.method == "GET":
        q= request.values["q"]
    if request.method == "POST":
        q = request.data.decode("utf-8")
    addhistory()

    #started = ddg.query(q)
    started = sp.query(q)
    started = dg.query(q)
    started = wiki.query(q)

    rval = []
    for i in [wiki, sp, dg]:
        if i.get_result().confidence > 0:
            rval[:0] = [{
                "title":i.title,
                "result":i.get_result().ans
            }]

    if len(rval) == 0:
        rval[:0] = [{"title":"No Results", "result":""}]

    return jsonify(json_list=rval)


if __name__ == '__main__':
    #import history
    loadhistory()
    app.run(debug=True)
