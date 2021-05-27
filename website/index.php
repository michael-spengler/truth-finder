<!doctype html>
<html>
  <head>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <link rel="stylesheet" href="styles.css">
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <?php
    include_once(".\includes\header.php");
    include_once(".\includes\Functions.php");
    ?>
    <title>Fake News Casino</title>
  </head>
  <body>
    <?php   
    include('.\includes\dbh.php')
    
    //Erstelle User "Cadogan" mit Informationen und gebe diese auf Seite aus
    // $Cadogan = new user('Cadogan',"HalloDasIstMeiPW", "100", "100", "0", "05.12.1999");
    // echo $Cadogan->getUsername();
    // echo $Cadogan->getAmountVoted();

    
    
    
    ?>

  <!-- Beginn Webpage -->
    <div class="container">
        <div class="row">
          <div class="col-sm-4">
            <h3>Hier steht eine tolle Zeile</h3>
          </div>
          <div class="col-sm-4">
            <?php

            if (!func::CheckLoginState($conn))
            {
              echo "Bitte anmelden! <a href = 'login.php'>Login</a>";
                        }
            else{
              echo "Welcome " . $_SESSION['user_username'] . ' !';
            }

            ?>
             
            
          
            
          </div>
          <div class="col-sm-4">
            <h3>Oh Wow! Noch eine viel tollere Zeile!</h3>

            
          </div>
        </div>
      </div>
  </body>
  <?php
    include_once(".\includes\Footer.php");
    ?>
</html>