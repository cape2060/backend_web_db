# BhasaBridge Backend API

Flask + MySQL backend for the BhasaBridge Newari language learning platform.

---

## Setup & Run

1. **Clone the repo**
   ```bash
   git clone https://github.com/cape2060/backend_web_db.git
   cd backend_web_db/backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   or manually:
   ```bash
   pip install flask flask_cors bcrypt flask_mail PyJWT python-dotenv pymysql
   ```

3. **Create `.env`** in the `/backend` directory:
   ```env
   SECRET_KEY=HELLO_WORLD
   MAIL_USERNAME=your_gmail@gmail.com
   MAIL_PASSWORD=your_gmail_app_password
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_mysql_root_password
   ```

4. **Run the server**
   ```bash
   python app.py
   ```
   Server starts at `http://127.0.0.1:5000`

> The database `Bhasabridge` and all tables are created automatically on first run.  
> Seed lesson and quiz data is also inserted automatically.

---

## Authentication

Sessions are cookie-based. Login sets a server-side session.  
Endpoints marked **🔒 Login required** return `401` if not logged in.  
Endpoints marked **🔑 Admin only** return `403` if the user role is not `admin`.

---

## API Reference

### Base URL: `/api`

---

## 1. Auth Routes

### `POST /api/register`
Register a new user account.

**Request body:**
```json
{
  "Name": "John Doe",
  "Email Id": "john@example.com",
  "Password": "secret123"
}
```
| Code | Response |
|------|---------|
| 201 | `{ "Status": "Registered" }` |
| 400 | Invalid name or email syntax |
| 409 | User already registered |

---

### `POST /api/login`
Log in and start a session.

**Request body:**
```json
{
  "Email Id": "john@example.com",
  "Password": "secret123"
}
```
| Code | Response |
|------|---------|
| 200 | `{ "Status": "Login Sucess", "Username": "John" }` |
| 400 | Invalid email syntax |
| 401 | Invalid credentials |

---

### `POST /api/request_reset`
Send a password-reset token to the user's email.

**Request body:**
```json
{ "Email Id": "john@example.com" }
```
| Code | Response |
|------|---------|
| 200 | `{ "Status": "Reset password email sent" }` |
| 400 | Invalid email syntax |
| 404 | No user with this email |

---

### `POST /api/reset_password`
Reset password using the JWT token received in the email.

**Request body:**
```json
{
  "Token": "<jwt_token_from_email>",
  "New Password": "newpassword123"
}
```
| Code | Response |
|------|---------|
| 200 | `{ "Status": "Password Reset Sucess" }` |
| 400 | Token expired / invalid, or password shorter than 6 characters |

---

## 2. Lesson Routes

### `GET /api/lessons`
Get all lessons. Supports filtering and pagination.

**Query params:**
| Param | Type | Description |
|-------|------|-------------|
| `level` | string | `easy`, `intermediate`, or `hard` |
| `item_type` | string | `word` or `sentence` |
| `limit` | int | Max results to return (default `50`) |
| `offset` | int | Pagination offset (default `0`) |

**Response `200`:** Array of lesson objects:
```json
[
  {
    "id": 1,
    "level": "easy",
    "item_type": "word",
    "english_text": "Hello",
    "newari_text": "ज्वजलपा।",
    "romanized_text": "jvajalapa.",
    "source_url": "https://...",
    "created_at": "...",
    "updated_at": "..."
  }
]
```

---

### `GET /api/lessons/<lesson_id>`
Get a single lesson by its ID.

| Code | Response |
|------|---------|
| 200 | Lesson object |
| 404 | `{ "Status": "Lesson not found" }` |

---

### `POST /api/admin/lessons` 🔒 🔑
Add a new lesson.

**Request body:**
```json
{
  "level": "easy",
  "item_type": "word",
  "english_text": "Hello",
  "newari_text": "ज्वजलपा।",
  "romanized_text": "jvajalapa.",
  "source_url": "https://..."
}
```
| Code | Response |
|------|---------|
| 201 | `{ "Status": "Lesson added", "id": 5 }` |
| 400 | Validation error message |
| 403 | Not an admin |

---

### `PUT /api/admin/lessons/<lesson_id>` 🔒 🔑
Update an existing lesson (same body fields as POST).

| Code | Response |
|------|---------|
| 200 | `{ "Status": "Lesson updated" }` |
| 404 | Lesson not found |

---

### `DELETE /api/admin/lessons/<lesson_id>` 🔒 🔑
Delete a lesson.

| Code | Response |
|------|---------|
| 200 | `{ "Status": "Lesson deleted" }` |
| 404 | Lesson not found |

---

## 3. Quiz Routes

### `GET /api/quizzes`
Get all quiz questions. Supports filtering and pagination. Returns `correct_option`.

**Query params:**
| Param | Type | Description |
|-------|------|-------------|
| `level` | string | `easy`, `intermediate`, or `hard` |
| `lesson_id` | int | Filter by linked lesson |
| `limit` | int | Default `50` |
| `offset` | int | Default `0` |

**Response `200`:** Array of quiz objects.

---

### `GET /api/quizzes/<quiz_id>`
Get a single quiz question by ID. Returns `correct_option`.

| Code | Response |
|------|---------|
| 200 | Quiz object |
| 404 | `{ "Status": "Quiz not found" }` |

---

### `GET /api/quiz/random`
Get random quiz questions for **practice mode** — `correct_option` is **NOT** returned.

**Query params:**
| Param | Type | Description |
|-------|------|-------------|
| `level` | string | **Required.** `easy`, `intermediate`, or `hard` |
| `count` | int | Number of questions, default `5`, max `20` |

**Response `200`:**
```json
{
  "level": "easy",
  "count": 5,
  "questions": [
    {
      "id": 1,
      "level": "easy",
      "question_text": "What is Hello in Newari?",
      "option_a": "ज्वजलपा।",
      "option_b": "सुभाय्।",
      "option_c": "बिन्ति।",
      "option_d": "ख।"
    }
  ]
}
```

---

### `POST /api/admin/quizzes` 🔒 🔑
Add a new quiz question.

**Request body:**
```json
{
  "level": "easy",
  "lesson_id": 1,
  "question_text": "What is Hello in Newari?",
  "option_a": "ज्वजलपा।",
  "option_b": "सुभाय्।",
  "option_c": "बिन्ति।",
  "option_d": "ख।",
  "correct_option": "A",
  "explanation": "Hello in Newari is ज्वजलपा।"
}
```
| Code | Response |
|------|---------|
| 201 | `{ "Status": "Quiz added", "id": 7 }` |
| 400 | Validation error |
| 403 | Not an admin |

---

### `PUT /api/admin/quizzes/<quiz_id>` 🔒 🔑
Update a quiz question (same body fields as POST).

| Code | Response |
|------|---------|
| 200 | `{ "Status": "Quiz updated" }` |
| 404 | Quiz not found |

---

### `DELETE /api/admin/quizzes/<quiz_id>` 🔒 🔑
Delete a quiz question.

| Code | Response |
|------|---------|
| 200 | `{ "Status": "Quiz deleted" }` |
| 404 | Quiz not found |

---

## 4. Quiz Session Routes (Tracked Play)

Use these endpoints to play a quiz with full progress tracking.

### `POST /api/quiz/session/start` 🔒
Start a new tracked quiz session. Returns questions **without** `correct_option`.

**Request body:**
```json
{
  "level": "easy",
  "question_count": 5
}
```
`question_count` can be 1–20 (default `5`).

**Response `201`:**
```json
{
  "session_id": 12,
  "level": "easy",
  "total_questions": 5,
  "questions": [
    {
      "id": 1,
      "question_text": "...",
      "option_a": "...",
      "option_b": "...",
      "option_c": "...",
      "option_d": "...",
      "explanation": "..."
    }
  ]
}
```

---

### `POST /api/quiz/session/<session_id>/submit` 🔒
Submit answers for a session. Scores automatically and saves progress.

**Request body:**
```json
{
  "answers": [
    { "quiz_id": 1, "selected_option": "A" },
    { "quiz_id": 2, "selected_option": "C" }
  ]
}
```

**Response `200`:**
```json
{
  "session_id": 12,
  "level": "easy",
  "total_questions": 5,
  "correct_answers": 4,
  "score_percent": 80.0,
  "results": [
    {
      "quiz_id": 1,
      "selected_option": "A",
      "correct_option": "A",
      "is_correct": true
    },
    {
      "quiz_id": 2,
      "selected_option": "C",
      "correct_option": "B",
      "is_correct": false
    }
  ]
}
```
| Code | Response |
|------|---------|
| 200 | Score + per-question results |
| 404 | Session not found |
| 409 | Session already completed or abandoned |

---

### `POST /api/quiz/session/<session_id>/abandon` 🔒
Mark a session as abandoned (user left mid-quiz without submitting).

| Code | Response |
|------|---------|
| 200 | `{ "Status": "Session abandoned" }` |
| 404 | Session not found or already finalised |

---

## 5. User Progress Routes

### `GET /api/progress/me` 🔒
Overall quiz statistics for the logged-in user.

**Response `200`:**
```json
{
  "name": "John",
  "email": "john@example.com",
  "total_sessions": 10,
  "total_questions_attempted": 50,
  "total_correct": 40,
  "avg_score_percent": 80.0,
  "best_score_percent": 100.0,
  "last_played_at": "2026-02-25T10:00:00"
}
```

---

### `GET /api/progress/me/levels` 🔒
Per-level breakdown for the logged-in user (easy / intermediate / hard).

**Response `200`:** Array, one entry per level played:
```json
[
  {
    "level": "easy",
    "total_sessions": 5,
    "total_questions_answered": 25,
    "total_correct": 22,
    "overall_accuracy_percent": 88.0,
    "best_score_percent": 100.0,
    "last_played_at": "2026-02-25T10:00:00"
  }
]
```

---

### `GET /api/progress/me/history` 🔒
Paginated session history with per-question attempt detail.

**Query params:**
| Param | Type | Description |
|-------|------|-------------|
| `level` | string | Filter by level |
| `status` | string | `in_progress`, `completed`, or `abandoned` |
| `limit` | int | Default `20` |
| `offset` | int | Default `0` |

**Response `200`:** Array of session objects, each with an `attempts` array showing what the user answered, the correct answer, and whether it was correct.

---

## 6. Admin Analytics Routes

### `GET /api/admin/analytics` 🔒 🔑
Summary stats for every registered user — sessions played, accuracy, best score.

**Response `200`:** Array of user stat objects sorted by highest average score.

---

### `GET /api/admin/analytics/leaderboard` 🔒 🔑
Top scorers per level with automatic ranking.

**Query params:**
| Param | Type | Description |
|-------|------|-------------|
| `level` | string | Optional. Limit to one level. |

**Response `200`:** Array of leaderboard entries:
```json
[
  {
    "level": "easy",
    "user_id": 3,
    "name": "John",
    "total_sessions": 5,
    "overall_accuracy_percent": 92.0,
    "best_score_percent": 100.0,
    "rank_in_level": 1
  }
]
```

---

### `GET /api/admin/analytics/user/<user_id>` 🔒 🔑
Full progress detail for a specific user: overview + per-level stats + last 10 sessions.

**Response `200`:**
```json
{
  "id": 3,
  "name": "John",
  "email": "john@example.com",
  "total_sessions": 10,
  "avg_score_percent": 75.0,
  "best_score_percent": 100.0,
  "level_progress": [ ... ],
  "recent_sessions": [ ... ]
}
```

---

### `GET /api/admin/analytics/quiz-stats` 🔒 🔑
Per-question difficulty analysis — attempt count and the correct-answer rate for every question.

**Query params:**
| Param | Type | Description |
|-------|------|-------------|
| `level` | string | Optional filter |

**Response `200`:**
```json
[
  {
    "quiz_id": 1,
    "level": "easy",
    "question_text": "What is Hello in Newari?",
    "total_attempts": 42,
    "correct_attempts": 38,
    "correct_rate_percent": 90.48
  }
]
```
Questions are sorted by `correct_rate_percent` ascending (hardest first).

---

## Database Tables

| Table | Description |
|-------|-------------|
| `users` | Registered users with roles (`learner` / `admin`) |
| `lesson` | Vocabulary and sentence lessons (easy / intermediate / hard) |
| `quiz` | Quiz questions linked to lessons |
| `quiz_sessions` | One row per quiz attempt — level, score, status, timestamps |
| `quiz_attempts` | One row per answered question within a session |
| `user_level_progress` | Aggregated accuracy and best scores per user per level |

