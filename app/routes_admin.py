from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from app import db
from app.models import User, Role, Inventory, Resource, Storage
from functools import wraps
from flask_login import current_user

def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)
            user_roles = [role.name for role in current_user.roles]
            if not any(role in user_roles for role in roles):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

bp = Blueprint('routes', __name__)

# Assign role to user
@bp.route('/admin/assign-role', methods=['GET', 'POST'])
@roles_required('Admin')
def assign_role():
    users = User.query.all()
    roles = Role.query.all()
    if request.method == 'POST':
        user = User.query.get(request.form['user_id'])
        role = Role.query.get(request.form['role_id'])
        if role and role not in user.roles:
            user.roles.append(role)
            db.session.commit()
        return redirect(url_for('routes.assign_role'))
    return render_template('assign_role.html', users=users, roles=roles)

# Edit Inventory
@bp.route('/inventory/edit/<int:id>', methods=['GET', 'POST'])
@roles_required('Admin')
def edit_inventory(id):
    inventory = Inventory.query.get_or_404(id)
    if request.method == 'POST':
        inventory.asset_no = request.form['asset_no']
        inventory.asset_name = request.form['asset_name']
        db.session.commit()
        return redirect(url_for('routes.dashboard'))
    return render_template('edit_inventory.html', inventory=inventory)

# Delete Inventory
@bp.route('/inventory/delete/<int:id>', methods=['POST'])
@roles_required('Admin')
def delete_inventory(id):
    inventory = Inventory.query.get_or_404(id)
    db.session.delete(inventory)
    db.session.commit()
    return redirect(url_for('routes.dashboard'))

# Edit Resource
@bp.route('/resource/edit/<int:id>', methods=['GET', 'POST'])
@roles_required('Admin')
def edit_resource(id):
    resource = Resource.query.get_or_404(id)
    if request.method == 'POST':
        resource.vcpu = request.form['vcpu']
        resource.ram = request.form['ram']
        resource.private_ip = request.form['private_ip']
        resource.public_ip_enabled = request.form.get('public_ip_enabled') == 'yes'
        resource.public_ip = request.form['public_ip'] if resource.public_ip_enabled else None
        db.session.commit()
        return redirect(url_for('routes.dashboard'))
    return render_template('edit_resource.html', resource=resource)

# Delete Resource
@bp.route('/resource/delete/<int:id>', methods=['POST'])
@roles_required('Admin')
def delete_resource(id):
    resource = Resource.query.get_or_404(id)
    db.session.delete(resource)
    db.session.commit()
    return redirect(url_for('routes.dashboard'))