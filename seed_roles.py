from app import create_app, db
from app.models import Role

app = create_app()

with app.app_context():
    roles_to_create = ['Admin', 'User']
    for role_name in roles_to_create:
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            db.session.add(Role(name=role_name))
            print(f"Created role: {role_name}")
        else:
            print(f"Role already exists: {role_name}")
    db.session.commit()
    print("Done seeding roles.")