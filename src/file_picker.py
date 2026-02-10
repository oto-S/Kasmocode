import curses
import os

class FilePicker:
    def __init__(self, ui, start_path=".", allowed_extensions=None):
        self.ui = ui
        self.current_path = os.path.abspath(start_path)
        self.allowed_extensions = allowed_extensions # Ex: ['.json', '.zip']
        self.selected_file = None
        self.active = True
        self.items = []
        self.selected_idx = 0
        self.scroll_offset = 0
        self.refresh_items()

    def refresh_items(self):
        try:
            items = os.listdir(self.current_path)
            dirs = []
            files = []
            for item in items:
                if item.startswith('.'): continue # Ignora ocultos por simplicidade
                full_path = os.path.join(self.current_path, item)
                if os.path.isdir(full_path):
                    dirs.append(item)
                else:
                    if self.allowed_extensions:
                        if any(item.lower().endswith(ext) for ext in self.allowed_extensions):
                            files.append(item)
                    else:
                        files.append(item)
            
            dirs.sort()
            files.sort()
            
            self.items = [("..", True)] + [(d, True) for d in dirs] + [(f, False) for f in files]
            self.selected_idx = 0
            self.scroll_offset = 0
        except OSError:
            self.items = [("..", True)]

    def run(self):
        self.ui.stdscr.timeout(-1) # Garante modo bloqueante (espera input)
        while self.active:
            self.draw()
            key = self.ui.get_input()
            self.handle_input(key)
        return self.selected_file

    def draw(self):
        h, w = self.ui.height, self.ui.width
        win_h = min(20, h - 4)
        win_w = min(80, w - 6)
        win_y = (h - win_h) // 2
        win_x = (w - win_w) // 2
        
        if win_h < 3 or win_w < 10: return # Evita erro se terminal for muito pequeno

        win = curses.newwin(win_h, win_w, win_y, win_x)
        win.bkgd(' ', curses.color_pair(5))
        win.box()
        
        win.addstr(0, 2, " Selecionar Arquivo ", curses.A_BOLD)
        
        path_display = f" {self.current_path} "
        if len(path_display) > win_w - 2:
            path_display = "..." + path_display[-(win_w-6):]
        win.addstr(1, 1, path_display, curses.A_REVERSE)
        
        list_y = 2
        max_items = win_h - 3
        
        if self.selected_idx < self.scroll_offset: self.scroll_offset = self.selected_idx
        if self.selected_idx >= self.scroll_offset + max_items: self.scroll_offset = self.selected_idx - max_items + 1

        for i in range(max_items):
            data_idx = self.scroll_offset + i
            if data_idx >= len(self.items): break
            
            name, is_dir = self.items[data_idx]
            display_name = name + "/" if is_dir else name
            
            style = curses.A_REVERSE if data_idx == self.selected_idx else curses.A_NORMAL
            win.addstr(list_y + i, 2, display_name[:win_w-4].ljust(win_w - 4), style)

        win.refresh()

    def handle_input(self, key):
        key_code = key if isinstance(key, int) else ord(key)

        if key_code == 27: # Esc
            self.active = False
            self.selected_file = None
        elif key_code == curses.KEY_UP:
            self.selected_idx = max(0, self.selected_idx - 1)
        elif key_code == curses.KEY_DOWN:
            self.selected_idx = min(len(self.items) - 1, self.selected_idx + 1)
        elif key_code in (10, 13): # Enter
            if not self.items: return
            name, is_dir = self.items[self.selected_idx]
            
            if name == "..":
                self.current_path = os.path.dirname(self.current_path)
                self.refresh_items()
            elif is_dir:
                self.current_path = os.path.join(self.current_path, name)
                self.refresh_items()
            else:
                self.selected_file = os.path.join(self.current_path, name)
                self.active = False