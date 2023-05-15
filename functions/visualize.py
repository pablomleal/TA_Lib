# Import libraries for data handling and visualization
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


def filter_companies(keyStats, filterSet=False):
    keyStats.sort_values(by='avgRatio', ascending=False, inplace=True)
    if (filterSet):
        if("aboveAvgRatio" in filterSet.keys()): keyStats = keyStats[keyStats['avgRatio'] >= filterSet['aboveAvgRatio']]
        if("aboveMinAbs" in filterSet.keys()): keyStats = keyStats[keyStats['MinAbsRatio'] >= filterSet['aboveMinAbs']]
        if("minPositivePeriod" in filterSet.keys()): keyStats = keyStats[keyStats['Turning point'] >= filterSet['minPositivePeriod']]
        if("ratioContr" in filterSet.keys()): keyStats = keyStats[keyStats['ratioContr'] >= filterSet['ratioContr']]
        if("latestGrowth" in filterSet.keys()): keyStats = keyStats[keyStats['latestGrowth'] >= filterSet['latestGrowth']]
        print (f"Main companies filtered. {keyStats.shape[0]} outstanding companies.")

    result = pd.DataFrame({'Symbol': keyStats.index.values})
    return (result) 

def plot_all(rawdata, EMA_df, filteredCompanies, limit=10):
    print (f"Displaying {min(limit, filteredCompanies.shape[0])} first companies")
    x_axis = rawdata.index

    for x in (filteredCompanies[0:limit]['Symbol']):
        print(f"Company {x}")
        plt.plot(x_axis, EMA_df['Quick'][x], 'r')
        plt.plot(x_axis, EMA_df['Slow'][x], 'b')
        plt.plot(x_axis, rawdata[x], 'g')
        plt.show()


""" def new_viz():
    

    selCompanies = filteredCompanies[0:10]['Symbol']
    fig, axs = plt.subplots(nrows=10, sharex=True)

    for (ax, company) in zip(axs, selCompanies):
        ax.set_title(company)
        ax.plot(x_axis, EMA_df['Quick'][company], color='r')
        ax.plot(x_axis, EMA_df['Slow'][company], color='b')
        ax.plot(x_axis, rawdata[company], color='g')
        ax.tick_params(axis='x', labelrotation = 45)
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1)) 
    
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.grid(True)
    ax.set_ylabel(r'Price [\$]')

def plot_one(x):
    x_axis = rawdata.index
    plt.plot(x_axis, EMA_df['Quick'][x], 'r')
    plt.plot(x_axis, EMA_df['Slow'][x], 'b')
    plt.plot(x_axis, rawdata[x], 'g')
    plt.show() """