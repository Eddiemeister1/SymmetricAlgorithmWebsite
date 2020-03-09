#CNT 4713 Assignment 6
#By Eduardo Dotel
#Most of this code is credited to Jake Rieger who was responsible in Guiding viewers through the basic features of Flask in the video:
#Learn Flask for Python - Full Tutorial by freeCodeCamp.org
#This code can be seen in github right here:
#https://github.com/jakerieger/FlaskIntroduction
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = str(request.form.getlist('content'))
        print('Message to be Encrypted:')
        print(task_content)
        #The Encryption portion of the algorithm would go here
        encrypted = ''
        for element in task_content:
            character = str(chr(ord(element) + 5))
            encrypted += character
        new_task = Todo(content=encrypted)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding the encrypted message'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting the message'

@app.route('/update/<int:id>', methods=['GET', 'POSt'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = str(request.form.getlist('content'))
        try:
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        #The decryption portion of the symmetric algorithm is shown below
        decrypted = ''
        for element in task.content:
            character = str(chr(ord(element) - 5))
            decrypted += character
        print('Decrypted Message: ')
        print(decrypted)
        return render_template('update.html', task = task, decrypted = decrypted)

if __name__ == "__main__":
    app.run(debug=True)
