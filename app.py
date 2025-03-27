from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configurações devem vir antes da inicialização do banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "sua-chave-secreta-aqui"  # Importante para segurança!

db = SQLAlchemy(app)

# Modelo de Usuário
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Senha criptografada

    def __repr__(self):
        return f"<User {self.email}>"

# Rotas
# @app.route("/")
# def home():
#     return render_template("index.html")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Verifica se o usuário existe
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Email ou senha incorretos!", "danger")

    return render_template("auth/login.html")

@app.route('/dashboard')
def dashboard():
    return "<h1>Bem-vindo ao Dashboard!</h1>"

# Inicialização do banco de dados
def init_db():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    init_db()  # Cria o banco de dados antes de rodar
    app.run(debug=True)