from pathlib import Path

from flask import (abort, flash, redirect, render_template, request, send_file,
                   session, url_for)

from app import commands, forms, model
from app_core import utils
from app_core.converter import JsonConvereter
from app_core.settings import (ARGS_SEPARATOR, OUT_POEMS, POEMS_STORE,
                               URL_PATHS_FOR_ANONIM)

from . import app

COMMANDS = commands.COMMANDS


too_many_requests = utils.AllowTries(time_limit=60, tries=20)


@app.before_request
def set_request_user():
    if request.path.startswith('/static'):
        return
    too_many_requests(request.remote_addr, abort, 429)
    user = session.get('user')
    if hasattr(user, 'get') and user.get('user_id'):
        user = model.User.get_by_id(user_id=user.get('user_id'))
    request.user = user or model.AnonimUser()
    if request.user.is_authenticated or request.path in URL_PATHS_FOR_ANONIM:
        return
    return redirect(url_for('login_view'))


@app.route('/')
def index_view():
    return render_template('index.html')


@app.route('/login/',  methods=('GET', 'POST'))
def login_view():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = model.User.login(
            username=form.username.data,
            password=form.password.data
        )
        if user is not None:
            session['user'] = user.as_dict()
            return redirect(url_for('choose_parsing_view'))
        flash('Введены неверные данные')
    return render_template('login.html', form=form)


@app.route('/logout/')
def logout_view():
    if hasattr(request, 'user'):
        request.user.logout()
    session.pop('user', None)
    return redirect(url_for('index_view'))


@app.route('/choose_parsing/', methods=('GET', 'POST'))
def choose_parsing_view():
    form = forms.ChoiceParseForm()
    context = {
        'template_name_or_list': 'choose_parsing.html',
        'form': form,
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
        'form': form
    }
    form.choice.choices = utils.create_choice_list()
    if request.method == 'POST' and form.validate_on_submit:
        choised = ARGS_SEPARATOR.join(form.choice.data)
        commands.parse(COMMANDS[commands.CHOOSE_POEMS] % choised)
        return redirect(url_for('choose_download_view'))
    return render_template(**context)


@app.route('/choose_download/')
def choose_download_view():
    context = {
        'template_name_or_list': 'choose_download.html',
        'poems_store': Path(POEMS_STORE).exists()
    }
    return render_template(**context)


@app.route('/download/<doc_type>')
def download_view(doc_type: str):
    source = Path(POEMS_STORE)
    if not source.exists() or doc_type not in {'json', 'md', 'docx'}:
        return redirect(url_for('choose_parsing_view'))

    converter = JsonConvereter(doc_type, source)
    out_file = converter.convert(out_file=OUT_POEMS)
    return send_file(out_file, as_attachment=True)


@app.route('/create_user/', methods=('GET', 'POST'))
def create_user_view():
    form = forms.CreateUserForm()
    context = {
        'template_name_or_list': 'create_user.html',
        'form': form
    }

    if not hasattr(request, 'user') or not request.user.is_admin:
        return redirect(url_for('index_view'))

    if form.validate_on_submit():
        checked, error = model.check_su_password(form.su_password.data)
        if not checked:
            flash(error)
            return render_template(**context)

        _, msg = request.user.create_user(
            username=form.username.data,
            password=form.password.data
        )
        flash(msg)
    return render_template(**context)


if __name__ == '__main__':
    app.run()
