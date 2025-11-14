from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change in production

# Load phishing examples
def load_phishing_examples():
    with open('data/phishing_examples.json', 'r') as f:
        return json.load(f)

# Quiz questions
QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "Which of these is a common sign of a phishing email?",
        "options": [
            "Generic greeting like 'Dear Customer'",
            "Professional company logo",
            "Clear sender information",
            "Proper grammar and spelling"
        ],
        "correct_answer": 0,
        "explanation": "Phishing emails often use generic greetings instead of your name."
    },
    {
        "id": 2,
        "question": "What should you do if you receive a suspicious email?",
        "options": [
            "Click on links to verify",
            "Reply to ask if it's legitimate",
            "Report it to your IT department",
            "Forward it to coworkers"
        ],
        "correct_answer": 2,
        "explanation": "Always report suspicious emails to your IT department for verification."
    },
    {
        "id": 3,
        "question": "Which URL is most likely legitimate?",
        "options": [
            "http://paypal-security.verify-account.com",
            "https://www.paypal.com/account/verify",
            "paypal.secure-login.net/update",
            "http://paypal.com.user.verification.org"
        ],
        "correct_answer": 1,
        "explanation": "Legitimate URLs use the actual domain name (paypal.com) with proper HTTPS protocol."
    },
    {
        "id": 4,
        "question": "What is social engineering?",
        "options": [
            "A type of computer hardware",
            "Manipulating people to reveal confidential information",
            "A programming language",
            "A network protocol"
        ],
        "correct_answer": 1,
        "explanation": "Social engineering manipulates human psychology rather than technical hacking techniques."
    },
    {
        "id": 5,
        "question": "Which of these is a best practice for email security?",
        "options": [
            "Use the same password for all accounts",
            "Enable two-factor authentication",
            "Click on links in emails from unknown senders",
            "Share passwords with colleagues"
        ],
        "correct_answer": 1,
        "explanation": "Two-factor authentication adds an extra layer of security beyond just passwords."
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/module/<int:module_id>')
def show_module(module_id):
    examples = load_phishing_examples()
    return render_template(f'modules/module{module_id}.html', examples=examples)

@app.route('/quiz')
def quiz():
    return render_template('quiz.html', questions=QUIZ_QUESTIONS)

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    user_answers = request.json.get('answers', {})
    score = 0
    results = []
    
    for question in QUIZ_QUESTIONS:
        q_id = str(question['id'])
        user_answer = user_answers.get(q_id)
        correct_answer = question['correct_answer']
        
        is_correct = user_answer == correct_answer
        if is_correct:
            score += 1
            
        results.append({
            'question_id': q_id,
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct,
            'explanation': question['explanation']
        })
    
    percentage = (score / len(QUIZ_QUESTIONS)) * 100
    session['quiz_score'] = percentage
    
    return jsonify({
        'score': score,
        'total': len(QUIZ_QUESTIONS),
        'percentage': percentage,
        'results': results
    })

@app.route('/certificate')
def certificate():
    score = session.get('quiz_score', 0)
    if score >= 80:  # Pass threshold
        return render_template('certificate.html', score=score)
    else:
        return redirect(url_for('quiz'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)