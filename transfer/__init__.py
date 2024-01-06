from functools import wraps
from flask_login import current_user, login_required
from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy.orm import joinedload
from auth import admin_required
from models import  Customers, SwiftConnectRequest, SwiftTransferEditForm, SwiftTransferForm
from models import db

transfer = Blueprint('transfer', __name__)

@transfer.route('/swift_transfer/my_requests')
@login_required
def my_swift_transfer_requests():
   page = request.args.get('page', 1, type=int)
   requests = SwiftConnectRequest.query.options(joinedload(SwiftConnectRequest.customer), joinedload(SwiftConnectRequest.sender)).filter_by(sender_id=current_user.customer.id).paginate(page=page, per_page=5, error_out=False)
   return render_template('my_swift_transfer_requests.html', requests=requests)

@transfer.route('/transfer_requests')
@login_required
@admin_required
def transfer_requests():
   page = request.args.get('page', 1, type=int)
   requests = SwiftConnectRequest.query.options(joinedload(SwiftConnectRequest.sender), joinedload(SwiftConnectRequest.customer)).paginate(page=page, per_page=5, error_out=False)
   return render_template('transfer_requests.html', requests=requests)

@transfer.route('/swift_transfer', methods=['GET', 'POST'])
@login_required
def swift_transfer():
    form = SwiftTransferForm()
    if form.validate_on_submit():
        if current_user.is_authenticated and current_user.customer:
            if request.method == 'POST':
                sender_email = current_user.email
                recipient_email = form.recipient_email.data
                amount = form.amount.data
                
                sender_customer = Customers.query.filter_by(customer_email=current_user.email).first()
                recipient_customer = Customers.query.filter_by(customer_email=recipient_email).first()

                if recipient_customer:
                    swift_request = SwiftConnectRequest(
                        customer_name=sender_email,
                        customer_email=recipient_email,
                        request_details=f'Transfer of {amount} to {recipient_email}',
                        amount=amount,
                        customer_id=recipient_customer.id,
                        sender_id=sender_customer.id
                    )
                    db.session.add(swift_request)
                    db.session.commit()

                    flash('SWIFT transfer initiated successfully.', 'success')
                    return redirect(url_for('transfer.my_swift_transfer_requests'))
                else:
                    flash('Recipient not found.', 'danger')
                    return redirect(url_for('transfer.swift_transfer'))
        else:
            flash('Error: User has no associated customer.', 'error')
            return redirect(url_for('main.index'))
    customers = Customers.query.filter(Customers.id != current_user.customer.id).all()
    return render_template('swift_transfer.html', customers=customers, form=form)

@transfer.route('/swift_transfer/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_swift_transfer(id):
    swift_request = SwiftConnectRequest.query.get_or_404(id)
    form = SwiftTransferEditForm(obj=swift_request)
    if request.method == 'POST':
        swift_request.status = form.status.data
        db.session.commit()
        flash('SWIFT transfer updated successfully.', 'success')
        return redirect(url_for('transfer.transfer_requests'))
    return render_template('edit_swift_transfer.html', swift_request=swift_request, form=form)

@transfer.route('/customer/swift_transfer/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def customer_edit_swift_transfer(id):
 swift_request = SwiftConnectRequest.query.options(joinedload(SwiftConnectRequest.sender), joinedload(SwiftConnectRequest.customer)).get_or_404(id)
 form = SwiftTransferEditForm(obj=swift_request)
 if request.method == 'POST':
   new_status = form.status.data
   if new_status == 'Approved' and not current_user.role == 'admin':
       flash('Only administrators can approve transfers.', 'danger')
       return render_template('customer_edit_swift_transfer.html', swift_request=swift_request,form=form)
   swift_request.status = new_status
   db.session.commit()
   flash('SWIFT transfer updated successfully.', 'success')
   return redirect(url_for('transfer.my_swift_transfer_requests'))
 return render_template('customer_edit_swift_transfer.html', swift_request=swift_request,form=form)


