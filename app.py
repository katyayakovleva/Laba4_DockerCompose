from flask import redirect, url_for, render_template, request
from flask_login import login_user, login_required, logout_user, current_user

from website.Nagware import nagwareInfo
from website.Vigener import encrypt

from website.FileWorker import *
from website.models import User
from website import create_app, db
from flask_wtf import FlaskForm, RecaptchaField, Recaptcha
from wtforms import StringField, PasswordField, SubmitField


app = create_app()

app.config['RECAPTCHA_PUBLIC_KEY'] = '6LfH2M4fAAAAAH5unMpAyxWxHWBGRU5667QggXHJ'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LfH2M4fAAAAACRbiT9HaA20gJ3kq30XW9WaIZLf'
app.config['TESTING'] = True
RECAPTCHA_PARAMETERS = {'hl': 'zh', 'render': 'explicit'}
RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}

class LoginForm(FlaskForm):
    login = StringField('Login')
    password = PasswordField('Password')
    # recaptcha = RecaptchaField(validators=[Recaptcha(message="Your custom message")])
    submit = SubmitField('Перевірити')


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        # captcha_response = request.form['g-recaptcha-response']
        # if len(captcha_response) > 0:
            login = form.login.data
            password = form.password.data
            user = User.query.filter_by(login=login).first()
            if user:
                if encrypt(password, 'katya') == user.password:
                    login_user(user, remember=True)
                    return redirect(url_for('home'))
                else:
                    flash('Не правильний пароль, спробуйте ще.', category='error')
            else:
                flash('Такого акаунту не існує', category='error')
        # else:
        #     flash("Підтвердіть, що ви не робот", category='error')

    return render_template("login.html", user=current_user, form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        login = request.form.get('login')

        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        fullAccess = request.form.get('fullAccess')
        user = User.query.filter_by(login=login).first()

        if user:
            flash('Email already exists.', category='error')
        elif len(login) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:

            if fullAccess == 'on':
                new_user = User(login=login, password=encrypt(password1, 'katya'), fullAccess=True)
            else:
                new_user = User(login=login, password=encrypt(password1, 'katya'), fullAccess=False)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Вітаємо з реєстрацією', category='success')
            return redirect(url_for('login'))

    return render_template("sign_up.html", user=current_user)


@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        access = User.get_access(self=current_user)
        return render_template('home.html', access=access, variant=0, user=current_user)
    else:
        return redirect(url_for('login'))


@app.route('/home', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        access = User.get_access(self=current_user)
        if not access:
            nagwareInfo()
        variant = request.form.get('variants')
        return render_template('home.html', user=current_user, variant=variant, access=access)
    else:
        return redirect(url_for('login'))

@app.route('/read_file', methods=['GET', 'POST'])
def read_file():
    if request.method == 'POST':
        file = request.form.get('file')
        readFile(file)
    return redirect(url_for('home'))


@app.route('/read_file_properties', methods=['GET', 'POST'])
def read_file_properties():
    if request.method == 'POST':
        file = request.form.get('file')
        getFileProperties(file)

    return redirect(url_for('home'))


@app.route('/write_to_file', methods=['GET', 'POST'])
def write_to_file():
    if request.method == 'POST':
        file = request.form.get('file')
        text = request.form.get('inputText')
        writeToFile(file, text)

    return redirect(url_for('home'))


@app.route('/create_file', methods=['GET', 'POST'])
def create_file():
    if request.method == 'POST':
        file = request.form.get('file')
        createFile(file)

    return redirect(url_for('home'))


@app.route('/rename_file', methods=['GET', 'POST'])
def rename_file():
    if request.method == 'POST':
        file = request.form.get('file')
        name = request.form.get('inputNewName')
        renameFile(file, name)

    return redirect(url_for('home'))


@app.route('/check_word_in_file', methods=['GET', 'POST'])
def check_word_in_file():
    if request.method == 'POST':
        file = request.form.get('file')
        word = request.form.get('inputFindWord')
        checkIfWordExistInFile(file, word)

    return redirect(url_for('home'))


@app.route('/combine_files', methods=['GET', 'POST'])
def combine_files():
    if request.method == 'POST':
        file1 = request.form.get('file')
        file2 = request.form.get('inputSecondFile')
        combineTwoFiles(file1, file2)

    return redirect(url_for('home'))


@app.route('/delete_file', methods=['GET', 'POST'])
def delete_file():
    if request.method == 'POST':
        file = request.form.get('file')
        deleteFile(file)

    return redirect(url_for('home'))


# Timer(1, openBrowser).start()
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
