import pandas as pd
import pickle


from flask import Flask, request, Response
from rossmann.Rossmann import Rossmann

#Loading Model
modelo = pickle.load(open('/home/bruna/Documentos/Rossmann_Stores/model/model_rossman.pkl', 'rb'))

app = Flask(__name__)

@app.route('/rossmann/predict', methods=['POST'])
def rossmann_predict():
    test_json = request.get_json()
    
    if test_json: #there is data
        if isinstance(test_json,dict): #Unique Example       
            test_raw = pd.DataFrame(test_json, index=[0])
       
        else:#Multiple Example
            test_raw = pd.DataFrame(test_json, columns=test_json[0].keys())
            
    
        #Instantiate Rossmann class
        pipeline = Rossmann()

        #data cleaning
        df1 = pipeline.data_cleaning(test_raw)

        #feature engineering
        df2 = pipeline.feature_engineering(df1)

        #data preparation
        df3 = pipeline.data_preparation(df2)

        #prediction
        df_response = pipeline.get_prediction(modelo,test_raw,df3)
    
        return df_response

    else:
        return Response('{}',status=200,mimetype='application/json')
   
    
if __name__ == '__main__':
    
    app.run( host='0.0.0.0')
