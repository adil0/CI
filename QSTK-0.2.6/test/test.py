'''

'''

# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def main():
    ''' Main Function'''
    # creating the weights
    wts=[]
    for a in range(0,11,1):
        for b in range(0,11,1):
            for c in range(0,11,1):
                for d in range(0,11,1):
                    wt=[round(a*0.1,2),round(b*0.1,2),round(c*0.1,2),round(d*0.1,2)]
                    if(sum(wt)==1):
                        wts.append(wt)

    # Setting the dates.
    start_date = dt.datetime(2011, 1, 1)
    end_date = dt.datetime(2011,12,31)
    
    # setting the symbols
    symbols=['BRCM', 'ADBE', 'AMD', 'ADI']
    
           
    max_shrp=0    
    for wt in wts:            
#         print(wt)
        vol, daily_ret, sharpe, cum_ret = simulate(start_date, end_date, symbols, wt)
#         print(sharpe)
        if(sharpe > max_shrp):
            max_shrp=sharpe
            opt_wt=wt
            max_vol=vol
            max_daily_ret=daily_ret
            max_sharpe=sharpe
            max_cum_ret=cum_ret
    
    # print the output
    print("Start Date: " + str(start_date.date()))
    print("End Date: " + str(end_date.date()))
    print("Symbols: " + str(symbols))
    print("Optimal Allocations: " + str(opt_wt))
    print("Sharpe Ratio: " + str(max_sharpe))
    print("Volatility (stdev of daily returns):" + str(max_vol))
    print("Average Daily Return: " + str(max_daily_ret))
    print("Cumulative Return: " + str(max_cum_ret))
 
def simulate(start_date,end_date,symbols,allocations):
    
    # Create two list for symbol names and allocation
    ls_port_syms = symbols
    lf_port_alloc = allocations
 
    # Creating an object of the dataaccess class with Yahoo as the source.
    c_dataobj = da.DataAccess('Yahoo')
    ls_all_syms = c_dataobj.get_all_symbols()
  
    # Bad symbols are symbols present in portfolio but not in all syms
    ls_bad_syms = list(set(ls_port_syms) - set(ls_all_syms))

    if len(ls_bad_syms) != 0:
        print "Portfolio contains bad symbols : ", ls_bad_syms

    for s_sym in ls_bad_syms:
        i_index = ls_port_syms.index(s_sym)
        ls_port_syms.pop(i_index)
        lf_port_alloc.pop(i_index)

    # We need closing prices so the timestamp should be hours=16.
    dt_timeofday = dt.timedelta(hours=16)

    # Get a list of trading days between the start and the end.
    ldt_timestamps = du.getNYSEdays(start_date, end_date, dt_timeofday)

    # Keys to be read from the data, it is good to read everything in one go.
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    # Reading the data, now d_data is a dictionary with the keys above.
    # Timestamps and symbols are the ones that were specified before.
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_port_syms, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    # Copying close price into separate dataframe to find rets
    df_rets = d_data['close'].copy()
    # Filling the data.
    df_rets = df_rets.fillna(method='ffill')
    df_rets = df_rets.fillna(method='bfill')
    df_rets = df_rets.fillna(1.0)

    # Numpy matrix of filled data values
    na_rets = df_rets.values
    na_rets= na_rets/na_rets[0]
    # returnize0 works on ndarray and not dataframes.
    na_portrets = np.sum(na_rets * lf_port_alloc, axis=1)    
    tsu.returnize0(na_portrets)
    na_port_total = np.cumprod(na_portrets + 1)
        

    stan_dev= np.std(na_portrets)
    av_ret=np.mean(na_portrets)    
    shrp_rat= av_ret*np.sqrt(252)/stan_dev 
    cum_ret=na_port_total[len(na_port_total)-1]
        
    return stan_dev, av_ret, shrp_rat, cum_ret
 
if __name__ == '__main__':
    main()
