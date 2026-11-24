from bottle import Bottle, run, route, static_file, request, response, redirect
from app.controllers.application import Application

app = Bottle()
ctl = Application()


# --- ARQUIVOS ESTÁTICOS ---
@app.route("/static/<filepath:path>")
def serve_static(filepath):
    return static_file(filepath, root="./app/static")


# --- ROTA INICIAL E HELPER ---
@app.route("/", method="GET")
def index():
    return redirect("/portal")


@app.route("/helper", method="GET")
def helper():
    return ctl.render("helper")


# --- AUTENTICAÇÃO (PORTAL, CADASTRO E LOGOUT) ---
@app.route("/portal", method="GET")
def login():
    return ctl.portal()


@app.route("/portal", method="POST")
def action_portal():
    username = request.forms.get("username")
    password = request.forms.get("password")
    session_id, auth_user = ctl.authenticate_user(username, password)

    if session_id:
        response.set_cookie("session_id", session_id, httponly=True, max_age=3600)
        return redirect(f"/relatorio_metabolico/{auth_user}")

    return ctl.portal(erro="Usuário ou senha incorretos.")


@app.route("/cadastro", method="POST")
def action_cadastro():
    username = request.forms.get("username")
    password = request.forms.get("password")

    if ctl.register_user(username, password):
        session_id, auth_user = ctl.authenticate_user(username, password)
        response.set_cookie("session_id", session_id, httponly=True, max_age=3600)
        return redirect(f"/relatorio_metabolico/{auth_user}")

    return ctl.portal(erro="Este nome de usuário já está em uso.")


@app.route("/logout", method="POST")
def logout():
    ctl.logout_user()
    response.delete_cookie("session_id")
    return redirect("/portal")


# --- PÁGINA RESTRITA E CRUD DO RELATÓRIO METABÓLICO ---
@app.route("/relatorio_metabolico", method="GET")
@app.route("/relatorio_metabolico/<username>", method="GET")
def action_relatorio(username=None):
    return ctl.render("relatorio_metabolico", username)


@app.route("/avaliacao/salvar", method="POST")
def action_salvar_avaliacao():
    return ctl.salvar_avaliacao()


@app.route("/avaliacao/editar/<av_id>", method="GET")
def action_editar_avaliacao(av_id):
    return ctl.editar_avaliacao(av_id)


@app.route("/avaliacao/excluir/<av_id>", method="GET")
def action_excluir_avaliacao(av_id):
    return ctl.excluir_avaliacao(av_id)


if __name__ == "__main__":
    run(app, host="localhost", port=8080, debug=True)