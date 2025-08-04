from typing import Dict, Any
from plugin_system import plugin_command, js_export, PluginBase, console, ui_toggle, ui_search_with_results, ui_autocomplete_input
from config_manager import config_manager

class PackageTogglePlugin(PluginBase):
    VERSION = "1.0.2"
    DESCRIPTION = "Toggle bought packages / bundles"
    PLUGIN_ORDER = 5
    CATEGORY = "Unlocks"

    def __init__(self, config=None):
        super().__init__(config or {})
        self.injector = None
        self.name = 'package_toggle'
        self.debug = config_manager.get_path('plugin_configs.package_toggle.debug', False)
        self._bundle_cache = None
        self._cache_timestamp = 0
        self._cache_duration = 300

    async def cleanup(self) -> None:
        pass

    async def update(self) -> None:
        pass

    async def on_config_changed(self, config: Dict[str, Any]) -> None:
        self.debug = config_manager.get_path('plugin_configs.package_toggle.debug', False)
        if self.debug:
            console.print(f"[package_toggle] Config changed: {config}")
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)

    async def on_game_ready(self) -> None:
        pass

    @ui_toggle(
        label="Debug Mode",
        description="Enable debug logging for package toggle plugin",
        config_key="debug",
        default_value=False
    )
    async def enable_debug(self, value: bool = None):
        if value is not None:
            self.config["debug"] = value
            self.save_to_global_config()
        return f"Debug mode {'enabled' if self.config.get('debug', False) else 'disabled'}"

    @ui_search_with_results(
        label="List Bought Packages",
        description="List all bought packages with their status",
        button_text="List Bought",
        placeholder="Enter filter term (leave empty to list all)",
    )
    async def list_bought_packages_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.list_bought_packages(self.injector)
                if value and value.strip():
                    lines = result.split('\n')
                    filtered_lines = []
                    query_lower = value.lower()
                    for line in lines:
                        if query_lower in line.lower():
                            filtered_lines.append(line)
                    return '\n'.join(filtered_lines) if filtered_lines else f"No packages found matching: {value}"
                else:
                    return result
            except Exception as e:
                return f"ERROR: Error listing packages: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_autocomplete_input(
        label="Toggle Package",
        description="Enter package code to toggle (with autocomplete)",
        button_text="Toggle",
        placeholder="Package code (e.g. bun_a, bun_b)"
    )
    async def toggle_package_ui(self, value: str = None):
        if value:
            package_code = value.strip()
            if hasattr(self, 'injector') and self.injector:
                try:
                    result = await self.toggle_package(package_code, self.injector)
                    return f"SUCCESS: {result}"
                except Exception as e:
                    return f"ERROR: Error toggling package: {str(e)}"
            else:
                return "ERROR: No injector available - run 'inject' first to connect to the game"
        return "Enter package code to toggle (e.g. 'bun_a')"

    async def get_toggle_autocomplete(self, query: str = ""):
        if not hasattr(self, 'injector') or not self.injector:
            return []
        try:
            result = await self.get_all_package_codes(self.injector)
            if not result or result.startswith("ERROR"):
                return []
            suggestions = []
            query_lower = query.lower()
            lines = result.split('\n')
            for line in lines:
                if ' : ' in line:
                    parts = line.split(' : ')
                    if len(parts) >= 1:
                        package_code = parts[0].strip()
                        if query_lower in package_code.lower():
                            suggestions.append(package_code)
            return suggestions[:10]
        except Exception as e:
            return []

    async def get_all_package_codes(self, injector=None, **kwargs):
        bundle_definitions = [
            ("Lava Supporter Pack", "bun_a"),
            ("New Year Supporter Pack", "bun_b"),
            ("Starter Pack", "bun_c"),
            ("Easter Bundle", "bun_d"),
            ("Totally Chill Pack", "bun_e"),
            ("Summer Bundle", "bun_f"),
            ("Dungeon Bundle", "bun_g"),
            ("Giftmas Bundle", "bun_h"),
            ("Auto Loot Pack", "bun_i"),
            ("Outta This World Pack", "bun_j"),
            ("Eggscellent Pack", "bun_k"),
            ("Super Hot Fire Pack", "bun_l"),
            ("Gem Motherlode Pack", "bun_m"),
            ("Riftwalker Pack", "bun_n"),
            ("Bloomin Pet Pack", "bun_o"),
            ("Island Explorer Pack", "bun_p"),
            ("Equinox Dreamer Pack", "bun_q"),
            ("Calm Serenity Pack", "bun_r"),
            ("Sacred Methods Pack", "bun_s"),
            ("Timeless Pack", "bun_t"),
            ("Ancient Echoes Pack", "bun_u"),
            ("Deathbringer Pack", "bun_v"),
            ("Windwalker Pack", "bun_w"),
            ("Arcande Cultist Pack", "bun_x"),
            ("Valenslime Day Pack", "bun_y"),
            ("Fallen Spirits Pet Pack", "bun_z"),
            ("Storage Ram Pack", "bon_a"),
            ("Blazing Star Anniversary Pack", "bon_c"),
            ("Midnight Tide Anniversary Pack", "bon_d"),
            ("Lush Emerald Anniversary Pack", "bon_e"),
            ("Eternal Hunter Pack", "bon_f"),
            ("Gilded Treasure Pack", "bon_g")
        ]
        return '\n'.join([f"{code} : {name}" for name, code in bundle_definitions])

    @plugin_command(
        help="List all bought packages with their status.",
        params=[],
    )
    async def list_bought_packages(self, injector=None, **kwargs):
        if self.debug:
            console.print("[package_toggle] Listing bought packages...")
        result = self.run_js_export('list_bought_packages_js', injector)
        if self.debug:
            console.print(f"[package_toggle] Result: {result}")
        return result

    @js_export()
    def list_bought_packages_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const GemPopupBundleMessages = ctx["scripts.CustomMapsREAL"].GemPopupBundleMessages().h;
            const bundles_received = bEngine.gameAttributes.h.BundlesReceived.h;
            const results = [];
            let owned_count = 0;
            let total_count = 0;
            const bundleDefinitions = [
                ["Lava Supporter Pack", "bun_a"],
                ["New Year Supporter Pack", "bun_b"],
                ["Starter Pack", "bun_c"],
                ["Easter Bundle", "bun_d"],
                ["Totally Chill Pack", "bun_e"],
                ["Summer Bundle", "bun_f"],
                ["Dungeon Bundle", "bun_g"],
                ["Giftmas Bundle", "bun_h"],
                ["Auto Loot Pack", "bun_i"],
                ["Outta This World Pack", "bun_j"],
                ["Eggscellent Pack", "bun_k"],
                ["Super Hot Fire Pack", "bun_l"],
                ["Gem Motherlode Pack", "bun_m"],
                ["Riftwalker Pack", "bun_n"],
                ["Bloomin Pet Pack", "bun_o"],
                ["Island Explorer Pack", "bun_p"],
                ["Equinox Dreamer Pack", "bun_q"],
                ["Calm Serenity Pack", "bun_r"],
                ["Sacred Methods Pack", "bun_s"],
                ["Timeless Pack", "bun_t"],
                ["Ancient Echoes Pack", "bun_u"],
                ["Deathbringer Pack", "bun_v"],
                ["Windwalker Pack", "bun_w"],
                ["Arcande Cultist Pack", "bun_x"],
                ["Valenslime Day Pack", "bun_y"],
                ["Fallen Spirits Pet Pack", "bun_z"],
                ["Storage Ram Pack", "bon_a"],
                ["Blazing Star Anniversary Pack", "bon_c"],
                ["Midnight Tide Anniversary Pack", "bon_d"],
                ["Lush Emerald Anniversary Pack", "bon_e"],
                ["Eternal Hunter Pack", "bon_f"],
                ["Gilded Treasure Pack", "bon_g"]
            ];
            for (const [displayName, code] of bundleDefinitions) {
                total_count++;
                const is_owned = bundles_received[code] === 1;
                if (is_owned) owned_count++;
                const status = is_owned ? "**✓ OWNED**" : "○ NOT OWNED";
                const status_emoji = is_owned ? "🟢" : "⚪";
                results.push(`${status_emoji} **${code}** : ${displayName} ${status}`);
            }
            const summary = `\\n\\n**Summary:** ${owned_count}/${total_count} packages owned`;
            return results.join("\\n") + summary;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @plugin_command(
        help="Toggle a package (buy if not owned, remove if owned).",
        params=[
            {"name": "package_code", "type": str, "help": "Package code to toggle (e.g. 'bun_a')"},
        ],
    )
    async def toggle_package(self, package_code: str, injector=None, **kwargs):
        if self.debug:
            console.print(f"[package_toggle] Toggling package: {package_code}")
        result = self.run_js_export('toggle_package_js', injector, package_code=package_code)
        if self.debug:
            console.print(f"[package_toggle] Result: {result}")
        return result

    @js_export(params=["package_code"])
    def toggle_package_js(self, package_code=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const bundles_received = bEngine.gameAttributes.h.BundlesReceived.h;
            const bundleDefinitions = [
                ["Lava Supporter Pack", "bun_a"],
                ["New Year Supporter Pack", "bun_b"],
                ["Starter Pack", "bun_c"],
                ["Easter Bundle", "bun_d"],
                ["Totally Chill Pack", "bun_e"],
                ["Summer Bundle", "bun_f"],
                ["Dungeon Bundle", "bun_g"],
                ["Giftmas Bundle", "bun_h"],
                ["Auto Loot Pack", "bun_i"],
                ["Outta This World Pack", "bun_j"],
                ["Eggscellent Pack", "bun_k"],
                ["Super Hot Fire Pack", "bun_l"],
                ["Gem Motherlode Pack", "bun_m"],
                ["Riftwalker Pack", "bun_n"],
                ["Bloomin Pet Pack", "bun_o"],
                ["Island Explorer Pack", "bun_p"],
                ["Equinox Dreamer Pack", "bun_q"],
                ["Calm Serenity Pack", "bun_r"],
                ["Sacred Methods Pack", "bun_s"],
                ["Timeless Pack", "bun_t"],
                ["Ancient Echoes Pack", "bun_u"],
                ["Deathbringer Pack", "bun_v"],
                ["Windwalker Pack", "bun_w"],
                ["Arcande Cultist Pack", "bun_x"],
                ["Valenslime Day Pack", "bun_y"],
                ["Fallen Spirits Pet Pack", "bun_z"],
                ["Storage Ram Pack", "bon_a"],
                ["Blazing Star Anniversary Pack", "bon_c"],
                ["Midnight Tide Anniversary Pack", "bon_d"],
                ["Lush Emerald Anniversary Pack", "bon_e"],
                ["Eternal Hunter Pack", "bon_f"],
                ["Gilded Treasure Pack", "bon_g"]
            ];
            if (!package_code) {
                return "Error: Package code is required";
            }
            const packageDef = bundleDefinitions.find(([name, code]) => code === package_code);
            if (!packageDef) {
                return `Error: Package code '${package_code}' not found`;
            }
            const [displayName, code] = packageDef;
            const is_owned = bundles_received[code] === 1;
            if (is_owned) {
                bundles_received[code] = 0;
                return `✅ Removed package: **${displayName}**`;
            } else {
                bundles_received[code] = 1;
                return `🎁 Added package: **${displayName}**`;
            }
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @plugin_command(
        help="Buy a specific package.",
        params=[
            {"name": "package_code", "type": str, "help": "Package code to buy (e.g. 'bun_a')"},
        ],
    )
    async def buy_package(self, package_code: str, injector=None, **kwargs):
        if self.debug:
            console.print(f"[package_toggle] Buying package: {package_code}")
        result = self.run_js_export('buy_package_js', injector, package_code=package_code)
        if self.debug:
            console.print(f"[package_toggle] Result: {result}")
        return result

    @js_export(params=["package_code"])
    def buy_package_js(self, package_code=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const bundles_received = bEngine.gameAttributes.h.BundlesReceived.h;
            const bundleDefinitions = [
                ["Lava Supporter Pack", "bun_a"],
                ["New Year Supporter Pack", "bun_b"],
                ["Starter Pack", "bun_c"],
                ["Easter Bundle", "bun_d"],
                ["Totally Chill Pack", "bun_e"],
                ["Summer Bundle", "bun_f"],
                ["Dungeon Bundle", "bun_g"],
                ["Giftmas Bundle", "bun_h"],
                ["Auto Loot Pack", "bun_i"],
                ["Outta This World Pack", "bun_j"],
                ["Eggscellent Pack", "bun_k"],
                ["Super Hot Fire Pack", "bun_l"],
                ["Gem Motherlode Pack", "bun_m"],
                ["Riftwalker Pack", "bun_n"],
                ["Bloomin Pet Pack", "bun_o"],
                ["Island Explorer Pack", "bun_p"],
                ["Equinox Dreamer Pack", "bun_q"],
                ["Calm Serenity Pack", "bun_r"],
                ["Sacred Methods Pack", "bun_s"],
                ["Timeless Pack", "bun_t"],
                ["Ancient Echoes Pack", "bun_u"],
                ["Deathbringer Pack", "bun_v"],
                ["Windwalker Pack", "bun_w"],
                ["Arcande Cultist Pack", "bun_x"],
                ["Valenslime Day Pack", "bun_y"],
                ["Fallen Spirits Pet Pack", "bun_z"],
                ["Storage Ram Pack", "bon_a"],
                ["Blazing Star Anniversary Pack", "bon_c"],
                ["Midnight Tide Anniversary Pack", "bon_d"],
                ["Lush Emerald Anniversary Pack", "bon_e"],
                ["Eternal Hunter Pack", "bon_f"],
                ["Gilded Treasure Pack", "bon_g"]
            ];
            if (!package_code) {
                return "Error: Package code is required";
            }
            const packageDef = bundleDefinitions.find(([name, code]) => code === package_code);
            if (!packageDef) {
                return `Error: Package code '${package_code}' not found`;
            }
            const [displayName, code] = packageDef;
            bundles_received[code] = 1;
            return `🎁 Bought package: **${displayName}**`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @plugin_command(
        help="Remove a specific package.",
        params=[
            {"name": "package_code", "type": str, "help": "Package code to remove (e.g. 'bun_a')"},
        ],
    )
    async def remove_package(self, package_code: str, injector=None, **kwargs):
        if self.debug:
            console.print(f"[package_toggle] Removing package: {package_code}")
        result = self.run_js_export('remove_package_js', injector, package_code=package_code)
        if self.debug:
            console.print(f"[package_toggle] Result: {result}")
        return result

    @js_export(params=["package_code"])
    def remove_package_js(self, package_code=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const bundles_received = bEngine.gameAttributes.h.BundlesReceived.h;
            const bundleDefinitions = [
                ["Lava Supporter Pack", "bun_a"],
                ["New Year Supporter Pack", "bun_b"],
                ["Starter Pack", "bun_c"],
                ["Easter Bundle", "bun_d"],
                ["Totally Chill Pack", "bun_e"],
                ["Summer Bundle", "bun_f"],
                ["Dungeon Bundle", "bun_g"],
                ["Giftmas Bundle", "bun_h"],
                ["Auto Loot Pack", "bun_i"],
                ["Outta This World Pack", "bun_j"],
                ["Eggscellent Pack", "bun_k"],
                ["Super Hot Fire Pack", "bun_l"],
                ["Gem Motherlode Pack", "bun_m"],
                ["Riftwalker Pack", "bun_n"],
                ["Bloomin Pet Pack", "bun_o"],
                ["Island Explorer Pack", "bun_p"],
                ["Equinox Dreamer Pack", "bun_q"],
                ["Calm Serenity Pack", "bun_r"],
                ["Sacred Methods Pack", "bun_s"],
                ["Timeless Pack", "bun_t"],
                ["Ancient Echoes Pack", "bun_u"],
                ["Deathbringer Pack", "bun_v"],
                ["Windwalker Pack", "bun_w"],
                ["Arcande Cultist Pack", "bun_x"],
                ["Valenslime Day Pack", "bun_y"],
                ["Fallen Spirits Pet Pack", "bun_z"],
                ["Storage Ram Pack", "bon_a"],
                ["Blazing Star Anniversary Pack", "bon_c"],
                ["Midnight Tide Anniversary Pack", "bon_d"],
                ["Lush Emerald Anniversary Pack", "bon_e"],
                ["Eternal Hunter Pack", "bon_f"],
                ["Gilded Treasure Pack", "bon_g"]
            ];
            if (!package_code) {
                return "Error: Package code is required";
            }
            const packageDef = bundleDefinitions.find(([name, code]) => code === package_code);
            if (!packageDef) {
                return `Error: Package code '${package_code}' not found`;
            }
            const [displayName, code] = packageDef;
            bundles_received[code] = 0;
            return `✅ Removed package: **${displayName}**`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

plugin_class = PackageTogglePlugin