## Установка

1. Клонируйте репозиторий:
   git clone https://github.com/NanReven/swoyo-internship

2. Создайте виртуальное окружение:
   python -m venv venv

3. Активируйте виртуальное окружение:
    .\venv\Scripts\activate

4. Установите зависимости:
   pip install -r requirements.txt

5. Создайте файл конфигурации 'config.toml' в папке 'configuration'. 
    [user_settings]
    username = "admin"
    password = "password"
    host = "127.0.0.1"

    [request_settings]
    port = 4010
    url = "/send_sms"
    host = "127.0.0.1"
    
## Запуск

python main.py --sender "79877464235" --recipient "79877245123" --message "hello world"

- `--sender`: номер отправителя
- `--recipient`: номер получателя
- `--message`: текст сообщения