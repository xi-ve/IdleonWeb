#!/usr/bin/env python3

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

class PluginWebAPI:
    def __init__(self, plugin_manager: PluginManager):
        self.plugin_manager = plugin_manager
        self.app = web.Application()
        self.setup_templates()
        self.setup_routes()
    
    def setup_templates(self):
        template_dir = Path(__file__).parent / 'templates'
        setup_jinja2(self.app, loader=FileSystemLoader(str(template_dir)))
    
    def setup_routes(self):
        self.app.router.add_post('/api/plugin-ui-action', self.handle_ui_action)
        self.app.router.add_post('/api/autocomplete', self.handle_autocomplete)
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
            
            use_tabs = len(all_ui_elements) > 1
            
            context = {
                'plugin_schemas': all_ui_elements,
                'use_tabs': use_tabs
            }
            
            if use_tabs:
                response = render_template('html/tabbed_interface.html', request, context)
            else:
                response = render_template('html/plugin_cards.html', request, context)
            
            return response
            
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