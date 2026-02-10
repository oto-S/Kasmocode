# /home/johnb/tasma-code-absulut/src/statusbar_plugin_manager.py
import os
import importlib.util
import sys

class StatusBarPluginManager:
    def __init__(self, plugin_dir="plugins/statu_bar-plugins"):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.plugin_dir = os.path.join(base_dir, plugin_dir)
        self.plugins = []
        self.color_modifiers = []
        if not os.path.exists(self.plugin_dir):
            try:
                os.makedirs(self.plugin_dir)
            except OSError:
                pass

    def load_plugins(self):
        if not os.path.isdir(self.plugin_dir):
            return

        for item in sorted(os.listdir(self.plugin_dir)):
            path = os.path.join(self.plugin_dir, item)
            if os.path.isfile(path) and item.endswith(".py"):
                try:
                    plugin_name = f"statusbar_plugin_{item[:-3]}"
                    spec = importlib.util.spec_from_file_location(plugin_name, path)
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[plugin_name] = module
                    spec.loader.exec_module(module)
                    if hasattr(module, "get_status"):
                        self.plugins.append(getattr(module, "get_status"))
                    if hasattr(module, "get_message_color_attr"):
                        self.color_modifiers.append(getattr(module, "get_message_color_attr"))
                except Exception:
                    pass

    def get_all_statuses(self, context):
        statuses = []
        # statuses will be a list of lists of dicts
        for plugin_func in self.plugins:
            try:
                status = plugin_func(context)
                if status:
                    # Normalize to a list of dicts
                    if isinstance(status, str):
                        statuses.append([{'text': status, 'color_name': None}])
                    elif isinstance(status, list): # Assumes list of dicts
                        statuses.append(status)
            except Exception:
                pass
        
        # Flatten and add separators
        flat_list = []
        for i, group in enumerate(statuses):
            flat_list.extend(group)
            if i < len(statuses) - 1:
                flat_list.append({'text': ' | ', 'color_name': None})
        return flat_list

    def get_message_color(self, status_message, ui):
        """
        Executa todos os modificadores de cor e retorna o primeiro atributo de cor válido.
        """
        for modifier_func in self.color_modifiers:
            try:
                attr = modifier_func(status_message, ui)
                if attr is not None:
                    return attr # Retorna o primeiro que encontrar
            except Exception:
                pass
        return None # Retorna None se nenhum plugin retornar uma cor