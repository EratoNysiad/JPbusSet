#-------------------------------------------------
#JbusPyNML: made by Erato
#-------------------------------------------------
#This is JbusPyNML, a variant of PyNML developed specifically for JPbus
#This code is released under GPL v3
#I do not guarantee that it works
#-------------------------------------------------
#Not yet implemented:
#Articulation
#Trams

import pandas as pd
import math
import os

import pysrc.newBus as newBus

main = open('jpbus.pnml', 'w')#w overrides, a appends
main.write("#include \"src/header.pnml\"\n" +
"#include \"src/sorting.pnml\"\n" +
"#include \"src/template.pnml\"\n" +
"#include \"src/loadspeed.pnml\"\n")
main.close()

busList = pd.read_table("pysrc/all.csv", sep = ',')
amountHouses = busList.shape[0]
for i in range(amountHouses):
	newBus.addBus(csvID = i)

print("PNML generated")

#Outputs the final grf file
os.system('make -B')