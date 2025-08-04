from plugin_system import PluginBase, ui_toggle, ui_button, ui_slider, plugin_command, js_export
from config_manager import config_manager

class ExamplePlugin(PluginBase):
    VERSION = "1.0.0"
    DESCRIPTION = "A simple example plugin"
    PLUGIN_ORDER = 5  # This plugin will appear as #5 in the dropdown

    def __init__(self, config=None):
        super().__init__(config or {})
        self.name = 'example_plugin'

    # Required methods (minimal implementation)
    async def cleanup(self): pass
    async def update(self): pass
    async def on_config_changed(self, config): 
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)
    async def on_game_ready(self): pass

    # Simple UI Elements
    @ui_toggle(
        label="Enable Feature",
        description="Turn this feature on/off",
        config_key="enabled",
        default_value=False
    )
    async def enable_feature_ui(self, value=None):
        if value is not None:
            self.config["enabled"] = value
            self.save_to_global_config()
        return f"Feature {'enabled' if self.config.get('enabled', False) else 'disabled'}"

    @ui_slider(
        label="Speed",
        description="Adjust speed (1-10)",
        config_key="speed",
        default_value=5,
        min_value=1,
        max_value=10
    )
    async def speed_ui(self, value=None):
        if value is not None:
            self.config["speed"] = value
            self.save_to_global_config()
        return f"Speed set to {self.config.get('speed', 5)}"

    @ui_button(
        label="Test Action",
        description="Click to test the plugin"
    )
    async def test_action_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = self.run_js_export('test_action_js', self.injector)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "ERROR: No injector available - run 'inject' first"

    # CLI Command
    @plugin_command(help="Test the plugin")
    async def test(self, injector=None, **kwargs):
        return self.run_js_export('test_action_js', injector)

    # JavaScript Export
    @js_export()
    def test_action_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (ctx && ctx["com.stencyl.Engine"]) {
                return "Plugin working correctly!";
            } else {
                return "Game not ready";
            }
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

plugin_class = ExamplePlugin 