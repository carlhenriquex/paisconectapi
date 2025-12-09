from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
import bcrypt
from datetime import datetime, date, time

app = Flask(__name__)
CORS(app)

# === CONEXÃO AO BANCO ===
def get_db_connection():
    try:
        return mysql.connector.connect(
            host= "69.6.212.194",
            user="esco6819_api_intelbras",
            password="6WGTaYjQwfMBvlE",
            database="esco6819_admin_paiconect"
        )
    except mysql.connector.Error as erro:
        print("Erro ao conectar ao banco:", erro)
        return None
    
# def get_db_connection():
#     try:
#         return mysql.connector.connect(
#             host= "localhost",
#             user="root",
#             password="",
#             database="escola_db"
#         )
#     except mysql.connector.Error as erro:
#         print("Erro ao conectar ao banco:", erro)
#         return None

# === HOME ===
@app.route("/")
def home():
    return "API rodando!"


# === LOGIN ===
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"erro": "JSON inválido"}), 400

        matricula = data.get("matricula")
        senha = data.get("senha")

        if not matricula or not senha:
            return jsonify({"erro": "Campos obrigatórios faltando"}), 400

        db = get_db_connection()
        if not db:
            return jsonify({"erro": "Falha na conexão com o banco"}), 500

        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM alunos WHERE matricula = %s", (matricula,))
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if not user:
            return jsonify({"erro": "Usuário não encontrado"}), 404

        if not bcrypt.checkpw(senha.encode("utf-8"), user["senha"].encode("utf-8")):
            return jsonify({"erro": "Senha incorreta"}), 401

        return jsonify({
            "success": True,
            "id": user["id"],
            "nome": user["nome"]
        })

    except Exception as e:
        print("Erro no login:", e)
        return jsonify({"erro": "Erro interno no servidor"}), 500


# === DADOS DO ALUNO ===
@app.route("/dados/<int:aluno_id>", methods=["GET"])
def dados(aluno_id):

    try:
        mes = request.args.get("mes", type=int)
        ano_atual = datetime.now().year
        hoje_date = datetime.now().date()
        hora_atual = datetime.now().time()

        resultado = {
            "entradas": [],
            "comunicados": [],
            "presenca": 0,
            "statusHoje": []
        }

        db = get_db_connection()
        if not db:
            return jsonify({"erro": "Falha ao conectar ao banco"}), 500

        # === COMUNICADOS ===
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, titulo, imagem_url AS imagemUrl, conteudo AS descricao, data_publicacao AS dataComunicado
            FROM comunicados
            WHERE YEAR(data_publicacao) = %s
            ORDER BY data_publicacao DESC
        """, (ano_atual,))
        comunicados = cursor.fetchall()
        cursor.close()

        # === ENTRADAS DO ALUNO ===
        cursor = db.cursor(dictionary=True)

        if mes and (mes != 0):
            cursor.execute("""
                SELECT id, status, data AS dataEntrada, hora AS horaEntrada
                FROM entradas
                WHERE aluno_id = %s AND MONTH(data) = %s
                ORDER BY data DESC, hora DESC
            """, (aluno_id, mes))
        else:
            cursor.execute("""
                SELECT id, status, data AS dataEntrada, hora AS horaEntrada
                FROM entradas
                WHERE aluno_id = %s
                ORDER BY data DESC, hora DESC
            """, (aluno_id,))

        entradas = cursor.fetchall()
        cursor.close()

        # === CALCULAR PORCENTAGEM DE PRESENÇA ===
        presentes = sum(1 for entrada in entradas if entrada["status"] == "presente" or entrada["status"] == "atraso")
        total = len(entradas)

        presenca = round((presentes / total) * 100, 2) if total > 0 else 0

        # === STATUS DO DIA ===
        entrada_hoje = next((entrada for entrada in entradas if entrada["dataEntrada"] == hoje_date), None)

        if entrada_hoje:
            status_hoje = [
                {
                    "status": entrada_hoje["status"],
                    "dataStatus": entrada_hoje["dataEntrada"],
                    "horaStatus": entrada_hoje["horaEntrada"],
                    "descricao": f"ola mundo, {entrada_hoje['status']}"
                }
            ]

        else:
            status_hoje = [
                {
                    "status": "Sem registro",
                    "dataStatus": hoje_date,
                    "horaStatus": hora_atual,
                    "descricao": "Ainda sem registro hoje"
                }
            ]

        # === CONVERTER DATAS ===
        def formatar(valor):
            if valor is None:
                return None
            if isinstance(valor, datetime):
                return valor.strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(valor, date):
                return valor.strftime("%Y-%m-%d")
            if isinstance(valor, time):
                return valor.strftime("%H:%M:%S")
            return str(valor)

        for item in entradas:
            item["dataEntrada"] = formatar(item["dataEntrada"])
            item["horaEntrada"] = formatar(item["horaEntrada"])

        for item in comunicados:
            item["dataComunicado"] = formatar(item["dataComunicado"])

        for item in status_hoje:
            item["dataStatus"] = formatar(item["dataStatus"])
            item["horaStatus"] = formatar(item["horaStatus"])

        # === FINALIZA CURSOR DE BUSCA E SALVA NO JSON ===
        cursor.close()
        db.close()

        resultado["entradas"] = entradas
        resultado["comunicados"] = comunicados
        resultado["presenca"] = presenca
        resultado["statusHoje"] = status_hoje

        return jsonify(resultado)

    except Exception as e:
        print("Erro no endpoint /dados:", e)
        return jsonify({"erro": "Erro interno no servidor"}), 500


# === RUN ===
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")