#!/bin/bash

echo -n "Enter the node to localize id: "
read nodeidTL
echo -n "Enter the first localizor node id: "
read nodeid1
echo -n "Enter the second localizor node id: "
read nodeid2
echo -n "Enter the third localizor node id: "
read nodeid3

echo "Changing files accordingly..."

# Setting the nodes ids
sed -i "s/new_node_id\ =.*/new_node_id\ = ${nodeidTL};/" node_to_localize.c
sed "s/new_node_id\ =.*/new_node_id\ = ${nodeid1};/" localizor.c > localizor1.c
sed "s/new_node_id\ =.*/new_node_id\ = ${nodeid2};/" localizor.c > localizor2.c
sed "s/new_node_id\ =.*/new_node_id\ = ${nodeid3};/" localizor.c > localizor3.c

# Calculating the RIME addresses
u8_0_nodeTL=$(python3 -c "print($nodeidTL & 0xff)")
u8_1_nodeTL=$(python3 -c "print($nodeidTL >> 8)")
u8_0_node1=$(python3 -c "print($nodeid1 & 0xff)")
u8_1_node1=$(python3 -c "print($nodeid1 >> 8)")
u8_0_node2=$(python3 -c "print($nodeid2 & 0xff)")
u8_1_node2=$(python3 -c "print($nodeid2 >> 8)")
u8_0_node3=$(python3 -c "print($nodeid3 & 0xff)")
u8_1_node3=$(python3 -c "print($nodeid3 >> 8)")

# Setting the nodes RIME addresses...
# ... on node_to_localize.c
sed -i "s/addr1\.u8\[0\].*/addr1.u8[0] = ${u8_0_node1};/" node_to_localize.c
sed -i "s/addr1\.u8\[1\].*/addr1.u8[1] = ${u8_1_node1};/" node_to_localize.c
sed -i "s/addr2\.u8\[0\].*/addr2.u8[0] = ${u8_0_node2};/" node_to_localize.c
sed -i "s/addr2\.u8\[1\].*/addr2.u8[1] = ${u8_1_node2};/" node_to_localize.c
sed -i "s/addr3\.u8\[0\].*/addr3.u8[0] = ${u8_0_node3};/" node_to_localize.c
sed -i "s/addr3\.u8\[1\].*/addr3.u8[1] = ${u8_1_node3};/" node_to_localize.c
sed -i "s/from->u8\[0\] ==.*/from->u8[0] == ${u8_0_node3} \&\& from->u8[1] == ${u8_1_node3}) {/" node_to_localize.c
# ... on localizor1.c
sed -i "s/addr2\.u8\[0\].*/addr2.u8[0] = ${u8_0_node2};/" localizor1.c
sed -i "s/addr2\.u8\[1\].*/addr2.u8[1] = ${u8_1_node2};/" localizor1.c
# ... on localizor2.c
sed -i "s/addr2\.u8\[0\].*/addr2.u8[0] = ${u8_0_node3};/" localizor2.c
sed -i "s/addr2\.u8\[1\].*/addr2.u8[1] = ${u8_1_node3};/" localizor2.c
# ... on localizor3.c
sed -i "s/addr2\.u8\[0\].*/addr2.u8[0] = ${u8_0_node1};/" localizor3.c
sed -i "s/addr2\.u8\[1\].*/addr2.u8[1] = ${u8_1_node1};/" localizor3.c

echo "Running make..."
if make TARGET=wismote > /dev/null; then
  if [ "$1" = "flash" ]; then 
    echo "Done! Plug in the Wismote to localize using Olimex. When done, press Enter."
    read -n1 -s
    echo "Flashing the code to the mote..."
    sudo mspdebug olimex "prog node_to_localize.wismote"

    echo "Plug in the first localizor Wismote using Olimex. When done, press Enter."
    read -n1 -s
    echo "Flashing the code to the mote..."
    sudo mspdebug olimex "prog localizor1.wismote"

    echo "Done! Plug in the second localizor Wismote using Olimex. When done, press Enter."
    read -n1 -s
    echo "Flashing the code to the mote..."
    sudo mspdebug olimex "prog localizor2.wismote"

    echo "Done! Plug in the third localizor Wismote using Olimex. When done, press Enter."
    read -n1 -s
    echo "Flashing the code to the mote..."
    sudo mspdebug olimex "prog localizor3.wismote"

    echo "Everything is done!"
  fi
fi
