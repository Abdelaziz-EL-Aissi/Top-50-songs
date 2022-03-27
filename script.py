import pandas as pd
from datetime import datetime

logfileopen=open("sample_listen-2021-12-01_2Mlines.log","r",encoding="utf-8").readlines() ##reading the log file

allcountry=[]

for line in logfileopen:
    try:
        country=line.split("|")[2].replace("\n","")
        if(len(country)==2):
            allcountry.append(country)  #get only country to group to find valid country code
    except:
        continue
        

coutryfilterd=list(dict.fromkeys(allcountry)) ## removing duplicates from country code to find valid country code
# coutryfilterd == ['NL', 'DE', 'GB', 'BE']

alldataframes=[]
for coun in coutryfilterd:
    
    data=[]
    songarray=[]  
    usersarray=[]
    countryarray=[]   
    for line in logfileopen:
        try:
            if(coun.strip().lower().replace("\n","") == line.split("|")[2].lower().replace("\n","")):          
                    songarray.append(line.split("|")[0])                                                 #############split the data to dataframe using  filterd country code
                    usersarray .append(line.split("|")[1])
                    countryarray.append(line.split("|")[2].replace("\n",""))
        except:
            y=""  
    # print(len(songarray))
            
    data.append(songarray)
    data.append(usersarray)
    data.append(countryarray)
    
    # print(len(data))
    data = {'sng_id':songarray,
        'user_id':usersarray,
    "country":countryarray}
    
    df = pd.DataFrame(data)
    
    alldataframes.append(df)         ###making data frame for each country and appending it to a variable


def top_50_song():

    dater=datetime.today().strftime('%Y%m%d')
    fileopen=open(f"country_top50_{dater}.txt","w",encoding="utf-8")  ##writing the file

    for frame in alldataframes:
        sorted_df = frame.groupby(['sng_id']).size().sort_values(ascending=False)    

        country=frame.iloc[0]["country"]
        line=country+"|"

        for i in range(0,49):                       ###getting top 50 song id
            line+=f'{sorted_df.keys()[i]}' + ":" + f'{sorted_df.values[i]}'+","

        line+=f'{sorted_df.keys()[50]}' + ":" + f'{sorted_df.values[50]}'+"\n"   ##last one

        fileopen.write(line)

    fileopen.close()

top_50_song()




