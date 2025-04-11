import os
from app import create_app, db
from app.models import User, Employee, Department, Position, Leave, Project, Task, ProjectAssignment
from flask_migrate import Migrate

# Yapılandırma ortamını belirle
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    """Flask shell için otomatik içe aktarmalar"""
    return dict(
        app=app, db=db, User=User, Employee=Employee,
        Department=Department, Position=Position,
        Leave=Leave, Project=Project, Task=Task, ProjectAssignment=ProjectAssignment
    )

@app.cli.command("create-admin")
def create_admin():
    """Admin kullanıcısı oluştur"""
    from app.models import ROLE_ADMIN
    
    admin_email = input("Admin e-posta adresi: ")
    admin_password = input("Admin şifresi: ")
    admin_first_name = input("Admin adı: ")
    admin_last_name = input("Admin soyadı: ")
    
    user = User.query.filter_by(email=admin_email).first()
    if user:
        print(f"Bu e-posta adresi ({admin_email}) zaten kullanımda!")
        return
    
    user = User(
        email=admin_email,
        password=admin_password,
        first_name=admin_first_name,
        last_name=admin_last_name,
        role=ROLE_ADMIN
    )
    db.session.add(user)
    db.session.commit()
    print(f"Admin kullanıcısı oluşturuldu: {admin_email}")

if __name__ == '__main__':
    app.run(debug=True) 