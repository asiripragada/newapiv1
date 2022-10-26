import pandas as pd
import numpy as np
import time
from tqdm import tqdm
import json
import openpyxl

def api_function(Price_per_promo,lower_guardrail,upper_guardrail,Incremental_Spend,Step_size):
        data = pd.read_excel('https://viatris.customerinsights.ai/ds/3cZRyN8y255Tg4y', engine='openpyxl')
        data = data[['Brick ID', 'Historical PDEs','Segment', 'Asymptote', 'Curvature']]

        #Price_per_promo = 80 # Inputs
        Historical_Calls = round(sum(data['Historical PDEs']))
        #lower_guardrail = 0.3 # Inputs
        #upper_guardrail = 0.3 # Inputs
        #Incremental_Spend = 1000000 # Inputs
        #Step_size = 1 # Inputs

        Iterations = round(((Incremental_Spend/Price_per_promo)+(lower_guardrail*Historical_Calls))/Step_size)
        # print("Sum of Hist PDEs:", round(Historical_Calls))
        #print(Iterations)
        data['Starting PDE'] = data['Historical PDEs']*(1-lower_guardrail)
        data['Upper Check'] = np.where((data['Starting PDE']+Step_size)/(data['Historical PDEs'])>(1+upper_guardrail),0,1)

        op = pd.DataFrame()
        temp = data.copy()
        temp['Inc PDE'] = temp['Starting PDE']
        for i in tqdm(range(Iterations)):
            #print(i)
            temp['Base Impact'] = temp['Asymptote']*(1-np.exp(-1*temp['Curvature']*(temp['Inc PDE'])))
            temp['Inc Impact'] = np.where(temp['Upper Check'] == 0, 0, temp['Asymptote']*(1-np.exp(-1*temp['Curvature']*(temp['Inc PDE']+Step_size))))
            temp['Impact Diff'] = temp['Inc Impact'] - temp['Base Impact']
            max_impact = np.max(temp['Impact Diff'])
            temp['Inc Flag'] = np.where(temp['Impact Diff'] == max_impact, 1, 0)
            temp['Inc PDE'] = np.where(temp['Inc Flag']==1, temp['Inc PDE']+Step_size,temp['Inc PDE'])
            temp['Upper Check'] = np.where((temp['Inc PDE']+Step_size)/(temp['Historical PDEs'])>(1+upper_guardrail),0,1)                           
        op = pd.concat([op, temp], axis = 0)

        return op


