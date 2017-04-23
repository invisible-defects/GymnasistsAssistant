# Помощник Гимназиста
## Telegram чат-бот для учеников Государственной Столичной Гимназии
### Установка
1. Установите [Python 3.6](https://www.python.org/downloads/release/python-361/)  
2. Установите несколько модулей с помощью [pip](https://pip.pypa.io/en/stable/installing/)
```bash
pip install bs4
pip install pyTelegramBotAPI
pip install feedParser
pip install openpyxl
pip install pymySQL
```
3. Установите [MySQL Community Server](https://dev.mysql.com/downloads/mysql/) и после настройки сервера выполните команды ниже
```sql
CREATE USER 'bot'@'localhost' IDENTIFIED BY 'password';
CREATE DATABASE main;
USE main;
CREATE TABLE main(chatid INT unsigned NOT NULL, status TINYINT unsigned NULL, class varchar (255) DEFAULT 0)ENGINE=InnoDB;
CREATE TABLE lost(item varchar(255) NOT NULL)ENGINE=InnoDB;
CREATE TABLE events(name varchar(255) NOT NULL, date DATE NOT NULL, desc varchar(255) NOT NULL)ENGINE=InnoDB;
```
4. Настройте файл "config.py" изменяя переменные "token" (вставьте HTTP токен своего бота) и "teacher_pass" (выставьте пароль ждя входа в режим учителя
5. Запустите "source.py"!
