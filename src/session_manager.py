# /home/johnb/tasma-code-absulut/src/session_manager.py
import json
import os

class SessionManager:
    """
    Responsabilidade: Gerenciar a persistência de estado da sessão (ex: última pasta aberta).
    Isola a lógica de I/O de configuração de sessão do fluxo principal.
    """
    def __init__(self, session_file="session.json"):
        # Define o caminho do arquivo de sessão relativo à raiz do projeto
        # __file__ é src/session_manager.py -> dirname é src/ -> dirname é root/
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(base_dir)
        self.session_path = os.path.join(project_root, session_file)

    def save_sidebar_path(self, path):
        """Salva o caminho atual da sidebar no arquivo de sessão."""
        try:
            data = {}
            # Tenta ler dados existentes para não sobrescrever outras configs futuras
            if os.path.exists(self.session_path):
                try:
                    with open(self.session_path, 'r') as f:
                        data = json.load(f)
                except json.JSONDecodeError:
                    pass # Se corrompido, sobrescreve
            
            data["last_path"] = os.path.abspath(path)
            
            with open(self.session_path, 'w') as f:
                json.dump(data, f)
        except IOError:
            pass # Falha silenciosa em I/O não deve travar o editor

    def load_sidebar_path(self):
        """Carrega o último caminho da sidebar ou retorna a home do usuário."""
        default_path = os.path.expanduser("~")
        
        if not os.path.exists(self.session_path):
            return default_path
            
        try:
            with open(self.session_path, 'r') as f:
                data = json.load(f)
                last_path = data.get("last_path")
                if last_path and os.path.isdir(last_path):
                    return last_path
        except (IOError, json.JSONDecodeError):
            pass
            
        return default_path