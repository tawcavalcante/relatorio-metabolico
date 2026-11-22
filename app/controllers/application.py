from bottle import template, request, redirect
from app.models.avaliacao import AvaliacaoMetabolica
from app.controllers.db.avaliacao_record import AvaliacaoRecord


class Application:
    def __init__(self):
        self.db = AvaliacaoRecord()
        self.pages = {
            "relatorio_metabolico": self.relatorio_metabolico
        }

    def render(self, page, parameter=None):
        content = self.pages.get(page, self.helper)
        if not parameter:
            return content()
        return content(parameter)

    def helper(self):
        return template("app/views/html/helper")

    def relatorio_metabolico(self, avaliacao_edicao=None):
        avaliacoes = self.db.listar_todas()
        ultima_avaliacao = avaliacoes[-1] if avaliacoes else None
        return template(
            "app/views/html/relatorio_metabolico",
            avaliacoes=avaliacoes,
            avaliacao_edicao=avaliacao_edicao,
            ultima_avaliacao=ultima_avaliacao,
        )

    def salvar_avaliacao(self):
        avaliacao_id = request.forms.get("id", "").strip()
        titulo = request.forms.get("titulo", "Avaliação Metabólica")
        sexo = request.forms.get("gender", "male")
        idade = int(request.forms.get("age", 20))
        peso = float(request.forms.get("weight", 75.0))
        altura = float(request.forms.get("height", 172.0))
        atividade = float(request.forms.get("activity", 1.55))
        prot_ratio = float(request.forms.get("protein_ratio", 2.0))
        fat_ratio = float(request.forms.get("fat_ratio", 1.0))

        if avaliacao_id:
            existente = self.db.buscar_por_id(avaliacao_id)
            data_original = existente.data_registro if existente else None
            avaliacao = AvaliacaoMetabolica(
                id=avaliacao_id,
                titulo=titulo,
                sexo=sexo,
                idade=idade,
                peso=peso,
                altura=altura,
                atividade=atividade,
                prot_ratio=prot_ratio,
                fat_ratio=fat_ratio,
                data_registro=data_original,
            )
            self.db.atualizar(avaliacao)
        else:
            nova_avaliacao = AvaliacaoMetabolica(
                titulo=titulo,
                sexo=sexo,
                idade=idade,
                peso=peso,
                altura=altura,
                atividade=atividade,
                prot_ratio=prot_ratio,
                fat_ratio=fat_ratio,
            )
            self.db.adicionar(nova_avaliacao)

        return redirect("/relatorio_metabolico")

    def editar_avaliacao(self, avaliacao_id):
        avaliacao = self.db.buscar_por_id(avaliacao_id)
        return self.relatorio_metabolico(avaliacao_edicao=avaliacao)

    def excluir_avaliacao(self, avaliacao_id):
        self.db.excluir(avaliacao_id)
        return redirect("/relatorio_metabolico")