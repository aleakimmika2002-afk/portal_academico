from flask import Flask, render_template, request, redirect, url_for, session, make_response, flash

portal = Flask(__name__)
portal.secret_key = "clave_portal_742"

registro_usuarios = {
    "juan": "1234",
    "maria": "abcd",
    "pedro": "2026"
}

catalogo_cursos = [
    {
        "nombre": "Programación Web",
        "docente": "Luis Pérez",
        "cupos": 15
    },
    {
        "nombre": "Bases de Datos",
        "docente": "Ana López",
        "cupos": 8
    },
    {
        "nombre": "Inteligencia Artificial",
        "docente": "Carlos Rojas",
        "cupos": 0
    }
]


@portal.route("/")
def pagina_inicio():
    visitante = request.cookies.get("usuario_preferido")

    return render_template(
        "index.html",
        visitante=visitante
    )
@portal.route("/login", methods=["GET", "POST"])
def acceso_usuario():

    if request.method == "POST":

        usuario_ingresado = request.form.get("usuario")
        clave_ingresada = request.form.get("contrasena")

        if registro_usuarios.get(usuario_ingresado) == clave_ingresada:

            session["usuario_actual"] = usuario_ingresado

            respuesta = make_response(
                redirect(url_for("lista_cursos"))
            )

            respuesta.set_cookie(
                "usuario_preferido",
                usuario_ingresado,
                max_age=60 * 60 * 24 * 30
            )

            return respuesta

        return render_template(
            "login.html",
            aviso="Usuario o contraseña incorrectos."
        )

    return render_template("login.html")


@portal.route("/cursos")
def lista_cursos():

    if "usuario_actual" not in session:
        return redirect(url_for("acceso_usuario"))

    return render_template(
        "cursos.html",
        usuario=session["usuario_actual"],
        cursos=catalogo_cursos
    )

@portal.route("/logout")
def cerrar_sesion():
    session.clear()
    flash("Sesión cerrada correctamente.")
    return redirect(url_for("pagina_inicio"))

@portal.route("/perfil")
def datos_perfil():
    if "usuario_actual" not in session:
        return redirect(url_for("acceso_usuario"))

    usuario = session["usuario_actual"]

    return render_template(
        "perfil.html",
        usuario=usuario
    )
@portal.route("/quitar-cookie")
def quitar_cookie():
    respuesta = make_response(
        redirect(url_for("pagina_inicio"))
    )

    respuesta.delete_cookie("usuario_preferido")

    return respuesta

if __name__ == "__main__":
    portal.run(debug=True)
