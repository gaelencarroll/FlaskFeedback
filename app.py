from flask import Flask, render_template, session, redirect
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from forms import RegisterForm, DeleteForm, LoginForm, FeedbackForm
from models import connect_db, db, User, Feedback

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask-feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'chickens'

toolbar = DebugToolbarExtension(app)
connect_db(app)


@app.route('/')
def main_page():
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(f"/users/{session['username']}")
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        user = User.register(username, first_name, last_name, password, email)
        db.session.commit()
        session['username'] = user.username
        return redirect(f'/users/{user.username}')

    else:
        return render_template("users/register.html", form=form)


@app.route('/login', methods=["GET", 'POST'])
def login():
    if 'username' in session:
        return redirect(f"/users/{session['username']}")
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ['Invalid username or password.']
            return render_template("users/login.html", form=form)

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/login')


@app.route('/users/<username>')
def user_page(username):
    if 'username' not in session or username != session['username']:
        raise Unauthorized
    form = DeleteForm()
    user = User.query.get('username')
    render_template('users/show.html', form=form, user=user)


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    if 'username' not in session or username != session['username']:
        raise Unauthorized
    user = User.query.get('username')
    db.session.delete(user)
    db.session.commit()
    session.pop(username)
    return redirect('/login')


@app.route('/users/<username>/feedback/new')
def add_feedback(username):
    if 'username' not in session or username != session['username']:
        raise Unauthorized
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(username=username, title=title, content=content)
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{feedback.username}')
    else:
        return render_template('/feedback/new.html', form=form)


@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def edit_feedback(feedback_id):
    if 'username' not in session or feedback.username != session['username']:
        raise Unauthorized
    feedback = Feedback.query.get(feedback_id)
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f'/users/{feedback.username}')
    else:
        return render_template('/feedback/edit.html', form=form, feedback=feedback)


@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    if 'username' not in session or feedback.username != session['username']:
        raise Unauthorized
    feedback = Feedback.query.get(feedback_id)
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f'/users/{feedback.username}')
