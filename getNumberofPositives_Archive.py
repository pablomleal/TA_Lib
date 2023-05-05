numpos = dict()
def countPosEmadifs(x):
    for company in x.columns:
        print (f"Analyzing company {company}...")
        brokenPos = 0
        numpos[company] = 0
        for i in np.arange(-1, -70, -1):
        # print (company)
            if (emadif[i:][company].values[0] > 0):
                # print(f"Company {company} has a positive on item {i}")
                numpos[company] = numpos[company] + 1
            else:
                brokenPos = 1
                break
        if(brokenPos == 1):
            continue
    
countPosEmadifs(emadif)
numpos_df = pd.DataFrame(numpos, index = [0]).transpose().sort_values(by=0, ascending=False)