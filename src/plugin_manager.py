# /home/johnb/tasma-code-absulut/src/plugin_manager.py
import os
import importlib.util
import sys

class PluginManager:
    def __init__(self, plugin_dir="plugins"):
        self.plugin_dir = plugin_dir
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir)

    def load_plugins(self, context):
        """
        Carrega plugins do diretório.
        Context é um dict {'editor': editor, 'ui': ui, ...}
        """
        if not os.path.exists(self.plugin_dir):
            return

        for item in os.listdir(self.plugin_dir):
            path = os.path.join(self.plugin_dir, item)
            module = None
            
            if os.path.isfile(path) and item.endswith(".py"):
                plugin_name = item[:-3]
                spec = importlib.util.spec_from_file_location(plugin_name, path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
            
            elif os.path.isdir(path):
                init_path = os.path.join(path, "__init__.py")
                if os.path.exists(init_path):
                    plugin_name = item
                    spec = importlib.util.spec_from_file_location(plugin_name, init_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

            if module and hasattr(module, "register"):
                try:
                    module.register(context)
                except Exception as e:
                    print(f"Erro ao registrar plugin {item}: {e}")