#!/bin/sh
# update_nodes.sh: upload the lattest versions of TreeNET and TreeNET Reader on each node involved 
# in the measure campaign (no matter if they had previous versions or not). The existence of 
# the TreeNET folder is also checked.

echo "Updating TreeNET, TreeNET Reader and shell scripts on remote machines"

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
    echo "Updating ${nodes[$i]}"
    commands="mkdir -p TreeNET;"
    ssh ulgple_lisp@${nodes[$i]} -i ~/.ssh/id_rsa -T $commands
    scp -i ~/.ssh/id_rsa /home/jefgrailet/TFE/PlanetLab/treenet ulgple_lisp@${nodes[$i]}:/home/ulgple_lisp/TreeNET
    scp -i ~/.ssh/id_rsa /home/jefgrailet/TFE/PlanetLab/treenet_reader ulgple_lisp@${nodes[$i]}:/home/ulgple_lisp/TreeNET
    i=`expr $i + 1`
done

