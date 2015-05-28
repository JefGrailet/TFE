#!/bin/sh
# merge_measures.sh: merge the 9 sets of measurements collected for AS224 and starts TreeNET 
# Reader on a single node (planetlab4.mini.pw.edu.pl, in this case) to recompute the routes and 
# alias resolution hints.

echo "Merging measurements together"

date="22-05"
node="planetlab4.mini.pw.edu.pl"

n_nodes=9
measuresList="/home/jefgrailet/TFE/PlanetLab/AS224/"$date"/AS224_1"
newSet="Measures_AS224_"$date"_To_Refine"
i=2
while [ $i -le $n_nodes ]
do
    measuresList=$measuresList",/home/jefgrailet/TFE/PlanetLab/AS224/"$date"/AS224_$i"
    i=`expr $i + 1`
done

# First merges the measures and places the result in the PlanetLab folder
(cd /home/jefgrailet/TFE/TreeNET/Reader/Release/; ./treenet_reader -i $measuresList -o -l $newSet -a FALSE)
mv /home/jefgrailet/TFE/TreeNET/Reader/Release/$newSet /home/jefgrailet/TFE/PlanetLab

echo $newSet" has been generated"

# Sends the file by SSH to planetlab4.mini.pw.edu.pl
scp -i ~/.ssh/id_rsa /home/jefgrailet/TFE/PlanetLab/$newSet ulgple_lisp@$node:/home/ulgple_lisp/TreeNET
rm /home/jefgrailet/TFE/PlanetLab/$newSet

echo $newSet" has been put on "$node

# Starts TreeNET Reader on planetlab4.mini.pw.edu.pl
command1="cd TreeNET;"
command2="sudo ./treenet_reader -i $newSet -a FALSE -o -r -l Measures_AS224_"$date
commands=$command1" "$command2
ssh ulgple_lisp@$node -i ~/.ssh/id_rsa -t $commands

echo "Routes were successfully recomputed"

# Retrieves the final measures file
scp -r ulgple_lisp@$node:/home/ulgple_lisp/TreeNET/Measures_AS224_$date /home/jefgrailet/TFE/PlanetLab/AS224/$date/

echo "Obtained Measures_AS224_$date"

# Removes it from remote node
echo "Cleaning $node..."
command3="cd TreeNET;"
command4="rm Measures_AS224_"$date";"
command5="rm Measures_AS224_"$date"_To_Refine;"
commandsBis=$command3" "$command4" "$command5
ssh ulgple_lisp@$node -i ~/.ssh/id_rsa -t $commandsBis
