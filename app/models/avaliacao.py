import uuid
from datetime import datetime


class AvaliacaoMetabolica:
    def __init__(
        self,
        titulo,
        sexo,
        idade,
        peso,
        altura,
        atividade,
        prot_ratio,
        fat_ratio,
        username="Tawan",
        id=None,
        data_registro=None,
    ):
        self.id = id if id else str(uuid.uuid4())[:8]
        self.username = username
        self.titulo = titulo.strip() if titulo and titulo.strip() else "Avaliação Metabólica"
        self.sexo = sexo
        self.idade = int(idade)
        self.peso = float(peso)
        self.altura = float(altura)
        self.atividade = float(atividade)
        self.prot_ratio = float(prot_ratio)
        self.fat_ratio = float(fat_ratio)
        self.data_registro = (
            data_registro if data_registro else datetime.now().strftime("%d/%m/%Y")
        )

    def calcular_tmb(self):
        base = (10 * self.peso) + (6.25 * self.altura) - (5 * self.idade)
        return round(base + 5 if self.sexo == "male" else base - 161)

    def calcular_tdee(self):
        return round(self.calcular_tmb() * self.atividade)

    def calcular_hidratacao(self):
        return round((self.peso * 40) / 1000, 1)

    def calcular_macros(self):
        tdee = self.calcular_tdee()
        proteina_g = round(self.peso * self.prot_ratio)
        gordura_g = round(self.peso * self.fat_ratio)
        kcal_restante = tdee - (proteina_g * 4 + gordura_g * 9)
        carbo_g = max(0, round(kcal_restante / 4))
        return {"proteina": proteina_g, "gordura": gordura_g, "carboidrato": carbo_g}

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "titulo": self.titulo,
            "sexo": self.sexo,
            "idade": self.idade,
            "peso": self.peso,
            "altura": self.altura,
            "atividade": self.atividade,
            "prot_ratio": self.prot_ratio,
            "fat_ratio": self.fat_ratio,
            "data_registro": self.data_registro,
        }

    @classmethod
    def from_dict(cls, dados):
        return cls(
            id=dados.get("id"),
            username=dados.get("username", "Tawan"),
            titulo=dados.get("titulo", "Avaliação Metabólica"),
            sexo=dados.get("sexo", "male"),
            idade=dados.get("idade", 20),
            peso=dados.get("peso", 75.0),
            altura=dados.get("altura", 172.0),
            atividade=dados.get("atividade", 1.55),
            prot_ratio=dados.get("prot_ratio", 2.0),
            fat_ratio=dados.get("fat_ratio", 1.0),
            data_registro=dados.get("data_registro"),
        )