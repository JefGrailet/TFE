#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Computes and plots the local density in the projection, averaged by subnet prefix length, for a 
# given AS (inputted as a bipartite).

import os
import sys
import numpy as np
from matplotlib import pyplot as plt

if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("Input file is missing")
        sys.exit()
    
    filePath = './' + str(sys.argv[1])
    
    # Optional argument: ylimit (for the plot)
    ylimit = 1
    if len(sys.argv) > 2:
        ylimit = float(sys.argv[2])

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
    
    # Adjacency dictionaries
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
    nbSubnetsMinusArtifacts = 0
    for i in range(0, nbRouters):
        # Ignores artifacts and degree-0 subnets
        if (i + 1) not in adjRS:
            continue
        
        nbSubnetsMinusArtifacts += 1
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
    
    # Computes the average neighbor degree and average neighbor router degree for each prefix 
    # length. It consists of a 12 x 2 array, where each line corresponds to a prefix length 
    # (/20 to /31) and contains 2 cells for 
    # -[0] number of subnets for this prefix length
    # -[1] sum of local densities of each subnet of this prefix length
    
    degreeData = np.zeros((12, 3))
    for i in range(0, nbSubnets):
        if subnets[i] != 'Imaginary' and (i + 1) in projBottom:
            splitted = subnets[i].split("/")
            prefixLength = int(splitted[1])
            
            row = degreeData[prefixLength - 20]
            localDensity = float(len(projBottom[i + 1])) / nbSubnetsMinusArtifacts
            
            row[0] += 1
            row[1] += localDensity
    
    # Computes average local densityby prefix length
    avgLocalDensities = np.zeros((12, 1))
    print("Subnet degree by prefix length:")
    for i in range(0, 12):
        print("/" + str(20 + i) + " subnets:")
        if degreeData[i][0] > 0:
            avgLocalDensity = float(degreeData[i][1]) / degreeData[i][0]
            avgLocalDensities[i] = avgLocalDensity
            print("Average local density: " + str(avgLocalDensity))
        else:
            print("Average local density: 0.0")
    
    # Plots everything together
    splittedFileName = str(sys.argv[1]).split(' ')
    plotFileName = "Local Density Analysis " + splittedFileName[1] + " " + splittedFileName[2]

    x = range(0, 12)
    plt.xticks(x, ["/20", "/21", "/22", "/23", "/24", "/25", 
                   "/26", "/27", "/28", "/29", "/30", "/31"])

    plt.plot(x, avgLocalDensities)
    plt.xlim([0,11])
    plt.ylim([0,ylimit])
    plt.xlabel("Subnet prefix length")
    plt.ylabel("Average local density (projection)")
    plt.savefig(plotFileName + ".pdf")
    plt.clf()
