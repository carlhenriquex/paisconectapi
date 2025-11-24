-- --------------------------------------------------------
-- Servidor:                     localhost
-- Versão do servidor:           10.1.13-MariaDB - mariadb.org binary distribution
-- OS do Servidor:               Win32
-- HeidiSQL Versão:              11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Copiando estrutura do banco de dados para escola_db
CREATE DATABASE IF NOT EXISTS `escola_db` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `escola_db`;

-- Copiando estrutura para tabela escola_db.alunos
CREATE TABLE IF NOT EXISTS `alunos` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `matricula` int(20) NOT NULL DEFAULT '0',
  `nome` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ano_entrada` int(11) NOT NULL,
  `telefone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `responsavel` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contato_responsavel` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `turma_id` int(11) NOT NULL,
  `status` enum('cursando','transferido','concluinte') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `senha` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `senha_provisoria` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `matricula` (`matricula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Copiando dados para a tabela escola_db.alunos: ~1 rows (aproximadamente)
DELETE FROM `alunos`;
/*!40000 ALTER TABLE `alunos` DISABLE KEYS */;
INSERT INTO `alunos` (`id`, `matricula`, `nome`, `ano_entrada`, `telefone`, `responsavel`, `contato_responsavel`, `email`, `turma_id`, `status`, `senha`, `senha_provisoria`) VALUES
	(1, 2970637, 'David Remigio', 2024, '8199412345', 'Guilherme', '81911122233', 'david.remigio@etegec.net.br', 1, 'cursando', '$2y$10$oVz9vKtYBbiEQzB6cnjUP.WfsAWs33cRqpMpG.34MorCtFWSOpT2e', 0);
/*!40000 ALTER TABLE `alunos` ENABLE KEYS */;

-- Copiando estrutura para tabela escola_db.turmas
CREATE TABLE IF NOT EXISTS `turmas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ano_entrada` int(11) NOT NULL,
  `identificacao` varchar(50) NOT NULL,
  `descricao` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Copiando dados para a tabela escola_db.turmas: ~1 rows (aproximadamente)
DELETE FROM `turmas`;
/*!40000 ALTER TABLE `turmas` DISABLE KEYS */;
INSERT INTO `turmas` (`id`, `ano_entrada`, `identificacao`, `descricao`) VALUES
	(1, 2024, 'Turma-Teste', 'Turma de teste do sistema');
/*!40000 ALTER TABLE `turmas` ENABLE KEYS */;

-- Copiando estrutura para tabela escola_db.comunicados
CREATE TABLE IF NOT EXISTS `comunicados` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `titulo` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `conteudo` text COLLATE utf8mb4_unicode_ci,
  `imagem_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `data_publicacao` datetime DEFAULT CURRENT_TIMESTAMP,
  `publicado_por` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Copiando dados para a tabela escola_db.comunicados: ~0 rows (aproximadamente)
DELETE FROM `comunicados`;
/*!40000 ALTER TABLE `comunicados` DISABLE KEYS */;
/*!40000 ALTER TABLE `comunicados` ENABLE KEYS */;

-- Copiando estrutura para tabela escola_db.entradas
CREATE TABLE IF NOT EXISTS `entradas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `matricula_alunos` int(11) NOT NULL,
  `aluno_id` int(11) unsigned DEFAULT NULL,
  `turma_id` int(11) DEFAULT NULL,
  `data` date NOT NULL,
  `hora` time NOT NULL,
  `status` enum('presente','atraso','ausente') NOT NULL,
  PRIMARY KEY (`id`),
  KEY `turma_id` (`turma_id`),
  KEY `matricula_alunos` (`matricula_alunos`),
  KEY `entradas_ibfk_1` (`aluno_id`),
  CONSTRAINT `entradas_ibfk_1` FOREIGN KEY (`aluno_id`) REFERENCES `alunos` (`id`),
  CONSTRAINT `entradas_ibfk_2` FOREIGN KEY (`turma_id`) REFERENCES `turmas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Copiando dados para a tabela escola_db.entradas: ~2 rows (aproximadamente)
DELETE FROM `entradas`;
/*!40000 ALTER TABLE `entradas` DISABLE KEYS */;
INSERT INTO `entradas` (`id`, `matricula_alunos`, `aluno_id`, `turma_id`, `data`, `hora`, `status`) VALUES
	(1, 2970637, 1, 1, '2025-10-14', '07:12:57', 'presente'),
	(2, 2970637, 1, 1, '2025-10-13', '08:14:11', 'atraso');
/*!40000 ALTER TABLE `entradas` ENABLE KEYS */;

-- Copiando estrutura para tabela escola_db.recuperacao_senhas
CREATE TABLE IF NOT EXISTS `recuperacao_senhas` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `token` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Copiando dados para a tabela escola_db.recuperacao_senhas: ~0 rows (aproximadamente)
DELETE FROM `recuperacao_senhas`;
/*!40000 ALTER TABLE `recuperacao_senhas` DISABLE KEYS */;
/*!40000 ALTER TABLE `recuperacao_senhas` ENABLE KEYS */;

-- Copiando estrutura para tabela escola_db.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome_usuario` varchar(50) NOT NULL,
  `senha` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `nivel_acesso` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nome_usuario` (`nome_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Copiando dados para a tabela escola_db.usuarios: ~2 rows (aproximadamente)
DELETE FROM `usuarios`;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` (`id`, `nome_usuario`, `senha`, `email`, `nivel_acesso`) VALUES
	(1, 'admin', '$2y$10$/foIap/3ChNGnrv7YJU5bu79BwyspTeg0UC4HMbQHk1CflK2Thpwm', 'admin@paisconect.com.br', 'admin'),
	(3, 'remigio', '$2y$10$tIRzZAeFayrLfdiPmB8Laeq47ei9ShcvGmE7w3iY/EkUwEminzgvi', 'david.remigio@etegec.net.br', 'admin');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
