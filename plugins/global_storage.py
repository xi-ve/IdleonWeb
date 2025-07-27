from plugin_system import PluginBase, ui_toggle, plugin_command, js_export
from config_manager import config_manager

class GlobalStoragePlugin(PluginBase):
    VERSION = "1.0.1"
    DESCRIPTION = "Provides global storage functionality."

    def __init__(self, config=None):
        super().__init__(config or {})
        self.name = 'global_storage'
        self.enabled = self.config.get('enabled', False)

    async def cleanup(self):
        pass

    async def update(self):
        pass

    async def on_config_changed(self, config):
        self.enabled = config.get('enabled', False)
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)
            if self.enabled:
                self.run_js_export('global_storage_js', self.injector, enabled=True)
            else:
                self.run_js_export('global_storage_js', self.injector, enabled=False)

    async def on_game_ready(self):
        if self.injector:
            self.set_config(config_manager.get_plugin_config(self.name))
            if self.config.get('enabled', False):
                self.run_js_export('global_storage_js', self.injector, enabled=True)

    @ui_toggle(
        label="Toggle Global Storage",
        description="Toggle global storage",
        config_key="enabled",
        default_value=False,
        category="Storage",
        order=1
    )
    async def toggle_global_storage_ui(self, value=None):
        if value is not None:
            self.config['enabled'] = value
            self.save_to_global_config()
            self.enabled = value
            if hasattr(self, 'injector') and self.injector:
                self.run_js_export('global_storage_js', self.injector, enabled=value)
        return f"Global Storage is {'enabled' if self.config.get('enabled', False) else 'disabled'}"

    @plugin_command(help="Set quickref unlock state (on/off)")
    async def set(self, injector=None, **kwargs):
        if not injector:
            return "ERROR: No injector available - run 'inject' first"
        current_state = self.config.get('enabled', False)
        new_state = not current_state
        self.config['enabled'] = new_state
        self.save_to_global_config()
        self.enabled = new_state
        return self.run_js_export('global_storage_js', injector, enabled=new_state)

    @js_export(params=["enabled"])
    def global_storage_js(self, enabled=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            const engine = ctx["com.stencyl.Engine"].engine;
            const optionsListAccount = engine.getGameAttribute("OptionsListAccount");
            if (!optionsListAccount || typeof optionsListAccount !== 'object') {
                return "OptionsListAccount not found.";
            }
            if (!optionsListAccount.hasOwnProperty('_34')) {
                optionsListAccount._34 = optionsListAccount[34];
                Object.defineProperty(optionsListAccount, 34, {
                    get: function() {
                        if (window.pluginConfigs && window.pluginConfigs['global_storage'] && window.pluginConfigs['global_storage'].enabled)
                            return 450;
                        return this._34;
                    },
                    set: function(value) {
                        if (window.pluginConfigs && window.pluginConfigs['global_storage'] && window.pluginConfigs['global_storage'].enabled)
                            return true;
                        this._34 = value;
                        return true;
                    },
                    enumerable: true
                });
            }
            return "Storage limit increased to 450.";
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

plugin_class = GlobalStoragePlugin 