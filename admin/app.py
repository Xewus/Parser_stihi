from flask import Flask, flash, redirect, render_template, url_for

from admin import commands, forms, models
from app_core import utils

app = Flask(__name__)
app.config['SECRET_KEY'] = 'settings.SECRET_KEY'

USERS = {}


@app.before_request
def before_request():
    print('ok')


@app.route('/')
def index_view():
    return render_template('index.html')


@app.route('/logout')
def logout_view(user: models.User = None):
    if isinstance(user, models.User):
        user.time_token = None
        user.token = None
    return redirect(url_for('index_view'))


@app.route('/login',  methods=('GET', 'POST'))
def login_view():
    form = forms.LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if models.User.check_user(username=username, password=password):
            USERS[username] = models.User(username=username, password=password)
            return redirect(url_for('parsing_view', username=username))
        flash('Введены неверные данные')
    return render_template('login.html', form=form)


@app.route('/parsing/<username>', methods=('GET', 'POST'))
def parsing_view(username: str):
    form = forms.ChoiceParseForm()
    user = USERS.get(username)
    if user is None or not user.check_time_token():
        return redirect(url_for('index_view'))
    print(form.choice.data)
    if form.validate_on_submit():
        author = utils.extract_author(form.author.data)
        choice = form.choice.data

        if choice == commands.CHOOSE_POEMS:
            commands.parse(commands.COMMANDS[commands.LIST_POEMS] % author)
        else:
            commands.parse(commands.COMMANDS.get(choice) % author)
            return redirect(url_for('index_view'))
    return render_template('parsing.html', form=form, user=user)


if __name__ == '__main__':
    app.run()
