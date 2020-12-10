from flask import render_template, url_for, flash, redirect

from simulator import app, db, bcrypt
from simulator.forms import RegistrationForm, LoginForm, TradeForm
from simulator.models import User
from simulator.simulation import Trading

stocks = [('AAPL', 'Apple Inc'), ('AMZN', ' Amazon.com, Inc'), ('BAC', 'Bank of America Corp'),
          ('DIS', 'Walt Disney Co'), ('FB', 'Facebook, Inc. Common Stock'), ('GOOGL', 'Alphabet Inc Class A'),
          ('JPM', 'JPMorgan Chase & Co.'), ('MA', 'Mastercard Inc'), ('MSFT', 'Microsoft Corporation'),
          ('UNH', 'UnitedHealth Group Inc')]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(password=form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=form.password.data, hashed_pwd=hashed_pwd)
        print(user)
        db.session.add(user)
        db.session.commit()
        flash(message=f"Account created for {form.username.data} and you can Log In.", category='success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title="Register")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            if bcrypt.check_password_hash(user.hashed_pwd, form.password.data):
                flash(message=f"{form.email.data}, You've logged in successfully ", category='success')
                return redirect(url_for('trade_form'))
            else:
                flash(message="Incorrect Login Credentials.", category='danger')
        elif user is None:
            flash(message="You are not registered with us, please resgister.", category='danger')
            return redirect(url_for('register'))

    return render_template('login.html', form=form, title="Login")


@app.route('/trade_form', methods=['GET', 'POST'])
def trade_form():
    form = TradeForm()
    if form.validate_on_submit():
        shares_li = [form.shares.data]
        form_data = [form.amount.data, form.shares.data, form.start_date.data,
                     form.no_of_years.data, form.no_of_shares.data]
        print(int(form.amount.data), shares_li, str(form.start_date.data),
              int(form.no_of_years.data), int(form.no_of_shares.data))
        trade_sim = Trading(int(form.amount.data), shares_li, str(form.start_date.data),
                            int(form.no_of_years.data), int(form.no_of_shares.data))
        results = trade_sim.simulate()
        print(results[0])
        for st in stocks:
            if str(form.shares.data) == st[0]:
                form_data.append(st[-1])
        form_data.append(results[-1]['net_worth'])
        profit_loss = round((float(results[-1]['net_worth']) - float(form.amount.data)), 2)
        profit_loss_per = round((profit_loss/float(form.amount.data)), 2)*100
        avg_ret = round((profit_loss_per/float(form.no_of_years.data)), 2)
        if profit_loss < 0:
            form_data.append(f'the Loss is  ${profit_loss}')
        else:
            form_data.append(f'the Profit is  ${profit_loss}')
        form_data.append(avg_ret)
        return render_template('trade_results.html', title='Trade Results', results=results, form=form_data)
    return render_template('trade_form.html', title='Trade Form', form=form)
