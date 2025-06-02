from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from app import db
from app.models import User, Inventory, Resource, Storage
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

@bp.route('/')
def home():
    return redirect(url_for('routes.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not User.query.filter_by(username=username).first():
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('routes.login'))
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            session['user'] = user.username
            return redirect(url_for('routes.dashboard'))
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('routes.login'))

@bp.route('/dashboard')
def dashboard():
    inventory = Inventory.query.all()
    return render_template('dashboard.html', inventory=inventory)

@bp.route('/inventory/add', methods=['GET', 'POST'])
def add_inventory():
    if request.method == 'POST':
        asset_no = request.form['asset_no']
        asset_name = request.form['asset_name']
        inventory = Inventory(asset_no=asset_no, asset_name=asset_name)
        db.session.add(inventory)
        db.session.commit()
        return redirect(url_for('routes.dashboard'))
    return render_template('add_inventory.html')

@bp.route('/resource/add/<asset_no>', methods=['GET', 'POST'])
def add_resource(asset_no):
    if request.method == 'POST':
        vcpu = request.form['vcpu']
        ram = request.form['ram']
        private_ip = request.form['private_ip']
        public_ip_enabled = request.form.get('public_ip_enabled') == 'yes'
        public_ip = request.form['public_ip'] if public_ip_enabled else None

        resource = Resource(
            asset_no=asset_no,
            vcpu=vcpu,
            ram=ram,
            private_ip=private_ip,
            public_ip_enabled=public_ip_enabled,
            public_ip=public_ip
        )
        db.session.add(resource)
        db.session.flush()  # Get resource.id before commit

        storage_types = request.form.getlist('storage_type[]')
        storage_sizes = request.form.getlist('storage_size[]')
        for stype, ssize in zip(storage_types, storage_sizes):
            db.session.add(Storage(
                resource_id=resource.id,
                storage_type=stype,
                storage_size=int(ssize)
            ))

        db.session.commit()
        return redirect(url_for('routes.dashboard'))

    return render_template('add_resource.html', asset_no=asset_no)

# --- Admin Routes ---
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
