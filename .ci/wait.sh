#!/bin/bash

echo "Waiting for mysql"
while ! mysqladmin ping -h"mySQL" --silent; do
    sleep 1
done