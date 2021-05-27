<?php include_once(".\includes\Functions.php");
include_once(".\includes\dbh.php");

//$stmt = $conn->prepare("DELETE FROM sessions WHERE sessions_user_id = :sessions_user_id;");
//$stmt->bindParam("s", $user_id);
//$stmt->execute(array(":sessions_user_id"=>$_SESSION['user_id']));
func::deleteCookies();

//$_SESSION = [];

header('location:index.php');