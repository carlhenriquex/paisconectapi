from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
import bcrypt
from datetime import datetime, date, time, timedelta

hoje = datetime.now()
data_atual = hoje.year
print(data_atual)

app = Flask(__name__)
CORS(app)  # conexão do FlutterFlow

# CONEXAO AO BANCO DE DADOS MYSQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="escola_db"
)

@app.route("/")
def home():
    return "Hello world! A API ESTÁ RODANDO!"

# ENDPOINT PARA VALIDAR LOGIN E SENHA
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    matricula = data.get("matricula")
    senha = data.get("senha")

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alunos WHERE matricula = %s", (matricula,))
    user = cursor.fetchone()
    cursor.close()

    if not user:
        return jsonify({"mensagem": "Usuário inválido!"}), 404

    # Verifica a senha com hash bcrypt (passwordhash PHP)
    if bcrypt.checkpw(senha.encode("utf-8"), user["senha"].encode("utf-8")):
        return jsonify({
            "success": True,
            "id": user["id"],
            "nome": user["nome"]
        })
    else:
        return jsonify({"mensagem": "Senha incorreta."}), 401

# ENDPOINT PARA VER TODOS OS DADOS DE ENTRADAS, COMUNICADOS, PORCENTAGEM DE PRESENÇA E STATUS DO DIA SALVOS NO BANCO
@app.route("/dados/<int:aluno_id>", methods=["GET"])
def dados(aluno_id):

    mes = request.args.get("mes", type=int)

    dados = {
        "entradas" : [],
        "comunicados" : [],
        "presenca": 0,
        "status_hoje": "Ainda em registro hoje"
    }

    # === comunicados ===
    cursor = db.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM comunicados WHERE YEAR(data_publicacao) = {data_atual} ORDER BY data_publicacao DESC")

    comunicados = cursor.fetchall()

    # === entradas ===
    if mes:
        cursor.execute(
            """
            SELECT * FROM entradas
            WHERE aluno_id = %s AND MONTH(data) = %s
            """,
            (aluno_id, mes)
        )
    else:
        cursor.execute(
            """
            SELECT * FROM entradas
            WHERE aluno_id = %s
            """,
            (aluno_id,)
        )

    entradas = cursor.fetchall()

    # === porcentagem de presença ===

    if mes:
        cursor.execute(
            """
            SELECT ROUND((SUM(CASE WHEN status = 'presente' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2)
            AS porcentagem_presenca
            FROM entradas
            WHERE aluno_id = %s AND MONTH(data) = %s
            """,
            (aluno_id, mes)
        )
    else:
        cursor.execute(
            """
            SELECT ROUND((SUM(CASE WHEN status = 'presente' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2)
            AS porcentagem_presenca
            FROM entradas
            WHERE aluno_id = %s
            """,
            (aluno_id,)
        )

    presenca = cursor.fetchone()["porcentagem_presenca"] or 0

    cursor.close()

    # === converção dos dados do tipo datetime p/ string ===
    def converter_para_str(obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        
        if isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        
        if isinstance(obj, time):
            return obj.strftime("%H:%M:%S")
        
        if isinstance(obj, timedelta):
            return str(obj)

        return obj

    for lista in [entradas, comunicados]:
        for item in lista:
            for chave, valor in item.items():
                item[chave] = converter_para_str(valor)

    # === status do dia ===
    hoje_date = datetime.now().date()

    cursor.execute(
        """
        SELECT status
        FROM entradas
        WHERE aluno_id = %s AND DATE(data) = %s
        """,
        (aluno_id, hoje_date)
    )

    registro_hoje = cursor.fetchone()

    if registro_hoje:
        status_hoje = registro_hoje["status"]
    else:
        status_hoje = "Ainda sem registro hoje"

    # === Salvando dados no json ===
    dados["comunicados"] = comunicados
    dados["entradas"] = entradas
    dados["presenca"] = presenca
    dados["status_hoje"] = status_hoje

    return jsonify(dados)

if __name__ == "__main__":
    app.run(debug= True, host="0.0.0.0")