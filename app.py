from flask import Flask, render_template, request, json
import numpy as np
import pandas as pd


MyApp = Flask(__name__)

df = pd.read_csv('static/data/master_ho_v2.csv');

def getUni(df, fed, col):
   mean_cols = ['ndip_n', 'nent_n', 'nequ_n']
   if fed == 'all':
       if col in mean_cols:
           return df[['department', col]].groupby('department').mean().reset_index().rename(columns={col:'result'})
       else:
           return df[['department', col]].groupby('department').sum().reset_index().rename(columns={col:'result'})
   temp = df.query('fedecode=='+str(fed))[['department', col]].copy(deep=True).reset_index(drop=True)
   return temp.rename(columns={col:'result'})


def test_df(df, department):
	return df[df.department == int(department)].head(1).region.values[0]

def getRatio(df, fed, cols):
   if fed == 'all':
       ndf = df[['department']+cols].copy(deep=True)
       temp = df[['department']+cols].groupby('department').sum().reset_index()
       temp['result'] = temp[cols[0]]/temp[cols[1]]*100
       return temp.reset_index(drop=True)[['department', 'result']]
   else:
       ndf = df.query('fedecode=='+str(fed))[['department']+cols].copy(deep=True)
       ndf['result'] = ndf[cols[0]]/df[cols[1]]*100
       return ndf[['department', 'result']]


def getCorr(df, cols):
   temp = df.groupby('department')[cols].corr()[cols[0]].reset_index().query('level_1==\''+cols[1]+'\'').reset_index()[['department', cols[0]]]
   temp = temp.rename(columns={cols[0] : 'result'})
   return temp



def to_dict(df):
   #converts a pandas.DataFrame to a dictionary
   if 'department' in df.columns:
       tmp = df.set_index('department').to_dict()['result']
   elif 'fed' in df.columns:
       tmp = df.set_index(df.columns[0]).to_dict()['result']
   return str({str(k):v for k, v in tmp.iteritems()}).replace("'", '"')


def getDf(df, var1, metric, fed=None, var2=None):
   if metric == 'uni':
       return getUni(df, fed, var1)
   if metric == 'ratio':
       return getRatio(df, fed, [var1, var2])
   if metric == 'corr':
       return getCorr(df, [var1, var2])




@MyApp.route('/')
def home():
	return render_template('index.html', title = 'Home')


@MyApp.route('/request', methods=['POST', 'GET'])
def request__():
	var1 =str(eval(request.form['var1']))
	var2 =str(eval(request.form['var2']))
	method =str(eval(request.form['method']))
	fede =str(eval(request.form['fede']))
	df_temp = getDf(df, var1, method, fed=fede, var2=var2)
	df_temp.index.name = 'id'
	df_temp.to_csv("static/data/tempfile.csv")
	json_file = df_temp.to_json(orient='records')
	return json.dumps({'status':'OK','answer':'response', 'var1':var1, 'var2':var2, 'method':method, 'fede':fede, 'data':json_file})





if __name__ == "__main__":
	MyApp.run(debug=True)
