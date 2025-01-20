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

// Проверка подключения
if ($conn->connect_error) {
    $response = array("success" => false, "message" => "Ошибка подключения к базе данных: " . $conn->connect_error);
    echo json_encode($response);
    die();
}

// Получение данных из метода POST
$user = $_POST['username'];
$pass = $_POST['password'];
$admin1 = 0;

// Подготовка SQL-запроса
$sql = "INSERT INTO users (userName, userPass, admin) VALUES ('$user', '$pass', '$admin1')";

// Выполнение запроса
if ($conn->query($sql) === TRUE) {
    $response = array("success" => true, "message" => "Данные успешно добавлены в базу данных");
    echo json_encode($response);
} else {
    $response = array("success" => false, "message" => "Ошибка при выполнении запроса: " . $conn->error);
    echo json_encode($response);
}

// Закрытие соединения с базой данных
$conn->close();
?>
