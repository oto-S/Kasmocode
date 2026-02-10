# /home/johnb/tasma-code-absulut/src/file_handler.py
import os
import shutil

class FileHandler:
    """
    Responsabilidade: Lidar com operações de I/O de arquivos.
    Não mantém estado do editor nem interage com o usuário.
    """
    
    def load_file(self, filepath):
        """Lê um arquivo e retorna uma lista de strings (linhas)."""
        if not os.path.exists(filepath):
            return [""]  # Arquivo novo começa vazio
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
                return lines if lines else [""]
        except IOError as e:
            raise IOError(f"Erro ao ler arquivo: {e}")

    def save_file(self, filepath, lines):
        """Escreve a lista de strings no arquivo."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("\n".join(lines))
        except IOError as e:
            raise IOError(f"Erro ao salvar arquivo: {e}")

    def list_directory(self, path, show_hidden=False):
        """Lista conteúdo do diretório, pastas primeiro. Retorna [(nome, is_dir), ...]"""
        if not os.path.isdir(path):
            return []
        try:
            items = os.listdir(path)
            if not show_hidden:
                items = [i for i in items if not i.startswith('.')]
            
            items_info = [(i, os.path.isdir(os.path.join(path, i))) for i in items]
            items_info.sort(key=lambda x: (not x[1], x[0].lower()))
            
            if os.path.abspath(path) != os.path.abspath(os.sep):
                items_info.insert(0, ("..", True))
            return items_info
        except OSError:
            return []

    def is_dir(self, path):
        return os.path.isdir(path)

    def move_file(self, src, dst):
        """Move ou renomeia arquivo/diretório."""
        try:
            shutil.move(src, dst)
            return True
        except OSError:
            return False

    def create_file(self, path):
        """Cria um arquivo vazio."""
        try:
            with open(path, 'w') as f:
                pass
            return True
        except OSError:
            return False

    def create_directory(self, path):
        """Cria um diretório."""
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except OSError:
            return False

    def copy_path(self, src, dst):
        """Copia arquivo ou diretório recursivamente."""
        try:
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
            return True
        except OSError:
            return False

    def search_in_files(self, root_path, query, show_hidden=False):
        """Busca string em arquivos recursivamente. Retorna lista de dicts."""
        results = []
        if not query: return results
        
        try:
            for root, dirs, files in os.walk(root_path):
                if not show_hidden:
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    files = [f for f in files if not f.startswith('.')]
                
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            for i, line in enumerate(f):
                                if query in line:
                                    results.append({
                                        'file': filepath, 'line': i + 1, 'content': line.strip(), 'is_dir': False
                                    })
                                    if len(results) > 200: return results # Limite para performance
                    except Exception: pass
        except Exception: pass
        return results
