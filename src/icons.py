import os


# Mapeamento de ícones Nerd Fonts + cores lógicas
# Ordem: ícone, cor (nome da cor do curses ou seu sistema de cores)
ICONS_BY_EXTENSION = {
    # Python & relacionados
    "py":       ("", "YELLOW"),
    "pyc":      ("", "YELLOW"),
    "pyo":      ("", "YELLOW"),
    "ipynb":    ("", "YELLOW"),

    # JavaScript / TypeScript / Node
    "js":       ("", "YELLOW"),
    "jsx":      ("", "CYAN"),
    "ts":       ("", "BLUE"),
    "tsx":      ("", "BLUE"),
    "json":     ("", "YELLOW"),
    "jsonc":    ("", "YELLOW"),

    # Web
    "html":     ("", "RED"),
    "htm":      ("", "RED"),
    "css":      ("", "BLUE"),
    "scss":     ("", "MAGENTA"),
    "sass":     ("", "MAGENTA"),
    "less":     ("", "MAGENTA"),

    # Outras linguagens populares
    "c":        ("", "BLUE"),
    "h":        ("", "MAGENTA"),
    "cpp":      ("", "BLUE"),
    "hpp":      ("", "MAGENTA"),
    "java":     ("", "RED"),
    "kt":       ("", "MAGENTA"),     # Kotlin
    "go":       ("", "CYAN"),
    "rs":       ("", "RED"),          # Rust
    "rb":       ("", "RED"),          # Ruby
    "php":      ("", "MAGENTA"),

    # Config / Dados
    "yml":      ("", "MAGENTA"),
    "yaml":     ("", "MAGENTA"),
    "toml":     ("", "MAGENTA"),
    "ini":      ("", "MAGENTA"),
    "env":      ("", "GREEN"),
    "md":       ("", "CYAN"),
    "markdown": ("", "CYAN"),
    "txt":      ("", "WHITE"),
    "log":      ("", "WHITE"),

    # Shell / Scripts
    "sh":       ("", "GREEN"),
    "bash":     ("", "GREEN"),
    "zsh":      ("", "GREEN"),
    "fish":     ("", "GREEN"),

    # Outros arquivos comuns
    "gitignore":("", "WHITE"),
    "gitattributes":("", "WHITE"),
    "gitmodules":("", "WHITE"),
    "lock":     ("", "RED"),          # package-lock.json, yarn.lock, etc.
}


DEFAULT_ICON = ("", "WHITE")          # arquivo genérico
FOLDER_ICON  = ("", "CYAN")           # se for pasta (você pode usar isso em outro lugar)


def get_file_icon_and_color(filepath: str | None) -> tuple[str, str]:
    """
    Retorna (ícone, cor) para um caminho de arquivo.
    Retorna DEFAULT_ICON se não encontrar.
    """
    if not filepath:
        return DEFAULT_ICON

    filename = os.path.basename(filepath).lower()

    # Casos especiais por nome exato (tem prioridade sobre extensão)
    special_cases = {
        "makefile":         ("", "YELLOW"),
        "dockerfile":       ("", "CYAN"),
        "docker-compose.yml":("", "CYAN"),
        ".gitignore":       ("", "WHITE"),
        ".gitattributes":   ("", "WHITE"),
        ".gitmodules":      ("", "WHITE"),
        ".env":             ("", "GREEN"),
        "license":          ("", "YELLOW"),
        "readme.md":        ("", "CYAN"),
    }

    if filename in special_cases:
        return special_cases[filename]

    # Por extensão
    if '.' in filename:
        ext = filename.split('.')[-1]
        return ICONS_BY_EXTENSION.get(ext, DEFAULT_ICON)

    # Sem extensão → genérico
    return DEFAULT_ICON


def get_icon_info(name, is_dir):
    if is_dir:
        return FOLDER_ICON
    return get_file_icon_and_color(name)

def get_status(context) -> list[dict]:
    """
    Retorna componentes para a barra de status.
    Formato: lista de dicionários com 'text' e 'color_name'
    
    Exemplo de uso:
    status_parts = get_status({'filepath': current_file})
    """
    filepath = context.get('filepath')
    if not filepath:
        return [{'text': '[sem arquivo]', 'color_name': 'GRAY'}]

    icon, color = get_file_icon_and_color(filepath)
    filename = os.path.basename(filepath)

    # Você pode customizar o formato aqui
    # Opção 1: só ícone + extensão
    # Opção 2: ícone + nome completo (mais comum em editores modernos)
    
    # Sugestão moderna (parecido com lualine / airline):
    return [
        {'text': f"{icon} ",               'color_name': color},
        {'text': filename,                 'color_name': 'WHITE'},
        # Se quiser extensão separada:
        # {'text': f"  .{ext.upper()}",   'color_name': 'GRAY'}  
    ]


# Exemplo de uso (teste)
if __name__ == "__main__":
    tests = [
        "/home/user/main.py",
        "index.html",
        "config.yml",
        "Dockerfile",
        ".gitignore",
        "script.sh",
        "documento sem extensão",
        None
    ]

    for path in tests:
        status = get_status({'filepath': path})
        print(f"{path:40} → ", end="")
        for part in status:
            print(f"[{part['color_name']}] {part['text']}", end="")
        print()