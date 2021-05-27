<?php 
include_once(".\includes\header.php");
include_once(".\includes\dbh.php");
include_once(".\includes\Functions.php");
include_once(".\includes\Footer.php");

?>

<section class="parent">

    <div class="child">

    <?php

        if (!func::CheckLoginState($conn) )
        {
        
            if(isset($_POST["username"]) && isset($_POST["passkey"]))
            {

                $user_name = $_POST["username"];
                $user_password = $_POST["passkey"];

                $stmt = $conn->prepare("SELECT * FROM user WHERE user_username = :username AND user_password = :passkey"); 
                //$stmt->execute(array(':username'=> $_POST["username"], ':passkey'=> $_POST["passkey"]));
                $stmt->bindParam(":username", $user_name);
                $stmt->bindParam(":passkey", $user_password);
                $stmt->execute();
                
                $row = $stmt->fetch(PDO::FETCH_ASSOC);
                
                if (!empty($row["user_id"]))
                {
                    func::createRecord($conn, $row["user_username"],$row["user_id"]);
                    //header("location:index.php");
                    //echo func::createString(32);
                    echo "Authentifizierung geglückt";
                   
                }
                else{
                    echo "Leider Falsch, bitt erneut eingeben";
                    echo "
                    <form action='login.php' method='post'>
                    <label>Username</label>><br />
                    <input type='text' name = 'username' /><br />
                    <label>Password</label>><br />
                    <input type='password' name = 'passkey' /><br />
                    <input type='submit' value='login'/>
                    </form>
                    ";
                }
            }
            else{
                echo "Bitte Daten eingeben";
                echo "
                <form action='login.php' method='post'>
                <label>Username</label>><br />
                <input type='text' name = 'username' /><br />
                <label>Password</label>><br />
                <input type='password' name = 'passkey' /><br />
                <input type='submit' value='login'/>
                </form>
                ";
            }
            
        
        }
        else
        {
            header("location:index.php");
        }

    ?>

    </div>

</section>