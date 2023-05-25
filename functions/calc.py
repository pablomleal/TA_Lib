# Import libraries for Finance (Yahoo Finance) and Technical Analysis
import talib

# Import libraries for data handling and visualization
import numpy as np
import pandas as pd




def get_EMA_df(qema_period, sema_period, rawdata):
    '''Builds a multiindex dataframe composed of two sub-dfs: quick and slow EMA'''
    df_dict = dict((label, pd.DataFrame()) for label in ['Quick', 'Slow', 'Ratio'])

    for x in rawdata.columns:
        df_dict['Quick'][x] = talib.EMA(real2double(rawdata[x].values), timeperiod=qema_period)
        df_dict['Slow'][x] = talib.EMA(real2double(rawdata[x].values), timeperiod=sema_period)
        df_dict['Ratio'][x] = (df_dict['Quick'][x] - df_dict['Slow'][x])/df_dict['Quick'][x]
    
    print ("--> EMA Dataframe calculated.")

    return(pd.concat([df_dict['Quick'], df_dict['Slow'], df_dict['Ratio']], axis=1, keys=['Quick', 'Slow', 'Ratio']))

def get_OBV_df(volumes, closes):
    df_dict= dict()
    for x in volumes.columns:
        df_dict[x] = talib.OBV(real2double(closes[x].values), real2double(volumes[x].values))

    return(pd.DataFrame(df_dict, index = volumes.index))

def get_intersection_point(EMA_df, rawdata):
    '''Returns a df containing:
    Index from where the qEMA started leading the sEMA.
    Value at that time
    Value now
    Average growth since turning point
    '''
    item_positive_bool = (EMA_df['Quick'] - EMA_df['Slow'])>0
    idx_intersection_dict = dict()
    value_intersection_dict = dict()
    value_now_dict = dict()
    growth_dict = dict()

    for company in item_positive_bool.columns:

        #Get the index when qEMA started bullysh trend
        company_positive_bool =(list(item_positive_bool[company]))
        company_positive_bool.reverse()
        turning_change_index = company_positive_bool.index(False)
        idx_intersection_dict[company] = turning_change_index

        #Get both values by the intersection and current, and associated growth
        value_intersection_dict[company] = round(rawdata[company].iloc[-(turning_change_index)],2)
        value_now_dict[company] = round(rawdata[company].iloc[-1],2)
        growth_dict[company] = round((value_now_dict[company] - value_intersection_dict[company])/value_intersection_dict[company],5)

    intersection_points_df = pd.DataFrame([idx_intersection_dict, value_intersection_dict, value_now_dict, growth_dict],
        index = ["Turning point", "Turning value", "Value now", "Percent Growth"]).transpose()#.sort_values(by="Percent Growth", ascending=False)
    
    print ("--> Intersection points found.")
    return (intersection_points_df)


def ratioWrapper(EMA_df, companies, keyStats):
    '''Return two more columns 
    - Average ratio of qEMA / sEMA since qEMA started leading (bullysh trend)
    - Minimum value of that ratio since that moment PLUS two periods (to allow the qEMA to gain momentum)

    The goal is to put first those companies with a stronger qEMA leadership.
    '''
    avgRatio_list = []
    minAbs_list = []

    for company in companies:
        
        getFrom = int(keyStats['Turning point'].loc[company])
        avgRatio = round(EMA_df['Ratio'][company][-getFrom:].mean(),5) * (getFrom > 0 ) 
        avgRatio_list.append(avgRatio)

        MinAbsRatio = round(EMA_df['Ratio'][company][-getFrom+2:].min(),5) * (getFrom > 0 ) 
        minAbs_list.append(MinAbsRatio)

    print ("--> Absolute and Relative Mins calculated.")
    return (avgRatio_list, minAbs_list)

def get_stocks_growing_now(rawdata, keyStats, recent_success_period):
    contribution_list = []
    for x in keyStats.index:
        #Calculate the Y-axis range (max-min of stock in both time frames) and its ratio
        range_local = rawdata[x][-recent_success_period:].values.max() - rawdata[x][-recent_success_period:].values.min()
        range_global = rawdata[x].values.max() - rawdata[x].values.min()
        contribution_recent = range_local/range_global
        
        #Get the X-Axis range (selected time frame w.r.t. total time analysed)
        proportion_recent = recent_success_period/rawdata.shape[0]

        #Get the final ratio and append to list.
        #Ratio 1 means that for 25% of timeframe, 25% of stock range is achieved.
        contribution_ratio = round(contribution_recent/proportion_recent,5)
        contribution_list.append(contribution_ratio)

        #print(f"For {x} in the past {recent_success_period} periods the range was {range_local} over {range_global}, hence contribution ratio is {contribution_ratio}")
        #print(f"Details: contribution_recent = {contribution_recent}, proportion_recent = {proportion_recent}")
    return (contribution_list)



def real2double(real_data):
    return(np.array(real_data,dtype='f8'))


