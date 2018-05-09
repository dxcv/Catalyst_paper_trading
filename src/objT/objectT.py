#coding:utf-8
from turtleConfig import config as cfg
from catalyst.api import symbol
from collections import deque
import numpy as np

class objectT():
    def __init__(self, name, timeType):
        self.name = name
        self.timeType = cfg['timeType'][timeType]
        self.asset = symbol(name)
        self.ATR = None
        self.unitsHold = 0
        self.state = None
        self.TRs = None
        self.price = []
        #self.setN(data)
        self.ATRs = None
        self.state = 'out'
        self.lastBuyPrice = None
        self.currentPrice = None

    def setATRs(self, data):
        timeLen = self.timeType[0]
        self.TRs = deque(maxlen=timeLen)
        self.ATRs = deque(maxlen=timeLen)
        hist = data.history(self.asset,['high','low','close','price'],timeLen+1,'D')
        for i in range(1,len(hist)):
            high,low,close = hist['high'][i],hist['low'][i],hist['close'][i-1]
            self.price.append(hist['price'][i])
            TR = max([high-low,high-close,close-low])
            self.TRs.append(TR)
            self.ATR = np.mean(np.array(self.TRs))
        self.ATRs.append(self.ATR)

    def update(self, data):
        hist = data.history(self.asset,['high','low','close','price'],2,'D')
        #print len(hist)
        high = hist['high'][1]
        low = hist['low'][1]
        close = hist['close'][0]
        price = hist['price'][1]
        TR = max([high-low,high-close,close-low])
        self.price.append(price)
        self.price = self.price[-(self.timeType[0]+1):]
        self.TRs.append(TR)
        self.ATR = np.mean(np.array(self.TRs))

    def updateCurrentPrice(self, data):
        price = data.current(self.asset, 'price')
        self.currentPrice = price

    def getUnit(self, allMoney):
        return allMoney * cfg['LossRate'] / self.ATR
    
    def getOperator(self):
        #print self.ATR
        if self.state == 'out':
            if self.currentPrice > max(self.price[:-1]):
                self.lastBuyPrice = self.currentPrice
                self.state = 'in'
                self.unitsHold += 1
                return 'entry'
        elif self.state == 'in':
            if self.currentPrice < min(self.price[:-1]):
                self.unitsHold = 0
                self.state = 'out'
                return 'outry'
            if self.currentPrice - max(self.price[:-1]) > cfg['addR']*self.ATR and self.unitsHold<=cfg['holdLimit']:
                self.lastBuyPrice = self.currentPrice
                self.unitsHold += 1
                return 'add'
            elif self.lastBuyPrice - self.currentPrice > cfg['stopR']*self.ATR and self.unitsHold > 0:
                self.unitsHold = 0
                return 'clean'
        else:
            raise DropItem("State Erro!")
        return 'relax'