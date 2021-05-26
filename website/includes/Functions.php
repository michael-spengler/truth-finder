<?php
include_once(".\includes\dbh.php");
class func
{
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
}

