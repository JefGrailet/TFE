#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Outputs some statistics on a given bipartite graph (given as a file). The script relies on two 
# built-in structures of Python: dictionaries and sets, which are used to quickly verify the 
# presence of an edge in the graph, rather than using a (costly) adjacency matrix.

import os
import sys
import gc

if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("Input file is missing")
        sys.exit()
    
    filePath = './' + str(sys.argv[1])

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
    adjSR = dict()
    adjRS = dict()
    adjRS_Sym = dict() # "Symmetric" of adjSR (indexed with subnets rather than routers)
    
    for i in range(0, len(linksSR)):
        splitted = linksSR[i].split(" - ")
        switchIndex = int(splitted[0][1:])
        routerIndex = int(splitted[1][1:])
        
        if switchIndex not in adjSR:
            adjSR[switchIndex] = set()
        
        # Add edge only if it does not exist yet (because of artifacts)
        if routerIndex not in adjSR[switchIndex]:
            adjSR[switchIndex].add(routerIndex)
    
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
    
    # Because artefacts exist and will not be counted in the following steps
    nbRoutersMinusArtefacts = len(adjRS)
    
    # Computes some statistics on the bipartite graphs
    avgSwitchDegree = 0.0
    avgRouterDegree = 0.0
    avgSubnetDegree = 0.0
    highestSwitchDegree = 0
    highestRouterDegree = 0
    highestSubnetDegree = 0
    degree1Routers = 0
    degree1Subnets = 0
    
    # True amounts of edges (computed on the fly to avoid counting artifacts)
    nbEdgesSR = 0
    nbEdgesRS = 0
    
    for i in range(0, nbSwitches):
        curDegree = len(adjSR[i + 1])
        nbEdgesSR += curDegree
        avgSwitchDegree += curDegree
        
        if curDegree > highestSwitchDegree:
            highestSwitchDegree = curDegree
        
    avgSwitchDegree /= nbSwitches
    
    for i in range(0, nbRouters):
        # Ignores artifacts
        if (i + 1) not in adjRS:
            continue
        
        curDegree = len(adjRS[i + 1])
        nbEdgesRS += curDegree
        if curDegree == 1:
            degree1Routers += 1
        elif curDegree == 0:
            nbRoutersMinusArtefacts -= 1
        avgRouterDegree += curDegree
        
        if curDegree > highestRouterDegree:
            highestRouterDegree = curDegree
        
    avgRouterDegree /= nbRoutersMinusArtefacts
    
    for i in range(0, nbSubnets):
        # Ignores artifacts
        if (i + 1) not in adjRS_Sym:
            continue
        
        curDegree = len(adjRS_Sym[i + 1])
        if curDegree == 1:
            degree1Subnets += 1
        avgSubnetDegree += curDegree
        
        if curDegree > highestSubnetDegree:
            highestSubnetDegree = curDegree
    
    avgSubnetDegree /= nbSubnets
    
    possibleEdgesSR = nbSwitches * nbRoutersMinusArtefacts
    possibleEdgesRS = nbRoutersMinusArtefacts * nbSubnets
    
    print("On bipartite graphs:")
    print("Amount of switches: " + str(nbSwitches))
    print("Amount of routers: " + str(nbRoutersMinusArtefacts))
    print("Amount of subnets: " + str(nbSubnets))
    print("Amount of edges (Switches - Routers): " + str(nbEdgesSR))
    print("Amount of edges (Routers - Subnets): " + str(nbEdgesRS))
    print("Possible edges (Switches - Routers): " + str(possibleEdgesSR))
    print("Possible edges (Routers - Subnets): " + str(possibleEdgesRS))
    print("Density (Switches - Routers): " + str(float(nbEdgesSR) / possibleEdgesSR))
    print("Density (Routers - Subnets): " + str(float(nbEdgesRS) / possibleEdgesRS))
    print("Average switch degree: " + str(avgSwitchDegree))
    print("Average router degree: " + str(avgRouterDegree))
    print("Average subnet degree: " + str(avgSubnetDegree))
    print("Highest switch degree: " + str(highestSwitchDegree))
    print("Highest router degree: " + str(highestRouterDegree))
    print("Highest subnet degree: " + str(highestSubnetDegree))
    print("Amount of degree-1 routers: " + str(degree1Routers))
    print("Amount of degree-1 subnets: " + str(degree1Subnets))
    
    # Free memory
    AS = None
    subnets = None
    routers = None
    linksRS = None
    linksSR = None
    adjRS_Sym = None
    adjSR = None
    gc.collect()
    
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
    
    # Some statistics on the projection
    countedEdges = set()
    possibleEdges = 0
    projAvgSubnetDegree = 0.0
    projHighestSubnetDegree = 0
    for i in range(0, nbSubnets):
        possibleEdges += nbSubnets - i - 1
    
        # Ignores artifacts and degree-0 subnets
        if (i + 1) not in projBottom:
            continue
    
        thisSubnetEdges = list(projBottom[i + 1])
        for j in range(0, len(thisSubnetEdges)):
            test1 = (i + 1, thisSubnetEdges[j]) not in countedEdges
            test2 = (thisSubnetEdges[j], i + 1) not in countedEdges
            if test1 and test2:
                countedEdges.add((i + 1, thisSubnetEdges[j]))
        
        curDegree = len(projBottom[i + 1])
        projAvgSubnetDegree += curDegree
        
        if curDegree > projHighestSubnetDegree:
            projHighestSubnetDegree = curDegree
    
    totalEdges = len(countedEdges)
    projAvgSubnetDegree /= nbSubnets
    
    print("\nOn bottom projection:")
    print("Number of edges: " + str(totalEdges))
    print("Possible edges: " + str(possibleEdges))
    print("Density: " + str(float(totalEdges) / float(possibleEdges)))
    print("Average subnet degree: " + str(projAvgSubnetDegree))
    print("Highest subnet degree: " + str(projHighestSubnetDegree))
    
