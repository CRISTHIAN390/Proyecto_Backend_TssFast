-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS `bd_Maxfer_app`;
USE `bd_Maxfer_app`;

-- Crear tabla de roles
CREATE TABLE IF NOT EXISTS `roles` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(191) NOT NULL UNIQUE,
    `state` INT
);

-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `first_name` VARCHAR(191),
    `last_name` VARCHAR(191),
    `DNI` VARCHAR(8),
    `age` INT,
    `sex` CHAR(1),
    `phone` VARCHAR(12) NOT NULL,
    `username` VARCHAR(191) NOT NULL UNIQUE,
    `email` VARCHAR(191) NOT NULL UNIQUE,
    `password` VARCHAR(191) NOT NULL,
    `role_id` INT,
    `date_created` DATETIME,
    `state` INT,
    FOREIGN KEY (`role_id`) REFERENCES `roles`(`id`)
);

-- Insertar roles predeterminados
INSERT IGNORE INTO `roles` (`name`, `state`) VALUES
('admin', 1),
('vigilante', 1),
('transportista', 1);

-- Insertar usuario administrador por defecto
INSERT IGNORE INTO `users` (`first_name`, `last_name`, `DNI`, `age`, `sex`, `phone`, `state`, `username`, `email`, `password`, `role_id`, `date_created`) VALUES
('criss', 'vidal', '76362554', 25, 'M', '917700319', 1, 'admin', 'admin@gmail.com', 'hashed_password_here', (SELECT `id` FROM `roles` WHERE `name` = 'admin'), NOW());