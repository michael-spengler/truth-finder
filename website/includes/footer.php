<?php 
include_once(".\includes\Header.php");
include_once(".\includes\Functions.php");
?>
<footer>

<?php
echo"
<a href = 'index.php'>Frontpage</a> | ";
if (func::CheckLoginState($conn)) {
        echo"<a href = 'logout.php'>Logout</a>";
    }
    else{
        echo"<a href = 'login.php'>Login</a>";
    }

?>

</footer>

</body>
</html>
