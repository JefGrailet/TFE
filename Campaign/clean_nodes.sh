#!/bin/sh
# clean_nodes.sh: removes log files from every machine involved in a measure campaign.

echo "Cleaning remote machines from log files"

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
    echo "Cleaning ${nodes[$i]}"
    commands="cd TreeNET; rm AS224_$i; rm AS224_$i.txt;"
    ssh ulgple_lisp@${nodes[$i]} -i ~/.ssh/id_rsa -t $commands
    i=`expr $i + 1`
done
