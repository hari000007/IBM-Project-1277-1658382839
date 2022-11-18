from flask import Flask,render_template,request

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "00CH8SAp9c5TMbHRGkAh6b6PmNxkfFxmWa68zY-yuVkO"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}



#model=pickle.load(open('flight.pkl','rb'))
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/prediction',methods=['POST'])
def predict():
    name=request.form['name']
    month=request.form['month']
    dayofmonth = request.form['dayofmonth']
    dayofweek = request.form['dayofweek']
    origin = request.form['origin']
    if(origin == "msp"):
        origin1,origin2,origin3,origin4,origin5 = 0,0,0,0,1
    if(origin == "dtw"):
        origin1,origin2,origin3,origin4,origin5= 1,0,0,0,0
    if(origin == "jfk"):
        origin1,origin2,origin3,origin4,origin5 = 0,0,1,0,0
    if(origin == "sea"):
        origin1,origin2,origin3,origin4,orgin5 = 0,1,0,0,0
    if(origin == "alt"):
        origin1,origin2,origin3,origin4,origin5 = 0,0,0,1,0
        
    destination = request.form['destination']
    if(destination == "msp"):
        destination1,destination2, destination3,destination4,destination5 =0,0,0,0,1
    if(destination == "dtw"):
        destination1,destination2, destination3,destination4,destination5 = 1,0,0,0,0
    if(destination == "jfk"):
        destination1,destination2, destination3,destination4,destination5 = 0,0,1,0,0
    if(destination == "sea"):
        destination1,destination2, destination3,destination4,destination5 =0,1,0,0,0
    if(destination == "alt"):
        destination1,destination2, destination3,destination4,destination5 =0,0,0,1,0
    dept = request.form['dept']
    arrtime = request.form['arrtime']
    actdept = request.form['actdept']
    dept15 = int(dept) - int(actdept)
    print(dept15)
    
    total = [[name,month,dayofmonth,dayofweek,origin1,origin2,origin3,origin4,origin5,destination1,destination2,destination3,destination4,destination5,dept15,arrtime]]
    #y_pred = model.predict(total)
    
    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    #payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored, another_array_of_values_to_be_scored]}]}
    payload_scoring = {"input_data": [{"fields": ["EnterflightNum","Month","Dayofmonth","Dayofweek","origin","Destination","scheduleddeparturetime","scheduledarrivaltime","actualdeparturetime"],"values":[1.768e+03, 6.000e+00, 1.300e+01, 1.000e+00, 4.000e+00, 3.000e+00,
       1.300e+01, 0.000e+00, 0.000e+00]}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/a49cde5f-7a8f-4af8-9418-45bdef9ed9d9/predictions?version=2022-11-17', json = payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions= response_scoring.json()
    ans=predictions['predictions'][0]['values'][0][0]
    print(ans)
    
    #print(y_pred)
    if (ans == 0):
            ans = "The Flight will be on time"
    else:
            ans = "The Flight will be delayed"
    print(ans)
    return render_template("index.html",showcase = ans)
if __name__=='__main__':
    app.run(debug = False)




