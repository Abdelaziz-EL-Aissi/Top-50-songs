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
        y=""
        

coutryfilterd=list(dict.fromkeys(allcountry)) ## removing duplicates from country code to find valid country code
alldataframes=[]
 



for coun in coutryfilterd:
    
    data=[]
    songarray=[]  
    usersarray=[]
    countryarray=[]   
    for line in logfileopen:
        try:
            if(coun.strip().lower().replace("\n","") == line.split("|")[2].lower().replace("\n","")):          
                    songarray.append(line.split("|")[0])                                                 #############split the data to datafrome using  filterd country code
                    usersarray .append(line.split("|")[1])
                    countryarray.append(line.split("|")[2].replace("\n",""))
        except:
            y=""  
    # print(len(songarray))
            
    data.append(songarray)
    data.append(usersarray)
    data.append(countryarray)
    
    # print(len(data))
    data = {'songid':songarray,
        'users':usersarray,
    "country":countryarray}
    
    df = pd.DataFrame(data)
    
    alldataframes.append(df)         ###making data frame for each country and appending it to a variable
            


finallines=""        ##declaring this variable to append the lines to a file
for frame in alldataframes:
    sorted_df = frame.sort_values(by=['users'], ascending=True)           ###sprting each data frome to get ghighest value to top
    
    country=sorted_df.iloc[0]["country"]
    line=country+"|"
    
    
    for i in range(0,50):                       ###getting top 50 song id

        
        line+=sorted_df.iloc[i]["songid"]+":"+sorted_df.iloc[i]["users"]+","        

    finallines+=line+"\n"
    
dater=datetime.today().strftime('%d%m%Y')


fileopen=open(f"country_top50_{dater}.txt","w",encoding="utf-8")  ##writing the file
fileopen.write(finallines)
fileopen.close()