from pathlib import Path

from flask import (Flask, flash, redirect, render_template, request, send_file,
                   url_for)

from admin import commands, forms, users
from app_core import settings, utils
from app_core.converter import JsonConvereter

COMMANDS = commands.COMMANDS

URL_PATHS_FOR_ANONIM = settings.URL_PATHS_FOR_ANONIM
POEMS_STORE = settings.POEMS_STORE
ARGS_SEPARATOR = settings.ARGS_SEPARATOR
OUT_POEMS = settings.OUT_POEMS


app = Flask(__name__)
app.config['SECRET_KEY'] = 'settings.SECRET_KEY'

USERS = {'session': 'username'}


@app.before_request
def before_request():
    request.user = users.User.get_request_user_by_session(
        USERS, request.cookies.get('session')
    )
    if request.user is None and request.path not in URL_PATHS_FOR_ANONIM:
        return redirect(url_for('login_view'))


@app.route('/')
def index_view():
    return render_template('index.html', user=request.user)


@app.route('/logout')
def logout_view():
    USERS.pop(request.cookies['session'], None)
    return redirect(url_for('index_view'))


@app.route('/login',  methods=('GET', 'POST'))
def login_view():
    form = forms.LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if users.User.check_user(username=username, password=password):
            USERS[request.cookies['session']] = users.User(username)
            return redirect(url_for('choose_parsing_view'))
        flash('Введены неверные данные')
    return render_template('login.html', form=form)


@app.route('/choose_parsing/', methods=('GET', 'POST'))
def choose_parsing_view():
    form = forms.ChoiceParseForm()
    context = {
        'template_name_or_list': 'choose_parsing.html',
        'form': form,
        'user': request.user
    }
    if form.validate_on_submit():
        choice = COMMANDS.get(form.choice.data)
        if choice is None:
            return render_template(**context)

        author = utils.extract_author(form.author.data)
        if author is None:
            flash('Ошибка в переданной строке')
            return render_template(**context)

        if choice == COMMANDS[commands.CHOOSE_POEMS]:
            commands.parse(COMMANDS[commands.LIST_POEMS] % author)
            return redirect(url_for('choose_poems_view'))
        else:
            commands.parse(choice % author)
            return redirect(url_for('choose_download_view'))
    return render_template(**context)


@app.route('/choose_poems/', methods=('GET', 'POST'))
def choose_poems_view():
    form = forms.ChoicePoemsForm()
    context = {
        'template_name_or_list': 'choose_poems.html',
        'form': form,
        'user': request.user
    }
    form.choice.choices = utils.create_choice_list()
    if request.method == 'POST' and form.validate_on_submit:
        choised = ARGS_SEPARATOR.join(form.choice.data)
        commands.parse(commands.COMMANDS[commands.CHOOSE_POEMS] % choised)
        return redirect(url_for('choose_download_view'))
    return render_template(**context)


@app.route('/choose_download/')
def choose_download_view():
    context = {
        'template_name_or_list': 'choose_download.html',
        'user': request.user,
        'poems_store': Path(POEMS_STORE).exists()
    }
    return render_template(**context)


@app.route('/download/<doc_type>')
def download_view(doc_type: str):
    source = Path(POEMS_STORE)
    if not source.exists() or doc_type not in {'json', 'md', 'docx'}:
        return redirect(url_for('choose_parsing_view'))

    convert = JsonConvereter(doc_type, source)
    out_file = convert.converter(out_file=OUT_POEMS)
    return send_file(out_file, as_attachment=True)


@app.route('/create_user/', methods=('GET', 'POST'))
def create_user_view():
    form = forms.CreateUserForm()
    context = {
        'template_name_or_list': 'create_user.html',
        'form': form,
        'user': request.user
    }
    if form.validate_on_submit():
        su_password = form.password.data
        username = form.username.data
        user_password = form.user_password.data

        create, error = users.SuperUser.create_user(
            su_password=su_password,
            username=username,
            user_password=user_password
        )
        if create:
            return redirect(url_for('index_view'))
        flash(error)
    return render_template(**context)


if __name__ == '__main__':
    app.run()
