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
   MAIL_USERNAME=your_gmail(change with actual gmail)
   MAIL_PASSWORD=your_app_password_from_gmail(change with actual app password)
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your password for root user(change with mysql root password)
   ```
6. Run the app:
   ```
   $ python app.py
   ```
7. To test register and login in command prompt using curl:
   ### Register
   ```
   $ curl -X POST http://localhost:5000/api/register -H "Content-Type: application/json" -d "{\"Name\":\"Hello\",\"Email Id\":\"hell@ball.com\",\"Password\":\"123123\"}"
   ```
   ### Login
   ```
   $ curl -X POST http://localhost:5000/api/login -H "Content-Type: application/json" -d "{\"Email Id\":\"hell@ball.com\",\"Password\":\"123123\"}"
   ```
