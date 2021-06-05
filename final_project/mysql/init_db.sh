#!/bin/bash
mysql -u root -ppass;
show databases;
use test_db;
source ./init.sql;
