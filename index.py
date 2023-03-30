from datetime import date, datetime
from flask import Flask, render_template, request
import requests
from requests.exceptions import ConnectTimeout
from bs4 import BeautifulSoup

app = Flask(__name__)

# Static variable to hold latest exchange rate.
latest_rate = 1.0
latest_update = date(1900, 1, 1)

def get_rate():
   global latest_update
   global latest_rate

   source = 'Banco Central de Nicaragua'
   source_url = "https://www.bcn.gob.ni/"
   if (latest_update < date.today()):
      print('Fetching fresh rate from BCN.gob.ni ...')
      headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0' }

      try:
         bcn_code = requests.get("https://www.bcn.gob.ni/", timeout=4, headers=headers).content
         soup = BeautifulSoup(bcn_code, 'html.parser')
         table_cell = soup.select("#economicos tr:nth-of-type(5) td:nth-of-type(1)")[0]
         cell_value = table_cell.get_text()
         latest_rate = float(cell_value[1:8])
         latest_update = date.today()

      except ConnectTimeout:
         print('Fetching fresh rate from Dele Peso a sus Pesos ...')
         source = 'Dele Peso a sus Pesos'
         dpasp_code = requests.get("https://www.delepesoasuspesos.com/indicadores-economicos/cambio-del-dolar", timeout=3, headers=headers).content
         soup = BeautifulSoup(dpasp_code, 'html.parser')
         table_rows = soup.select("#page-main-content article table:nth-of-type(2) tr")
         table_rows.pop(0)
         for row in table_rows:
            row_date = datetime.strptime(row.select("td.col-1")[0].get_text(), '%Y-%m-%d').date()
            if row_date == date.today():
               latest_rate = float(row.select("td.col-2")[0].get_text())
               source_url = "https://www.delepesoasuspesos.com/indicadores-economicos/cambio-del-dolar"
               latest_update = date.today()
               break

   result = {
      "rate" : latest_rate,
      "source" : source,
      "source_url" : source_url
   }
   return result

@app.route("/", methods=['GET'])
def homepage():
   rate_results = get_rate()
   rate = rate_results['rate']
   source = rate_results['source']
   source_url = rate_results['source_url']
   if (request.args.get('operation') != None and request.args.get('amount') != None):
      print('Received GET parameters!')
      operation = request.args.get('operation')
      amount = request.args.get('amount')
      float_amount = float(amount)
      if (operation == 'usdnio'):
         usd_amount = float(amount)
         nio_amount = round(float(usd_amount) * rate, 2)
      if (operation == 'niousd'):
         nio_amount = float(amount)
         usd_amount = round(float(nio_amount) / rate, 2)
      return render_template("index.html",
         exchange_rate=rate,
         amount=float_amount,
         radio_value=operation,
         latest_update=latest_update.strftime("%d-%b-%Y"),
         source=source,
         source_url=source_url)
      # return render_template("result.html", exchange_rate=rate, usd="US$ {:,.2f}".format(usd_amount), nio="C$ {:,.2f}".format(nio_amount), latest_update=latest_update.strftime("%d-%b-%Y"),source=source,source_url=source_url)
   else:
      print('No parameters ')
      return render_template("index.html",
         exchange_rate="{0:.4f}".format(rate),
         latest_update=latest_update.strftime("%d-%b-%Y"),
         source=source,
         source_url=source_url)
