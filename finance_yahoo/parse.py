import csv
import os.path
from datetime import datetime

import requests
import wget
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from db import Company, Item, engine, Base

Base.metadata.drop_all(bind=engine, tables=[Company.__table__, Item.__table__])
Base.metadata.create_all(bind=engine)

API = 'https://query1.finance.yahoo.com/v7/finance/download/{}?period1=0&period2={}'
search_url = 'https://finance.yahoo.com/trending-tickers'


class Parse:
    ts = int(datetime.today().timestamp())

    @staticmethod
    def get_companies():
        page = requests.get(search_url).text
        soup = BeautifulSoup(page, 'html.parser')
        for el in soup.select('[data-symbol]'):
            yield el['data-symbol']

    def fill_in_db(self):
        session = Session(engine)
        company_names = self.get_companies()
        for company_name in company_names:
            comp = Company(name=company_name)
            session.add(comp)
            session.commit()
            local_file = f'files/{company_name}.csv'
            if os.path.isfile(local_file):
                file = local_file
            else:
                file = wget.download(API.format(company_name, self.ts), local_file)
            with open(file) as f:
                dr = csv.DictReader(f)
                items = []
                for i in dr:
                    items.append(Item(
                        date=i['Date'],
                        open=i['Open'],
                        high=i['High'],
                        low=i['Low'],
                        close=i['Close'],
                        adj_close=i['Adj Close'],
                        volume=i['Volume'],
                        company_id=session.query(Company).get({'id': comp.id}).name,
                    ))
                session.add_all(items)
                session.commit()
        session.close()


parse = Parse()
parse.fill_in_db()
