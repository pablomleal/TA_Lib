# Import libraries for data handling and visualization
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


def filter_companies(keyStats, filterSet=False):
    print ("Starting filtering...")
    keyStats.sort_values(by='avgRatio', ascending=False, inplace=True)
    if (filterSet):
        if("aboveAvgRatio" in filterSet.keys()): keyStats = keyStats[keyStats['avgRatio'] >= filterSet['aboveAvgRatio']]
        if("aboveMinAbs" in filterSet.keys()): keyStats = keyStats[keyStats['MinAbsRatio'] >= filterSet['aboveMinAbs']]
        if("minPositivePeriod" in filterSet.keys()): keyStats = keyStats[keyStats['Turning point'] >= filterSet['minPositivePeriod']]
        if("ratioContr" in filterSet.keys()): keyStats = keyStats[keyStats['ratioContr'] >= filterSet['ratioContr']]
        if("latestGrowth" in filterSet.keys()): keyStats = keyStats[keyStats['latestGrowth'] >= filterSet['latestGrowth']]
        print (f"--> Main companies filtered. {keyStats.shape[0]} outstanding companies.")

    result = pd.DataFrame({'Symbol': keyStats.index.values})
    return (result) 

def get_chart_labels(company, keyStats):
    turning_value = str(keyStats.loc[company, 'Turning value'])
    value_now = str(keyStats.loc[company, 'Value now'])
    percent_growth = str(round(100*keyStats.loc[company, 'Percent Growth'],2))
    turning_point = str(int(keyStats.loc[company, 'Turning point']))
    last_label = "since beginning of chart" if (turning_point == 0) else " in last " + turning_point + " days testing"
    label = turning_value + " to " + value_now + " (" + percent_growth + "%)" + last_label
    #print(label)
    return(label)



def plot_all(closes, EMA_df, OBV_df, filteredCompanies, tickers_df, keyStats, limit=10):
    print (f"Displaying {min(limit, filteredCompanies.shape[0])} first companies")

    x_axis = closes.index

    for x in (filteredCompanies[0:limit]['Symbol']):
        t = get_chart_labels(x, keyStats)
        #print(f"Company {x}")
        fig, axs = (plt.subplots(2, sharex=True))

        maxlim = max(closes[x])
        axs[0].set_title(tickers_df.loc[x]['Name'] + " (" + x +")")
        axs[0].plot(x_axis, EMA_df['Quick'][x], 'r')
        axs[0].plot(x_axis, EMA_df['Slow'][x], 'b')
        axs[0].plot(x_axis, closes[x], 'g')
        axs[0].set_ylim([0.5*maxlim, 1.25*maxlim])
        axs[0].tick_params(axis='x', labelrotation = 45)

        axs[1].plot(x_axis, OBV_df[x], 'g')
        axs[1].tick_params(axis='x', labelrotation = 45)
        axs[0].text(0, 0.6*maxlim, t, ha="left", fontsize=10, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})




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