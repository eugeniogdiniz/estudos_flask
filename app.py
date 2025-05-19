from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from utils.utils import get_mysql_connection

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
            return redirect(url_for("home"))
        else:
            flash("Email ou senha incorretos!", "danger")

    return render_template("auth/login.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/sistemas')
def sistemas():
    return render_template('base.html')

@app.route('/helpdesk')
def helpdesk    ():
    return render_template('base.html')

@app.route('/contratos')
def contratos():
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT c.idContrato, c.Numero_Contrato, cli.Cliente, c.Nome_Consorcio, c.Data_Assinatura
    FROM CONT_REG_Contrato c
    LEFT JOIN CONT_CAD_Cliente cli ON c.idCliente = cli.idCliente
    ORDER BY c.Data_Assinatura DESC
    LIMIT 100
    """

    cursor.execute(query)
    contratos = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('contato.html', contratos=contratos)

@app.route('/contratos/edit/<idContrato>', methods=['GET', 'POST'])
def editar_contrato(idContrato):
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        numero_contrato = request.form.get('Numero_Contrato')
        nome_consorcio = request.form.get('Nome_Consorcio')
        id_cliente = request.form.get('idCliente')

        update_sql = """
        UPDATE CONT_REG_Contrato SET Numero_Contrato = %s, Nome_Consorcio = %s, idCliente = %s
        WHERE idContrato = %s
        """
        cursor.execute(update_sql, (numero_contrato, nome_consorcio, id_cliente, idContrato))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Contrato atualizado com sucesso!", "success")
        return redirect(url_for('contratos'))

    # GET
    cursor.execute("SELECT * FROM CONT_REG_Contrato WHERE idContrato = %s", (idContrato,))
    contrato = cursor.fetchone()

    cursor.execute("SELECT idCliente, Cliente FROM CONT_CAD_Cliente")
    clientes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('editarcontrato.html', contrato=contrato, clientes=clientes)


@app.route('/customers') 
def customers():
    return render_template('base.html')

# Inicialização do banco de dados
def init_db():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    init_db()  # Cria o banco de dados antes de rodar
    app.run(debug=True)