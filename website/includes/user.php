<?php
//User class definition
class user  {
    private $username;
    private $password;
    private $amountVoted;
    private $correctVotes;
    private $falseVotes;
    private $dateOfBirth;

    //Class Costructor
    public function __construct($username, $password, $amountVoted, $correctVotes, $falseVotes, $dateOfBirth){
        $this->username = $username;
        $this->password = $password;
        $this->amountVoted = $amountVoted;
        $this->correctVotes = $correctVotes;
        $this->falseVotes = $falseVotes;
        $this->dateOfBirth= $dateOfBirth;
    }

    //Eingabe als Username festlegen
    public function setUserName($username){
        $this->username = $username;
    }

    public function getUsername(){
        return $this->username;
    }

    public function getPassword(){
        return $this->password;
    }

    public function getAmountVoted(){
        return $this->amountVoted;
    }

    public function getCorrectVotes(){
        return $this->correctVotes;
    }

    public function getFalseVotes(){
        return $this->falseVotes;
    }
    
    public function getDateOfBirth(){
        return $this->dateOfBirth;
    }

    
}?>
