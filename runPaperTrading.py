#coding:utf-8
#rom sample import *
from TurtleM import *
from datetime import datetime
import pytz
from catalyst.utils.run_algo import run_algorithm

results = run_algorithm(initialize=initialize,
                        handle_data=handle_data,
                        analyze=analyze,
                        live=True,
                        #data_frequency='minute',
                        exchange_name='bitfinex',
                        capital_base=10000,
                        base_currency = 'usd',
                        output='PaperTrading.pickle'
                        )
