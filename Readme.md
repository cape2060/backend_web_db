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

3. create .env in /backend dir and there put:
   ```
   SECRET_KEY=HELLO_WORLD
   MAIL_USERNAME=your_gmail(change with actual gmail)
   MAIL_PASSWORD=your_app_password_from_gmail(change with actual app password)
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your password for root user(change with mysql root password)
   ```
4. Run the app:
   ```
   $ python app.py
   ```
   > Database `Bhasabridge` and all tables are created automatically on first run. Seed data is also inserted automatically.

---

## API Endpoints

Base URL: `http://localhost:5000/api`

🔒 = login required &nbsp;&nbsp; 🔑 = admin role required

---

### Auth

#### Register
```
POST /api/register
```
Body:
```json
{ "Name": "John", "Email Id": "john@mail.com", "Password": "secret123" }
```
curl:
```
$ curl -X POST http://localhost:5000/api/register -H "Content-Type: application/json" -d "{\"Name\":\"John\",\"Email Id\":\"john@mail.com\",\"Password\":\"secret123\"}"
```
Response: `201 { "Status": "Registered" }` | `409` already registered | `400` invalid input

---

#### Login
```
POST /api/login
```
Body:
```json
{ "Email Id": "john@mail.com", "Password": "secret123" }
```
curl:
```
$ curl -X POST http://localhost:5000/api/login -c cookies.txt -H "Content-Type: application/json" -d "{\"Email Id\":\"john@mail.com\",\"Password\":\"secret123\"}"
```
Response: `200 { "Status": "Login Sucess", "Username": "John" }` | `401` invalid credentials

> Save cookies with `-c cookies.txt` and reuse with `-b cookies.txt` for all 🔒 endpoints.

---

#### Request Password Reset
```
POST /api/request_reset
```
Body:
```json
{ "Email Id": "john@mail.com" }
```
curl:
```
$ curl -X POST http://localhost:5000/api/request_reset -H "Content-Type: application/json" -d "{\"Email Id\":\"john@mail.com\"}"
```
Response: `200 { "Status": "Reset password email sent" }` | `404` no user with this email

---

#### Reset Password
```
POST /api/reset_password
```
Body:
```json
{ "Token": "<jwt_from_email>", "New Password": "newpass123" }
```
curl:
```
$ curl -X POST http://localhost:5000/api/reset_password -H "Content-Type: application/json" -d "{\"Token\":\"<jwt>\",\"New Password\":\"newpass123\"}"
```
Response: `200 { "Status": "Password Reset Sucess" }` | `400` expired/invalid token

---

### Lessons

#### Get all lessons
```
GET /api/lessons?level=easy&item_type=word&limit=50&offset=0
```
curl:
```
$ curl "http://localhost:5000/api/lessons?level=easy"
```
Response: `200` array of lesson objects

---

#### Get lesson by ID
```
GET /api/lessons/<id>
```
curl:
```
$ curl http://localhost:5000/api/lessons/1
```
Response: `200` lesson object | `404` not found

---

#### Add lesson 🔒 🔑
```
POST /api/admin/lessons
```
Body:
```json
{ "level": "easy", "item_type": "word", "english_text": "Hello", "newari_text": "jvajlapa", "romanized_text": "jvajalapa." }
```
curl:
```
$ curl -X POST http://localhost:5000/api/admin/lessons -b cookies.txt -H "Content-Type: application/json" -d "{\"level\":\"easy\",\"item_type\":\"word\",\"english_text\":\"Hello\",\"newari_text\":\"jvajlapa\"}"
```
Response: `201 { "Status": "Lesson added", "id": 5 }` | `403` not admin

---

#### Update lesson 🔒 🔑
```
PUT /api/admin/lessons/<id>
```
Same body as add. Response: `200 { "Status": "Lesson updated" }` | `404` not found

---

#### Delete lesson 🔒 🔑
```
DELETE /api/admin/lessons/<id>
```
curl:
```
$ curl -X DELETE http://localhost:5000/api/admin/lessons/1 -b cookies.txt
```
Response: `200 { "Status": "Lesson deleted" }` | `404` not found

---

### Quiz Questions

#### Get all quizzes
```
GET /api/quizzes?level=easy&lesson_id=1&limit=50&offset=0
```
curl:
```
$ curl "http://localhost:5000/api/quizzes?level=easy"
```
Response: `200` array of quiz objects (includes `correct_option`)

---

#### Get quiz by ID
```
GET /api/quizzes/<id>
```
curl:
```
$ curl http://localhost:5000/api/quizzes/1
```
Response: `200` quiz object | `404` not found

---

#### Get random questions (practice, no tracking)
```
GET /api/quiz/random?level=easy&count=5
```
curl:
```
$ curl "http://localhost:5000/api/quiz/random?level=easy&count=5"
```
Response:
```json
{ "level": "easy", "count": 5, "questions": [ { "id": 1, "question_text": "...", "option_a": "...", "option_b": "...", "option_c": "...", "option_d": "..." } ] }
```
> `correct_option` is NOT returned — safe for frontend quiz UI

---

#### Add quiz 🔒 🔑
```
POST /api/admin/quizzes
```
Body:
```json
{ "level": "easy", "lesson_id": 1, "question_text": "What is Hello?", "option_a": "A", "option_b": "B", "option_c": "C", "option_d": "D", "correct_option": "A", "explanation": "Hello is option A" }
```
curl:
```
$ curl -X POST http://localhost:5000/api/admin/quizzes -b cookies.txt -H "Content-Type: application/json" -d "{\"level\":\"easy\",\"question_text\":\"Q?\",\"option_a\":\"A\",\"option_b\":\"B\",\"option_c\":\"C\",\"option_d\":\"D\",\"correct_option\":\"A\"}"
```
Response: `201 { "Status": "Quiz added", "id": 7 }` | `403` not admin

---

#### Update quiz 🔒 🔑
```
PUT /api/admin/quizzes/<id>
```
Same body as add. Response: `200 { "Status": "Quiz updated" }` | `404` not found

---

#### Delete quiz 🔒 🔑
```
DELETE /api/admin/quizzes/<id>
```
curl:
```
$ curl -X DELETE http://localhost:5000/api/admin/quizzes/1 -b cookies.txt
```
Response: `200 { "Status": "Quiz deleted" }` | `404` not found

---

### Quiz Sessions (Tracked Play)

#### Start session 🔒
```
POST /api/quiz/session/start
```
Body:
```json
{ "level": "easy", "question_count": 5 }
```
curl:
```
$ curl -X POST http://localhost:5000/api/quiz/session/start -b cookies.txt -H "Content-Type: application/json" -d "{\"level\":\"easy\",\"question_count\":5}"
```
Response:
```json
{ "session_id": 12, "level": "easy", "total_questions": 5, "questions": [ { "id": 1, "question_text": "...", "option_a": "...", "option_b": "...", "option_c": "...", "option_d": "..." } ] }
```
> `correct_option` is NOT returned until submit

---

#### Submit answers 🔒
```
POST /api/quiz/session/<session_id>/submit
```
Body:
```json
{ "answers": [ { "quiz_id": 1, "selected_option": "A" }, { "quiz_id": 2, "selected_option": "C" } ] }
```
curl:
```
$ curl -X POST http://localhost:5000/api/quiz/session/12/submit -b cookies.txt -H "Content-Type: application/json" -d "{\"answers\":[{\"quiz_id\":1,\"selected_option\":\"A\"}]}"
```
Response:
```json
{ "session_id": 12, "level": "easy", "total_questions": 5, "correct_answers": 4, "score_percent": 80.0, "results": [ { "quiz_id": 1, "selected_option": "A", "correct_option": "A", "is_correct": true } ] }
```
`409` if session already completed or abandoned

---

#### Abandon session 🔒
```
POST /api/quiz/session/<session_id>/abandon
```
curl:
```
$ curl -X POST http://localhost:5000/api/quiz/session/12/abandon -b cookies.txt
```
Response: `200 { "Status": "Session abandoned" }`

---

### User Progress

#### Overall stats 🔒
```
GET /api/progress/me
```
curl:
```
$ curl http://localhost:5000/api/progress/me -b cookies.txt
```
Response:
```json
{ "name": "John", "email": "john@mail.com", "total_sessions": 10, "total_questions_attempted": 50, "total_correct": 40, "avg_score_percent": 80.0, "best_score_percent": 100.0, "last_played_at": "2026-02-25T10:00:00" }
```

---

#### Per-level breakdown 🔒
```
GET /api/progress/me/levels
```
curl:
```
$ curl http://localhost:5000/api/progress/me/levels -b cookies.txt
```
Response:
```json
[ { "level": "easy", "total_sessions": 5, "total_questions_answered": 25, "total_correct": 22, "overall_accuracy_percent": 88.0, "best_score_percent": 100.0, "last_played_at": "2026-02-25T10:00:00" } ]
```

---

#### Session history 🔒
```
GET /api/progress/me/history?level=easy&status=completed&limit=20&offset=0
```
curl:
```
$ curl "http://localhost:5000/api/progress/me/history?limit=10" -b cookies.txt
```
Response: paginated list of sessions, each with a per-question `attempts` array showing selected option, correct option, and whether it was correct.

---

### Admin Analytics

#### All users summary 🔒 🔑
```
GET /api/admin/analytics
```
curl:
```
$ curl http://localhost:5000/api/admin/analytics -b cookies.txt
```
Response: array of all users with total sessions, accuracy, best score — sorted by highest average score.

---

#### Leaderboard 🔒 🔑
```
GET /api/admin/analytics/leaderboard?level=easy
```
curl:
```
$ curl "http://localhost:5000/api/admin/analytics/leaderboard?level=easy" -b cookies.txt
```
Response:
```json
[ { "level": "easy", "user_id": 3, "name": "John", "best_score_percent": 100.0, "overall_accuracy_percent": 92.0, "rank_in_level": 1 } ]
```

---

#### User full detail 🔒 🔑
```
GET /api/admin/analytics/user/<user_id>
```
curl:
```
$ curl http://localhost:5000/api/admin/analytics/user/3 -b cookies.txt
```
Response: user overview + per-level progress + last 10 sessions.

---

#### Quiz difficulty stats 🔒 🔑
```
GET /api/admin/analytics/quiz-stats?level=easy
```
curl:
```
$ curl "http://localhost:5000/api/admin/analytics/quiz-stats" -b cookies.txt
```
Response: per-question attempt count and correct-rate (sorted hardest first):
```json
[ { "quiz_id": 1, "level": "easy", "question_text": "...", "total_attempts": 42, "correct_attempts": 38, "correct_rate_percent": 90.48 } ]
```

---

## Database Tables

| Table | What it stores |
|-------|---------------|
| `users` | Registered users (name, email, bcrypt password, role) |
| `lesson` | Vocabulary and sentences per level |
| `quiz` | Quiz questions linked to lessons |
| `quiz_sessions` | One row per play — level, score, status, timestamps |
| `quiz_attempts` | One row per answered question in a session |
| `user_level_progress` | Aggregated totals per user per level (best score, accuracy) |

