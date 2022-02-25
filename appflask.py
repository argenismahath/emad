from distutils.log import debug
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os




app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
ma=Marshmallow(app)


class Employe(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    age=db.Column(db.Integer)
    salary=db.Column(db.Integer)

    def __init__(self, name, age, salary):
        self.name=name
        self.age=age
        self.salary=salary

db.create_all()

class EmployeE(ma.Schema):
    class Meta:
        fields=('id','name','age','salary')

Employe_schema=EmployeE()
Employes_schema=EmployeE(many=True)

# ---------------------- A P I --------------------------

@app.route('/')
def inicio():
    return render_template('inicio.html')

# --------------------- G E T --------------------------

@app.route('/empleados', methods=['GET'])
def get_empleados():
    all_empleados=Employe.query.all()
    result=Employes_schema.dump(all_empleados)
    return jsonify(result)

# -------------------------------- P O S T --------------------------

@app.route('/empleado/nuevo', methods=['POST'])
def empleados():
    name_empleado= request.json['name']
    age_empleado= request.json['age']
    salary_empleado= request.json['salary']

    new_empleado=Employe(name_empleado, age_empleado, salary_empleado)
    db.session.add(new_empleado)
    db.session.commit()
    
    print(request.json)
    return render_template('añadir.html')

# ---------------------------------- P U T --------------------------
@app.route('/empleado/actualizar/byid/<id>', methods=['GET', 'POST', 'PUT'])
def mostrar(id):
    empleado=Employe.query.get(id)
  
    return render_template('actualizar.html', empleado=empleado)


@app.route('/empleados/actualizar/<int:id>', methods=['PUT', 'GET'])
def actualizar_empleado(id):
    empleado=Employe.query.get(id)
    print(empleado.id)
    
    empleado.name=request.json['name']
    empleado.age=request.json['age']
    empleado.salary=request.json['salary']
    db.session.commit()
    return render_template('lista.html', empleado=empleado)

# --------------------------- D E L E T E ----------------------------

@app.route('/empleados/eliminar/<string:name>', methods=['DELETE'])
def borrar_empleado():
    name_empleado=request.json['name']
    empleado=Employe.query.filter_by(name=name_empleado).first()
    db.session.delete(empleado)
    db.session.commit()
    return jsonify('Empleado eliminado')

# --------------------------mostar lista de empleados --------------------------

@app.route('/empleados/lista', methods=['GET', 'POST'])
def lista_empleados():
    empleados=Employe.query.all()
    return render_template('lista.html', empleados=empleados)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int(os.environ.get('PORT',8080)))
