#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Computes the amount of subnets of each prefix for each AS (best data set) and a single plot 
# to compare the proportions of each AS.

import numpy as np
import os
import sys
from matplotlib import pyplot as plt
from matplotlib import ticker as ticker

if __name__ == "__main__":

    filePrefix = "Bipartite "
    ASes = ["AS224", "AS5400", "AS3209", "AS7018"]
    dates = ["20-04", "29-03", "13-04", "25-03"]
    folder = "/home/jefgrailet/TFE/PlanetLab/"
    
    ASPrefixes = []
    for x in range(0, 4):
        print("Analysing results of " + ASes[x])

        inputFileName = filePrefix + ASes[x] + " " + dates[x]
        filePath = folder + ASes[x] + "/" + dates[x] + "/" + inputFileName

        if not os.path.isfile(filePath):
            print(filePath + " does not exist")
            continue

        with open(filePath) as f:
            AS = f.read().splitlines()

        # Gets all sets of components of the file separately
        subnets = []
        counter = 0
        for i in range(0, len(AS)):
            if not AS[i]:
                counter += 1
            else:
                if counter == 1:
                    pos = AS[i].find('-')
                    subnets.append(AS[i][(pos+2):])
                else:
                    continue
        
        nbSubnets = len(subnets)
        trueNbSubnets = 0
        
        # Counts the amount of subnets per prefix for this AS and this date.
        prefixesData = np.zeros((12,))
        for i in range(0, nbSubnets):
            if subnets[i] != 'Imaginary':
                splitted = subnets[i].split("/")
                prefixLength = int(splitted[1])
                prefixesData[prefixLength - 20] += 1
                trueNbSubnets += 1
        
        # Normalize the array
        for i in range(0, 12):
            prefixesData[i] = (float(prefixesData[i]) / trueNbSubnets) * 100
        
        # And saves it
        ASPrefixes.append(prefixesData)
        
        print("Done with " + ASes[x])
    
    ASPrefixes = np.array(ASPrefixes)
    
    print(str(ASes[0]) + ": " + str(ASPrefixes[0]))
    print(str(ASes[1]) + ": " + str(ASPrefixes[1]))
    print(str(ASes[2]) + ": " + str(ASPrefixes[2]))
    print(str(ASes[3]) + ": " + str(ASPrefixes[3]))
    
    # Plots results
    plotFileName = "Prefixes comparison"
    
    ind = np.arange(12)
    width = 0.20
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects1 = ax.bar(ind, ASPrefixes[0], width, color='r')
    rects2 = ax.bar(ind + width, ASPrefixes[1], width, color='g')
    rects3 = ax.bar(ind + width * 2, ASPrefixes[2], width, color='b')
    rects4 = ax.bar(ind + width * 3, ASPrefixes[3], width, color='y')
    ax.autoscale(tight=True)
    
    positions = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5]
    labels = ["/20", "/21", "/22", "/23", "/24", "/25", 
              "/26", "/27", "/28", "/29", "/30", "/31"]
    
    a = ax.get_axes()
    a.xaxis.set_major_formatter(ticker.NullFormatter())
    a.xaxis.set_minor_locator(ticker.FixedLocator(positions))
    a.xaxis.set_minor_formatter(ticker.FixedFormatter(labels))

    plt.xlim([0,12])
    plt.ylim([0,60])
    plt.legend(["AS224", "AS5400", "AS3209", "AS7018"], loc='upper left')
    plt.xlabel("Prefix length")
    plt.ylabel("Subnet amount (%)")
    plt.savefig("./" + plotFileName + ".pdf")
    plt.clf()
