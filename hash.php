<?php
// Senha que será hashada
$senha = "senha123";

// Gerar o hash da senha
$hash = password_hash($senha, PASSWORD_DEFAULT);

// Exibir o hash gerado
echo "Hash gerado: " . $hash;
?>