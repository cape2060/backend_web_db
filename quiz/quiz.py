from flask import Blueprint,jsonify,request,session
from db import connect_db
import pymysql
from routes.login_required import login_required
import random

quiz = Blueprint('quiz',__name__)

@quiz.route('/get_quiz/<level>',methods=['GET'])
@login_required
def get_quiz(level):
    if 'user_id' not in session:
        return jsonify({'Status':'unauthorized'}),401
    if level not in ['beginner','moderate','hard']:
        return jsonify({'Status':'Invalid level'}),400
    try:
        conn = connect_db()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('USE Bhasabridge')
        cursor.execute('SELECT * FROM quiz_questions WHERE level=%s',(level,))
        question = cursor.fetchall()
        question = random.sample(question,min(5,len(question)))
        q_data = []
        for q in question:
            q_data.append({
                'id':q['id'],
                'question':q['question'],
                'options': [q['option1'],q['option2'],q['option3'],q['option4']]
            })
        cursor.close()
        conn.close()
        return jsonify({'Status':'Success','level':level,'questions':q_data}),200
    except Exception as e:
        return jsonify({'Status':'Error'}),500

@quiz.route('/submit',methods=['POST'])
@login_required
def submit():
    if 'user_id' not in session:
        return jsonify({'Status':'unauthorized'}),401
    data = request.json
    
    answers = data.get('answers')
    user_id = session['user_id']

    score = {}

    try:
        conn = connect_db()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('USE Bhasabridge')
        for qid, ans in answers.items():
            cursor.execute('SELECT level,correct_answer FROM quiz_questions WHERE id=%s',(qid,))
            q = cursor.fetchone()
            if q:
                level = q['level']
                if level not in score:
                    score[level] = {'score':0,'total':0}
                score[level]['total'] += 1
                if ans == q['correct_answer']:
                    score[level]['score'] += 1
        for l,s in score.items():
            cursor.execute('INSERT INTO quiz_results(user_id,level,score,total_questions) VALUES (%s,%s,%s,%s)',(user_id,l,s['score'],s['total']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'Status':'Success','score':score}),200
    except Exception as e:
        return jsonify({'Status':'Error'}),500
    
            


