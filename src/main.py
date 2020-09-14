"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Contact, Subscription, Group
#from models import db, User, Contact
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

####################        Formal API Documentation    #######################  
#####  1.-Obtenga una lista de todos los contactos GET /contact/all  #########

@app.route('/contact/all', methods=["GET"])

def getAllContact():
    if request.method == "GET":
        contact = Contact.query.all()
        contact_list = list(map(lambda contact: contact.serialize(), contact))
        return jsonify(contact_list), 200
    else:
        response_body = {
            "msj":"Metodo request invalido"
        }
        return jsonify(response_body), 400


##########  2.- Crear un nuevo Contacto POST /contact ########### 

@app.route('/contact', methods=["GET", "POST",])
def add_contact():
    if request.method == "POST":  
     body = request.get_json()
     contact = Contact(full_name=body['full_name'], email=body['email'], address=body['address'], phone=body['phone'])
     db.session.add(contact)
   #  db.session.commit()
    # print(contact)
    #return jsonify(contact.serialize()), 200   

    try:
        db.session.commit()
        # devolvemos el nuevo donante serializado y 200_CREATED
        return jsonify(contact.serialize()), 200
    except Exception as error:
        db.session.rollback()
        print(f"{error.args} {type(error)}")
        # devolvemos "mira, tuvimos este error..."
        return jsonify({
            "Presenete error": f"{error.args}"
        }), 500


##########  3.- Obtener un Contacto específico (con los objetos del grupo al                    que pertenece) GET /contact/{contact_id} ###########  

@app.route('/contact/<int:contact_id>', methods=["GET"])
def getSpecificContact(contact_id):

    if request.method == "GET":
        contact = Contact.query.filter(Contact.id == contact_id)
        contact_list = list(map(lambda contact: contact.serialize(), contact))

        if contact_list == []:
            msj="no se encontro el contacto ingresado"
            return jsonify(msj), 200
        else:
            return jsonify(contact_list), 200
    else:
            response_body = {"msj":"Metodo invalido request"}
            return jsonify(response_body), 400

##########  4.- Eliminar un Contacto DELETE /contact/{contact_id} ########### 

@app.route('/delete/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    contact = Contact.query.get(contact_id)
    if contact is None:
        raise APIException('Contacto no encontrado', status_code=404)
   # db.session.delete(contact)
  #  db.session.commit()
   # response_body = {
    #    "msg": "El contacto a sido eliminado"
    #}
    #return jsonify(response_body), 200

    else:
        # remover el donante específico de la sesión de base de datos
        db.session.delete(contact)
        # hacer commit y devolver 204
        try:
            db.session.commit()
            response_body = {
           "msg": "El contacto a sido eliminado"
           }
            return jsonify(response_body), 200
        except Exception as error:
            db.session.rollback()
            print(f"{error.args} {type(error)}")
            return jsonify({
                "resultado": f"{error.args}"
            }), 500


##########  5.- Actualiza el Contacto UPDATE /contact/{contact_id} ###########     
@app.route('/contact/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    body = request.get_json()
    contact = Contact.query.get(contact_id)
    if contact is None:
        raise APIException('Contacto no encontrado', status_code=404)

    if "full_name" in body:
        contact.full_name = body["full_name"]
    if "email" in body:
        contact.email = body["email"]
    if "address" in body:
        contact.address = body['address']
    if "phone" in body:
        contact.phone = body['phone']
  # db.session.commit()
   # return jsonify(contact.serialize()), 200

    try:
        db.session.commit()
        # devolvemos el nuevo donante serializado y 200_CREATED
        return jsonify(contact.serialize()), 200
    except Exception as error:
        db.session.rollback()
        print(f"{error.args} {type(error)}")
        # devolvemos "mira, tuvimos este error..."
        return jsonify({
            "Presenete error": f"{error.args}"
        }), 500    

##########  6.- Obtener una lista de todos los nombres e IDs del grupo                          GET /group/all ###########  

@app.route('/group/all', methods=["GET"])

def getAllGroup():
    if request.method == "GET":
        group = Group.query.all()
        group_list = list(map(lambda group: group.serialize(), group))
        return jsonify(group_list), 200
    else:
        response_body = {
            "msj":"Metodo invalido request"
        }
        return jsonify(response_body), 400
    
##########  7.- Crea un nuevo Grupo POST /group  ###########  
   
@app.route('/group', methods=['POST'])
def add_group():
    body = request.get_json()
    group = Group(name=body['name'])
    db.session.add(group)
  #  db.session.commit()
  #  print(group)
  #  return jsonify(group.serialize()), 200   

    try:
        db.session.commit()
        # devolvemos el nuevo donante serializado y 200_CREATED
        return jsonify(group.serialize()), 200
    except Exception as error:
        db.session.rollback()
        print(f"{error.args} {type(error)}")
        # devolvemos "mira, tuvimos este error..."
        return jsonify({
            "Presenete error": f"{error.args}"
        }), 500
 
 ##########  8.- Obtener un grupo específico (con todos los objetos de contacto relacionados con él) GET /group/{group_id}  ###########  

@app.route('/group/<int:group_id>', methods=["GET"])
def getSpecificGroup(group_id):

    if request.method == "GET":
        group = Group.query.filter(Group.id == group_id)
        group_list = list(map(lambda group: group.serialize(), group))

        if group_list == []:
            msj="No se encontro el grupo ingresado"
            return jsonify(msj), 200
        else:
            return jsonify(group_list), 200
    else:
            response_body = {"msj":"Metodo invalido request"}
            return jsonify(response_body), 400

 ####  9.- Actualizar el nombre de grupo UPDATE /group/{group_id}  ######  

@app.route('/group/<int:group_id>', methods=['PUT'])
def update_group(group_id):
    body = request.get_json()
    group = Group.query.get(group_id)
    if group is None:
        raise APIException('grupo no ha sido añadido', status_code=404)

    if "name" in body:
        group.name = body["name"]
  #  db.session.commit()
   # return jsonify(group.serialize()), 200

    try:
        db.session.commit()
        # devolvemos el nuevo donante serializado y 200_CREATED
        return jsonify(group.serialize()), 200
    except Exception as error:
        db.session.rollback()
        print(f"{error.args} {type(error)}")
        # devolvemos "mira, tuvimos este error..."
        return jsonify({
            "Presenete error": f"{error.args}"
        }), 500        

 ####  10.- Elimina un Grupo DELETE /group/{group_id}  ######  

@app.route('/group/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    group = Group.query.get(group_id)
    if group is None:
        raise APIException('grupo no ha sido encontrado', status_code=404)
   # db.session.delete(group)
   # db.session.commit()
    #response_body = {
     #   "msg": "El grupo ha sido eliminado"
    #}
    #return jsonify(response_body), 200

    else:
        # remover el donante específico de la sesión de base de datos
        db.session.delete(group)
        # hacer commit y devolver 204
        try:
            db.session.commit()
            response_body = {
           "msg": "El grupo a sido eliminado"
           }
            return jsonify(response_body), 200
        except Exception as error:
            db.session.rollback()
            print(f"{error.args} {type(error)}")
            return jsonify({
                "resultado": f"{error.args}"
            }), 500



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)