import pandas as pd
import matplotlib.pyplot as plt

def logger(tra,i):
    for each in tra:
        global perf
        vlu = perf['portfolio_value'][i]
        csh = perf['ending_cash'][i]
        mkt = each['sid']
        amt = each['amount']
        prc = each['price']
        dat = each['dt']
        print dat,mkt,round(amt,2),round(prc,2),round(vlu,2),round(csh,2)


perf = pd.read_pickle('TutleMinute.pickle') # read in perf DataFrame
lineo = perf['portfolio_value']
line = []
for i in range(0*1440,30*1440):
    #line.append(lineo[i*1440])
    print perf['alpha'][i]
    trand = perf['transactions'][i]
    if trand:
        logger(trand,i)
#x = range(len(line))
#plt.plot(x,line)
#plt.show()