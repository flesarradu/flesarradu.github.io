<?php
session_start();
header("Content-Type: application/json; charset=utf-8");

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    http_response_code(405);
    echo json_encode(["ok" => false]);
    exit;
}

if (!empty($_POST["company"])) {
    echo json_encode(["ok" => true]);
    exit;
}

$given = strtoupper(preg_replace("/\s+/", "", (string) ($_POST["captcha"] ?? "")));
$expected = (string) ($_SESSION["captcha"] ?? "");
$fresh = (time() - (int) ($_SESSION["captcha_at"] ?? 0)) < 600;
unset($_SESSION["captcha"], $_SESSION["captcha_at"]);
if ($expected === "" || !$fresh || strlen($given) !== strlen($expected) || !hash_equals($expected, $given)) {
    http_response_code(422);
    echo json_encode(["ok" => false, "error" => "captcha"]);
    exit;
}

$fields = [
    "nume" => "Nume",
    "prenume" => "Prenume",
    "email" => "Email",
    "telefon" => "Telefon",
    "societate" => "Societate",
    "serviciu" => "Serviciu",
    "incarcare" => "Locația încărcării",
    "descarcare" => "Locația descărcării",
    "model" => "Model autoturism",
    "stare" => "Stare autoturism",
    "numar_auto" => "Număr autoturisme",
    "paleti" => "Număr paleți",
    "volum" => "Volum paleți",
    "greutate" => "Greutate paleți",
    "mesaj" => "Mesaj",
];

$lines = [];
foreach ($fields as $key => $label) {
    $value = trim((string) ($_POST[$key] ?? ""));
    if ($value !== "") {
        $lines[] = $label . ": " . str_replace(["\r", "\n"], " ", $value);
    }
}

if (count($lines) < 2) {
    http_response_code(422);
    echo json_encode(["ok" => false]);
    exit;
}

$to = "office@gistransporturi.ro";
$subject = "Cerere de pe gistransporturi.ro";
$body = implode("\n", $lines);
$headers = "From: GIS Transporturi <office@gistransporturi.ro>\r\nContent-Type: text/plain; charset=UTF-8";

$sent = mail($to, $subject, $body, $headers);
http_response_code($sent ? 200 : 500);
echo json_encode(["ok" => $sent]);
