#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Computes and plots the average neighbors degree (projection) and the average degree of neighbor 
# routers (original bipartite), averaged by subnet prefix length, for a given AS (inputted as a 
# bipartite).

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
    ylimit = 30
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
    
    # Adjacency dictionaries
    adjRS = dict()
    adjRS_Sym = dict() # "Symmetric" of adjSR (indexed with subnets rather than routers)
    
    for i in range(0, len(linksRS)):
        splitted = linksRS[i].split(" - ")
        routerIndex = int(splitted[0][1:])
        subnetIndex = int(splitted[1][1:])
        
        if routerIndex not in adjRS:
            adjRS[routerIndex] = set()
        
        # Add edge only if it does not exist yet (because of artifacts)
        if subnetIndex not in adjRS[routerIndex]:
            adjRS[routerIndex].add(subnetIndex)
        
        if subnetIndex not in adjRS_Sym:
            adjRS_Sym[subnetIndex] = set()
        
        # Add edge only if it does not exist yet (because of artifacts)
        if routerIndex not in adjRS_Sym[subnetIndex]:
            adjRS_Sym[subnetIndex].add(routerIndex)
    
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
    
    # Computes the average neighbor degree and average neighbor router degree for each prefix 
    # length. It consists of a 12 x 3 array, where each line corresponds to a prefix length 
    # (/20 to /31) and contains 3 cells for 
    # -[0] number of subnets for this prefix length
    # -[1] sum of average neighbor degrees of each subnet of this prefix length
    # -[2] sum of average neighbor router degrees of each subnet of this prefix length
    
    degreeData = np.zeros((12, 3))
    for i in range(0, nbSubnets):
        if subnets[i] != 'Imaginary' and (i + 1) in projBottom:
            splitted = subnets[i].split("/")
            prefixLength = int(splitted[1])
            
            row = degreeData[prefixLength - 20]
            row[0] += 1
            
            # Average neighbor subnets degree
            neighborSubnets = list(projBottom[i + 1])
            accumulator = 0
            nbSubnetsAvg = 0
            for j in range(0, len(neighborSubnets)):
                subnetJ = neighborSubnets[j]
                if (subnetJ + 1) in projBottom:
                    accumulator += len(projBottom[subnetJ + 1])
                    nbSubnetsAvg += 1
            
            if nbSubnetsAvg > 0:
                row[1] += float(accumulator) / nbSubnetsAvg
            else:
                row[1] = 0.0
            
            # Average neighbor routers degree
            neighborRouters = list(adjRS_Sym[i + 1])
            accumulator = 0
            nbRoutersAvg = 0
            for j in range(0, len(neighborRouters)):
                routerJ = neighborRouters[j]
                if (routerJ + 1) in adjRS:
                    accumulator += len(adjRS[routerJ + 1])
                    nbRoutersAvg += 1
            
            if nbRoutersAvg > 0:
                row[2] += float(accumulator) / nbRoutersAvg
            else:
                row[2] = 0.0
    
    # Computes average by prefix length
    avgNeighborSubnetsDegrees = np.zeros((12, 1))
    avgNeighborRoutersDegrees = np.zeros((12, 1))
    print("Subnet degree by prefix length:")
    for i in range(0, 12):
        print("/" + str(20 + i) + " subnets:")
        if degreeData[i][0] > 0:
        
            # Average neighbor subnet degree
            avgNeighborSubnetsDegree = float(degreeData[i][1]) / degreeData[i][0]
            avgNeighborSubnetsDegrees[i] = avgNeighborSubnetsDegree
            
            print("Average neighbor subnet (projection) degree: " + str(avgNeighborSubnetsDegree))
            
            # Average neighbor subnet degree
            avgNeighborRoutersDegree = float(degreeData[i][2]) / degreeData[i][0]
            avgNeighborRoutersDegrees[i] = avgNeighborRoutersDegree
            
            print("Average neighbor router (bipartite) degree: " + str(avgNeighborRoutersDegree))
        else:
            print("Average neighbor subnet (projection) degree: 0.0")
            print("Average neighbor router (bipartite) degree: 0.0")
    
    # Plots everything together
    splittedFileName = str(sys.argv[1]).split(' ')
    plotFileName = "Neighbor Degree Analysis " + splittedFileName[1] + " " + splittedFileName[2]

    x = range(0, 12)
    plt.xticks(x, ["/20", "/21", "/22", "/23", "/24", "/25", 
                   "/26", "/27", "/28", "/29", "/30", "/31"])

    plt.plot(x, avgNeighborSubnetsDegrees)
    plt.plot(x, avgNeighborRoutersDegrees)
    plt.xlim([0,11])
    plt.ylim([0,ylimit])
    plt.legend(["Averaged average neighbor subnet degree", 
                "Averaged average neighbor router degree"])
    plt.xlabel("Subnet prefix length")
    plt.ylabel("Degree")
    plt.savefig(plotFileName + ".pdf")
    plt.clf()
