#!/usr/bin/env python3

import asyncio
import json
from aiohttp import web, ClientSession
from plugin_system import PluginManager
from webui.web_ui_generator import WebUIGenerator

class PluginWebAPI:
    def __init__(self, plugin_manager: PluginManager):
        self.plugin_manager = plugin_manager
        self.app = web.Application()
        self.setup_routes()
    
    def setup_routes(self):
        self.app.router.add_post('/api/plugin-ui-action', self.handle_ui_action)
        self.app.router.add_post('/api/autocomplete', self.handle_autocomplete)
        self.app.router.add_get('/', self.serve_ui)
    
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
            print(f"Error handling autocomplete request: {e}")
            return web.json_response({'error': str(e)})
    
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
    
    async def serve_ui(self, request):
        try:
            from config_manager import config_manager
            config_manager.reload()
            
            all_ui_elements = self.plugin_manager.get_all_ui_elements()
            
            ui_schemas = {}
            for plugin_name, plugin_data in all_ui_elements.items():
                ui_schemas[plugin_name] = {
                    "plugin_info": plugin_data.get("plugin_info", {}),
                    "categories": plugin_data.get("categories", {})
                }
            
            generator = WebUIGenerator()
            html_content = generator.generate_ui_html(ui_schemas)
            
            return web.Response(text=html_content, content_type='text/html')
            
        except Exception as e:
            return web.json_response({
                'error': f'Error generating UI: {str(e)}'
            }, status=500)
    
    async def start_server(self, host='localhost', port=8080):
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, host, port)
        await site.start()
        
        print(f"Plugin UI server started at http://{host}:{port}")
        print("Press Ctrl+C to stop the server")
        
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