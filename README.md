# Relatório Metabólico (BMVC)

Aplicação web para cálculo metabólico, estimativa de gasto energético e planejamento de macronutrientes, desenvolvida em **Python** (microframework **Bottle**) com **HTML5, CSS3 e JavaScript** para a disciplina **Orientação a Objetos**
## Finalidade

Fornecer uma interface interativa para cálculo da Taxa Metabólica Basal (TMB), Gasto Energético Total (TDEE), meta diária de hidratação e distribuição de macronutrientes por cenário de composição corporal (déficit, manutenção e superávit calórico), com validação científica em tempo real.

O projeto aplica o padrão arquitetural **BMVC** (Bottle Model-View-Controller), evoluindo progressivamente de páginas estáticas dinâmicas no cliente para persistência de modelos, autenticação de usuários e comunicação em tempo real.

## Níveis do projeto

| Nível | Propósito | Interface / Recursos | Vídeo | Commit de entrega | Status |
|:---:|---|---|---------------|----------------------|:---:|
| **1** | Servir página estática personalizada com HTML, CSS e JS funcionais e ativos | Web (`HTML` + `CSS` + `JS`) | [link](https://youtu.be/N7vum7XAaRY) | `concluído` | Enviado |
| **2** | Implementação de modelos em Python com operações completas de CRUD | Web (`TPL` + Persistência) | [Em breve]() | `A definir` | Pendente |
| **3** | Controle de acesso de usuários com sistema de login e rotas restritas | Web (`Login` + Sessão) | [Em breve]() | `A definir` | Pendente |
| **4** | Atualização assíncrona de dados na página em tempo real | Web (`WebSockets`) | [Em breve]() | `A definir` | Pendente |


## Funcionalidades (Base)

- **Cálculo Energético:** estimativa de TMB (Mifflin-St Jeor), TDEE ajustado pelo nível de atividade física e meta diária de ingestão hídrica (`40 ml/kg`).
- **Validação Científica de Macros:** alertas visuais dinâmicos para faixas de proteína (`1.2 a 3.0 g/kg`) e gordura (`0.5 a 1.5 g/kg`), destacando zonas ideais para hipertrofia e limites de segurança.
- **Matriz de Estratégias:** geração automática de 5 cenários calóricos (perda de `500g` ou `250g`/semana, manutenção e ganho de `250g` ou `500g`/semana) com ajuste automático de carboidratos.

## Como executar

1. Clone o repositório e acesse a pasta do projeto:
```bash
git clone [https://github.com/tawcavalcante/relatorio-metabolico.git]
cd relatorio-metabolico

```

2. Crie e ative o ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate

```

3. Instale as dependências e inicie o servidor:

```bash
pip install -r requirements.txt
python3 route.py

```

4. Acesse no navegador:

```text
http://localhost:8080/relatorio_metabolico

```

## Estrutura

```
relatorio-metabolico/
├── app/
│   ├── controllers/
│   │   ├── db/                 Persistência de dados em arquivo (Níveis 2 a 4)
│   │   └── application.py      Controlador principal e mapeamento de páginas
│   ├── models/                 Modelos de domínio em Python (Níveis 2 a 4)
│   ├── static/
│   │   ├── css/                Folhas de estilo (relatorio_metabolico.css)
│   │   ├── img/                Recursos visuais e ícones
│   │   └── js/                 Lógica de cálculo e DOM (relatorio_metabolico.js)
│   └── views/
│       └── html/               Templates HTML/TPL (relatorio_metabolico.html)
├── route.py                    Ponto de entrada: configura rotas e inicia o servidor Bottle
├── bmvc_setup.sh               Script de configuração do ambiente BMVC
├── docker_install.sh           Script auxiliar de instalação Docker
└── Dockerfile                  Configuração de contêiner da aplicação

```

A estrutura base do framework concentra o roteamento em `route.py` e `application.py`, permitindo expandir os modelos (`app/models/`) e templates (`app/views/`) nos próximos níveis sem alterar a arquitetura central.

## Autor
GitHub: @tawcavalcante
