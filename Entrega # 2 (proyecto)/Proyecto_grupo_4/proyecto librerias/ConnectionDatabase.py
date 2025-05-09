import pyodbc
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth 

app = Flask(__name__)
auth = HTTPBasicAuth()

def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=xxxxx;'  
        'DATABASE=Librerias;'
        'UID=sa;'
        'PWD=******;'
        'TrustServerCertificate=yes;'
    )
    return conn

usuarios ={
    "Maria_Gomez":"2025",
    "Carlos_Rodriguez":"2024",
    "Laura_Fernandez":"2023",
    "Pedro_Sanchez":"2022",
    "Ana_Martinez":"2021"
}

@auth.verify_password
def verify_password(usuario, contraseña):
    if usuario in usuarios and usuarios[usuario] == contraseña:
        return usuario
    return None

@app.route('/Recursos', methods=['GET'])
@auth.login_required
def obtener_recursos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('select * from Recursos')
    recursos = cursor.fetchall()
    conn.close()
    return jsonify(
        [
            {
                'codigoRecurso': recurso[0],
                'nombre': recurso[1],
                'estado': recurso[2]
            
            }for recurso in recursos
        ]
    )

if __name__ == '__main__':
    app.run(port=5000, debug=True)
