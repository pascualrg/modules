#!/bin/bash

echo "<odoo><data>"

while read line
do
    nom=$(echo $line | cut -d',' -f1)
    dni=$(echo $line | cut -d',' -f2)
    anyo=$(echo $line | cut -d',' -f3)

    echo "<record id='student$dni' model='school.student'>"
    echo "<field name='name'>$nom</field>"
    echo "<field name='dni'>$dni</field>"
    echo "<field name='birth_year'>$anyo</field>"
    echo "<field name='classroom' ref='school.class1'></field>"
    echo "<field name='profile_pic'>$(base64 profileimg.png)</field>"
    echo "</record>"

done

echo "</data></odoo>"