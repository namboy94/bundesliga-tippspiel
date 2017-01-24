<?php
/*  Copyright Hermann Krumrey <hermann@krumreyh.com> 2017

    This file is part of bundesliga-tippspiel.

    bundesliga-tippspiel is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    bundesliga-tippspiel is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with bundesliga-tippspiel.  If not, see <http://www.gnu.org/licenses/>.
*/


class Database {

    /**
     * @var string: The Username to be used when authenticating with the database
     */
    private $user;

    /**
     * @var string: The Password to be used when authenticating with the database
     */
    private $pass;

    /**
     * Database constructor.
     * Automatically reads the username and password from secret files
     */
    public function __construct() {
        $this->user = trim(file_get_contents(dirname(__FILE__) . "/../../secrets/db_user"));
        $this->pass = trim(file_get_contents(dirname(__FILE__) . "/../../secrets/db_pass"));
    }

    /**
     * Opens the Database Connection
     * @return mysqli: The Database Connection
     */
    private function openDatabase() {
        return new mysqli("localhost", $this->user, $this->pass, "bundesliga_tippspiel");
    }

    /**
     * Turns an array into a reference array for use with call_user_func_array
     * @param $array array: The source array
     * @return       array: The reference array
     */
    private function makeReference($array) {
        $reference = array();
        foreach($array as $key => $value) {
            $reference[$key] = &$array[$key];
        }
        return $reference;
    }

    /**
     * Runs an SQL query
     * @param $sql                 string:               The parameterized SQL query
     * @param $types               string:               The types of the variables
     * @param $variables           array:                The variables to be put into the SQL statement
     * @param $asArray             boolean:              Can be set to return the query result as an array
     * @return                     mysqli_result|array : The Query Result (or false if the SQL statement failed)
     */
    public function query($sql, $types, $variables, $asArray=false) {

        $db = $this->openDatabase();
        $stmt = $db->prepare($sql);

        if ($types === '') {
            $result = $db->query($sql);
        }
        else {
            $params = $this->makeReference(array_merge(array($types), $variables));
            call_user_func_array(array($stmt, 'bind_param'), $params);
            $stmt->execute();
            $result = $stmt->get_result();
        }
        $db->close();

        if ($asArray) {
            $result_array = array();
            while($item = $result->fetch_assoc()) {
                array_push($result_array, $item);
            }
            return $result_array;
        }
        else {
            return $result;
        }
    }

    /**
     * Executes an SQL command
     * @param $sql       string: The SQL Statement
     * @param $types     string: The Types of the Variables
     * @param $variables array:  The Variables
     */
    public function queryWrite($sql, $types, $variables) {

        $db = $this->openDatabase();
        $stmt = $db->prepare($sql);

        if ($types === '') {
            $db->query($sql);
        }
        else {
            $params = $this->makeReference(array_merge(array($types), $variables));
            call_user_func_array(array($stmt, 'bind_param'), $params);
            $stmt->execute();
        }

        $db->commit();
        $db->close();
    }
}