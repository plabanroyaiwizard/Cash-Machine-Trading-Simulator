import datetime as dt
from calendar import isleap
from datetime import date

import numpy as np
import pandas as pd
import pandas_datareader as web


class Trading:
    def __init__(self, amount, inp_stock, inp_date, no_of_years, shares):
        self.amount = amount
        self.inp_stock = inp_stock
        self.inp_date = inp_date
        self.no_of_years = no_of_years
        self.shares = shares

    def add_years(self, d, years):
        new_year = d.year + years
        try:
            return d.replace(year=new_year)
        except ValueError:
            if (d.month == 2 and d.day == 29 and  # leap day
                    isleap(d.year) and not isleap(new_year)):
                return d.replace(year=new_year, day=28)
            raise

    def simulate(self):
        stocks = self.inp_stock
        out_date = self.add_years(
            date(int(self.inp_date.split("-")[0]), int(self.inp_date.split("-")[1]), int(self.inp_date.split("-")[2])),
            5).strftime("%Y-%m-%d")
        data = web.DataReader(stocks, "yahoo", start=self.inp_date, end=out_date)
        # print(data)
        SMA30 = pd.DataFrame()
        SMA30 = data['Adj Close'].rolling(window=30).mean()

        SMA100 = pd.DataFrame()
        SMA100 = data['Adj Close'].rolling(window=100).mean()

        specific_compute = pd.DataFrame()

        for i in data['Adj Close'].columns:
            specific_compute[i] = data['Adj Close'][i]
            specific_compute[str('SMA30_' + i)] = SMA30[i]
            specific_compute[str('SMA100_' + i)] = SMA100[i]

        amount = self.amount
        sigBuy = []
        sigSell = []
        flag = -1
        transactions = []

        stocks = stocks[0]
        stock_balance = 0

        for tmp in range(len(specific_compute)):
            if specific_compute[str('SMA30_' + stocks)][tmp] > specific_compute[str('SMA100_' + stocks)][tmp]:
                if flag != 1:
                    sigBuy.append(data['Adj Close'][stocks][tmp])
                    sigSell.append(np.nan)
                    price = round(data['Adj Close'][stocks][tmp], 2)
                    date_time_str = str(specific_compute.index[tmp])
                    date_time_obj = dt.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
                    transactions.append({'stocks': stocks, "amount": price * self.shares, "price": price,
                                         "date": str(date_time_obj.date()), 'type': 'Buy'})
                    flag = 1
                else:
                    sigBuy.append(np.nan)
                    sigSell.append(np.nan)
            elif specific_compute[str('SMA30_' + stocks)][tmp] < specific_compute[str('SMA100_' + stocks)][tmp]:
                if flag != 0:
                    sigBuy.append(np.nan)
                    sigSell.append(data['Adj Close'][stocks][tmp])
                    price = round(data['Adj Close'][stocks][tmp], 2)
                    date_time_str = str(specific_compute.index[tmp])
                    date_time_obj = dt.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
                    transactions.append({'stocks': stocks, "amount": price * self.shares, "price": price,
                                         "date": str(date_time_obj.date()), 'type': 'Sell'})
                    flag = 0
                else:
                    sigBuy.append(np.nan)
                    sigSell.append(np.nan)
            else:
                sigBuy.append(np.nan)
                sigSell.append(np.nan)

        if transactions[0]['type'] == 'Sell':
            del transactions[0]

        for tmp in transactions:
            if tmp['type'] == 'Buy':
                stock_balance += self.shares
                amount = amount - (tmp['price'] * self.shares)
                net_worth = (stock_balance * tmp['price']) + amount
                tmp["amount"] = round(tmp['price'] * self.shares, 2)
                tmp["stock_balance"] = stock_balance
                tmp['budget'] = round(amount, 2)
                tmp['net_worth'] = round(net_worth, 2)
            if tmp['type'] == 'Sell':
                stock_balance -= self.shares
                amount = amount + (tmp['price'] * self.shares)
                net_worth = (stock_balance * tmp['price']) + amount
                tmp["amount"] = round(tmp['price'] * self.shares, 2)
                tmp["stock_balance"] = stock_balance
                tmp['budget'] = round(amount, 2)
                tmp['net_worth'] = round(net_worth, 2)

        return transactions
