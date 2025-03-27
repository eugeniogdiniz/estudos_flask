from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurações devem vir antes da inicialização do banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "sua-chave-secreta-aqui"  # Importante para segurança!

db = SQLAlchemy(app)

class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __repr__(self):
        return f"<Mensagem {self.nome}>"

# Rotas
# @app.route("/")
# def home():
#     return render_template("index.html")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lógica de autenticação aqui
        return redirect(url_for('dashboard'))
    return render_template('auth/login.html')

@app.route("/sobre")
def sobre():
    return "<h2>Sobre Nós</h2>"

@app.route("/contato", methods=["GET", "POST"])
def contato():
    if request.method == "POST":
        nova_mensagem = Mensagem(
            nome=request.form.get("nome"),
            email=request.form.get("email")
        )
        db.session.add(nova_mensagem)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("contato.html")

# Inicialização do banco de dados
def init_db():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    init_db()  # Cria o banco de dados antes de rodar
    app.run(debug=True)