from pprint import pprint
from flask import Flask, flash, redirect, render_template, url_for, request

from admin import commands, forms, users
from app_core import utils, settings

app = Flask(__name__)
app.config['SECRET_KEY'] = 'settings.SECRET_KEY'

USERS = {}


@app.before_request
def before_request():
    request.user = users.User.get_request_user_by_session(
        USERS, request.cookies.get('session')
    )
    if request.user is None and request.path not in settings.PATHS_FOR_ANONIM:
        return redirect(url_for('login_view'))



@app.route('/')
def index_view():
    return render_template('index.html', user = request.user)


@app.route('/logout')
def logout_view():
    USERS.pop(request.cookies['session'])
    return redirect(url_for('index_view'))


@app.route('/login',  methods=('GET', 'POST'))
def login_view():
    form = forms.LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if users.User.check_user(username=username, password=password):
            USERS[request.cookies['session']] = users.User(username)
            return redirect(url_for('choose_parsing_view', username=username))
        flash('Введены неверные данные')
    return render_template('login.html', form=form)


@app.route('/choose_parsing/', methods=('GET', 'POST'))
def choose_parsing_view():
    form = forms.ChoiceParseForm()
    if form.validate_on_submit():
        author = utils.extract_author(form.author.data)
        choice = form.choice.data

        if choice == commands.CHOOSE_POEMS:
            commands.parse(commands.COMMANDS[commands.LIST_POEMS] % author)
            return redirect(url_for('choose_poems_view'))
        else:
            commands.parse(commands.COMMANDS.get(choice) % author)
    return render_template(
        'choose_parsing.html', form=form, user = request.user
    )


@app.route('/choose_poems/', methods=('GET', 'POST'))
def choose_poems_view():
    form = forms.ChoicePoemsForm()
    form.choice.choices = utils.create_choice_list()
    if request.method == 'POST' and form.validate_on_submit:
        choised = settings.ARGS_SEPARATOR.join(form.choice.data)
        print(choised)
        commands.parse(commands.COMMANDS[commands.CHOOSE_POEMS] % choised)
    return render_template(
        'choose_poems.html', form=form, user = request.user
    )


if __name__ == '__main__':
    app.run()
