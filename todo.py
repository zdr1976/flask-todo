from datetime import datetime
from uuid import uuid4

from flask import Flask, redirect, render_template, request, url_for

from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm

from wtforms import BooleanField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ZYZe_b8IxWMWx5ZVj7D2mg'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False)
    title = db.Column(db.String(20), unique=False, nullable=False)
    description = db.Column(db.String(120), nullable=True)
    added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    done = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"ToDo('{self.title}', '{self.added}')"

    def __str__(self):
        return f"Notification: '{self.title}', '{self.added}'"


class ToDoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=20)])
    description = TextAreaField('Description', validators=[Length(max=120)])
    done = BooleanField('Add')


# Create DB with 'todos' table.
#db.create_all()


@app.route("/")
@app.route("/<int:page_num>")
def list_todo(page_num=1):
    todos = Todo.query.order_by(Todo.added.desc()).paginate(per_page=5,
                                                            page=page_num,
                                                            error_out=True)
    return render_template('todo.html', todos=todos, update=False)


@app.route("/todo/add", methods=['GET', 'POST'])
def add_todo():
    form = ToDoForm()

    if form.validate_on_submit():
        todo = Todo(title=form.title.data, description=form.description.data,
                    uuid=str(uuid4()))
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('list_todo'))
    else:
        return render_template('add.html', form=form)


@app.route("/todo/<uuid:todo_uuid>/delete")
def delete_todo(todo_uuid):
    todo = Todo.query.filter_by(uuid=str(todo_uuid)).first_or_404()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('list_todo'))


@app.route("/todo/<uuid:todo_uuid>/done")
def done_todo(todo_uuid):
    todo = Todo.query.filter_by(uuid=str(todo_uuid)).first_or_404()
    todo.done = True
    todo.added = datetime.utcnow()
    db.session.commit()
    return redirect(url_for('list_todo'))


@app.route("/todo/<uuid:todo_uuid>/update", methods=['GET', 'POST'])
def update_todo(todo_uuid):
    todo = Todo.query.filter_by(uuid=str(todo_uuid)).first_or_404()
    form = ToDoForm()

    if form.validate_on_submit():
        todo.title = form.title.data
        todo.description = form.description.data
        todo.done = form.done.data
        todo.added = datetime.utcnow()
        db.session.commit()
        return redirect(url_for('list_todo'))
    elif request.method == 'GET':
        form.title.data = todo.title
        form.description.data = todo.description
        form.done.data = todo.done

    return render_template('add.html', form=form, update=True)


if __name__ == '__main__':
    app.run(debug=True)
