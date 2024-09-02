from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Using SQLite for simplicity in development
db = SQLAlchemy(app)

class Todo(db.Model):
    # Define the Todo model with an ID, content, and date created
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)  # Ensures content is always provided
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # Automatically set the date when a task is created

    def __repr__(self):
        return '<Task %r>' % self.id  # Provides a human-readable representation of the Task instance

@app.route('/', methods=['POST', 'GET'])
def index():
    # Handle both GET and POST requests to the index route
    if request.method == 'POST':
        task_content = request.form['content']  # Extract content from the form submission
        new_task = Todo(content=task_content)  # Create a new Todo instance

        try:
            db.session.add(new_task)  # Add the new task to the session
            db.session.commit()  # Commit the session to save the task to the database
            return redirect('/')  # Redirect to the home page upon successful task addition
        except:
            return 'There was an issue adding your task'  # Handle any exceptions by notifying the user

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()  # Retrieve all tasks, ordered by their creation date
        return render_template('index.html', tasks=tasks)  # Render the index template with the list of tasks

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)  # Retrieve the task by ID or return a 404 error if not found

    try:
        db.session.delete(task_to_delete)  # Remove the task from the session
        db.session.commit()  # Commit the session to delete the task from the database
        return redirect('/')  # Redirect to the home page after successful deletion
    except:
        return 'There was a problem deleting that task'  # Handle any exceptions by notifying the user

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)  # Retrieve the task by ID or return a 404 error if not found

    if request.method == 'POST':
        task.content = request.form['content']  # Update the task's content with the new data from the form

        try:
            db.session.commit()  # Commit the session to save the changes to the database
            return redirect('/')  # Redirect to the home page after successful update
        except:
            return 'There was an issue updating your task'  # Handle any exceptions by notifying the user

    else:
        return render_template('update.html', task=task)  # Render the update template with the task data for editing

if __name__ == "__main__":
    app.run(debug=True)  # Run the app in debug mode for development purposes
