from flask import Flask, render_template, request
from datetime import datetime
import requests
import json

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
czas=datetime.now()

def refresh_data():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    return data

app=Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def welcome():
   # data = refresh_data()


    waluta=''
    waluta1 = ''
    message1 = " "
    if request.method == "POST":
        dane = request.form
        waluta = dane.get('waluta')
        dlugosc=len(waluta)
        ilosc = dane.get('ilosc')
        ''' 
        if ilosc.isdigit() == False:
            message1 = " Wartosc musi być liczbą całkowitą lub zmiennoprzecinkową większą od zera.Wybierz jeszcze raz."
            ilosc = 0
        else:
            ilosc = float(dane.get('ilosc')) '''


        try:
            ilosc = float(dane.get('ilosc'))
            if ilosc<0:
                ilosc=0
                message1 = " Wartosc musi być liczbą całkowitą lub zmiennoprzecinkową większą od zera.Wybierz jeszcze raz."
        except ValueError:
            message1 = " Wartosc musi być liczbą całkowitą lub zmiennoprzecinkową większą od zera.Wybierz jeszcze raz."
            ilosc=0




        waluta1=waluta.strip()
        dlugosc1=len(waluta1)
      #  wynik=0.00

        for item in data[0]["rates"]:
            if item['currency'] == waluta1:
                wynik=item['bid']*ilosc

     #   return "Wybrana waluta: "+waluta1+"dlugosc"+str(dlugosc1)+" wybrana ilosc: "+ilosc+"wynik calkowity to"+str(wynik)
        return render_template("kalkulator_walut.html", message=str(data[0]["effectiveDate"]),message1=message1,
                           tablica=data[0]['table'], data=data[0]["rates"], wynik=round(wynik,2), waluta1=dane.get('waluta'), ilosc=ilosc,
                            opis="Wybrana waluta: "+waluta1+", wybrana ilość: "+str(ilosc)+".   Wynik calkowity to: "+str(round(wynik,2)))


    if request.method == "GET":
        return render_template("kalkulator_walut.html",message=str(data[0]["effectiveDate"]),
                            tablica=data[0]['table'],data= data[0]["rates"],wynik=0.00, waluta1='    ', ilosc=0)


@app.route("/date")
def date():
    return "this page was served at "+str(datetime.now())

counter=0
@app.route("/counter_views")
def counter_views():
    global counter
    counter+=1

    return "this page was served "+str(counter)+ " times"