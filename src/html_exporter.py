# /home/johnb/tasma-code-absulut/src/html_exporter.py
import html
import keyword

class HtmlExporter:
    def __init__(self):
        self.PYTHON_KEYWORDS = set(keyword.kwlist)
        # Estilos CSS básicos para o HTML gerado
        self.css = """
        body { background-color: #ffffff; color: #000000; font-family: monospace; white-space: pre; }
        .keyword { color: #aa5500; font-weight: bold; }
        .string { color: #00aa00; }
        .comment { color: #00aaaa; font-style: italic; }
        .number { color: #aa00aa; }
        .decorator { color: #aa00aa; }
        .class { color: #aa0000; font-weight: bold; }
        .linenum { color: #888888; border-right: 1px solid #ccc; margin-right: 10px; padding-right: 5px; user-select: none; display: inline-block; width: 30px; text-align: right;}
        .line { display: block; }
        """

    def export(self, lines, output_path):
        """Gera um arquivo HTML com o conteúdo fornecido."""
        html_content = ["<!DOCTYPE html>", "<html>", "<head>", "<meta charset='utf-8'>", "<style>", self.css, "</style>", "</head>", "<body>"]
        
        for i, line in enumerate(lines):
            formatted_line = self._format_line(line)
            html_content.append(f'<div class="line"><span class="linenum">{i+1}</span>{formatted_line}</div>')
            
        html_content.append("</body></html>")
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(html_content))
            return True
        except IOError:
            return False

    def _format_line(self, line):
        """Aplica syntax highlighting simples e retorna HTML."""
        result = []
        i = 0
        while i < len(line):
            # Strings
            if line[i] in "\"'":
                quote_char = line[i]
                j = i + 1
                while j < len(line) and line[j] != quote_char:
                    j += 1
                j = min(j + 1, len(line))
                token = line[i:j]
                result.append(f'<span class="string">{html.escape(token)}</span>')
                i = j
                continue
            
            # Comentários
            if line[i] == '#':
                token = line[i:]
                result.append(f'<span class="comment">{html.escape(token)}</span>')
                break # Fim da linha
            
            # Decoradores
            if line[i] == '@':
                j = i + 1
                while j < len(line) and (line[j].isalnum() or line[j] == '_'): j += 1
                token = line[i:j]
                result.append(f'<span class="decorator">{html.escape(token)}</span>')
                i = j
                continue

            # Palavras-chave e identificadores
            if line[i].isalpha() or line[i] == '_':
                j = i
                while j < len(line) and (line[j].isalnum() or line[j] == '_'): j += 1
                token = line[i:j]
                if token in self.PYTHON_KEYWORDS: result.append(f'<span class="keyword">{html.escape(token)}</span>')
                elif token == 'self' or token[0].isupper(): result.append(f'<span class="class">{html.escape(token)}</span>')
                else: result.append(html.escape(token))
                i = j
                continue

            # Outros caracteres
            result.append(html.escape(line[i]))
            i += 1
            
        return "".join(result)