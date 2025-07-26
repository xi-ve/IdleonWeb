import json
from typing import Dict, List, Any
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

class WebUIGenerator:
    def __init__(self):
        template_dir = Path(__file__).parent / 'templates'
        self.jinja_env = Environment(loader=FileSystemLoader(str(template_dir)))
    
    def generate_ui_html(self, plugin_schemas: Dict[str, Dict[str, Any]]) -> str:
        use_tabs = len(plugin_schemas) > 1
        
        if use_tabs:
            template = self.jinja_env.get_template('html/tabbed_interface.html')
        else:
            template = self.jinja_env.get_template('html/plugin_cards.html')
        
        import sys
        sys.path.append(str(Path(__file__).parent.parent))
        from config_manager import config_manager
        config_manager.reload()
        
        context = {
            'plugin_schemas': plugin_schemas,
            'use_tabs': use_tabs,
            'plugin_configs': config_manager.get_all_plugin_configs()
        }
        
        return template.render(**context)
    
    def save_ui_file(self, plugin_schemas: Dict[str, Dict[str, Any]], output_path: str = "webui/html/plugin_ui.html") -> None:
        html_content = self.generate_ui_html(plugin_schemas)
        
        import os
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Plugin UI saved to: {output_path}")

if __name__ == "__main__":
    generator = WebUIGenerator()
    
    example_schemas = {
        "ui_example_plugin": {
            "plugin_info": {
                "name": "UI Example Plugin",
                "description": "Example plugin demonstrating UI element decorators",
                "version": "1.0.0"
            },
            "categories": {
                "General Settings": [
                    {
                        "name": "enable_debug",
                        "type": "toggle",
                        "label": "Enable Debug Mode",
                        "description": "Enable debug logging for this plugin",
                        "config_key": "debug",
                        "default_value": False,
                        "order": 1
                    }
                ]
            }
        }
    }
    
    generator.save_ui_file(example_schemas) 