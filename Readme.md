## To run 
1. clone this repo
   ```
   $ git clone https://github.com/cape2060/backend_web_db.git
   ```
2. requirement :
   ```
    $ pip install flask flask_cors bcrypt flask_mail PyJWT python-dotenv pymysql
   ```
   or
   ```
   $ pip install -r requirements.txt
   ```

4. create .env in /backend dir and there put:
   ```
   SECRET_KEY=HELLO_WORLD
   MAIL_USERNAME=your_gmail
   MAIL_PASSWORD=your_app_password_from_gmail
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your password for root user
   ```
6. python app.py
