#coding:utf-8
#rom sample import *
from Turtle import *
from datetime import datetime
import pytz
from catalyst.utils.run_algo import run_algorithm

start = datetime(2018, 1, 1, 0, 0, 0, 0, pytz.utc)
end = datetime(2018, 5, 1, 0, 0, 0, 0, pytz.utc)
results = run_algorithm(initialize=initialize,
                        handle_data=handle_data,
                        analyze=analyze,
                        start=start,
                        end=end,
                        data_frequency='daily',
                        exchange_name='bitfinex',
                        capital_base=10000,
                        base_currency = 'usd',
                        #output='TutleDaily.pickle'
                        )