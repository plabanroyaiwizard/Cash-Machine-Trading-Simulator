from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from simulator.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=2, max=10,
                                              message='Username should be between 2 and 10 characters.')])

    email = StringField('Email Id', validators=[DataRequired(), Email(message='Please enter a valid Email Id.',
                                                                      allow_empty_local=True)])

    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=4, max=30,
                                                message='Password should be between 4 and 30 characters.'),
                                         Regexp(regex="^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{4,}$",
                                                message='Password should have minimum of 4 characters, at least one '
                                                        'letter, one number and one special character.')])

    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 Length(min=4, max=30,
                                                        message='Password should be between 4 and 30 characters.'),
                                                 Regexp(
                                                     regex="^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{4,}$",
                                                     message='Password should have minimum of 4 characters, at least one '
                                                             'letter, one number and one special character.'),
                                                 EqualTo(fieldname='password',
                                                         message='The Password and Confirm Password should have same '
                                                                 'value.')])

    submit = SubmitField(label='Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(f"The {username.data} is already taken, please choose a new one!")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(f"The {email.data} is already in use, please choose a new one!")


class LoginForm(FlaskForm):
    email = StringField('Email Id', validators=[DataRequired(), Email(message='Please enter a valid Email Id.',
                                                                      allow_empty_local=True)])

    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=4, max=30,
                                                message='Password should be between 4 and 30 characters.'),
                                         Regexp(regex="^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{4,}$",
                                                message='Password should have minimum of 4 characters, at least one '
                                                        'letter, one number and one special character.')])

    submit = SubmitField(label='Login')


class TradeForm(FlaskForm):
    amount = SelectField(u'Amount',
                         choices=[(10000, '$ 10,000'), (15000, '$ 15,000'), (20000, '$ 20,000'), (25000, '$ 25,000'),
                                  (30000, '$ 30,000')])
    shares = SelectField(u'Shares',
                         choices=[('AAPL', 'Apple Inc'), ('AMZN', ' Amazon.com, Inc'), ('BAC', 'Bank of America Corp'),
                                  ('DIS', 'Walt Disney Co'), ('FB', 'Facebook, Inc. Common Stock'),
                                  ('GOOGL', 'Alphabet Inc Class A'), ('JPM', 'JPMorgan Chase & Co.'),
                                  ('MA', 'Mastercard Inc'), ('MSFT', 'Microsoft Corporation'),
                                  ('UNH', 'UnitedHealth Group Inc')])
    no_of_shares = SelectField(u'No. of Shares',
                               choices=[(100, '100'), (200, '200'), (300, '300'), (400, '400'), (500, '500'), (600, '600')])
    start_date = SelectField(u'Simulation Start Date',
                             choices=[('2005-01-01', '01 Jan 2005'), ('2006-01-01', '01 Jan 2006'),
                                      ('2007-01-01', '01 Jan 2007'), ('2008-01-01', '01 Jan 2008'),
                                      ('2009-01-01', '01 Jan 2009'), ('2010-01-01', '01 Jan 2010')])
    no_of_years = SelectField(u'No. of Years',
                              choices=[(4, 'Four'), (5, 'Five'), (6, 'Six'), (7, 'Seven'), (8, 'Eight')])
    submit = SubmitField(label='Submit')
