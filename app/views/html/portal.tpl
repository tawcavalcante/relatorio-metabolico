<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Entrar - Relatório Metabólico</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="/static/css/portal.css">
</head>
<body>
    <div class="auth-wrapper">
        <div class="auth-card">
            <div class="auth-header">
                <h1>Relatório Metabólico</h1>
                <p>Acesse sua conta para acompanhar suas avaliações</p>
            </div>

            % if defined('erro') and erro:
            <div class="alert alert-error">{{ erro }}</div>
            % end

            % if defined('sucesso') and sucesso:
            <div class="alert alert-success">{{ sucesso }}</div>
            % end

            <div class="auth-tabs">
                <button type="button" class="tab-btn active" id="tab-login">Entrar</button>
                <button type="button" class="tab-btn" id="tab-register">Criar Conta</button>
            </div>

            <form id="form-login" class="auth-form active" action="/portal" method="POST">
                <div class="form-group">
                    <label for="login-username">Usuário</label>
                    <input type="text" id="login-username" name="username" placeholder="Seu nome de usuário" required>
                </div>

                <div class="form-group">
                    <label for="login-password">Senha</label>
                    <div class="password-wrapper">
                        <input type="password" id="login-password" name="password" placeholder="••••••••" required>
                        <button type="button" class="toggle-pass" data-target="login-password">Mostrar</button>
                    </div>
                </div>

                <button type="submit" class="submit-btn">ENTRAR</button>
            </form>

            <form id="form-register" class="auth-form" action="/cadastro" method="POST">
                <div class="form-group">
                    <label for="reg-username">Usuário</label>
                    <input type="text" id="reg-username" name="username" placeholder="Escolha um usuário" required>
                </div>

                <div class="form-group">
                    <label for="reg-password">Senha</label>
                    <div class="password-wrapper">
                        <input type="password" id="reg-password" name="password" placeholder="Mínimo 4 caracteres" minlength="4" required>
                        <button type="button" class="toggle-pass" data-target="reg-password">Mostrar</button>
                    </div>
                </div>

                <button type="submit" class="submit-btn">CRIAR CONTA</button>
            </form>
        </div>
    </div>

    <script src="/static/js/portal.js"></script>
</body>
</html>