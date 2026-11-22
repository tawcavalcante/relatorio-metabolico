<!DOCTYPE html>
<html lang="pt-BR">
<head>
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>Relatório Metabólico - BMVC II</title>
   <link rel="stylesheet" type="text/css" href="/static/css/relatorio_metabolico.css">
   <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <main class="dashboard-container">
        <!-- Painel Esquerdo: Formulário CRUD -->
        <form class="input-panel" action="/avaliacao/salvar" method="POST">
            <input type="hidden" name="id" value="{{ avaliacao_edicao.id if avaliacao_edicao else '' }}">

            <div class="panel-header">
                <h2>{{ 'Editar Avaliação' if avaliacao_edicao else 'Parâmetros Corporais' }}</h2>
                <p>Preencha as métricas para calcular ou salvar</p>
            </div>

            <div class="input-group" style="margin-bottom: 20px;">
                <label>Identificação do Registro</label>
                <input type="text" name="titulo" placeholder="Ex: Início Bulking - Nov/26"
                       value="{{ avaliacao_edicao.titulo if avaliacao_edicao else '' }}" required>
            </div>

            <div class="toggle-group">
                <input type="radio" id="male" name="gender" value="male"
                       {{ 'checked' if (not avaliacao_edicao or avaliacao_edicao.sexo == 'male') else '' }}>
                <label for="male">MASCULINO</label>
                <input type="radio" id="female" name="gender" value="female"
                       {{ 'checked' if (avaliacao_edicao and avaliacao_edicao.sexo == 'female') else '' }}>
                <label for="female">FEMININO</label>
            </div>

            <div class="input-grid">
                <div class="input-group">
                    <label>Idade</label>
                    <input type="number" id="age" name="age"
                           value="{{ avaliacao_edicao.idade if avaliacao_edicao else 20 }}">
                </div>
                <div class="input-group">
                    <label>Peso (kg)</label>
                    <input type="number" step="0.1" id="weight" name="weight"
                           value="{{ avaliacao_edicao.peso if avaliacao_edicao else 75 }}">
                </div>
                <div class="input-group">
                    <label>Altura (cm)</label>
                    <input type="number" id="height" name="height"
                           value="{{ avaliacao_edicao.altura if avaliacao_edicao else 172 }}">
                </div>
            </div>

            <div class="panel-header">
                <h2>Nível de Atividade</h2>
            </div>
            % act = avaliacao_edicao.atividade if avaliacao_edicao else 1.55
            <select id="activity" name="activity">
                <option value="1.2" {{ 'selected' if act == 1.2 else '' }}>Sedentário (0 treinos na semana)</option>
                <option value="1.375" {{ 'selected' if act == 1.375 else '' }}>Leve (1 a 3 treinos na semana)</option>
                <option value="1.55" {{ 'selected' if act == 1.55 else '' }}>Moderado (3 a 5 treinos na semana)</option>
                <option value="1.725" {{ 'selected' if act == 1.725 else '' }}>Intenso (6 a 7 treinos na semana)</option>
            </select>

            <div class="panel-header">
                <h2>Alvos de Macronutrientes (g/kg)</h2>
            </div>
            <div class="input-grid">
                <div class="input-group">
                    <label>Proteína</label>
                    <input type="number" step="0.1" id="protein-ratio" name="protein_ratio"
                           value="{{ avaliacao_edicao.prot_ratio if avaliacao_edicao else 2.0 }}">
                    <span id="prot-warning" class="warning-msg"></span>
                </div>
                <div class="input-group">
                    <label>Gordura</label>
                    <input type="number" step="0.1" id="fat-ratio" name="fat_ratio"
                           value="{{ avaliacao_edicao.fat_ratio if avaliacao_edicao else 1.0 }}">
                    <span id="fat-warning" class="warning-msg"></span>
                </div>
            </div>

            <div class="btn-stack">
                <button type="button" id="calculate-btn">CALCULAR NA TELA</button>
                <button type="submit" class="save-btn">
                    {{ 'ATUALIZAR REGISTRO' if avaliacao_edicao else 'SALVAR AVALIAÇÃO' }}
                </button>
                % if avaliacao_edicao:
                    <a href="/relatorio_metabolico" class="cancel-link">Cancelar edição</a>
                % end
            </div>
        </form>

        <!-- Painel Direito: Resultados + Histórico CRUD -->
        <section class="result-panel">
            <div class="results-header">
                <h2>Relatório Metabólico</h2>
                <p>Simulação em tempo real e histórico persistido em Python</p>
            </div>

            <div class="cards-grid">
                <div class="result-card highlight-card">
                    <h3>Gasto Total (TDEE)</h3>
                    <div class="card-value"><span id="tdee-result">0</span> <small>kcal</small></div>
                    <p>Calorias de manutenção</p>
                </div>
                <div class="result-card">
                    <h3>Taxa Basal (TMB)</h3>
                    <div class="card-value"><span id="tmb-result">0</span> <small>kcal</small></div>
                    <p>Gasto em repouso absoluto</p>
                </div>
                <div class="result-card">
                    <h3>Meta de Hidratação</h3>
                    <div class="card-value"><span id="water-result">0</span> <small>L</small></div>
                    <p>Porção diária recomendada</p>
                </div>
            </div>

            <div class="results-header" style="margin-top: 35px;">
                <h2>Estratégias de Composição Corporal</h2>
            </div>

            <div class="table-container">
                <table class="modern-table">
                    <thead>
                        <tr>
                            <th>Objetivo</th>
                            <th>Kcal Totais</th>
                            <th>Carboidratos</th>
                            <th>Proteínas</th>
                            <th>Gorduras</th>
                        </tr>
                    </thead>
                    <tbody id="table-body">
                        <!-- Renderizado via JS -->
                    </tbody>
                </table>
            </div>

            <!-- Seção CRUD: Registros salvos no Back-end -->
            <div class="results-header" style="margin-top: 35px;">
                <h2>Histórico de Avaliações Salvas ({{ len(avaliacoes) }})</h2>
                <p>Objetos persistidos no servidor via modelo Python</p>
            </div>

            <div class="table-container">
                % if not avaliacoes:
                    <p style="padding: 20px 0; color: #64748b; font-size: 0.9rem;">
                        Nenhuma avaliação salva ainda. Preencha o formulário ao lado e clique em <strong>Salvar Avaliação</strong>.
                    </p>
                % else:
                    <table class="modern-table">
                        <thead>
                            <tr>
                                <th>Título / Data</th>
                                <th>Peso</th>
                                <th>TMB / TDEE</th>
                                <th>Macros (C / P / G)</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for av in avaliacoes:
                            % macros = av.calcular_macros()
                            <tr>
                                <td>
                                    <strong>{{ av.titulo }}</strong><br>
                                    <small style="color: #94a3b8;">{{ av.data_registro }}</small>
                                </td>
                                <td>{{ av.peso }} kg</td>
                                <td>{{ av.calcular_tmb() }} / <strong>{{ av.calcular_tdee() }} kcal</strong></td>
                                <td>{{ macros['carboidrato'] }}g / {{ macros['proteina'] }}g / {{ macros['gordura'] }}g</td>
                                <td class="actions-cell">
                                    <a href="/avaliacao/editar/{{ av.id }}" class="action-btn edit-btn">Editar</a>
                                    <a href="/avaliacao/excluir/{{ av.id }}" class="action-btn delete-btn">Excluir</a>
                                </td>
                            </tr>
                            % end
                        </tbody>
                    </table>
                % end
            </div>
        </section>
    </main>
    <script src="/static/js/relatorio_metabolico.js"></script>
</body>
</html>