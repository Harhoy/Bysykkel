
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib as mp
from patsy import dmatrices
import numpy as np
import sys

#####STASJONSDATA######

stasjonsdata = open("stasjoner.csv","r")
stasjoner = {}

for line in stasjonsdata:
    data = line.split(';')
    stasjoner[int(data[1])] = {'navn':data[0],'x':float(data[2]),'y':float(data[3].strip('\n'))}

for key,value in stasjoner.items():
    print(key,value)

print(stasjoner)
######SYKKELDATA######

#Import
sykkeldata = pd.read_csv("data.csv", sep = ";")
sykkeldata = sykkeldata.apply(pd.to_numeric,errors = "coerce")
sykkeldata = sykkeldata[sykkeldata['Sykler']>=0]
sykkeldata = sykkeldata.sort_values(by=['ID'])

#Liste med stasjoner
stasjonsliste =sykkeldata.ID.unique()
status = {}
parameterFil = open("parametereOslo.csv","w")

for nummer,stasjon in enumerate(stasjonsliste):
    try:
        #Definerer modell og estimerer den
        endog, exog = dmatrices('Sykler ~ MinMid + I(MinMid**2)+ I(MinMid**3) + I(MinMid**4)', data=sykkeldata[sykkeldata['ID']==stasjon], return_type='dataframe')
        mod = sm.Poisson(endog, exog)
        res = mod.fit(maxiter = 1500)
        #print(res.summary())
        par = res.params
        #ypred = res.predict(exog)
        status[stasjon] = "Ok"
        linje = ""

        parameterFil.write(str(stasjon)+';')
        for i in range(len(par)):
            #print(par[i])
            parameterFil.write(str(par[i])+';')

        x = stasjoner[stasjon]['x']
        y = stasjoner[stasjon]['y']

        try:
            navn = stasjoner[stasjon]['navn']
        except:
            navn = "N/A"

        parameterFil.write(str(x)+';'+str(y)+';'+navn)
        parameterFil.write('\n')

    except:
        status[stasjon] = "Feil"

parameterFil.close()
