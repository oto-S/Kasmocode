# /home/johnb/tasma-code-absulut/plugins/chattovex/chat_ui.py
import curses
import textwrap
import time

class ChatUI:
    def __init__(self):
        self.history = [] # Lista de (role, text)
        self.input_buffer = ""
        self.scroll_offset = 0
        self.spinner_frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.on_message_added = None # Callback para persistência

    def add_message(self, role, text):
        self.history.append((role, text))
        if self.on_message_added:
            self.on_message_added()
        # Auto-scroll para o final
        self.scroll_offset = 0 

    def scroll_up(self):
        self.scroll_offset += 1

    def scroll_down(self):
        if self.scroll_offset > 0:
            self.scroll_offset -= 1

    def draw(self, stdscr, x, y, h, w, is_active, is_processing=False):
        """Desenha o histórico de chat e a caixa de entrada com nova lógica de buffer virtual."""
        # 1. Limpeza e Bordas
        for i in range(h):
            try:
                stdscr.addstr(y + i, x, " " * w, curses.color_pair(0))
                stdscr.addch(y + i, x, '│', curses.color_pair(0) | curses.A_DIM)
            except: pass

        # 2. Cabeçalho
        header_title = " Chattovex AI "
        try:
            stdscr.addstr(y, x + 1, "─" * (w - 1), curses.color_pair(0) | curses.A_DIM)
            title_pos = x + 1 + max(0, (w - 2 - len(header_title)) // 2)
            stdscr.addstr(y, title_pos, header_title, curses.color_pair(6) | curses.A_BOLD)
        except: pass

        # 3. Definição de Áreas
        input_height = 3
        chat_height = h - input_height - 1
        chat_width = w - 3 # Margem esquerda (2) + direita (1)

        # 4. Construção do Buffer Virtual de Linhas
        lines_buffer = [] # (texto, atributo, alinhamento_direita)
        
        temp_history = list(self.history)
        if is_processing:
            frame = self.spinner_frames[int(time.time() * 10) % len(self.spinner_frames)]
            temp_history.append(("system", f"{frame} Pensando..."))

        for role, text in temp_history:
            is_user = (role == "user")
            is_system = (role == "system")
            
            # Configuração de Estilo
            if is_user:
                header = "You"
                header_attr = curses.color_pair(2) | curses.A_BOLD
                align_right = True
            elif is_system:
                header = "System"
                header_attr = curses.color_pair(3) | curses.A_BOLD
                align_right = False
            else:
                header = "AI"
                header_attr = curses.color_pair(6) | curses.A_BOLD
                align_right = False

            # Adiciona Cabeçalho da Mensagem
            lines_buffer.append((f"[{header}]", header_attr, align_right))

            # Processa Conteúdo
            raw_lines = text.splitlines()
            in_code = False
            
            for line in raw_lines:
                # Detecção de bloco de código
                if line.strip().startswith("```"):
                    in_code = not in_code
                    lines_buffer.append(("─" * chat_width, curses.color_pair(0) | curses.A_DIM, False))
                    continue
                
                # Atributos da linha
                line_attr = curses.color_pair(0)
                if in_code:
                    line_attr = curses.color_pair(3) # Amarelo para código
                elif is_system:
                    line_attr = curses.color_pair(3) | curses.A_DIM

                # Quebra de linha (Word Wrap)
                wrapped = textwrap.wrap(line, chat_width)
                if not wrapped: wrapped = [""]
                
                for wrapped_line in wrapped:
                    lines_buffer.append((wrapped_line, line_attr, False)) # Conteúdo sempre à esquerda para leitura

            # Espaçador entre mensagens
            lines_buffer.append(("", 0, False))

        # 5. Lógica de Scroll e Renderização
        total_lines = len(lines_buffer)
        
        # Clamp scroll
        max_scroll = max(0, total_lines - chat_height)
        if self.scroll_offset > max_scroll:
            self.scroll_offset = max_scroll
        
        # Define janela de visualização (de baixo para cima logicamente)
        # scroll_offset 0 = ver o final
        start_idx = max(0, total_lines - chat_height - self.scroll_offset)
        end_idx = min(total_lines, start_idx + chat_height)
        
        render_y = y + 1
        
        for i in range(start_idx, end_idx):
            text, attr, align_right = lines_buffer[i]
            
            draw_x = x + 2
            if align_right:
                draw_x = x + w - 1 - len(text)
                if draw_x < x + 2: draw_x = x + 2
            
            try:
                stdscr.addstr(render_y, draw_x, text, attr)
            except: pass
            render_y += 1

        # Indicadores de Scroll
        if self.scroll_offset > 0:
            try: stdscr.addch(y + h - input_height - 1, x + w - 1, 'v', curses.color_pair(0) | curses.A_BOLD)
            except: pass
        if start_idx > 0:
             try: stdscr.addch(y + 1, x + w - 1, '^', curses.color_pair(0) | curses.A_BOLD)
             except: pass

        # 6. Área de Input
        input_y = y + h - input_height
        try:
            # Separador
            stdscr.addstr(input_y, x + 1, "─" * (w - 1), curses.color_pair(0) | curses.A_DIM)
            
            # Prompt
            prompt = ">>> "
            stdscr.addstr(input_y + 1, x + 2, prompt, curses.color_pair(2) | curses.A_BOLD)
            
            # Texto do Input
            available_w = w - 2 - len(prompt) - 1
            display_input = self.input_buffer
            # Scroll horizontal do input
            if len(display_input) > available_w:
                display_input = display_input[-available_w:]
            
            stdscr.addstr(input_y + 1, x + 2 + len(prompt), display_input, curses.color_pair(0))
            
            # Cursor
            if is_active:
                cursor_x = x + 2 + len(prompt) + len(display_input)
                if cursor_x < x + w:
                    if int(time.time() * 2) % 2 == 0: # Blink
                        stdscr.addch(input_y + 1, cursor_x, '█', curses.color_pair(0))
        except: pass

    def draw_menu(self, stdscr, x, y, h, w, options, selected_idx):
        """Desenha o menu de contexto (Ctrl+M)."""
        menu_h = len(options) + 2
        menu_w = 26
        menu_y = y + (h - menu_h) // 2
        menu_x = x + (w - menu_w) // 2
        
        # Cor do menu (Pair 5 é usado para UI/Sidebar)
        menu_attr = curses.color_pair(5)

        try:
            # Desenha caixa preenchida e borda
            stdscr.addstr(menu_y, menu_x, "┌" + "─" * (menu_w - 2) + "┐", menu_attr)
            for i in range(len(options)):
                # Preenche o fundo da linha
                stdscr.addstr(menu_y + i + 1, menu_x, "│" + " " * (menu_w - 2) + "│", menu_attr)
            stdscr.addstr(menu_y + len(options) + 1, menu_x, "└" + "─" * (menu_w - 2) + "┘", menu_attr)
            
            # Título
            stdscr.addstr(menu_y, menu_x + 2, " Menu (Ctrl+L) ", menu_attr | curses.A_BOLD)

            # Opções
            for i, (label, _) in enumerate(options):
                style = curses.color_pair(4) | curses.A_REVERSE if i == selected_idx else menu_attr
                stdscr.addstr(menu_y + i + 1, menu_x + 2, label.ljust(menu_w - 4), style)

        except: pass
