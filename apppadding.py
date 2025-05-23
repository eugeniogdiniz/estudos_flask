from flask import Flask, render_template, request, redirect, url_for, flash, session
from utils.utils import get_mysql_connection

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index_padding.html')

@app.route('/home')
def home():
    return render_template("home.html")

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


if __name__ == '__main__':
    app.run(debug=True)
