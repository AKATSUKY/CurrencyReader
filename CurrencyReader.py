# from datetime import datetime, date, time
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import load_only
import requests
from argparse import ArgumentParser 
from datetime import timedelta, datetime

#BEGIN: You have to define this values to make this work.
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql' #Your own MYSQL URL
access_key = '' #https://currencylayer.com/
#END: 

engine = create_engine(SQLALCHEMY_DATABASE_URI)
session = Session(bind=engine)
Base = declarative_base()

class Currency(Base):
    __tablename__ = "currency"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True ) 
    code = Column(String(3), unique=True )
    stopGetValue = Column(DateTime, nullable = True) 

class CurrencyValue(Base):
    __tablename__ = "currency_value"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    value = Column(Numeric(10,6))
    currencyId = Column(Integer, ForeignKey('currency.id'))

Base.metadata.create_all(engine)

def addNewCurrencyValue(url): 
    print(url)
    response = requests.get(url)
    objs = response.json()
    quotes = objs["quotes"]
    currencies = session.query(Currency).filter_by(stopGetValue=None).all()
    for currency in currencies: 
        newCurrencyValue = CurrencyValue(timestamp = datetime.utcfromtimestamp(objs['timestamp']), value = quotes['USD' + currency.code], currencyId = currency.id)   
        if session.query(CurrencyValue).filter_by(timestamp=newCurrencyValue.timestamp, currencyId=newCurrencyValue.currencyId).first() == None:
            session.add(newCurrencyValue)
    session.commit()        
   
parser = ArgumentParser()
parser.add_argument("c", nargs='?', help="Import Currency")
args = parser.parse_args()

if args.c == 'c':
    #Get Currencies and register in table
    response = requests.get("http://apilayer.net/api/list?access_key=" + access_key + "&format=1")
    objs = response.json()
    for currency in objs["currencies"]:
        auxCurrency = Currency(code=currency, name=objs["currencies"][currency])
        # print auxCurrency.code
        # print auxCurrency.name
        if session.query(Currency).filter_by(code=auxCurrency.code).first() == None:
            session.add(auxCurrency)
    session.commit()
       
    #Get Historical Currency Values, 180 days.
    end_date = datetime.today()
    start_date = end_date - timedelta(days=180) 
    delta = end_date - start_date
    for i in range(delta.days):
        date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        url = 'http://apilayer.net/api/historical?access_key=' + access_key + '&source=USD&format=1&date=' + date
        addNewCurrencyValue(url)
else:
    url = 'http://apilayer.net/api/live?access_key=' + access_key + '&source=USD&format=1'
    addNewCurrencyValue(url)