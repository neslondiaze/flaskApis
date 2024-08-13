from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

from config import config
from validaciones import validar_codigo, validar_nombre, validar_creditos

app = Flask(__name__)

# CORS(app)
CORS(app, resources={r"/cursos/*": {"origins": "http://localhost"}})

conexion = MySQL(app)

# --------> CURSOS
# Listar todos los cursos
@app.route('/cursos', methods=['GET'])
def listar_cursos():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT codigo, nombre, creditos FROM curso ORDER BY nombre ASC"
        cursor.execute(sql)
        datos = cursor.fetchall()
        cursos = []
        for fila in datos:
            curso = {'codigo': fila[0], 'nombre': fila[1], 'creditos': fila[2]}
            cursos.append(curso)
        return jsonify({'cursos': cursos, 'mensaje': "Cursos listados.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})

# Leer curso por codigo
def leer_curso_bd(codigo):
    try:
       cursor = conexion.connection.cursor()
       sql = "SELECT codigo, nombre, creditos FROM curso WHERE codigo = '{0}'".format(codigo)
       cursor.execute(sql)
       datos = cursor.fetchone()
       if datos is not None:
           curso = {'codigo': datos[0], 'nombre': datos[1], 'creditos': datos[2]}
           return curso
       else:
           return None
    except Exception as ex:
        raise ex

# Leer curso por codigo GET
@app.route('/cursos/<codigo>', methods=['GET'])
def leer_curso(codigo):
    try:
        curso = leer_curso_bd(codigo)
        if curso is not None:
            return jsonify({'curso': curso, 'mensaje': "Curso encontrado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Curso no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})

# Agregar curso
@app.route('/cursos', methods=['POST'])
def registrar_curso():
    if (validar_codigo(request.json['codigo']) and validar_nombre(request.json['nombre']) and validar_creditos(request.json['creditos'])):
        try:
            curso = leer_curso_bd(request.json['codigo'])
            if curso is not None:
                return jsonify({'mensaje': "Código ya existe, no se puede duplicar.", 'exito': False})
            else:
                cursor = conexion.connection.cursor()
                sql = """INSERT INTO curso (codigo, nombre, creditos) 
                VALUES ('{0}', '{1}', {2})""".format(request.json['codigo'],
                                                     request.json['nombre'], request.json['creditos'])
                cursor.execute(sql)
                conexion.connection.commit()  # Confirma la acción de inserción.
                return jsonify({'mensaje': "Curso registrado.", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})
    else:
        return jsonify({'mensaje': "Parámetros inválidos...", 'exito': False})

# Actualizar curso
@app.route('/cursos/<codigo>', methods=['PUT'])
def actualizar_curso(codigo):
    if (validar_codigo(codigo) and validar_nombre(request.json['nombre']) and validar_creditos(request.json['creditos'])):
        try:
            curso = leer_curso_bd(codigo)
            if curso is not None:
                cursor = conexion.connection.cursor()
                sql = """UPDATE curso SET nombre = '{0}', creditos = {1} 
                WHERE codigo = '{2}'""".format(request.json['nombre'], request.json['creditos'], codigo)
                cursor.execute(sql)
                conexion.connection.commit()  # Confirma la acción de inserción.
                return jsonify({'mensaje': "Curso actualizado.", 'exito': True})
            else:
                return jsonify({'mensaje': "Curso no encontrado.", 'exit': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})
    else:
        return jsonify({'mensaje': "Parámetros inválidos...", 'exito': False})

# Eliminar curso
@app.route('/cursos/<codigo>', methods=['DELETE'])
def eliminar_curso(codigo):
    try:
        curso = leer_curso_bd(codigo)
        if curso is not None:
            cursor = conexion.connection.cursor()
            sql = "DELETE FROM curso WHERE codigo = '{0}'".format(codigo)
            cursor.execute(sql)
            conexion.connection.commit()  # Confirma la acción de eliminación.
            return jsonify({'mensaje': "Curso eliminado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Curso no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})

# --------> USUARIOS
# Leer usuarisos por username
def leer_user_bd(user_name):
    try:
        cursor = conexion.connection.cursor()
        sql  = "SELECT id, username, fullname  FROM user WHERE username = '{0}'".format(user_name)
        print(sql)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos is not None:
            user = {'id': datos[0], 'username': datos[1], 'fullname': datos[2]}
            return user
        else:
            return None
    except Exception as ex:
        raise ex

# Listar un usuarios
@app.route('/user', methods=['GET'])
def listar_user():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id, username, fullname FROM user ORDER BY username ASC"
        cursor.execute(sql)
        datos = cursor.fetchall()
        users = []
        for fila in datos:
            user = {'id': fila[0], 'username': fila[1], 'fullname': fila[2]}
            users.append(user)
        return jsonify({'users': user, 'mensaje': "Usuarios listados.", 'exit': True})

    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exti': False})

# Leer usuario por username
@app.route('/user/<username>', methods=['GET'])
def leer_username(username):
    try:
        user = leer_user_bd(username)
        if user is not None:
            return jsonify({'user': user, 'mensaje': "Usuario encontrado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Usuario no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})

# Agregar usuarios
@app.route('/user', methods=['POST'])

# --------> Funciones Generales
# Pagina no encontrada
def pagina_no_encontrada(error):
    return "<h1>Página no encontrada</h1>", 404

# Inicia aplicacion
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()