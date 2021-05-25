<!doctype html>
<html>
  <head>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <link rel="stylesheet" href="styles.css">
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fake News Casino</title>
  </head>
  <body>
    <?php   
    include('.\includes\user.php');
    include('.\includes\dbh.php')
    
    //Erstelle User "Cadogan" mit Informationen und gebe diese auf Seite aus
    // $Cadogan = new user('Cadogan',"HalloDasIstMeiPW", "100", "100", "0", "05.12.1999");
    // echo $Cadogan->getUsername();
    // echo $Cadogan->getAmountVoted();

    
    
    
    ?>

  <!-- Beginn Webpage -->
  <?php
  $sql = "SELECT * FROM user;";
  $result = mysqli_query($conn, $sql);
  $resultCheck = mysqli_num_rows($result);

  if ($resultCheck > 0) {
    while ($row = mysqli_fetch_assoc($result)){
      echo $row['Username'];
      echo $row['UserID'];
    }
    

  } 
  ?>
    <div class="container">
        <div class="row">
          <div class="col-sm-4">
            <h3>Hier steht eine tolle Zeile</h3>
          </div>
          <div class="col-sm-4">
            <h1>Willkommen im Fake News Casino! Um anzufangen gib uns all dein Geld:3</h1>
            
          </div>
          <div class="col-sm-4">
            <h3>Oh Wow! Noch eine viel tollere Zeile!</h3>

            
          </div>
        </div>
      </div>
  </body>
</html>