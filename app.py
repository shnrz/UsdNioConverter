from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_rate():
   bcn_source = requests.request("GET", "https://www.bcn.gob.ni/").content
   soup = BeautifulSoup(bcn_source, 'html.parser')
   table_cell = soup.select("#economicos tr:nth-of-type(5) td:nth-of-type(1)")[0]
   cell_value = table_cell.get_text()
   exchange_rate = float(cell_value[1:8])
   return exchange_rate

@app.route("/", methods=['GET','POST'])
def homepage():
   rate = get_rate()
   if request.method == 'POST':
      if request.form['operation'] == 'usdnio':
         usd_amount = request.form['amount']
         nio_amount = round(float(usd_amount) * rate, 2)
         return render_template("result.html", exchange_rate=rate, usd="US$ {:,.2f}".format(float(usd_amount)), nio="C$ {:,.2f}".format(nio_amount))
      else:
         nio_amount = request.form['amount']
         usd_amount = round(float(nio_amount) / rate, 2)
         return render_template("result.html", exchange_rate=rate, usd="US$ {:,.2f}".format(usd_amount), nio="C$ {:,.2f}".format(float(nio_amount)))
   else:
      return render_template("index.html", exchange_rate=rate)

@app.route("/usdtonio/<usd>")
def usd_convert(usd):
   rate = get_rate()
   usd_amount = float(usd)
   nio_amount = round(float(usd_amount) * rate, 2)
   return render_template("result.html", exchange_rate=rate, usd="US$ {:,.2f}".format(usd_amount), nio="C$ {:,.2f}".format(nio_amount))

@app.route("/niotousd/<nio>")
def nio_convert(nio):
   rate = get_rate()
   nio_amount = float(nio)
   usd_amount = round(float(nio_amount) / rate, 2)
   return render_template("result.html", exchange_rate=rate, usd="US$ {:,.2f}".format(float(usd_amount)), nio="C$ {:,.2f}".format(nio_amount))
