import json
from app.models.avaliacao import AvaliacaoMetabolica


class AvaliacaoRecord:
    def __init__(self, caminho_arquivo="app/controllers/db/avaliacoes.json"):
        self.caminho_arquivo = caminho_arquivo
        self._avaliacoes = []
        self.ler()

    def ler(self):
        try:
            with open(self.caminho_arquivo, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
                self._avaliacoes = [AvaliacaoMetabolica.from_dict(item) for item in dados]
        except (FileNotFoundError, json.JSONDecodeError):
            self._avaliacoes = []

    def salvar_arquivo(self):
        with open(self.caminho_arquivo, "w", encoding="utf-8") as arquivo:
            dados = [av.to_dict() for av in self._avaliacoes]
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    def listar_todas(self):
        return self._avaliacoes

    def adicionar(self, avaliacao):
        self._avaliacoes.append(avaliacao)
        self.salvar_arquivo()

    def buscar_por_id(self, av_id):
        for av in self._avaliacoes:
            if av.id == av_id:
                return av
        return None

    def atualizar(self, avaliacao_atualizada):
        for i, av in enumerate(self._avaliacoes):
            if av.id == avaliacao_atualizada.id:
                self._avaliacoes[i] = avaliacao_atualizada
                self.salvar_arquivo()
                return True
        return False

    def excluir(self, av_id):
        self._avaliacoes = [av for av in self._avaliacoes if av.id != av_id]
        self.salvar_arquivo()