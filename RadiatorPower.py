#!/usr/bin/env python
##############################################################################################################
# RadiatorPower.py 
# Last Update: October 18th 2020
# V0.1 : Initial Creation
##############################################################################################################
# Imports
##############################################################################################################
import numpy
import matplotlib.pyplot as plot

##############################################################################################################
# Definitions
##############################################################################################################

#RadsonRadiatorEN442CertificatieData is een dictionary met de volgende indeling:
# dict met key = RadiatorHoogte in cm
#    dict met key = Type radiator (11,21,22,33)
#       dict met keys voor vermogens berekening (nExponent,StandaardWperMeter)

RadsonRadiatorEN442CertificatieData = {
   30 : {
      11 : {
          'nExponent' : 1.3145,
          'StandaardWperMeter': 517 },
      21: {
          'nExponent' : 1.3290,
          'StandaardWperMeter': 776 },
      22: {
          'nExponent' : 1.3329,
          'StandaardWperMeter': 1012 },
      33: {
          'nExponent' : 1.3155,
          'StandaardWperMeter': 1418 }},
   40 : {
      11 : {
          'nExponent' : 1.3057,
          'StandaardWperMeter': 687 },
      21: {
          'nExponent' : 1.3284,
          'StandaardWperMeter': 1000 },
      22: {
          'nExponent' : 1.3321,
          'StandaardWperMeter': 1281 },
      33: {
          'nExponent' : 1.3261,
          'StandaardWperMeter': 1805 }},
   50 : {
      11 : {
          'nExponent' : 1.2968,
          'StandaardWperMeter': 848 },
      21: {
          'nExponent' : 1.3278,
          'StandaardWperMeter': 1210 },
      22: {
          'nExponent' : 1.3314,
          'StandaardWperMeter': 1535 },
      33: {
          'nExponent' : 1.3367,
          'StandaardWperMeter': 2169 }},
   60 : {
      11 : {
          'nExponent' : 1.2880,
          'StandaardWperMeter': 1000 },
      21: {
          'nExponent' : 1.3272,
          'StandaardWperMeter': 1409 },
      22: {
          'nExponent' : 1.3306,
          'StandaardWperMeter': 1778 },
      33: {
          'nExponent' : 1.3473,
          'StandaardWperMeter': 2514 }},
   70 : {
      11 : {
          'nExponent' : 1.2889,
          'StandaardWperMeter': 1142 },
      21: {
          'nExponent' : 1.3367,
          'StandaardWperMeter': 1597 },
      22: {
          'nExponent' : 1.3369,
          'StandaardWperMeter': 2011 },
      33: {
          'nExponent' : 1.3545,
          'StandaardWperMeter': 2841 }},
   90 : {
      11 : {
          'nExponent' : 1.2907,
          'StandaardWperMeter': 1397 },
      21: {
          'nExponent' : 1.3557,
          'StandaardWperMeter': 1941 },
      22: {
          'nExponent' : 1.3494,
          'StandaardWperMeter': 2453 },
      33: {
          'nExponent' : 1.3689,
          'StandaardWperMeter': 3448 }},
}

##############################################################################################################
# Functions
##############################################################################################################

def CreateDataArrays(RadiatorDefinitie, Ta, Tkamer):
   RawDeltaTRadiatorArray = numpy.arange(0.01,75.0,0.001)
   DeltaTRadiatorArray = []
   FlowArray = []
   AfgifteVermogenArray = []
   nExponent = RadsonRadiatorEN442CertificatieData[RadiatorDefinitie['HoogteInCentiMeters']][RadiatorDefinitie['Type']]['nExponent']
   StandaardWperMeter = RadsonRadiatorEN442CertificatieData[RadiatorDefinitie['HoogteInCentiMeters']][RadiatorDefinitie['Type']]['StandaardWperMeter']
   RadiatorBreedteInMeters = (0.01*RadiatorDefinitie['BreedteInCentiMeters'])

   for deltaT in RawDeltaTRadiatorArray:
      GemiddeldeRadiatorT = (Ta+Ta-deltaT)/2.0
      DeltaTRadiatorKamer = GemiddeldeRadiatorT-Tkamer
      if DeltaTRadiatorKamer > 0.0:
         RadiatorPower = RadiatorBreedteInMeters*StandaardWperMeter*(pow((DeltaTRadiatorKamer/50.0),nExponent))
         Flow = 60.0*RadiatorPower/(4186.8*deltaT)
         if Flow < MaxFlowToPlot:
            DeltaTRadiatorArray.append(deltaT)
            FlowArray.append(Flow)
            AfgifteVermogenArray.append(RadiatorPower)
   return(DeltaTRadiatorArray, FlowArray, AfgifteVermogenArray)


def AddDeltaTData(DeltaTRadiatorArray, AfgifteVermogenArray, FlowArray):
   for deltaT, power, flow in zip(DeltaTRadiatorArray, AfgifteVermogenArray, FlowArray):
      for interestingDeltaT in DeltaTOfInterest:
         if abs(interestingDeltaT - deltaT) < 0.0001:
            DeltaTVermogensData[interestingDeltaT].append(power)
            DeltaTFlowData[interestingDeltaT].append(flow)

def CreatePlot(PlotAxis, RadiatorDefinitie, FlowArray, AfgifteVermogenArray, Ta):
   PlotAxis.plot(FlowArray, AfgifteVermogenArray,'-', label="Afgifte Vermogen bij Ta="+Ta.__str__()+"C")

def CreateDeltaTPlot(PlotAxis, DeltaTFlowData, DeltaTVermogensData, DeltaT):
   PlotAxis.plot(DeltaTFlowData, DeltaTVermogensData,':', label="Afgifte Vermogen bij DeltaT="+DeltaT.__str__()+"C")

##############################################################################################################
# Main
##############################################################################################################
KamerTemperatuur = float(20.0)
MaxFlowToPlot = float(2.75)

#Tas is een lijst met Ta temperaturen die je wilt plotten.
Tas = [22.5, 25.0, 27.5, 30.0, 32.5, 35.0, 40.0, 45.0, 50.0, 55.0]
DeltaTOfInterest = [0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]

#Radiator definitie, Hoogte en Type moeten uit de onderstaande lijsten komen.
#HoogteLijst=[30,40,50,60,70,90]
#TypeLijst=[11,21,22,33]

RadiatorDefinitie = { 'BreedteInCentiMeters' : 100,
                      'HoogteInCentiMeters' : 60,
                      'Type' : 22 }

DeltaTVermogensData = dict()
DeltaTFlowData = dict()
for deltaT in DeltaTOfInterest:
   EmptyVermogensArray=[]
   EmptyFlowArray=[]
   DeltaTVermogensData[deltaT]=EmptyVermogensArray
   DeltaTFlowData[deltaT]=EmptyFlowArray
   
Figure, PlotAxis = plot.subplots(1,1, figsize=(12,10), frameon = True)
Figure.set_tight_layout(True)
PlotAxis.set_xlim(0.0,(1.30*MaxFlowToPlot))

for Ta in Tas:
   DeltaTRadiatorArray, FlowArray, AfgifteVermogenArray = CreateDataArrays(RadiatorDefinitie, Ta, KamerTemperatuur)
   CreatePlot(PlotAxis, RadiatorDefinitie, FlowArray, AfgifteVermogenArray, Ta)
   AddDeltaTData(DeltaTRadiatorArray, AfgifteVermogenArray, FlowArray)

for deltaT in DeltaTOfInterest:
   CreateDeltaTPlot(PlotAxis, DeltaTFlowData[deltaT], DeltaTVermogensData[deltaT], deltaT)

PlotAxis.set_title("T"+RadiatorDefinitie['Type'].__str__()+" "+RadiatorDefinitie['HoogteInCentiMeters'].__str__()+"x"+RadiatorDefinitie['BreedteInCentiMeters'].__str__()+" Radiator, Truimte="+KamerTemperatuur.__str__()+"C")
PlotAxis.set_xlabel("Flow [liters/minuut]")
PlotAxis.set_ylabel("Afgifte Vermogen [Watt]")
PlotAxis.grid(True)
PlotAxis.legend(loc="upper right", fontsize="8")
plot.show()



