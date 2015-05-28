#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Analyzes the degree of subnets (in the bottom-projection) by prefix length.

import numpy as np
import os
import sys
import math
from matplotlib import pyplot as plt

if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("Input file is missing")
        sys.exit()
    
    filePath = './' + str(sys.argv[1])
    
    # Optional argument: ylimit (for the plot)
    ylimit = 200
    if len(sys.argv) > 2:
        ylimit = int(sys.argv[2])

    if not os.path.isfile(filePath):
        print("Input file does not exist")
        sys.exit()

    with open(filePath) as f:
        AS = f.read().splitlines()

    # Gets all sets of components of the file separately
    subnets = []
    routers = []
    linksSR = []
    linksRS = []
    counter = 0
    nbSwitches = 0
    for i in range(0, len(AS)):
        if not AS[i]:
            counter += 1
        else:
            if counter == 0:
                pos = AS[i].find('-')
                routers.append(AS[i][(pos+2):])
            elif counter == 1:
                pos = AS[i].find('-')
                subnets.append(AS[i][(pos+2):])
            elif counter == 2:
                pos = AS[i].find(' ')
                nbSwitches = int(AS[i][1:pos])
                linksSR.append(AS[i])
            elif counter == 3:
                linksRS.append(AS[i])
    
    nbRouters = len(routers)
    nbSubnets = len(subnets)
    
    # Adjacency dictionary
    adjRS = dict()
    
    for i in range(0, len(linksRS)):
        splitted = linksRS[i].split(" - ")
        routerIndex = int(splitted[0][1:])
        subnetIndex = int(splitted[1][1:])
        
        if routerIndex not in adjRS:
            adjRS[routerIndex] = set()
        
        # Add edge only if it does not exist yet (because of artifacts)
        if subnetIndex not in adjRS[routerIndex]:
            adjRS[routerIndex].add(subnetIndex)
    
    # Projection on subnets
    projBottom = dict()
    for i in range(0, nbRouters):
        # Ignores artifacts and degree-0 subnets
        if (i + 1) not in adjRS:
            continue
    
        subnetList = list(adjRS[i + 1])
        for j in range(0, len(subnetList)):
            for k in range(j + 1, len(subnetList)):
                indexJ = subnetList[j]
                indexK = subnetList[k]
            
                if indexJ not in projBottom:
                    projBottom[indexJ] = set()
                
                if indexK not in projBottom[indexJ]:
                    projBottom[indexJ].add(indexK)
                
                if indexK not in projBottom:
                    projBottom[indexK] = set()
                
                if indexJ not in projBottom[indexK]:
                    projBottom[indexK].add(indexJ)
    
    # Computes the average, max and min degree for each prefix length. It consists of a 12 x 5 
    # array, where each line corresponds to a prefix length (/20 to /31) and contains 5 cells for 
    # -[0] minimum degree
    # -[1] maximum degree
    # -[2] number of subnets (for average degree computation)
    # -[3] sum of degrees of each subnet of this prefix length (for average degree computation)
    # -[4] sum of squared degrees of each subnet for this prefix (for std dev computation)
    
    degreeData = np.zeros((12, 5))
    listByPrefix = [] # For median computation
    for i in range(0, 12):
        listByPrefix.append([])
    
    for i in range(0, nbSubnets):
        if subnets[i] != 'Imaginary' and (i + 1) in projBottom:
            splitted = subnets[i].split("/")
            prefixLength = int(splitted[1])
            
            row = degreeData[prefixLength - 20]
            degree = len(projBottom[i + 1])
            listByPrefix[prefixLength - 20].append(degree)
            
            if degree < row[0] or row[0] == 0:
                row[0] = degree
            
            if degree > row[1]:
                row[1] = degree
            
            row[2] += 1
            row[3] += degree
            row[4] += degree * degree
    
    averageDegrees = np.zeros((12, 1))
    maximumDegrees = np.zeros((12, 1))
    medianDegrees = np.zeros((12, 1))
    standardDeviations = np.zeros((12, 1))
    
    # Computes each metric for each prefix length
    print("Subnet degree by prefix length:")
    for i in range(0, 12):
        print("/" + str(20 + i) + " subnets:")
        print("Minimum degree: " + str(degreeData[i][0]))
        print("Maximum degree: " + str(degreeData[i][1]))
        
        if degreeData[i][2] > 0:
        
            # Average and maximum degree
            averageDegree = float(degreeData[i][3]) / degreeData[i][2]
            averageDegrees[i] = averageDegree
            maximumDegrees[i] = degreeData[i][1]
            
            print("Average degree: " + str(averageDegree))
            
            # Median
            listByPrefix[i].sort()
            listLength = len(listByPrefix[i])
            median = 0
            if listLength % 2 == 0:
                median = listByPrefix[i][(listLength / 2) - 1]
                median += listByPrefix[i][(listLength / 2)]
                median = float(median) / 2
            else:
                median = float(listByPrefix[i][(listLength / 2)])
            medianDegrees[i] = median
            
            print("Median degree: " + str(median))
            
            # Standard deviation
            variance = (float(degreeData[i][4]) / degreeData[i][2])
            variance -= (averageDegree * averageDegree)
            stdDev = math.sqrt(variance)
            standardDeviations[i] = stdDev
            
            print("Standard deviation: " + str(stdDev))
        else:
            print("Average degree: 0.0")
            print("Median degree: 0.0")
            print("Standard deviation: 0.0")
    
    # Plots everything together
    splittedFileName = str(sys.argv[1]).split(' ')
    plotFileName = "Subnet Degree " + splittedFileName[1] + " " + splittedFileName[2]

    x = range(0, 12)
    plt.xticks(x, ["/20", "/21", "/22", "/23", "/24", "/25", 
                   "/26", "/27", "/28", "/29", "/30", "/31"])

    plt.plot(x, averageDegrees)
    plt.plot(x, maximumDegrees)
    plt.plot(x, medianDegrees)
    plt.plot(x, standardDeviations)
    plt.xlim([0,11])
    plt.ylim([0,ylimit])
    plt.legend(["Average degree", "Maximum degree", "Median degree", "Standard Deviation"])
    plt.xlabel("Subnet prefix length")
    plt.ylabel("Degree")
    plt.savefig(plotFileName + ".pdf")
    plt.clf()
    
