# /home/johnb/tasma-code-absulut/plugins/chattovex/__init__.py
import curses

class AIChatPlugin:
    def __init__(self):
        self.is_visible = False
        self.name = "Chattovex"

    def register(self, context):
        """Registra o plugin na UI."""
        self.ui = context.get('ui')
        if self.ui:
            self.ui.right_sidebar_plugin = self

    def draw(self, stdscr, x, y, h, w):
        """Desenha a barra lateral direita."""
        try:
            # Desenha borda esquerda
            for i in range(h):
                try:
                    stdscr.addch(y + i, x, '│', curses.color_pair(5))
                except curses.error: pass
            
            # Título
            title = f" {self.name} "
            try:
                stdscr.addstr(y, x + 1, title[:w-1], curses.A_BOLD | curses.A_REVERSE)
                stdscr.addstr(y + 2, x + 2, "Chat IA (Futuro)", curses.color_pair(5))
                stdscr.addstr(y + 3, x + 2, "----------------", curses.color_pair(5))
                stdscr.addstr(y + 4, x + 2, "Aguardando API...", curses.color_pair(5))
            except curses.error: pass
        except curses.error:
            pass

# Instância global para ser carregada pelo PluginManager
plugin = AIChatPlugin()

def register(context):
    plugin.register(context)