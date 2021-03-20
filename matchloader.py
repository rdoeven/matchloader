import os
import csv
import zipfile
import urllib.request
class Match:
    def __init__(self, div, date, hour, home, away, status, referee, assistent1, assistent2, referee4, matchtype):
        self.div = div
        self.date = date
        self.hour = hour
        self.home = home
        self.away = away
        if status == "":
            self.status = True
            self.statuscode = "as planned"
        else:
            self.status = False
            self.statuscode = status
        self.referee = referee
        self.assistent1 = assistent1
        self.assistent2 =assistent2
        self.referee4=referee4
        self.matchtype = matchtype

    def getStatus(self):
        return self.status

    def get_dict(self):
        return {
            "div":self.div, 
            "date":self.date,
            "hour":self.hour,
            "home":self.home,
            "away":self.away,
            "statuscode":self.statuscode,
            "status":self.status,
            "referee":self.referee, 
            "assistent1":self.assistent1,
            "assistent2":self.assistent2,
            "referee4":self.referee4,
            "matchtype":self.matchtype,
            "start":self.getStartString(),
            "end":self.getEndString()
        }
    
    def getStartString(self):
        hr,mn = [int(x) for x in self.hour.split(":")]
        d,m,y = [int(x) for x in self.date.split("/")]
        return f"{d}-{m}-{y} {hr}:{mn}"

    def getEndString(self):
        hr,mn = [int(x) for x in self.hour.split(":")]
        d,m,y = [int(x) for x in self.date.split("/")]
        return f"{d}-{m}-{y} {min([hr+3,23])}:{mn}"


    def __str__(self):
        return f"{self.date} {self.hour} {self.home} - {self.away}"

    def __eq__(self, other):
        return self.date == other.date and self.hour == other.hour and self.div == other.div and self.home == self.home and self.away == other.away

def get_matches(vnaam, fnaam):
    matches = []
    naam = f"{fnaam} {vnaam}"
    for csvfile in os.listdir("./static/data"):
        with open(f"static/data/{csvfile}", errors='ignore') as infile:
            csv_reader = csv.reader(infile, delimiter=';')
            for row in csv_reader:
                if naam in [nm.lower() for nm in row[6:10]]:
                    matches.append(Match(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]))
    return matches

def update_csv():
    files = [
    'http://static.belgianfootball.be/project/publiek/download/natdesdownP.zip',
    'http://static.belgianfootball.be/project/publiek/download/wvldesdownP.zip'
    ]
    for url in files:
        urllib.request.urlretrieve(url, "./static/zips/temp.zip")
        unzipfile("./static/zips/temp.zip")

def unzipfile(_file):
    with zipfile.ZipFile(_file,"r") as zip_ref:
        zip_ref.extractall("./static/data")