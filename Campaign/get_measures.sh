#!/bin/sh
# get_measures.sh: retrieves the measures obtained with TreeNET on the different remote 
# machines. It should be noted that the removal of these measures afterwards is carried out by 
# another script (clean_nodes.sh).

echo "Retrieving measures of AS224 from remote machines"

date="22-05"
mkdir -p $date

n_nodes=9

nodes[1]="planetlab1.cs.colorado.edu"
nodes[2]="sybaris.ipv6.lip6.fr"
nodes[3]="planetlab1.unl.edu"
nodes[4]="planetlab1.xeno.cl.cam.ac.uk"
nodes[5]="planetlab1.upc.es"
nodes[6]="planetlab1.net.in.tum.de" # Previously host2.planetlab.informatik.tu-darmstadt.de
nodes[7]="anateus.ipv6.lip6.fr" # Previously plab2.ple.silweb.pl, plab1.create-net.org
nodes[8]="planetlab4.mini.pw.edu.pl"
nodes[9]="planetlab2.di.unito.it" # Previous planetlab1.unineuchatel.ch

i=1
while [ $i -le $n_nodes ]
do
    echo "Getting measures from ${nodes[$i]}"
    scp -r ulgple_lisp@${nodes[$i]}:/home/ulgple_lisp/TreeNET/AS224_$i /home/jefgrailet/TFE/PlanetLab/AS224/$date/
    i=`expr $i + 1`
done
