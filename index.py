from sqlite3 import DateFromTicks
from flask import Flask, render_template, request
import requests
from requests.exceptions import ConnectTimeout
from bs4 import BeautifulSoup
from datetime import date, datetime

app = Flask(__name__)

# Static variable to hold latest exchange rate.
latest_rate = 1.0
latest_update = date(1900, 1, 1)

def get_rate():
   global latest_update
   global latest_rate

   source = 'Banco Central de Nicaragua'
   if (latest_update < date.today()):
      print('Fetching fresh rate from BCN.gob.ni ...')
      headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0' }

      try:
         bcn_source = requests.get("https://www.bcn.gob.ni/", timeout=4, headers=headers).content
         soup = BeautifulSoup(bcn_source, 'html.parser')
         table_cell = soup.select("#economicos tr:nth-of-type(5) td:nth-of-type(1)")[0]
         cell_value = table_cell.get_text()
         latest_rate = float(cell_value[1:8])

      except ConnectTimeout:
         print('Fetching fresh rate from Dele Peso a sus Pesos ...')
         source = 'Dele Peso a sus Pesos'
         dpasp_source = requests.get("https://www.delepesoasuspesos.com/indicadores-economicos/cambio-del-dolar", timeout=3, headers=headers).content
         soup = BeautifulSoup(dpasp_source, 'html.parser')
         table_rows = soup.select("#page-main-content article table:nth-of-type(2) tr")
         table_rows.pop(0)
         for row in table_rows:
            row_date = datetime.strptime(row.select("td.col-1")[0].get_text(), '%Y-%m-%d').date()
            if row_date == date.today():
               latest_rate = float(row.select("td.col-2")[0].get_text())
               break

   latest_update = date.today()
   return [latest_rate, source]

@app.route("/", methods=['GET','POST'])
def homepage():
   rate_results = get_rate()
   rate = rate_results[0]
   source = rate_results[1]
   source_url = "https://www.bcn.gob.ni/"
   if source != 'Banco Central de Nicaragua':
      source_url = "https://www.delepesoasuspesos.com/indicadores-economicos/cambio-del-dolar"
   if request.method == 'POST':
      if request.form['operation'] == 'usdnio':
         usd_amount = request.form['amount']
         nio_amount = round(float(usd_amount) * rate, 2)
      else:
         nio_amount = request.form['amount']
         usd_amount = round(float(nio_amount) / rate, 2)
      return render_template("result.html", exchange_rate=rate, usd="US$ {:,.2f}".format(float(usd_amount)), nio="C$ {:,.2f}".format(float(nio_amount)), latest_update=date.today().strftime("%d-%b-%Y"), source=source, source_url=source_url)
   else:
      global latest_update
      return render_template("index.html", exchange_rate="{0:.4f}".format(rate), latest_update=latest_update.strftime("%d-%b-%Y"), source=source, source_url=source_url)

@app.route("/usdtonio/<usd>")
def usd_convert(usd):
   rate = get_rate()
   global latest_update
   usd_amount = float(usd)
   nio_amount = round(float(usd_amount) * rate, 2)
   return render_template("result.html", exchange_rate=rate, usd="US$ {:,.2f}".format(usd_amount), nio="C$ {:,.2f}".format(nio_amount), latest_update=latest_update.strftime("%d-%b-%Y"))

@app.route("/niotousd/<nio>")
def nio_convert(nio):
   rate = get_rate()
   global latest_update
   nio_amount = float(nio)
   usd_amount = round(float(nio_amount) / rate, 2)
   return render_template("result.html", exchange_rate=rate, usd="US$ {:,.2f}".format(float(usd_amount)), nio="C$ {:,.2f}".format(nio_amount), latest_update=latest_update.strftime("%d-%b-%Y"))
