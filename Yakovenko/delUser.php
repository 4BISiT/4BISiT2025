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

// Получение данных из POST
$username = $_POST['username'];

// Подготовка SQL-запроса для удаления записи
$sql = "DELETE FROM users WHERE userName = '$username'";

// Выполнение запроса
if ($conn->query($sql) === TRUE) {
    $response = array("success" => true, "message" => "Запись успешно удалена");
} else {
    $response = array("success" => false, "message" => "Ошибка при удалении записи: " . $conn->error);
}

// Закрытие соединения с базой данных
$conn->close();

// Возврат ответа в формате JSON
echo json_encode($response);
?>
