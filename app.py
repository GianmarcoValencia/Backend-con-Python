from flask import Flask, render_template, request

app = Flask(__name__)

class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def presentarse(self):
        return f"Hola, soy {self.nombre} y tengo {self.edad} años."

class Estudiante(Persona):
    def __init__(self, nombre, edad, carrera):
        super().__init__(nombre, edad)
        self.carrera = carrera

    def presentarse(self):
        return f"Hola, soy {self.nombre}, tengo {self.edad} años y estudio {self.carrera}."

@app.route("/")
def formulario():
    return render_template("formulario.html")

@app.route("/resultado", methods=["POST"])
def resultado():
    nombre = request.form["nombre"]
    edad = request.form["edad"]
    carrera = request.form["carrera"]

    estudiante = Estudiante(nombre, edad, carrera)
    mensaje = estudiante.presentarse()

    return render_template("resultado.html", mensaje=mensaje)

if __name__ == "__main__":
    app.run(debug=True)
