CREATE DATABASE IF NOT EXISTS pishield;

USE pishield;

CREATE TABLE IF NOT EXISTS interfaces (
	endereco CHAR(17) PRIMARY KEY,
	endereco_ipv4_rede VARCHAR(15) NOT NULL,
	prefixo TINYINT NOT NULL,
	nome VARCHAR(64) NOT NULL,
	padrao BOOLEAN NOT NULL,
	ativa BOOLEAN NOT NULL,
	ultima_vez_vista DATETIME
);

CREATE TABLE IF NOT EXISTS dispositivos (
	endereco CHAR(17) PRIMARY KEY,
	endereco_interface CHAR(17) NOT NULL,
	sistema VARCHAR(255),
	ativo BOOLEAN,
	ultima_vez_visto DATETIME,
	FOREIGN KEY (endereco_interface) REFERENCES interfaces (endereco) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS servicos (
	cpe VARCHAR(255) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS vulnerabilidades (
	cve VARCHAR(20) PRIMARY KEY,
	descricao TEXT
);

CREATE TABLE IF NOT EXISTS servicos_vulnerabilidades (
	cpe VARCHAR(255),
	cve VARCHAR(20),
	FOREIGN KEY (cpe) REFERENCES servicos (cpe) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (cve) REFERENCES vulnerabilidades (cve) ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY (cpe, cve)
);

CREATE TABLE IF NOT EXISTS dispositivos_servicos (
	endereco_dispositivo CHAR(17),
	cpe VARCHAR(255),
	ativo BOOLEAN,
	ultima_vez_visto DATETIME,
	FOREIGN KEY (endereco_dispositivo) REFERENCES dispositivos (endereco) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (cpe) REFERENCES servicos (cpe) ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY (endereco_dispositivo, cpe)
);

CREATE TABLE IF NOT EXISTS dispositivos_vulnerabilidades (
	endereco_dispositivo CHAR(17),
	cpe VARCHAR(255),
	cve VARCHAR(20),
	resolucao BOOLEAN,
	FOREIGN KEY (endereco_dispositivo, cpe) REFERENCES dispositivos_servicos (endereco_dispositivo, cpe) ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY (endereco_dispositivo, cpe, cve)
);

CREATE TABLE IF NOT EXISTS escaneamentos (
	data_hora DATETIME PRIMARY KEY,
	data_hora_fim DATETIME,
	endereco_interface CHAR(17) NOT NULL,
	FOREIGN KEY (endereco_interface) REFERENCES interfaces (endereco) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS escaneamentos_dispositivos (
	data_hora DATETIME,
	endereco CHAR(17),
	sistema VARCHAR(255),
	FOREIGN KEY (data_hora) REFERENCES escaneamentos (data_hora) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (endereco) REFERENCES dispositivos (endereco) ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY (data_hora, endereco)
);

CREATE TABLE IF NOT EXISTS escaneamentos_servicos (
	data_hora DATETIME,
	endereco_dispositivo CHAR(17),
	cpe VARCHAR(255),
	FOREIGN KEY (data_hora, endereco_dispositivo) REFERENCES escaneamentos_dispositivos (data_hora, endereco) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (cpe) REFERENCES servicos (cpe) ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY (data_hora, endereco_dispositivo, cpe)
);

CREATE TABLE ativacoes_dispositivos (
	data_hora DATETIME,
	endereco_dispositivo CHAR(17),
	ativo BOOLEAN NOT NULL,
	FOREIGN KEY (endereco_dispositivo) REFERENCES dispositivos (endereco) ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY (data_hora, endereco_dispositivo)
);

CREATE TABLE ativacoes_servicos (
	data_hora DATETIME,
	endereco_dispositivo CHAR(17),
	cpe VARCHAR(255),
	ativo BOOLEAN NOT NULL,
	FOREIGN KEY (endereco_dispositivo, cpe) REFERENCES dispositivos_servicos (endereco_dispositivo, cpe) ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY (data_hora, endereco_dispositivo, cpe)
);

CREATE TABLE resolucoes_vulnerabilidades (
	data_hora DATETIME,
	endereco_dispositivo CHAR(17),
	cpe VARCHAR(255),
	cve VARCHAR(20),
	resolucao BOOLEAN NOT NULL,
	FOREIGN KEY (endereco_dispositivo, cpe, cve) REFERENCES dispositivos_vulnerabilidades (endereco_dispositivo, cpe, cve) ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY (data_hora, endereco_dispositivo, cpe, cve)
);