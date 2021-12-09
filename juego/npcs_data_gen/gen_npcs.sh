#!/bin/bash

echo "<odoo><data>"

$num = 0
while read line
do
    ((num=num+1))
    nombre=$(echo $line | cut -d',' -f1)
    nombreid=$(echo $nombre | cut -d' ' -f1)
    nombreid2=$(echo $nombre | cut -d' ' -f2)
    hambre=$(echo $line | cut -d',' -f2)
    sed=$(echo $line | cut -d',' -f3)
    chapas=$(echo $line | cut -d',' -f4)
    
    echo "<record id='npc$nombreid$nombreid2' model='juego.npc'>"
    echo "<field name='name'>$nombre</field>"
    echo "<field name='hunger'>$hambre</field>"
    echo "<field name='thirst'>$sed</field>"
    echo "<field name='bottle_caps'>$chapas</field>"
    echo "<field name='avatar'>$(base64 avatars/juego_avatar_npc_$num.jpeg)</field>"
    echo "</record>"

done

echo "</data></odoo>"