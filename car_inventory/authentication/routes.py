from flask import Blueprint, render_template, request
from drone_inventory.forms import UserLoginForm


auth = Blueprint('auth', __name__, template_folder='auth_templates')


@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()

     try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)
    except:
        raise Exception('Invalid form data, please check your form')

    return render_template('signup.html', form = form)

        

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    return render_template('signin.html')

