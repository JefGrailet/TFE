#!/bin/sh
# launch_campaign.sh: starts a measure campaign on AS224 with 9 PlanetLab nodes. Each node has 
# its own targets.

echo "Launching measure campaign on AS224"

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

targets[1]="78.91.0.0/16,84.38.14.0/23,129.177.0.0/16,157.249.0.0/16"
targets[2]="128.39.0.0/16,192.146.238.0/23"
targets[3]="129.240.0.0/16"
targets[4]="129.241.0.0/16"
targets[5]="129.242.0.0/16"
targets[6]="144.164.0.0/16,151.157.0.0/16,152.94.0.0/16"
targets[7]="158.36.0.0/15"
targets[8]="158.38.0.0/15"
targets[9]="161.4.0.0/16,192.111.33.0/24,193.156.0.0/15"

i=1
while [ $i -le $n_nodes ]
do
    echo "Contacting ${nodes[$i]} to start measures..."
    command1="cd TreeNET;"
    command2="sudo -S -b ./treenet -t ${targets[$i]} -c 256 -o AS224_$i > AS224_$i.txt 2>&1 &"
    commands=$command1" "$command2
    ssh ulgple_lisp@${nodes[$i]} -i ~/.ssh/id_rsa -t $commands
    i=`expr $i + 1`
done

