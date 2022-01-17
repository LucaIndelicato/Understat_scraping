import requests
from bs4 import BeautifulSoup
import json
import pandas as pd, numpy as np
import pickle

id_= []
minute= []
result= []
X= []
Y= []
xG= []
player= []
h_a= []
player_id= []
situation= []
season= []
shotType= []
match_id= []
h_team= []
a_team= []
h_goals= []
a_goals= []
date= []
player_assisted= []
lastAction= []
error_match_id= []

col_names = ['id' ,
'minute' ,
'result' ,
'X' ,
'Y' ,
'xG' ,
'player' ,
'h_a' ,
'player_id' ,
'situation' ,
'season' ,
'shotType' ,
'match_id' ,
'h_team' ,
'a_team' ,
'h_goals' ,
'a_goals' ,
'date' ,
'player_assisted' ,
'lastAction' ]

# final = pd.read_pickle('final.pkl')
final = pd.DataFrame(columns=col_names)
# last_match_id = int(final.match_id.max())

# wrong_id = pd.read_pickle('wrong_id.pkl')
# wrong_id = pd.DataFrame(columns=['empty_match_id'])
# match = str(input('Please enter the match id:'))


for id_match in np.arange(14116 , 16975 , 1 , dtype=int):
# for id_match in np.arange(last_match_id , last_match_id + 25, 1 , dtype=int):
    
    url  = f"https://understat.com/match/{id_match}"
    
    res = requests.get(url)
    soup = BeautifulSoup(res.content,'lxml')
    scripts = soup.find_all('script')
    try:
        
        strings = scripts[1].string

        # strip unnecessary symbols and get only JSON data 
        ind_start = strings.index("('")+2 
        ind_end = strings.index("')") 
        json_data = strings[ind_start:ind_end] 
        json_data = json_data.encode('utf8').decode('unicode_escape')

        #convert string to json format
        data = json.loads(json_data)    

        data_away = data['a']
        data_home = data['h']

        for index in range(len(data_home)):
            for key in data_home[index]:
                if key =='id':
                    id_.append(data_home[index][key])
                if key =='minute':
                    minute.append(data_home[index][key])
                if key =='result':
                    result.append(data_home[index][key])
                if key =='X':
                    X.append(data_home[index][key])
                if key =='Y':
                    Y.append(data_home[index][key])
                if key =='xG':
                    xG.append(data_home[index][key])
                if key =='player':
                    player.append(data_home[index][key])
                if key =='h_a':
                    h_a.append(data_home[index][key])
                if key =='player_id':
                    player_id.append(data_home[index][key])
                if key =='situation':
                    situation.append(data_home[index][key])
                if key =='season':
                    season.append(data_home[index][key])
                if key =='shotType':
                    shotType.append(data_home[index][key])
                if key =='match_id':
                    match_id.append(data_home[index][key])
                if key =='h_team':
                    h_team.append(data_home[index][key])
                if key =='a_team':
                    a_team.append(data_home[index][key])
                if key =='h_goals':
                    h_goals.append(data_home[index][key])
                if key =='a_goals':
                    a_goals.append(data_home[index][key])
                if key =='date':
                    date.append(data_home[index][key])
                if key =='player_assisted':
                    player_assisted.append(data_home[index][key])
                if key =='lastAction':
                    lastAction.append(data_home[index][key])

        for index in range(len(data_away)):
            for key in data_away[index]:
                if key =='id':
                    id_.append(data_away[index][key])
                if key =='minute':
                    minute.append(data_away[index][key])
                if key =='result':
                    result.append(data_away[index][key])
                if key =='X':
                    X.append(data_away[index][key])
                if key =='Y':
                    Y.append(data_away[index][key])
                if key =='xG':
                    xG.append(data_away[index][key])
                if key =='player':
                    player.append(data_away[index][key])
                if key =='h_a':
                    h_a.append(data_away[index][key])
                if key =='player_id':
                    player_id.append(data_away[index][key])
                if key =='situation':
                    situation.append(data_away[index][key])
                if key =='season':
                    season.append(data_away[index][key])
                if key =='shotType':
                    shotType.append(data_away[index][key])
                if key =='match_id':
                    match_id.append(data_away[index][key])
                if key =='h_team':
                    h_team.append(data_away[index][key])
                if key =='a_team':
                    a_team.append(data_away[index][key])
                if key =='h_goals':
                    h_goals.append(data_away[index][key])
                if key =='a_goals':
                    a_goals.append(data_away[index][key])
                if key =='date':
                    date.append(data_away[index][key])
                if key =='player_assisted':
                    player_assisted.append(data_away[index][key])
                if key =='lastAction':
                    lastAction.append(data_away[index][key])


            df = pd.DataFrame([id_, minute, result, X, Y, xG, player, h_a, player_id, situation, season,  shotType,  
                           match_id, h_team, a_team, h_goals, a_goals, date, player_assisted,lastAction] , index=col_names )
            df = df.T
            df['id'] = df['id'].astype(int) 

        final = pd.concat([final , df] , axis = 0 )
        final.drop_duplicates(subset='id' , inplace=True )
        final['div'] = 'I1'
        final['squadra'] = np.where(final['h_a']=='h' , final['h_team'] , final['a_team'] )
        final['X'] = final['X'].astype(float)
        final['Y'] = final['Y'].astype(float)

        final.to_pickle("final.pkl")
        print("Actual Total Occurrencies: "+ str(final.match_id.count()))
        
# Gestiamo l'errore nei match_id che non contengono dati: 
# raccolgo tutti i match id vuoti e evito di farli ciclare ogni volta        

    except IndexError:
        print('Index error:'+ str(id_match))
#         error_match_id.append(id_match)
#         error = pd.DataFrame([error_match_id] , index=['empty_match_id'])
        
        
#         wrong_id = pd.concat([wrong_id , error] , axis = 0 )
#         wrong_id.to_pickle("wrong_id.pkl")

print("Total Occurrencies: "+ str(final.match_id.count()) +"\n" + 
      "Total match id countd: " + str(final.match_id.nunique()) + "\n"     
#      + "Total Season count is: " + str(final.season.unique()) 
      + "Total wrong_id occured:" + str(wrong_id.nunique()['empty_match_id'])
     )

print(str(final.nunique()['h_team'] )+"\n")

for i in final['h_team'].unique():
    print(i)
  
    
# costruire l'export tutto su sql



