from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
db = SQLAlchemy(app)

# Modelos de la base de datos
class Estudiante(db.Model):
    codigoEstudiante = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    direccion = db.Column(db.String(255))
    prestamos = db.relationship('Prestamo', backref='estudiante', lazy=True)

class Recurso(db.Model):
    codigoRecurso = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    estado = db.Column(db.String(50))
    prestamos = db.relationship('Prestamo', backref='recurso', lazy=True)

class Prestamo(db.Model):
    codigoPrestamo = db.Column(db.Integer, primary_key=True)
    codigoEstudiante = db.Column(db.Integer, db.ForeignKey('estudiante.codigoEstudiante'))
    codigoRecurso = db.Column(db.Integer, db.ForeignKey('recurso.codigoRecurso'))
    fechaPrestamo = db.Column(db.DateTime)
    fechaDevolucion = db.Column(db.DateTime)
    estadoPrestamo = db.Column(db.String(50))

# Función para inicializar datos
with app.app_context():
    db.create_all()
    
    # Verificar si ya existen datos
    if not Estudiante.query.first():
        # Estudiantes
        estudiantes = [
            Estudiante(
                codigoEstudiante=1012345678,
                nombre='María Gómez',
                telefono='3105678901',
                email='maria.gomez@email.com',
                direccion='Carrera 45 #12-34, Bogotá'
            ),
            Estudiante(
                codigoEstudiante=1009876543,
                nombre='Carlos Rodríguez',
                telefono='3209876543',
                email='carlos.rodriguez@email.com',
                direccion='Avenida caracas 742, Bogotá'
            ),
            Estudiante(
                codigoEstudiante=1034567890,
                nombre='Laura Fernández',
                telefono='3006547890',
                email='laura.fernandez@email.com',
                direccion='Calle 56 #78-90, Bogotá'
            ),
            Estudiante(
                codigoEstudiante=1023456789,
                nombre='Pedro Sánchez',
                telefono='3113456789',
                email='pedro.sanchez@email.com',
                direccion='Transversal 23 #45-67, Bogotá'
            ),
            Estudiante(
                codigoEstudiante=1045678901,
                nombre='Ana Martínez',
                telefono='3222345678',
                email='ana.martinez@email.com',
                direccion='Diagonal 12 #34-56, Bogotá'
            )
        ]
        db.session.add_all(estudiantes)
        
        # Recursos
        recursos = [
            Recurso(
                codigoRecurso=201,
                nombre='Aprendiendo Python - Mark Lutz',
                estado='Disponible'
            ),
            Recurso(
                codigoRecurso=202,
                nombre='Fundamentos de Bases de Datos - Elmasri & Navathe',
                estado='Disponible'
            ),
            Recurso(
                codigoRecurso=203,
                nombre='Inteligencia Artificial: Un Enfoque Moderno - Stuart Russell y Peter Norvig',
                estado='Disponible'
            ),
            Recurso(
                codigoRecurso=204,
                nombre='Redes de Computadoras - Andrew S. Tanenbaum',
                estado='Disponible'
            ),
            Recurso(
                codigoRecurso=205,
                nombre='Seguridad Informática: Principios y Prácticas - William Stallings',
                estado='Disponible'
            )
        ]
        db.session.add_all(recursos)
        
        db.session.commit()
        print("Datos iniciales agregados a la base de datos")

# Rutas de la aplicación
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/estudiantes')
def estudiantes():
    estudiantes = Estudiante.query.all()
    return render_template('estudiantes.html', estudiantes=estudiantes)

@app.route('/recursos')
def recursos():
    recursos = Recurso.query.all()
    return render_template('recursos.html', recursos=recursos)

@app.route('/prestamos')
def prestamos():
    prestamos = Prestamo.query.all()
    return render_template('prestamos.html', prestamos=prestamos)

@app.route('/prestar', methods=['POST'])
def prestar():
    try:
        codigoEstudiante = request.form['codigoEstudiante']
        codigoRecurso = request.form['codigoRecurso']
        
        estudiante = Estudiante.query.get(codigoEstudiante)
        recurso = Recurso.query.get(codigoRecurso)
        
        if not estudiante or not recurso:
            flash('Estudiante o recurso no encontrado', 'error')
            return redirect(url_for('prestamos'))
            
        if recurso.estado != 'Disponible':
            flash('El recurso no está disponible para préstamo', 'error')
            return redirect(url_for('prestamos'))
            
        nuevo_prestamo = Prestamo(
            codigoEstudiante=codigoEstudiante,
            codigoRecurso=codigoRecurso,
            fechaPrestamo=datetime.now(),
            fechaDevolucion=datetime.now() + timedelta(days=7),
            estadoPrestamo='Activo'
        )
        
        db.session.add(nuevo_prestamo)
        recurso.estado = 'Prestado'
        db.session.commit()
        
        flash('Préstamo realizado con éxito', 'success')
        return redirect(url_for('prestamos'))
        
    except Exception as e:
        db.session.rollback()
        flash('Error al realizar el préstamo', 'error')
        return redirect(url_for('prestamos'))

if __name__ == '__main__':
    app.run(debug=True)
