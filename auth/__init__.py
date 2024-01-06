from functools import wraps
from flask_login import current_user, login_user, login_required, logout_user
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import AdminOnboardForm, ChangePasswordForm, LoginForm, User, UserForm
from models import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    form = LoginForm()
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # if form.validate_on_submit():
    #     user = User.query.filter_by(username=form.username.data).first()
    #     if user and user.check_password(form.password.data):
    #         login_user(user)
    #         flash('Login successful!', 'success')
    #         return redirect(url_for('home'))
    #     else:
    #         flash('Invalid username or password', 'danger')
    user = User.query.filter_by(username=username).first()
    
    if not user:
        flash('Please check your login details and try again.','warning')
        return redirect(url_for('auth.login'))
    
    if not user.check_password(password):
        flash('Please check your login details and try again.','error')
        return redirect(url_for('auth.login')) 

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() 

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, username=username, role="admin")
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))



def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.role != 'admin':
            flash('Access denied. Admins only.', 'danger')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    return decorated_view

@auth.route('/admin/onboard', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_onboard():
    if current_user.role != 'admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('main.index'))

    form = AdminOnboardForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        # new_user.set_password('default_password')
        password = form.password.data
        role = form.role.data

        new_user = User(username=username, role=role, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash(f'{role.capitalize()} {username} onboarded successfully!', 'success')
        return redirect(url_for('admin_onboard'))

    return render_template('admin_onboard.html', form=form)


# @auth.route('/admin/crm', methods=['GET'])
# @login_required
# @admin_required
# def admin_crm():
#     if current_user.role != 'admin':
#         flash('Access denied. Admins only.', 'danger')
#         return redirect(url_for('index'))
#     users = User.query.all()
#     return render_template('admin_crm.html', users=users)

@auth.route('/users/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def update_user(id):
  user = User.query.get_or_404(id)
  form = UserForm(obj=user)
  if form.validate_on_submit():
      user.username = form.username.data
      user.email = form.email.data
      db.session.commit()
      flash('User updated successfully.', 'success')
      return redirect(url_for('auth.list_users'))
  return render_template('user_update.html',user=user, form=form)

@auth.route('/users')
@login_required
@admin_required
def list_users():
    if current_user.role != 'admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=5, error_out=False)
    return render_template('users.html', users=users)


@auth.route('/users/delete/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_user(id):
  user = User.query.get_or_404(id)
  if request.method == 'POST':
      db.session.delete(user)
      db.session.commit()
      flash('User deleted successfully.', 'success')
      return redirect(url_for('auth.list_users'))
  return render_template('user_delete.html', user=user)


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
  user = User.query.get_or_404(current_user.id)
  form = ChangePasswordForm()
  if form.validate_on_submit():
      if user.check_password(form.old_password.data):
          password = form.new_password.data
          user.set_password(password)
          db.session.commit()
          flash('your password is changed successfully.', 'success')
          return redirect(url_for('main.index'))          
  else:
      for field, errors in form.errors.items():
          for error in errors:
              flash(f'{field}: {error}', 'warning')   
  return render_template('change_password.html',user=user, form=form)
