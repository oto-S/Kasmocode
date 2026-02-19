import os

# Mapeamento de ícones e cores (Nerd Fonts)
# Cores disponíveis: YELLOW, GREEN, CYAN, RED, BLUE, MAGENTA, WHITE, BLACK
ICONS = {
    "py": ("", "YELLOW"),
    "js": ("", "YELLOW"),
    "ts": ("", "BLUE"),
    "html": ("", "RED"),
    "css": ("", "BLUE"),
    "json": ("", "YELLOW"),
    "md": ("", "CYAN"),
    "txt": ("", "WHITE"),
    "c": ("", "BLUE"),
    "cpp": ("", "BLUE"),
    "h": ("", "MAGENTA"),
    "java": ("", "RED"),
    "rs": ("", "RED"),
    "go": ("", "CYAN"),
    "sh": ("", "GREEN"),
    "git": ("", "RED"),
    "yml": ("", "MAGENTA"),
    "toml": ("", "MAGENTA"),
}

DEFAULT_ICON = ""

def get_status(context):
    """
    Retorna o ícone e a extensão do arquivo para a barra de status.
    """
    filepath = context.get('filepath')
    if not filepath:
        return None

    filename = os.path.basename(filepath)
    ext = filename.split('.')[-1].lower() if '.' in filename else ""
    
    icon, color = ICONS.get(ext, (DEFAULT_ICON, "WHITE"))
    
    # Retorna lista de componentes: [{'text': '...', 'color_name': '...'}]
    return [
        {'text': f"{icon} {ext.upper()}", 'color_name': color}
    ]