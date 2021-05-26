<?php

$dbServername ='localhost';
$dbUsername = 'root';
$dbPassword = '';
$dbName = 'truthfinder';

$dsn = 'mysql:dbname=truthfinder;host=127.0.0.1';
$user = 'root';
$password = '';

//$conn = mysqli_connect($dbServername, $dbUsername, $dbPassword, $dbName );
$conn = new PDO($dsn, $user, $password);
//$dbh = new PDO ('mysql:dbname= truthfinder; port= 3306;host = localhost','root','');