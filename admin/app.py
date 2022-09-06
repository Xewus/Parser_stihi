from flask import Flask, flash, redirect, render_template, url_for, request
from werkzeug.datastructures import MultiDict
from admin import commands, forms, users
from app_core import utils, settings

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
def logout_view(user: users.User = None):
    if isinstance(user, users.User):
        user.time_token = None
        user.token = None
    return redirect(url_for('index_view'))


@app.route('/login',  methods=('GET', 'POST'))
def login_view():
    form = forms.LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if users.User.check_user(username=username, password=password):
            USERS[username] = users.User(username=username, password=password)
            return redirect(url_for('choose_parsing_view', username=username))
        flash('Введены неверные данные')
    return render_template('login.html', form=form)


@app.route('/choose_parsing/<username>', methods=('GET', 'POST'))
def choose_parsing_view(username: str):
    form = forms.ChoiceParseForm()
    # user = USERS.get(username)
    # if user is None or not user.check_time_token():
    #     return redirect(url_for('index_view'))
    if form.validate_on_submit():
        author = utils.extract_author(form.author.data)
        choice = form.choice.data

        if choice == commands.CHOOSE_POEMS:
            commands.parse(commands.COMMANDS[commands.LIST_POEMS] % author)
            return redirect(url_for('choose_poems_view'))
        else:
            commands.parse(commands.COMMANDS.get(choice) % author)
    return render_template('choose_parsing.html', form=form)


@app.route('/choose_poems/', methods=('GET', 'POST'))
def choose_poems_view():
    form = forms.ChoicePoemsForm()
    form.choice.choices = utils.create_choice_list()
    if request.method == 'POST' and form.validate_on_submit:
        choised = settings.SEPARATOR.join(form.choice.data)
        print(choised)
        commands.parse(commands.COMMANDS[commands.CHOOSE_POEMS] % choised)
    return render_template('choose_poems.html', form=form)


if __name__ == '__main__':
    app.run()
