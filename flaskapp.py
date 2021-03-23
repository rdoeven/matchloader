from flask import Flask, render_template, request
import os
import time
from datetime import timedelta
import matchloader
app = Flask(__name__)

@app.route("/")
def index():
  #if time.time() - os.stat('static/data/wvldesdownP.csv').st_mtime > timedelta(hours=6).total_seconds():
  #  matchloader.update_csv()
  if not os.path.exists("./static/data/"):
    os.makedirs("./static/data/")
  if not os.path.exists("./static/zips/"):
    os.makedirs("./static/zips/")
  matchloader.update_csv()
  return render_template("index.html")

@app.route('/referee', methods=['POST'])
def referee():
  vnaam, fnaam = request.form['vnaam'].lower().strip() ,request.form['fnaam'].lower().strip()
  matches = [mtc.get_dict() for mtc in matchloader.get_matches(vnaam, fnaam)]
  return render_template("referee.html",vnaam=vnaam ,fnaam=fnaam, matches=matches)

@app.route('/match', methods=['GET'])
def match():
  vnaam,fnaam,date,hour=request.args.get('vnaam'),request.args.get('fnaam'),request.args.get('date'),request.args.get('hour')
  reserve=None
  for mtc in matchloader.get_matches(vnaam,fnaam):
    if mtc.hour == hour and mtc.date == date:
      if mtc.statuscode:
        return render_template("match.html", mtc=mtc.get_dict())
      else:
        reserve=mtc
  if reserve != None:
    return render_template("match.html", mtc=mtc.get_dict())
  else:
    return "Match doesn't exist"
    
  

if __name__ == '__main__':
    app.run(debug=True)