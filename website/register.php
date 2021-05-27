<?php
include_once(".\includes\header.php");
include_once(".\includes\dbh.php");
include_once(".\includes\Functions.php");
include_once(".\includes\Footer.php");

?>

<section class="parent">

    <div class="child">

    <?php

        $form = "
        <form action='register.php' method='post'>
        <label>Username</label>><br />
        <input type='text' name = 'username' /><br />
        <label>Password</label>><br />
        <input type='password' name = 'passkey' /><br />
        <label>Password repeat</label>><br />
        <input type='password' name = 'passkeyrep' /><br />
        <label>E-Mail</label>><br />
        <input type='email' name = 'email' /><br />
        <label>Birth Date</label><br />
        <input type='date' name='birthday'>
        <input type='submit' value='Register'/>
        </form>
        ";
        //Loginb Status checken
        if (!func::CheckLoginState($conn) )
        {
            
        //überprüfen ob eingabe vorliegt
            if(isset($_POST["username"]) && isset($_POST["passkey"]) && isset($_POST["passkeyrep"]) && isset($_POST["email"]) && isset($_POST["birthday"]))
            {

                $new_user_name = $_POST["username"];
                $new_user_password = $_POST["passkey"];
                $new_user_password_rep = $_POST["passkeyrep"];
                $new_user_email = $_POST["email"];
                $new_user_birthday = $_POST["birthday"];
            
            //überprüfen ob passwörter übereinstimmen
                if($new_user_password != $new_user_password_rep){
                    echo "Passwörter stimmen nicht überein.";
                    echo $form;
                    }
            //check empty username
                elseif(empty($new_user_name)){
                    echo "Bitte Username eingeben";
                    echo $form;
                    }
            
            //check empty passwords
                elseif(empty($new_user_password)||empty($new_user_password_rep)){
                        echo "Bitte Password eingeben";
                        echo $form;
                    }

            //check empty email
                elseif(empty($new_user_email)){
                        echo "Bitte Email eingeben";
                        echo $form;
                    }
            //check empty birthday
                elseif(empty($new_user_birthday)){
                    echo "Bitte Geburtsdatum eingeben";
                    echo $form;
                    }
                
                //check ob alles gefüllt ist
                elseif(!empty($new_user_email) && !empty($new_user_password) && !empty($new_user_password_rep) && !empty($new_user_name)&& !empty($new_user_birthday)){

                //get usernames from db
                    $stmt = $conn->prepare("SELECT * FROM user WHERE user_username = :username");
                    $stmt->execute(array(':username'=> $_POST["username"]));
                    //$stmt->execute();
                    $row = $stmt->fetch(PDO::FETCH_ASSOC);
                
                //check if username already in db
                    if (!empty($row["user_username"]))
                    {
                        echo "Username already taken. Please enter different Name";
                        echo $form;
                        
                    }
                //get email from db
                    $stmt = $conn->prepare("SELECT * FROM user WHERE user_email = :email");
                    $stmt->execute(array(':email'=> $_POST["email"]));
                    //$stmt->execute();
                    $row = $stmt->fetch(PDO::FETCH_ASSOC);
                       
                //check if email already in use
                    if (!empty($row["user_email"]))
                        {
                                echo "Email already taken. Please enter different Email";
                                echo $form;
                                
                        }
                    
                    else{
                        // Validate password strength
                        $uppercase = preg_match('@[A-Z]@', $new_user_password);
                        $lowercase = preg_match('@[a-z]@', $new_user_password);
                        $number    = preg_match('@[0-9]@', $new_user_password);
                        $specialChars = preg_match('@[^\w]@', $new_user_password);

                        if(!$uppercase || !$lowercase || !$number || !$specialChars || strlen($new_user_password) < 8) {
                            echo 'Password should be at least 8 characters in length and should include at least one upper case letter, one number, and one special character.';
                            echo $form;
                        }
                        else{
                            $new_user_password_hash = password_hash($new_user_password, PASSWORD_DEFAULT);
                            $stmt = $conn->prepare("INSERT INTO `user`(`user_username`, `user_password`,`date_birth`, `user_id`, `user_email`) VALUES (:username,:userpassword,:birthday,:id,:email)");
                            $stmt->execute(array(':username'=> $new_user_name, ':userpassword'=>$new_user_password_hash,':birthday'=>$new_user_birthday, 'id'=>'',':email'=>$new_user_email));
                            echo "Registrierung geglückt";                        
                        }
                        
                    }
                }
            }
            //default state
            else{
                echo "Bitte Daten eingeben";
                echo $form;
                
            }
        }
    ?>

    </div>

</section>