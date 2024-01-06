from flask_login import login_required
from pymysql import IntegrityError
import traceback
from werkzeug.security import generate_password_hash
from flask import Blueprint, Flask, current_app, render_template, request, redirect, url_for,flash
from flask_paginate import Pagination
from auth import admin_required
from models import CustomerForm, User, db, Customers # Assuming your models are in a file named models.py
from models import db

customer = Blueprint('customer', __name__)

# List all customers
@customer.route('/customers', methods=['GET'])
@login_required
@admin_required
def list_customers():
   page = request.args.get('page', 1, type=int)
   customers = Customers.query.paginate(page=page, per_page=5, error_out=False)
   return render_template('customers.html', customers=customers)

# on board customer 
@customer.route('/customers/new', methods=['GET'])
@login_required
@admin_required
def new_customer():
   form = CustomerForm()
  #  form.user_id.choices = [(user.id, user.username) for user in User.query.all()]
   return render_template('customer_onboard.html', form=form)


@customer.route('/customers/new', methods=['POST'])
@login_required
@admin_required
def create_customer():
  form = CustomerForm()
  if form.validate_on_submit():
    try:
        new_user = User(username=form.first_name.data + '_' + form.last_name.data, email=form.customer_email.data, role="customer")
        new_user.set_password('default_password')
        db.session.add(new_user)
        db.session.commit() 
        new_customer = Customers(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            customer_email=form.customer_email.data,
            address=form.address.data,
            user_id=new_user.id 
        )
        db.session.add(new_customer)
        db.session.commit()
        flash('Customer added successfully.', 'success')
        return redirect(url_for('customer.list_customers'))
    except Exception as e:
        db.session.rollback() 
        error_info = str(e.orig)
        flash(f"An error occurred: {error_info}", 'warning')
        flash('Email already in use', 'warning')
        return render_template('customer_onboard.html', form=form)
  else:
    flash('Form validation failed', 'error')
    return render_template('customer_onboard.html', form=form)

# Show a form to edit an existing customer
@customer.route('/customers/edit/<int:customer_id>', methods=['GET'])
@login_required
@admin_required
def edit_customer(customer_id):
  customer = Customers.query.get(customer_id)
  form = CustomerForm(obj=customer)
  form.username.data = User.query.get(customer.user_id).username
  return render_template('customer_edit.html', form=form, customer=customer)

# Handle form submission to update an existing customer
@customer.route('/customers/edit/<int:customer_id>', methods=['POST'])
@login_required
@admin_required
def update_customer(customer_id):
  customer = Customers.query.get(customer_id)
  form = CustomerForm()
  if form.validate_on_submit():
      customer.first_name=form.first_name.data,
      customer.last_name=form.last_name.data,
      customer.customer_email = form.customer_email.data
      customer.address = form.address.data
      # customer.user_id = form.user_id.data
      db.session.commit()
      flash('Customer updated successfully.', 'success')
      return redirect(url_for('customer.list_customers'))
  return render_template('customer_edit.html', form=form)

# Delete a customer
@customer.route('/customers/delete/<int:customer_id>', methods=['GET','POST'])
@login_required
@admin_required
def delete_customer(customer_id):
  customer = Customers.query.get_or_404(customer_id)
  if request.method == 'POST':
      db.session.delete(customer)
      db.session.commit()
      flash('User deleted successfully.', 'success')
      return redirect(url_for('customer.list_customers'))
  return render_template('customer_delete.html', customer=customer)
