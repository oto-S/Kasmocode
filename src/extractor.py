# /home/johnb/tasma-code-absulut/src/extractor.py
import os
import shutil
import zipfile
import json
import tempfile

class ThemeExtractor:
    def __init__(self, themes_dir):
        self.themes_dir = themes_dir
        if not os.path.exists(self.themes_dir):
            os.makedirs(self.themes_dir)

    def import_themes(self, source_path):
        """
        Importa temas de um arquivo JSON ou de um arquivo ZIP contendo JSONs.
        Retorna (sucesso: bool, mensagem: str).
        """
        source_path = os.path.abspath(os.path.expanduser(source_path))
        
        if not os.path.exists(source_path):
            return False, f"Arquivo não encontrado: {source_path}"

        if source_path.lower().endswith('.json'):
            return self._import_single_json(source_path)
        elif source_path.lower().endswith('.zip'):
            return self._import_zip(source_path)
        else:
            return False, "Formato não suportado. Use .json ou .zip"

    def _import_single_json(self, filepath):
        try:
            if self._is_valid_theme(filepath):
                filename = os.path.basename(filepath)
                dest_path = os.path.join(self.themes_dir, filename)
                shutil.copy2(filepath, dest_path)
                return True, f"Tema '{filename}' importado com sucesso."
            else:
                return False, "O arquivo JSON não parece ser um tema válido (falta chave 'colors')."
        except Exception as e:
            return False, f"Erro ao importar JSON: {e}"

    def _import_zip(self, zip_path):
        count = 0
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                try:
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(temp_dir)
                except zipfile.BadZipFile:
                    return False, "Arquivo ZIP inválido ou corrompido."

                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        if file.lower().endswith('.json'):
                            full_path = os.path.join(root, file)
                            if self._is_valid_theme(full_path):
                                dest_path = os.path.join(self.themes_dir, file)
                                shutil.copy2(full_path, dest_path)
                                count += 1
            
            if count > 0:
                return True, f"{count} temas importados do pacote ZIP."
            else:
                return False, "Nenhum tema válido encontrado no ZIP."

        except Exception as e:
            return False, f"Erro ao processar ZIP: {e}"

    def _is_valid_theme(self, filepath):
        """Verifica se o JSON possui a estrutura básica de um tema."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return isinstance(data, dict) and "colors" in data
        except (json.JSONDecodeError, OSError):
            return False