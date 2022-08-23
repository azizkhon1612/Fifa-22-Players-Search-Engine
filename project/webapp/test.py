# load the libraries
import datetime
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from waitress import serve
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient
# suppress all warnings (ignore unnecessary warnings msgs)
import warnings
warnings.filterwarnings("ignore")

# define the flask and template directory 
app = Flask(__name__,template_folder='templates')


# 152.70.93.112 is the local mongodb address installed
client = MongoClient('mongodb://152.70.93.112/')

# getting my database
db = client['fifa18012835'] 

# serve the index 
@app.route("/")
def index():
    
    return render_template('form.html')

# handle the form action
@app.route("/search", methods=["GET"])
def search_result():
    
    args = request.args
    player = args.get('player')
    
    if(player is not None):
        print('search player:', player) #checking input
        results = findbyname(player)
    
    age = args.get('age',type=int)
    overall = args.get('overall',type=int)
    if((age and overall) is not None):
        # search by age and overall ranking
        print('Age:', age)
        print('Name:',overall)
        
        results = findbyage(age,overall)
        
    
    return render_template('result.html', results=results)

    
# function to retrieve last data from mongodb
def findbyname(plname):
    
    players = db['Players']
    
    results = players.find({'short_name':{'$regex': plname}})
    results_formatted = list()
    for data in results:
        long_name = data['long_name']
        player_age=data['age']
        overall = data['overall']
        player_face_url=data['player_face_url']
        value=data['value_eur']
        wage=data['wage_eur']
        
        single_player = {
            'long_name': long_name,
            'player_age': player_age,
            'overall': overall,
            'player_face_url': player_face_url,
            'value': str(value/10000)[:-4]+'M'+' €',
            'wage': str(wage/1000)[:-3]+'M'+' €'
        }
        
        results_formatted.append(single_player)
        
    return results_formatted

def findbyage(plage,ploverall):
    print(plage)
    print(ploverall)
    players= db['Players']

    results =players.find({'age':{'$gte':plage},'overall':{'$gte':ploverall}}) # above or equal to certain age and overall rating

    results_formatted = list()
    for data in results:
        long_name = data['long_name']
        player_age=data['age']
        overall = data['overall']
        player_face_url=data['player_face_url']
        value=data['value_eur']
        wage=data['wage_eur']
       
        single_player = {
            'long_name': long_name,
            'player_age': player_age,
            'overall': overall,
            'player_face_url': player_face_url,
            'value': str(value/10000)[:-4]+'M'+' €',
            'wage': str(wage/1000)[:-3]+'M'+' €'
        }
        results_formatted.append(single_player)
        
    return results_formatted

if __name__ == "__main__":
    '''
     # change the port number, available from 5200-5210
    '''
    portNumber = 5200 # change this portnumber based on above slots
    hostAddress = '0.0.0.0' # public ip or change to '127.0.0.1' for localhost in your local computer
    print('The webapp can be accessed at', hostAddress+':'+str(portNumber))
    serve(app, host=hostAddress, port=portNumber)
    