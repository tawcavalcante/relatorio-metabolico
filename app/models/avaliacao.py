import uuid
from datetime import datetime


class AvaliacaoMetabolica:
    def __init__(
        self,
        titulo: str,
        sexo: str,
        idade: int,
        peso: float,
        altura: float,
        atividade: float,
        prot_ratio: float,
        fat_ratio: float,
        id: str = None,
        data_registro: str = None,
    ):
        self.id = id or str(uuid.uuid4())[:8]
        self.titulo = titulo.strip() or "Avaliação sem título"
        self.sexo = sexo
        self.idade = int(idade)
        self.peso = float(peso)
        self.altura = float(altura)
        self.atividade = float(atividade)
        self.prot_ratio = float(prot_ratio)
        self.fat_ratio = float(fat_ratio)
        self.data_registro = data_registro or datetime.now().strftime("%d/%m/%Y")

    def calcular_tmb(self) -> int:
        tmb = (10 * self.peso) + (6.25 * self.altura) - (5 * self.idade)
        tmb += 5 if self.sexo == "male" else -161
        return round(tmb)

    def calcular_tdee(self) -> int:
        return round(self.calcular_tmb() * self.atividade)

    def calcular_agua(self) -> float:
        return round(self.peso * 0.040, 1)

    def calcular_macros(self) -> dict:
        tdee = self.calcular_tdee()
        prot_g = round(self.peso * self.prot_ratio)
        fat_g = round(self.peso * self.fat_ratio)
        kcal_fixas = (prot_g * 4) + (fat_g * 9)
        carb_kcal = tdee - kcal_fixas
        carb_g = round(carb_kcal / 4) if carb_kcal > 0 else 0

        return {
            "proteina": prot_g,
            "gordura": fat_g,
            "carboidrato": carb_g,
        }

    def to_dict(self) -> dict:
        return {
            "id": self.id,
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
    def from_dict(cls, dados: dict) -> "AvaliacaoMetabolica":
        return cls(
            id=dados.get("id"),
            titulo=dados.get("titulo", "Avaliação"),
            sexo=dados.get("sexo", "male"),
            idade=dados.get("idade", 20),
            peso=dados.get("peso", 75.0),
            altura=dados.get("altura", 172.0),
            atividade=dados.get("atividade", 1.55),
            prot_ratio=dados.get("prot_ratio", 2.0),
            fat_ratio=dados.get("fat_ratio", 1.0),
            data_registro=dados.get("data_registro"),
        )