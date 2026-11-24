<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório Metabólico - {{ username }}</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="/static/css/relatorio_metabolico.css">
</head>
<body>
    % av_atual = avaliacao_edicao if avaliacao_edicao else ultima_avaliacao
    % tmb_val = av_atual.calcular_tmb() if av_atual else 1730
    % tdee_val = av_atual.calcular_tdee() if av_atual else 2682
    % agua_val = av_atual.calcular_hidratacao() if av_atual else 3.0
    % macros_val = av_atual.calcular_macros() if av_atual else {'carboidrato': 352, 'proteina': 150, 'gordura': 75}

    <div class="dashboard-layout">
        <!-- PAINEL LATERAL FIXO -->
        <aside class="input-panel">
            <div>
                <div class="user-session-bar">
                    <div class="user-info">
                        <span class="user-dot"></span>
                        <span class="user-name">{{ username }}</span>
                    </div>
                    <form action="/logout" method="POST" style="margin: 0;">
                        <button type="submit" class="btn-logout">Sair</button>
                    </form>
                </div>

                <div class="panel-header">
                    <h2>{{ 'Editar Avaliação' if avaliacao_edicao else 'Nova Avaliação' }}</h2>
                    <p>Preencha as métricas para calcular ou salvar</p>
                </div>

                <form id="metabolic-form" action="/avaliacao/salvar" method="POST">
                    <input type="hidden" name="id" value="{{ avaliacao_edicao.id if avaliacao_edicao else '' }}">
                    <input type="hidden" name="gender" id="gender" value="{{ av_atual.sexo if av_atual else 'male' }}">

                    <div class="form-group">
                        <label for="titulo">Identificação do Registro</label>
                        <input type="text" id="titulo" name="titulo" placeholder="Ex: Início Bulking" value="{{ avaliacao_edicao.titulo if avaliacao_edicao else '' }}" required>
                    </div>

                    <div class="gender-toggle">
                        <button type="button" class="gender-btn {{ 'active' if not av_atual or av_atual.sexo == 'male' else '' }}" data-gender="male">MASCULINO</button>
                        <button type="button" class="gender-btn {{ 'active' if av_atual and av_atual.sexo == 'female' else '' }}" data-gender="female">FEMININO</button>
                    </div>

                    <div class="metrics-row">
                        <div class="form-group">
                            <label for="age">Idade</label>
                            <input type="number" id="age" name="age" value="{{ av_atual.idade if av_atual else 20 }}" min="10" max="100" required>
                        </div>
                        <div class="form-group">
                            <label for="weight">Peso (kg)</label>
                            <input type="number" id="weight" name="weight" step="0.1" value="{{ av_atual.peso if av_atual else 75.0 }}" min="30" max="250" required>
                        </div>
                        <div class="form-group">
                            <label for="height">Altura (cm)</label>
                            <input type="number" id="height" name="height" step="0.1" value="{{ av_atual.altura if av_atual else 172.0 }}" min="100" max="230" required>
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="activity">Nível de Atividade</label>
                        <select id="activity" name="activity">
                            % act = av_atual.atividade if av_atual else 1.55
                            <option value="1.2" {{ 'selected' if act == 1.2 else '' }}>Sedentário (pouco ou nenhum treino)</option>
                            <option value="1.375" {{ 'selected' if act == 1.375 else '' }}>Leve (1 a 2 treinos na semana)</option>
                            <option value="1.55" {{ 'selected' if act == 1.55 else '' }}>Moderado (3 a 5 treinos na semana)</option>
                            <option value="1.725" {{ 'selected' if act == 1.725 else '' }}>Intenso (6 a 7 treinos na semana)</option>
                            <option value="1.9" {{ 'selected' if act == 1.9 else '' }}>Muito Intenso (2x ao dia / atleta)</option>
                        </select>
                    </div>

                    <div class="macro-targets">
                        <span class="section-label">Alvos de Macronutrientes (g/kg)</span>
                        <div class="macro-row">
                            <div class="form-group">
                                <label for="prot_ratio">Proteína</label>
                                <input type="number" id="prot_ratio" name="prot_ratio" step="0.1" value="{{ av_atual.prot_ratio if av_atual else 2.0 }}" min="0.8" max="4.0" required>
                                <span class="hint-text">Faixa ideal hipertrofia</span>
                            </div>
                            <div class="form-group">
                                <label for="fat_ratio">Gordura</label>
                                <input type="number" id="fat_ratio" name="fat_ratio" step="0.1" value="{{ av_atual.fat_ratio if av_atual else 1.0 }}" min="0.4" max="2.0" required>
                                <span class="hint-text">Faixa ideal</span>
                            </div>
                        </div>
                    </div>

                    <div class="panel-actions">
                        <button type="submit" class="btn-primary">{{ 'ATUALIZAR REGISTRO' if avaliacao_edicao else 'SALVAR AVALIAÇÃO' }}</button>
                        <button type="button" id="btn-calcular" class="btn-secondary">CALCULAR NA TELA</button>
                        % if avaliacao_edicao:
                        <a href="/relatorio_metabolico/{{ username }}" class="btn-cancel">Cancelar Edição</a>
                        % end
                    </div>
                </form>
            </div>
        </aside>

        <!-- PAINEL PRINCIPAL DIREITO -->
        <main class="results-panel">
            <header class="results-header">
                <h1>Relatório Metabólico</h1>
                <p>Simulação em tempo real e histórico persistido em Python</p>
            </header>

            <!-- CARDS DE RESULTADO -->
            <section class="kpi-grid">
                <div class="kpi-card highlight">
                    <span class="kpi-title">GASTO TOTAL (TDEE)</span>
                    <div class="kpi-value"><span id="tdee-value">{{ tdee_val }}</span> <small>kcal</small></div>
                    <span class="kpi-sub">Calorias de manutenção</span>
                </div>

                <div class="kpi-card">
                    <span class="kpi-title">TAXA BASAL (TMB)</span>
                    <div class="kpi-value"><span id="tmb-value">{{ tmb_val }}</span> <small>kcal</small></div>
                    <span class="kpi-sub">Gasto em repouso absoluto</span>
                </div>

                <div class="kpi-card">
                    <span class="kpi-title">META DE HIDRATAÇÃO</span>
                    <div class="kpi-value"><span id="water-value">{{ agua_val }}</span> <small>L</small></div>
                    <span class="kpi-sub">Porção diária recomendada</span>
                </div>
            </section>

            <!-- TABELA DE ESTRATÉGIAS -->
            <section class="card-section">
                <h2>Estratégias de Composição Corporal</h2>
                <div class="table-card">
                    <table>
                        <thead>
                            <tr>
                                <th>OBJETIVO</th>
                                <th>KCAL TOTAIS</th>
                                <th>CARBOIDRATOS</th>
                                <th>PROTEÍNAS</th>
                                <th>GORDURAS</th>
                            </tr>
                        </thead>
                        <tbody id="strategies-body">
                            % estrategias = [("Perder 500g/sem", -500), ("Perder 250g/sem", -250), ("Manter o Peso", 0), ("Ganhar 250g/sem", 250), ("Ganhar 500g/sem", 500)]
                            % p_g = macros_val['proteina']
                            % g_g = macros_val['gordura']
                            % for nome_est, delta in estrategias:
                            % kcal_est = tdee_val + delta
                            % carb_est = max(0, round((kcal_est - (p_g * 4 + g_g * 9)) / 4))
                            <tr>
                                <td>{{ nome_est }}</td>
                                <td>{{ kcal_est }} kcal</td>
                                <td>{{ carb_est }}g</td>
                                <td>{{ p_g }}g</td>
                                <td>{{ g_g }}g</td>
                            </tr>
                            % end
                        </tbody>
                    </table>
                </div>
            </section>

            <!-- HISTÓRICO PERSISTIDO -->
            <section class="card-section">
                <div class="history-header">
                    <h2>Histórico de Avaliações Salvas ({{ len(avaliacoes) }})</h2>
                    <p>Objetos persistidos no servidor via modelo Python</p>
                </div>

                <div class="table-card">
                    % if avaliacoes:
                    <table>
                        <thead>
                            <tr>
                                <th>TÍTULO / DATA</th>
                                <th>PESO</th>
                                <th>TMB / TDEE</th>
                                <th>MACROS (C / P / G)</th>
                                <th>AÇÕES</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for av in reversed(avaliacoes):
                            % m = av.calcular_macros()
                            <tr>
                                <td>
                                    <strong>{{ av.titulo }}</strong><br>
                                    <small class="date-sub">{{ av.data_registro }}</small>
                                </td>
                                <td>{{ av.peso }} kg</td>
                                <td>{{ av.calcular_tmb() }} / <strong>{{ av.calcular_tdee() }} kcal</strong></td>
                                <td>{{ m['carboidrato'] }}g / {{ m['proteina'] }}g / {{ m['gordura'] }}g</td>
                                <td class="actions-cell">
                                    <a href="/avaliacao/editar/{{ av.id }}" class="btn-edit">Editar</a>
                                    <a href="/avaliacao/excluir/{{ av.id }}" class="btn-delete">Excluir</a>
                                </td>
                            </tr>
                            % end
                        </tbody>
                    </table>
                    % else:
                    <div class="empty-state">
                        Nenhuma avaliação salva para <strong>{{ username }}</strong> ainda. Preencha o formulário ao lado e clique em <strong>Salvar Avaliação</strong>.
                    </div>
                    % end
                </div>
            </section>
        </main>
    </div>

    <script src="/static/js/relatorio_metabolico.js"></script>
</body>
</html>