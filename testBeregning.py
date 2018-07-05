

from math import factorial as fac
import sys
import matplotlib.pyplot as plt
import numpy as np
import time

#Constant
e = 2.7182818284

#My posistion
x = 59.928908
y = 10.73471

#########FUNKSJONER############

#Probabilty of no bikes
def poissonNull(x,l):
    return e**(-l)

def minutter(time,min):
    return time*60+min

#########KLASSE############

#Bike station
class Station:

    def __init__(self,id,par,x,y,navn):
        self._id = id #ID
        self._par = par #Poisson model parameters
        self._navn = navn
        self._x = x
        self._y = y
        for i in range(len(self._par)): #Converting to float from string
            self._par[i] = float(self._par[i])

    #Get probability of no bikes
    def probTom(self,time,minutter):
        min = time*60+minutter
        l = self._par[0]+self._par[1]*min+self._par[2]*min**2+self._par[3]*min**3+self._par[4]*min**4
        l = max(l,0)
        return poissonNull(0,l)


def threeClosest(list):
    pass

def euclidean(x1,x2,y1,y2):
    return ((x1-x2)**2+(y1-y2)**2)**.5

if __name__=="__main__":

    #Getting parameters
    data = open(sys.argv[1],"r") #File with estimated parameters
    timer = float(sys.argv[2]) #Hours key
    min = float(sys.argv[2]) #Minutes key
    update = float(sys.argv[3]) #Sleeping interval (minutes)
    duration = 1 #Total run time of program
    stations =[] #Array to hold refernces to all station objects
    prob = [] #list of probabilites

    utfil = open("ut.csv",'w')

    #Reading parameters from file
    for line in data:
        stationInfo = line.split(';')
        if stationInfo[1] != "nan": #Dropping those where no parameters have been estimated
            stations.append(Station(stationInfo[0],stationInfo[1:6],stationInfo[6],stationInfo[7],stationInfo[8]))

    #Recording start time
    start = time.time()
    #Duration loop
    probs = []
    #Sleep pause
    #Looping through all stations and getting probability
    for s in stations:
        min += 1
        #If we get 60 minutes, we add an hour and reset minutes
        if min == 60:
            timer += 1
            min = 0

        print("P(0)",s.probTom(timer,min),"for stasjon",s._id,s._navn)
        utfil.write(str(s._id)+" " + s._navn+" P(0) " + str(s.probTom(timer,min)))
