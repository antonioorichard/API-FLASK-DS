#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""
Created on Sun Apr 20 19:42:04 2025

@author: Antonio Richard
"""
import pickle
from flask import Flask, request, Response
import pandas as pd
import os
import numpy as np

model = pickle.load(open( 'model/model_aws.pkl', 'rb'))

#Iniciar aplicação no Flask
app = Flask( __name__)

# Direcionar rota da aplicação, e o método que permite receber request! 
@app.route('/', methods = ['POST']) 

# Vamos criar a função predição
def get_prediction( ):
    # Solicitar os dados no formato json
    data_json =  request.get_json()
    
    # Fazer uma verificação se dados realmente vinheram
    if data_json:
        if isinstance( data_json, dict): #Verificando se veio como um dicionário
            data_raw = pd.DataFrame(data_json, index = [0])
            # estamos na linha acima convertendo o json para um 
            #dataframe, caso for somente um json.
        else: # vários json
            data_raw = pd.DataFrame( data_json, columns = data_json[0].keys())
            # conversão para vários json.
    
    # Predição
        pred     = model.predict( data_raw)
        
        if pred == 1:
            pred2 = "Uma doença"
        else:
            pred2 = " Não é 1, mas o retorno funcionou!"
        
        return pred2

    # se não der certo vamos retorna alguma coisa na linha abaixo. 
    # Finalizando o processo
    else:
        return Response('{}', status = 200, mimetype = 'application/json')
if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(host = '0.0.0.0', port = port, debug = True)
