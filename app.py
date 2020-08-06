from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


def create_app():
    app = Flask(__name__)
    return app

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.today())

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def home():
    print(request.method)
    if request.method == 'POST':
        task_data = request.form['data']
        print(task_data)
        new_task = Task(data=task_data)
        try:
            print("hio1")
            db.session.add(new_task)
            print("hio2")
            db.session.commit()
            print("hio3")
            return redirect('/')
        except:
            return 'Error adding task'
    else:
        tasks = Task.query.order_by(Task.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_del = Task.query.get_or_404(id)
    try:
        db.session.delete(task_del)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error deleting task %r' % id

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.data = request.form['data']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Error updating task %r' % id
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)