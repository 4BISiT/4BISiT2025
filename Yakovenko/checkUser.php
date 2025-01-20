<?php

// Добавляем заголовки для поддержки CORS
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST, GET, OPTIONS");
header("Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept");

// Данные для подключения к базе данных
$host = 'localhost';
$username = 'root';
$passwordd = '';
$database = 'usersDB';

// Подключение к базе данных
$conn = new mysqli($host, $username, $passwordd, $database);

// Проверка наличия ошибок при подключении
if ($conn->connect_error) {
    echo json_encode(array('result' => 'noConnection'));
    die();
}

// Получение данных из метода POST
$user = $_POST['username'];
$pass = $_POST['password'];

// SQL-запрос для проверки наличия пользователя в базе
$checkUserQuery = "SELECT * FROM users WHERE userName = '$user'";
$result = $conn->query($checkUserQuery);

if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();
    if($row['userPass'] == $pass) {
        echo json_encode(array('result' => $row));
    } else {
        echo json_encode(array('result' => 0));
    }
} else {
    
}

// Закрытие соединения с базой данных
$conn->close();
?>
