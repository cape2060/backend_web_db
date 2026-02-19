import pymysql
import os

def connect_db():
	return pymysql.connect(
		host=os.getenv('DB_HOST'),
		user=os.getenv('DB_USER'),
		password=os.getenv('DB_PASSWORD')
	)

def init_db():
	conn = connect_db()
	cursor = conn.cursor(pymysql.cursors.DictCursor)
	cursor.execute("CREATE DATABASE IF NOT EXISTS Bhasabridge")
	cursor.execute("USE Bhasabridge")


	cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        role ENUM('learner','admin') DEFAULT 'learner',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
	cursor.execute("""
	CREATE TABLE IF NOT EXISTS quiz_questions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        level ENUM('beginner','moderate','hard') NOT NULL,
        question TEXT NOT NULL,
        option1 VARCHAR(100) NOT NULL,
        option2 VARCHAR(100) NOT NULL,
        option3 VARCHAR(100) NOT NULL,
        option4 VARCHAR(100) NOT NULL,
        correct_answer VARCHAR(100) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
	cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_results (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        level ENUM('beginner','moderate','hard') NOT NULL,
        score INT NOT NULL,
        total_questions INT NOT NULL,
        date_taken TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)
	quizzes = {
        "beginner": [
            ("What is 'Hello' in Newari?", "jvajalapa", "subhay", "binti", "chhen", "jvajalapa"),
            ("What is 'Thank you' in Newari?", "majyu", "subhay", "gvahali", "bae", "subhay"),
            ("What is 'Water' in Newari?", "la", "nasa", "pasa", "kha", "la"),
            ("What is 'Food' in Newari?", "la", "nasa", "chhen", "pasa", "nasa"),
            ("What is 'Friend' in Newari?", "pasa", "chhen", "la", "gvahali", "pasa"),
            ("What is 'House' in Newari?", "chhen", "pasa", "la", "nasa", "chhen"),
            ("How do you say 'Help'?", "binti", "gvahali", "subhay", "majyu", "gvahali"),
            ("How do you say 'Yes'?", "majyu", "kha", "svaye", "bae", "kha"),
            ("How do you say 'No'?", "kha", "majyu", "subhay", "jvajalapa", "majyu"),
            ("How do you say 'Goodbye'?", "bae", "svaye", "jvajalapa", "subhay", "svaye")
        ],
        "moderate": [
            ("What is 'To Eat' in Newari?", "Nale", "Nale", "Wane", "Swa", "Dya"),
            ("How do you say 'Come here'?", "Thana wa", "Thana wa", "Gana wane", "Jita bi", "Pheta"),
            ("What is 'Morning'?", "Suth", "Suth", "Nihin", "Sanil", "Chya"),
            ("What is 'One' (Number)?", "Chhagu", "Chhagu", "Nigu", "Swangu", "Pyangu"),
            ("How do you say 'Where are you going'?", "Gana wane tya?", "Gana wane tya?", "Chhu yaana chona?", "Naa chhu kha?", "Jita masyu"),
            ("What is 'Mother'?", "Maa", "Maa", "Bau", "Kija", "Tata"),
            ("What is 'Father'?", "Bau", "Bau", "Maa", "Paju", "Daju"),
            ("What is 'Money'?", "Dheba", "Dheba", "La", "Chhen", "Pasa"),
            ("How do you say 'Sit down'?", "Pheta", "Pheta", "Dana", "Wane", "Nale"),
            ("What is 'Flower'?", "Swaan", "Swaan", "Sing", "Haa", "Kaa")
        ],
        "hard": [
            ("How do you say 'Please give me' (Respectful)?", "Biya disan", "Biya disan", "Bi", "Ka", "Wane"),
            ("What is 'Forgive me'?", "Ksama yana disan", "Ksama yana disan", "Jvajalapa", "Subhay", "Majyu"),
            ("How do you say 'I don't know'?", "Jita masyu", "Jita masyu", "Jita syu", "Kha", "Makhu"),
            ("What is 'Happy New Year'?", "Nhu Daya Bhintuna", "Nhu Daya Bhintuna", "Bhintuna", "Subhay", "Mati"),
            ("What is the word for 'Earthquake'?", "Baha", "Baha", "Wa", "Gaa", "Bu"),
            ("How do you say 'What happened?'?", "Chhu jula?", "Chhu jula?", "Gana?", "Su?", "Guble?"),
            ("What is 'Culture'?", "Sanskriti", "Sanskriti", "Ritithiti", "Chaj", "Parva"),
            ("How do you say 'Very Good'?", "Sakka bhin", "Sakka bhin", "Baala", "Mabaala", "Hakka"),
            ("What is the word for 'Shop'?", "Pasa", "Pasa", "Chhen", "Baha", "Kwa"),
            ("How do you say 'Congratulations'?", "Bhintuna", "Bhintuna", "Subhay", "Lhaso", "Syu")
        ]
    }
    
	for level, questions in quizzes.items():
		for q in questions:
			cursor.execute("""
            SELECT COUNT(*) as count FROM quiz_questions
            WHERE question=%s AND level=%s
            """, (q[0], level))
			if cursor.fetchone()['count'] == 0:
				cursor.execute("""
                INSERT INTO quiz_questions (level, question, correct_answer, option1, option2, option3, option4)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                """, (level, *q))
	conn.commit()
	cursor.close()
	conn.close()




