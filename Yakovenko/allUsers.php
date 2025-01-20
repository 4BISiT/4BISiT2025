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

$conn = new mysqli($host, $username, $passwordd, $database);

// Проверка подключения
if ($conn->connect_error) {
    $response = array("success" => false, "message" => "Ошибка подключения к базе данных: " . $conn->connect_error);
    echo json_encode($response);
    die();
}

// Получение данных из POST
$userTodo = $_POST['name'];
//$userTodo = "alex";

// Подготовка SQL-запроса
$sql = "SELECT userName FROM users WHERE admin = 0";

// Выполнение запроса
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // Преобразование результатов в массив объектов
    $rows = array();
    while ($row = $result->fetch_assoc()) {
        $rows[] = $row;
    }

    $response = array("success" => true, "data" => $rows);
    echo json_encode($response);
} else {
    $response = array("success" => false, "message" => "Записей не найдено");
    echo json_encode($response);
}

// Закрытие соединения с базой данных
$conn->close();
?>
