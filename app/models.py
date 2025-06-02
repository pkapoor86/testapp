from app import db
import hashlib

class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))

    def set_password(self, password):
        self.password = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password == hashlib.sha256(password.encode()).hexdigest()

    def get_roles(self):
        return [role.name for role in self.roles]

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_no = db.Column(db.String(100), unique=True, nullable=False)
    asset_name = db.Column(db.String(255), nullable=False)
    creation_date = db.Column(db.DateTime, server_default=db.func.now())
    resources = db.relationship('Resource', backref='inventory', lazy=True)

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_no = db.Column(db.String(100), db.ForeignKey('inventory.asset_no'), nullable=False)
    vcpu = db.Column(db.Integer, nullable=False)
    ram = db.Column(db.String(50), nullable=False)
    public_ip_enabled = db.Column(db.Boolean, default=False)
    public_ip = db.Column(db.String(45))
    private_ip = db.Column(db.String(45), nullable=False)
    storages = db.relationship('Storage', backref='resource', cascade="all, delete", lazy=True)

class Storage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'), nullable=False)
    storage_type = db.Column(db.String(50), nullable=False)
    storage_size = db.Column(db.Integer, nullable=False)

user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)