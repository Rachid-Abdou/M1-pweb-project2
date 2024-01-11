from flask import Flask, render_template
from flask_mysqldb import MySQL
import pandas as pd
import mysql.connector
import os


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rachid2002'
app.config['MYSQL_DB'] = 'db_university'

def get_mysql_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )


@app.route('/')
def index():

    connection = get_mysql_connection()
    df = pd.read_sql('SELECT * FROM resultats', connection)
    # print(df) # to test if the data importing work or no 

# plot1 data:
    plt1_X = list(df['annee'].unique())
    plt1_y = list(df['annee'].value_counts())

    data = {"plot1":[plt1_X, plt1_y]}
    

# plot2 data: 
    plt2_X = list(df['specialite'].unique())         # ["SPECIALITE_1", "SPECIALITE_2"......]
    plt2_y = list(df['specialite'].value_counts())

    # change  ["SPECIALITE_1", "SPECIALITE_2"......] to [1,2,3.....]
    for i, word in enumerate(plt2_X):
        plt2_X[i] = int(word.replace("SPECIALITE_", ""))

    data["plot2"] = {'X':plt2_X, 'y':plt2_y}

    #print(data['plot2']['X']) #just for testing


# plot3 data:
    plt3_y = list(df['moyenne'])
    data["plot3"] = plt3_y

#plot4 data
    
    # Filter data for male and female
    df_m = df[df['sexe'] == 'H'][['specialite','moyenne']]
    df_f = df[df['sexe'] == 'F'][['specialite','moyenne']]

    # Filter data for male and female
    df_male = df[df['sexe'] == 'H'].groupby('specialite')['moyenne'].mean()
    df_female = df[df['sexe'] == 'F'].groupby('specialite')['moyenne'].mean()

    # xm : y male : specialites ["SPECIALITE_1", "SPECIALITE_2"...]
    # ym : y male : mean of all men in each specialite : sum(men moyenne)/len(men in each specialite)
    xm = list(df_male.keys())
    ym = list(df_male)

    xf = list(df_female.keys())
    yf = list(df_female)

    # change  ["SPECIALITE_1", "SPECIALITE_2"......] to [1,2,3.....] for 
    for i in range(len(xm)):
        xm[i] = int(xm[i].replace("SPECIALITE_", ""))
        xf[i] = int(xf[i].replace("SPECIALITE_", ""))

    # add data4 to all data
    data['plot4'] = {"m":[xm, ym], "f":[xf, yf]}
    print(data['plot4'])

    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)