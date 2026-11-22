import json
import os
from app.models.avaliacao import AvaliacaoMetabolica


class AvaliacaoRecord:
    def __init__(self, filepath: str = "app/controllers/db/avaliacoes.json"):
        self.filepath = filepath
        self._garantir_arquivo()

    def _garantir_arquivo(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)

    def _ler_dados(self) -> list[dict]:
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _salvar_dados(self, lista_dicts: list[dict]):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(lista_dicts, f, ensure_ascii=False, indent=4)

    def listar_todas(self) -> list[AvaliacaoMetabolica]:
        dados = self._ler_dados()
        return [AvaliacaoMetabolica.from_dict(item) for item in dados]

    def buscar_por_id(self, avaliacao_id: str) -> AvaliacaoMetabolica | None:
        for av in self.listar_todas():
            if av.id == avaliacao_id:
                return av
        return None

    def adicionar(self, avaliacao: AvaliacaoMetabolica):
        dados = self._ler_dados()
        dados.append(avaliacao.to_dict())
        self._salvar_dados(dados)

    def atualizar(self, avaliacao_atualizada: AvaliacaoMetabolica) -> bool:
        dados = self._ler_dados()
        for i, item in enumerate(dados):
            if item.get("id") == avaliacao_atualizada.id:
                dados[i] = avaliacao_atualizada.to_dict()
                self._salvar_dados(dados)
                return True
        return False

    def excluir(self, avaliacao_id: str) -> bool:
        dados = self._ler_dados()
        nova_lista = [item for item in dados if item.get("id") != avaliacao_id]
        if len(nova_lista) < len(dados):
            self._salvar_dados(nova_lista)
            return True
        return False