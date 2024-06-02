#!/bin/bash

echo -n "Enter the alpha node id: "
read nodeidalpha
echo -n "Enter the helper node id: "
read nodeidhelper

echo "Changing files accordingly..."

# Setting the nodes ids
sed -i "s/new_node_id\ =.*/new_node_id\ = ${nodeidalpha};/" alpha.c
sed -i "s/new_node_id\ =.*/new_node_id\ = ${nodeidhelper};/" helper.c

# Calculating the helper RIME address
u8_0_nodehelper=$(python3 -c "print($nodeidhelper & 0xff)")
u8_1_nodehelper=$(python3 -c "print($nodeidhelper >> 8)")

# Setting the helper RIME address
sed -i "s/addr_helper\.u8\[0\].*/addr_helper.u8[0] = ${u8_0_nodehelper};/" alpha.c
sed -i "s/addr_helper\.u8\[1\].*/addr_helper.u8[1] = ${u8_1_nodehelper};/" alpha.c

echo "Running make..."
if make TARGET=wismote > /dev/null; then
  if [ "$1" = "flash" ]; then 
    echo "Done! Plug in the alpha Wismote using Olimex. When done, press Enter."
    read -n1 -s
    echo "Flashing the code to the mote..."
    sudo mspdebug olimex "prog alpha.wismote"

    echo "Plug in the helper Wismote using Olimex. When done, press Enter."
    read -n1 -s
    echo "Flashing the code to the mote..."
    sudo mspdebug olimex "prog helper.wismote"

    echo "Everything is done!"
  fi
fi
