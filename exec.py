from app import app, db, User  # Certifique-se de importar 'app'

from werkzeug.security import generate_password_hash

# Criar usuário de teste
email = "teste@email.com"
password = "123456"

hashed_password = generate_password_hash(password)

# Criar usuário dentro do contexto da aplicação Flask
with app.app_context():  # Agora usamos 'app' corretamente
    novo_usuario = User(email=email, password=hashed_password)
    db.session.add(novo_usuario)
    db.session.commit()

print("Usuário criado com sucesso!")
