from bottle import template, redirect, request
from app.controllers.datarecord import DataRecord
from app.controllers.db.avaliacao_record import AvaliacaoRecord
from app.models.avaliacao import AvaliacaoMetabolica


class Application:
    def __init__(self):
        self.pages = {
            "relatorio_metabolico": self.relatorio_metabolico,
            "portal": self.portal,
            "helper": self.helper,
        }
        self._model = DataRecord()
        self._avaliacao_db = AvaliacaoRecord()
        self._current_username = None

    def render(self, page, parameter=None):
        content = self.pages.get(page, self.helper)
        if not parameter:
            return content()
        return content(parameter)

    # --- MÉTODOS DE SESSÃO E AUTENTICAÇÃO (Helper BMVC) ---

    def get_session_id(self):
        return request.get_cookie("session_id")

    def get_logged_username(self):
        session_id = self.get_session_id()
        return self._model.getUserName(session_id)

    def is_authenticated(self, username):
        current_username = self.get_logged_username()
        return bool(username and current_username and username == current_username)

    def authenticate_user(self, username, password):
        session_id = self._model.checkUser(username, password)
        if session_id:
            self.logout_user()
            self._current_username = self._model.getUserName(session_id)
            return session_id, username
        return None, None

    def register_user(self, username, password):
        username = username.strip()
        if not username or not password:
            return False
        return self._model.book(username, password)

    def logout_user(self):
        self._current_username = None
        session_id = self.get_session_id()
        if session_id:
            self._model.logout(session_id)

    # --- VIEWS E ACTIONS ---

    def helper(self):
        return template("app/views/html/helper")

    def portal(self, erro=None, sucesso=None):
        return template("app/views/html/portal", erro=erro, sucesso=sucesso)

    def relatorio_metabolico(self, username=None):
        logged_user = self.get_logged_username()

        # Se acessou /relatorio_metabolico sem nome na URL, redireciona para a rota com seu username
        if not username:
            if logged_user:
                return redirect(f"/relatorio_metabolico/{logged_user}")
            return redirect("/portal")

        # Bloqueia acesso não autenticado ou tentativa de acessar URL de outro usuário
        if not self.is_authenticated(username):
            return redirect("/portal")

        todas = self._avaliacao_db.listar_todas()
        avaliacoes_usuario = [av for av in todas if av.username == username]
        ultima_avaliacao = avaliacoes_usuario[-1] if avaliacoes_usuario else None

        return template(
            "app/views/html/relatorio_metabolico",
            username=username,
            avaliacoes=avaliacoes_usuario,
            avaliacao_edicao=None,
            ultima_avaliacao=ultima_avaliacao,
        )

    # --- CRUD PROTEGIDO ---

    def salvar_avaliacao(self):
        username = self.get_logged_username()
        if not username:
            return redirect("/portal")

        av_id = request.forms.get("id")
        titulo = request.forms.get("titulo")
        sexo = request.forms.get("gender", "male")
        idade = request.forms.get("age", 20)
        peso = request.forms.get("weight", 75)
        altura = request.forms.get("height", 172)
        atividade = request.forms.get("activity", 1.55)
        prot_ratio = request.forms.get("prot_ratio", 2.0)
        fat_ratio = request.forms.get("fat_ratio", 1.0)

        avaliacao = AvaliacaoMetabolica(
            titulo=titulo,
            sexo=sexo,
            idade=idade,
            peso=peso,
            altura=altura,
            atividade=atividade,
            prot_ratio=prot_ratio,
            fat_ratio=fat_ratio,
            username=username,
            id=av_id if av_id else None,
        )

        if av_id:
            existente = self._avaliacao_db.buscar_por_id(av_id)
            if existente and existente.username == username:
                self._avaliacao_db.atualizar(avaliacao)
        else:
            self._avaliacao_db.adicionar(avaliacao)

        return redirect(f"/relatorio_metabolico/{username}")

    def editar_avaliacao(self, av_id):
        username = self.get_logged_username()
        if not username:
            return redirect("/portal")

        todas = self._avaliacao_db.listar_todas()
        avaliacoes_usuario = [av for av in todas if av.username == username]
        avaliacao_edicao = self._avaliacao_db.buscar_por_id(av_id)

        if not avaliacao_edicao or avaliacao_edicao.username != username:
            return redirect(f"/relatorio_metabolico/{username}")

        return template(
            "app/views/html/relatorio_metabolico",
            username=username,
            avaliacoes=avaliacoes_usuario,
            avaliacao_edicao=avaliacao_edicao,
            ultima_avaliacao=avaliacao_edicao,
        )

    def excluir_avaliacao(self, av_id):
        username = self.get_logged_username()
        if not username:
            return redirect("/portal")

        alvo = self._avaliacao_db.buscar_por_id(av_id)
        if alvo and alvo.username == username:
            self._avaliacao_db.excluir(av_id)

        return redirect(f"/relatorio_metabolico/{username}")