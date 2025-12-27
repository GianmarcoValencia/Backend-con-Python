from flask import Flask, render_template, request, redirect, url_for
from conexion import obtener_conexion

app = Flask(__name__)

@app.route("/")
def formulario():
    return render_template("formulario.html")


@app.route("/guardar", methods=["POST"])
def guardar():
    nombre = request.form["nombre"]
    direccion = request.form["direccion"]
    ciudad = request.form["ciudad"]

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO estudiantes (nombre, direccion, ciudad) VALUES (%s, %s, %s)",
            (nombre, direccion, ciudad)
        )
        conexion.commit()
    conexion.close()

    return redirect(url_for("listar"))


@app.route("/listar")
def listar():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM estudiantes")
        estudiantes = cursor.fetchall()
    conexion.close()

    return render_template("lista.html", estudiantes=estudiantes)


@app.route("/eliminar/<int:id>")
def eliminar(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM estudiantes WHERE id = %s", (id,))
        conexion.commit()
    conexion.close()

    return redirect(url_for("listar"))


@app.route("/editar/<int:id>")
def editar(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM estudiantes WHERE id = %s", (id,))
        estudiante = cursor.fetchone()
    conexion.close()

    return render_template("editar.html", estudiante=estudiante)


@app.route("/actualizar", methods=["POST"])
def actualizar():
    id = request.form["id"]
    nombre = request.form["nombre"]
    direccion = request.form["direccion"]
    ciudad = request.form["ciudad"]

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            UPDATE estudiantes
            SET nombre=%s, direccion=%s, ciudad=%s
            WHERE id=%s
        """, (nombre, direccion, ciudad, id))
        conexion.commit()
    conexion.close()

    return redirect(url_for("listar"))


if __name__ == "__main__":
    app.run(debug=True)
