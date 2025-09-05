#!/usr/bin/env python

import asyncio
import json
import os
import sys
from pathlib import Path
from aiohttp import web, ClientSession
from aiohttp_jinja2 import setup as setup_jinja2, render_template
from jinja2 import FileSystemLoader

sys.path.append(str(Path(__file__).parent.parent))
from plugin_system import PluginManager
from config_manager import config_manager

class PluginWebAPI:
    def __init__(self, plugin_manager: PluginManager):
        self.plugin_manager = plugin_manager
        self.app = web.Application()
        self.setup_templates()
        self.setup_routes()
        
        config_manager.reload()
        self.debug = config_manager.get_path('debug', False)
    
    def setup_templates(self):
        template_dir = Path(__file__).parent / 'templates'
        setup_jinja2(self.app, loader=FileSystemLoader(str(template_dir)))
    
    def setup_routes(self):
        self.app.router.add_post('/api/plugin-ui-action', self.handle_ui_action)
        self.app.router.add_post('/api/autocomplete', self.handle_autocomplete)
        self.app.router.add_post('/api/dark-mode', self.handle_dark_mode)
        self.app.router.add_get('/', self.serve_ui)
        
        static_dir = Path(__file__).parent / 'templates'
        self.app.router.add_static('/static', static_dir)
    
    async def handle_ui_action(self, request):
        try:
            data = await request.json()
            plugin_name = data.get('plugin_name')
            element_name = data.get('element_name')
            value = data.get('value')
            
            if not plugin_name or not element_name:
                return web.json_response({
                    'error': 'Missing plugin_name or element_name'
                }, status=400)
            
            result = await self.plugin_manager.execute_ui_action(
                plugin_name, element_name, value
            )
            
            # Reload config to get the latest values after the action
            config_manager.reload()
            
            return web.json_response(result)
            
        except Exception as e:
            return web.json_response({
                'error': f'Error handling UI action: {str(e)}'
            }, status=500)
    
    async def handle_autocomplete(self, request):
        try:
            data = await request.json()
            plugin_name = data.get('plugin_name')
            element_name = data.get('element_name')
            query = data.get('query', '')
            
            if not plugin_name or not element_name:
                return web.json_response({'error': 'Missing plugin_name or element_name'})
            
            plugin = self.plugin_manager.get_plugin(plugin_name)
            if not plugin:
                return web.json_response({'error': f'Plugin {plugin_name} not found'})
            
            autocomplete_method_name = f'get_{element_name}_autocomplete'
            if hasattr(plugin, autocomplete_method_name):
                autocomplete_method = getattr(plugin, autocomplete_method_name)
                if asyncio.iscoroutinefunction(autocomplete_method):
                    suggestions = await autocomplete_method(query)
                else:
                    suggestions = autocomplete_method(query)
                
                return web.json_response(suggestions)
            else:
                if hasattr(plugin, 'get_item_autocomplete'):
                    if asyncio.iscoroutinefunction(plugin.get_item_autocomplete):
                        suggestions = await plugin.get_item_autocomplete(query)
                    else:
                        suggestions = plugin.get_item_autocomplete(query)
                    return web.json_response(suggestions)
                else:
                    return web.json_response([])
                    
        except Exception as e:
            if self.debug:
                print(f"Error handling autocomplete request: {e}")
            return web.json_response({'error': str(e)})
    
    async def handle_dark_mode(self, request):
        try:
            data = await request.json()
            enabled = data.get('enabled', False)
            
            # Update the configuration
            config_manager.set_darkmode(enabled)
            
            return web.json_response({'success': True, 'darkmode': enabled})
            
        except Exception as e:
            if self.debug:
                print(f"Error handling dark mode request: {e}")
            return web.json_response({'error': str(e)}, status=500)
    
    async def get_ui_schemas(self, request):
        try:
            schemas = self.plugin_manager.get_all_ui_schemas()
            return web.json_response(schemas)
        except Exception as e:
            return web.json_response({
                'error': f'Error getting UI schemas: {str(e)}'
            }, status=500)
    
    async def get_ui_elements(self, request):
        try:
            elements = self.plugin_manager.get_all_ui_elements()
            return web.json_response(elements)
        except Exception as e:
            return web.json_response({
                'error': f'Error getting UI elements: {str(e)}'
            }, status=500)
    
    def _get_current_plugin_configs(self):
        """Get current plugin configs from config manager to ensure consistency."""
        # Reload config from file to get latest values
        config_manager.reload()
        
        # Get stored configs from file - this is what plugins use with config_manager.get_path()
        stored_configs = config_manager.get_all_plugin_configs()
        
        # Return the stored configs (which are what plugins actually use)
        return stored_configs

    async def serve_ui(self, request):
        try:
            config_manager.reload()
            
            all_ui_elements = self.plugin_manager.get_all_ui_elements()
            if self.debug:
                print(f"DEBUG: Found {len(all_ui_elements)} plugins with UI elements")
                for plugin_name, data in all_ui_elements.items():
                    print(f"DEBUG: Plugin {plugin_name} has {len(data.get('categories', {}))} categories")
            
            use_tabs = len(all_ui_elements) > 1
            if self.debug:
                print(f"DEBUG: Using tabs: {use_tabs}")
                print(f"DEBUG: Number of UI elements: {len(all_ui_elements)}")
                print(f"DEBUG: UI element names: {list(all_ui_elements.keys())}")
            
            context = {
                'plugin_schemas': all_ui_elements,
                'use_tabs': use_tabs,
                'plugin_configs': self._get_current_plugin_configs(),
                'darkmode': config_manager.get_darkmode()
            }
            
            # Always create sorted_plugin_schemas for template compatibility
            # First, collect all plugins with their order information
            plugins_with_order = []
            for plugin_name, schema in all_ui_elements.items():
                # Use the plugin's category from plugin_info, or 'General' if not defined
                plugin_category = schema.get('plugin_info', {}).get('category', 'General')
                
                # Add category to plugin info if not already present
                if 'plugin_info' not in schema:
                    schema['plugin_info'] = {}
                schema['plugin_info']['category'] = plugin_category
                
                # Get plugin order from the plugin instance
                plugin_instance = self.plugin_manager.get_plugin(plugin_name)
                plugin_order = getattr(plugin_instance, 'PLUGIN_ORDER', 999) if plugin_instance else 999
                
                plugins_with_order.append({
                    'name': plugin_name,
                    'category': plugin_category,
                    'order': plugin_order,
                    'schema': schema
                })
            
            # Sort plugins by their order
            plugins_with_order.sort(key=lambda x: x['order'])
            
            # Create a sorted dictionary of plugin schemas for the template
            sorted_plugin_schemas = {}
            for plugin_info in plugins_with_order:
                plugin_name = plugin_info['name']
                if plugin_name in all_ui_elements:
                    sorted_plugin_schemas[plugin_name] = all_ui_elements[plugin_name]
            
            context['sorted_plugin_schemas'] = sorted_plugin_schemas
            
            # Ensure sorted_plugin_schemas is always available as a fallback
            if 'sorted_plugin_schemas' not in context:
                context['sorted_plugin_schemas'] = all_ui_elements
            
            try:
                if use_tabs:
                    if self.debug:
                        print("DEBUG: Rendering categorized interface template")
                        print(f"DEBUG: use_tabs value: {use_tabs}")
                        print(f"DEBUG: Number of plugins: {len(all_ui_elements)}")
                    
                    plugin_categories = {}
                    for plugin_info in plugins_with_order:
                        plugin_category = plugin_info['category']
                        plugin_name = plugin_info['name']
                        if plugin_category not in plugin_categories:
                            plugin_categories[plugin_category] = []
                        plugin_categories[plugin_category].append(plugin_name)

                    def _category_sort_key(cat: str):
                        import re
                        m = re.match(r"^World\s+(\d+)$", cat.strip(), flags=re.IGNORECASE)
                        if m:
                            return (0, int(m.group(1)))
                        return (1, cat.lower())

                    ordered_categories_items = sorted(plugin_categories.items(), key=lambda kv: _category_sort_key(kv[0]))
                    ordered_plugin_categories = {k: v for k, v in ordered_categories_items}
                    context['plugin_categories'] = ordered_plugin_categories
                    
                    # Update the plugin schemas to include order information
                    for plugin_info in plugins_with_order:
                        plugin_name = plugin_info['name']
                        plugin_order = plugin_info['order']
                        if plugin_name in all_ui_elements:
                            if 'plugin_info' not in all_ui_elements[plugin_name]:
                                all_ui_elements[plugin_name]['plugin_info'] = {}
                            all_ui_elements[plugin_name]['plugin_info']['order'] = plugin_order
                    
                    # Keep the original plugin_schemas for JavaScript compatibility
                    context['plugin_schemas'] = all_ui_elements
                    
                    if self.debug:
                        print(f"DEBUG: Template context keys: {list(context.keys())}")
                        print(f"DEBUG: plugin_schemas count: {len(context['plugin_schemas'])}")
                        print(f"DEBUG: sorted_plugin_schemas count: {len(context['sorted_plugin_schemas'])}")
                        print(f"DEBUG: plugin_categories: {context['plugin_categories']}")
                    
                    if self.debug:
                        print("DEBUG: About to render categorized_interface.html")
                        print(f"DEBUG: Context keys before render: {list(context.keys())}")
                    response = render_template('html/categorized_interface.html', request, context)
                else:
                    if self.debug:
                        print("DEBUG: Rendering plugin cards template")
                        print(f"DEBUG: Context keys in else branch: {list(context.keys())}")
                        print(f"DEBUG: sorted_plugin_schemas available: {'sorted_plugin_schemas' in context}")
                    if self.debug:
                        print("DEBUG: About to render plugin_cards.html")
                        print(f"DEBUG: Context keys before render: {list(context.keys())}")
                    response = render_template('html/plugin_cards.html', request, context)
                
                if self.debug:
                    print(f"DEBUG: Response type: {type(response)}")
                    print(f"DEBUG: Response content length: {len(str(response))}")
                return response
            except Exception as e:
                if self.debug:
                    print(f"DEBUG: Template rendering error: {e}")
                    import traceback
                    traceback.print_exc()
                return web.json_response({
                    'error': f'Template rendering error: {str(e)}'
                }, status=500)
            
        except Exception as e:
            if self.debug:
                print(f"DEBUG: Error in serve_ui: {e}")
                import traceback
                traceback.print_exc()
            return web.json_response({
                'error': f'Error generating UI: {str(e)}'
            }, status=500)
    
    async def start_server(self, host='localhost', port=None):
        if port is None:
            port = config_manager.get_webui_port()
        
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, host, port)
        await site.start()
        
        if self.debug:
            print("DEBUG: Web API integration debug mode enabled")
        
        try:
            await asyncio.Future()
        except KeyboardInterrupt:
            await runner.cleanup()

async def main():
    plugin_manager = PluginManager(['ui_example_plugin'])
    
    await plugin_manager.load_plugins(None, global_debug=True)
    
    api = PluginWebAPI(plugin_manager)
    await api.start_server()

if __name__ == "__main__":
    asyncio.run(main()) 