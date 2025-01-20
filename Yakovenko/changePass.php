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

$updateSql = "UPDATE users SET userPass = '$pass' WHERE userName = '$user'";
$updateResult = $conn->query($updateSql);

$response = array("success" => true, "message" => "Пароль изменен");
echo json_encode($response);
// Закрытие соединения с базой данных
$conn->close();
?>
