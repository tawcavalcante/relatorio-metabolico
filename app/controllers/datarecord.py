import json
import uuid
from app.models.user_account import UserAccount


class DataRecord:
    """Banco de dados JSON e controle de sessão para Usuários"""

    def __init__(self):
        self._user_accounts = []
        self._authenticated_users = {}
        self.read()

    def read(self):
        try:
            with open("app/controllers/db/user_accounts.json", "r", encoding="utf-8") as arquivo_json:
                user_data = json.load(arquivo_json)
                self._user_accounts = [UserAccount(**data) for data in user_data]
        except (FileNotFoundError, json.JSONDecodeError):
            self._user_accounts = []

        if not self._user_accounts:
            self._user_accounts = [UserAccount("Tawan", "123456")]
            self._salvar_arquivo()

    def _salvar_arquivo(self):
        with open("app/controllers/db/user_accounts.json", "w", encoding="utf-8") as arquivo_json:
            user_data = [vars(user_account) for user_account in self._user_accounts]
            json.dump(user_data, arquivo_json, indent=4, ensure_ascii=False)

    def book(self, username, password):
        if any(u.username == username for u in self._user_accounts):
            return False
        new_user = UserAccount(username, password)
        self._user_accounts.append(new_user)
        self._salvar_arquivo()
        return True

    def getCurrentUser(self, session_id):
        if session_id in self._authenticated_users:
            return self._authenticated_users[session_id]
        return None

    def getUserName(self, session_id):
        if session_id in self._authenticated_users:
            return self._authenticated_users[session_id].username
        return None

    def getUserSessionId(self, username):
        for session_id, user in self._authenticated_users.items():
            if username == user.username:
                return session_id
        return None

    def checkUser(self, username, password):
        for user in self._user_accounts:
            if user.username == username and user.password == password:
                session_id = str(uuid.uuid4())
                self._authenticated_users[session_id] = user
                return session_id
        return None

    def logout(self, session_id):
        if session_id in self._authenticated_users:
            del self._authenticated_users[session_id]