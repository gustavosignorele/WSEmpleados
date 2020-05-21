from flask import Flask, jsonify, Response, request
import json

app = Flask(__name__)


@app.route("/hello")
def hello():
    return "Hello World! Flaskeando!"


# el GET es el verbo por defecto
@app.route('/empleados')
def lista_empleados():
    ''' apertura del archivo '''
    try:
        file = open("datos/datos_empleados.txt")
        lista_empleados = file.readlines()
        lista_retorno = []
        for emp in lista_empleados:
            fragments = emp.split("|")
            # sacamos los saltos de linea de cada elemento de la lista
            fragments = list(map(str.strip, fragments))
            empleado = {}
            empleado["ci"] = fragments[0]
            empleado["nombre"] = fragments[1]
            empleado["estado"] = fragments[2]
            lista_retorno.append(empleado)

        # si no hay datos, devolvemos 204 = no content
        if len(lista_retorno) == 0:
            return Response(None, status=204)

        # 200 es el valor por defecto, igualmente lo explicitamos
        return jsonify(lista_retorno), 200
    # si hay un error, devolvemos 500 = Internal server error
    # junto a un json para especificar los mensajes de error
    except Exception as e:
        error_retorno = {"message": str(e)}
        return jsonify(error_retorno), 500


@app.route('/empleados/<ci>')
def un_empleado(ci):
    return "empleado a devolver tiene la ci:{}".format(ci)


@app.route('/empleados', methods=['POST'])
def agregar_empleado():
    # obtener el json del body
    try:
        data_input = request.json
        # obtenemos los datos del json que envian. Si falla, 400: Bad request

        ci = data_input['ci']
        nombre = data_input['nombre']
        # aca debemos chequear si estado tiene el valor "aprobado" o "reprobado"
        estado = data_input['estado']
        if estado!="aprobado" and estado!="reprobado":
            error_retorno = {"message": "El campo estado solo admite 2 valores: aprobado y reprobado"}
            return jsonify(error_retorno), 400
    except Exception as e:
        error_retorno = {"message": str(e)}
        return jsonify(error_retorno), 400

    try:

        ''' apertura del archivo '''
        file = open("datos/datos_empleados.txt", "r")
        ''' obtenemos las todas las lineas del archivo 
            y las reccoremos para verificar CI '''
        lista_empleados = file.readlines()
        for emp in lista_empleados:
            cedula_identidad = emp.split("|")[0]
            print (cedula_identidad)
            print(ci)

            if (cedula_identidad == ci):
                ''' existe el empleado:  
                    devuelvo el codigo de error 400 (bad request) '''
                return jsonify({"mensaje": "Ya existe el empleado/a con la ci {}".format(ci)}), 400

        # fin de recorrida de archivo. Si llegamos hasta aca, la CI no estaba.
        # vamos a agregar el empleado con los datos de entrada
        file.close()
        file = open("datos/datos_empleados.txt", "a")
        file.write("{}|{}|{}\n".format(ci, nombre, estado))
        file.close()

        #  status_code 201 - created
        return Response(None, status=201)

    except Exception as e:
        error_retorno = {"message": str(e)}
        return jsonify(error_retorno), 500



@app.route('/empleados/<ci>',  methods=['PUT'])
def actualizar_empleado(ci):
    return "empleado a actualizar tiene la ci:{}".format(ci)


@app.route('/empleados/<ci>',  methods=['DELETE'])
def borrar_empleado(ci):
    return "empleado a borrar tiene la ci:{}".format(ci)
