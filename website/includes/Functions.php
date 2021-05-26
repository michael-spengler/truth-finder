<?php
include_once(".\includes\dbh.php");
class func
{
    //Kreirt Random String zur Verifizierung der Session

    public static function createString($len)
    {
        $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
        $s = "";
        $r_new = "";
        $r_old = "";

        for ($i = 0; $i < $len; $i++) {
            $s .= $characters[mt_rand(0, strlen($characters) - 1)];
        }

        return $s;
    }
    //Checkt den Login Status des Users

    public static function CheckLoginState($conn)
    {
        if (!isset($_SESSION["id"]) || !isset($_COOKIE["PHPSESSID"]))
        {
            session_start();
        }
        if (isset($_COOKIE["userid"]) && isset($_COOKIE["token"])&& isset($_COOKIE["serial"]))
        {
            $query = "SELECT * FROM sessions WHERE sessions_user_id = :userid AND sessions_token = :token AND sessions_serial = :serial;";

            $userid = $_COOKIE["userid"];
            $token = $_COOKIE["token"];
            $serial = $_COOKIE["serial"];

            $stmt = $conn->prepare($query);
            $stmt->execute(array(":userid"=> $userid, ":token"=> $token,":serial"=> $serial));

            $row = $stmt->fetch(PDO::FETCH_ASSOC);

            if($row["sessions_user_id"]>0){
                if ($row["sessions_user_id"] == $_COOKIE["userid"] &&
                    $row["sessions_token"] == $_COOKIE["token"] &&
                    $row["sessions_serial"] == $_COOKIE["serial"]);
            
                {
                    if ($row["sessions_user_id"] == $_SESSION["userid"] &&
                        $row["sessions_token"] == $_SESSION["token"] &&
                        $row["sessions_serial"] == $_SESSION["serial"]);
                }

                {
                    return true;
                }
            }
        }
    }

    public static function createRecord($conn, $user_username, $user_id)
    {
        //$row["user_username"],
        //$userid = $row["user_id"];
        $stmt = $conn->prepare("DELETE FROM sessions WHERE sessions_user_id = :sessions_user_id;");
        //$stmt->bindParam("s", $user_id);
        $stmt->execute(array(":sessions_user_id"=>$user_id));

        $token = func::createString(32);
        $serial = func::createString(32);


        func::createCookie($user_username, $user_id, $token, $serial);
        func::createSession($user_username, $user_id, $token, $serial);

        $stmt = $conn->prepare('INSERT INTO `sessions` (`sessions_id`,`sessions_user_id`,`sessions_token`, `sessions_serial`,`sessions_date`) VALUES (NULL,:user_id,:token,:serial, CURRENT_TIMESTAMP)');
        $stmt->execute(array(":user_id"=> $user_id, ":token"=> $token,":serial"=> $serial));
    }

    public static function createCookie($user_username, $user_id, $token, $serial)
    {
        setcookie('user_id', $user_id, time() + (86400) * 30, "/");
        setcookie('user_username', $user_username, time() + (86400) * 30, "/");
        setcookie('token', $token, time() + (86400) * 30, "/");
        setcookie('serial', $serial, time() + (86400) * 30, "/");
    }

    public static function createSession($user_username, $user_id, $token, $serial)
    {
        if (!isset($_SESSION["id"]) || !isset($_COOKIE["PHPSESSID"]))
        {
            session_start();
        }
        $_SESSION['user_username' ]= $user_username;
        setcookie('user_id', $user_id, time() + (86400) * 30, "/");
        setcookie('token', $token, time() + (86400) * 30, "/");
        setcookie('serial', $serial, time() + (86400) * 30, "/");
    }
    
    
}

