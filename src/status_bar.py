# /home/johnb/tasma-code-absulut/src/status_bar.py
import curses
from statusbar_plugin_manager import StatusBarPluginManager

class StatusBar:
    def __init__(self):
        self.plugin_manager = StatusBarPluginManager()
        self.plugin_manager.load_plugins()

    def draw(self, ui, active_editor, active_split, system_info, status_message, active_filepath):
        height, width = ui.height, ui.width
        stdscr = ui.stdscr
        
        # --- Partes da Direita ---
        plugin_context = {'filepath': active_filepath, 'status_message': status_message, 'editor': active_editor}
        plugin_statuses = self.plugin_manager.get_all_statuses(plugin_context)
        
        # --- Partes da Esquerda ---
        pct = int((active_editor.cy + 1) / max(1, len(active_editor.lines)) * 100)
        error_msg = f" [ERR: {active_editor.linter_errors[active_editor.cy][0]}]" if active_editor.cy in active_editor.linter_errors else ""
        left_part_1 = f" {system_info} | Split:{active_split+1} | Ln {active_editor.cy + 1}/{len(active_editor.lines)} ({pct}%) | Col {active_editor.cx + 1} | {'[+] ' if active_editor.is_modified else ''}"
        
        try:
            # 1. Desenha a barra de fundo
            statusbar_pair = getattr(ui, 'statusbar_pair', curses.A_REVERSE)
            stdscr.attron(statusbar_pair)
            stdscr.addstr(height - 1, 0, " " * (width - 1))
            
            # 2. Desenha partes da esquerda
            current_x = 0
            stdscr.addstr(height - 1, current_x, left_part_1)
            current_x += len(left_part_1)

            # Desenha a mensagem de status com cor customizada
            if status_message:
                message_attr = self.plugin_manager.get_message_color(status_message, ui)
                if message_attr:
                    stdscr.attroff(statusbar_pair)
                    stdscr.addstr(height - 1, current_x, status_message, message_attr)
                    stdscr.attron(statusbar_pair)
                else:
                    stdscr.addstr(height - 1, current_x, status_message)
                current_x += len(status_message)

            # Desenha a mensagem de erro do linter
            if error_msg:
                error_color = ui.statusbar_icon_pairs.get("RED", curses.A_BOLD)
                stdscr.attroff(statusbar_pair)
                stdscr.addstr(height - 1, current_x, error_msg, error_color)
                stdscr.attron(statusbar_pair)
                current_x += len(error_msg)
            
            # 3. Desenha partes da direita
            if plugin_statuses:
                total_right_len = sum(len(s['text']) for s in plugin_statuses)
                current_x_right = width - total_right_len - 1
            
                if current_x < current_x_right:
                    for status_part in plugin_statuses:
                        text = status_part['text']
                        color_name = status_part['color_name']
                        
                        part_attr = statusbar_pair
                        if color_name:
                            icon_pairs = getattr(ui, 'statusbar_icon_pairs', {})
                            part_attr = icon_pairs.get(color_name, statusbar_pair)
                        
                        if part_attr != statusbar_pair:
                            stdscr.attroff(statusbar_pair)
                            stdscr.addstr(height - 1, current_x_right, text, part_attr)
                            stdscr.attron(statusbar_pair)
                        else:
                            stdscr.addstr(height - 1, current_x_right, text, part_attr)
                        
                        current_x_right += len(text)
            
            stdscr.attroff(statusbar_pair)
        except curses.error: pass
