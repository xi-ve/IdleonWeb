from plugin_system import PluginBase, js_export, ui_toggle, ui_search_with_results, plugin_command, ui_autocomplete_input, console, ui_button, ui_banner


class SummoningManagerPlugin(PluginBase):
    VERSION = "1.0.0"
    DESCRIPTION = "Manage World 6 Summoning upgrades: view status, set levels, max all, and reset."
    PLUGIN_ORDER = 1
    CATEGORY = "World 6"

    def __init__(self, config=None):
        super().__init__(config or {})
        self.debug = config.get('debug', False) if config else False
        self._upgrade_cache = None
        self._cache_timestamp = 0
        self._cache_duration = 300
        self.name = 'summoning_manager'

    async def cleanup(self): pass
    async def update(self): pass
    async def on_config_changed(self, config):
        self.debug = config.get('debug', False)
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)
    async def on_game_ready(self): pass

    @ui_banner(
        label="Warning",
        description="Many summoning upgrades are infinitely expandable. Prefer setting a reasonable value (e.g., 200) instead of 'max' for those.",
        banner_type="warning",
        category="Actions",
        order=-100
    )
    async def warning_banner(self):
        return ""

    @ui_toggle(
        label="Debug Mode",
        description="Enable debug logging for summoning manager plugin",
        config_key="debug",
        default_value=False
    )
    async def enable_debug(self, value: bool = None):
        if value is not None:
            self.config["debug"] = value
            self.save_to_global_config()
            self.debug = value
        return f"Debug mode {'enabled' if self.config.get('debug', False) else 'disabled'}"

    @ui_search_with_results(
        label="Summoning Upgrades Status",
        description="Show World 6 summoning upgrades with their current and max levels",
        button_text="Show Summoning Status",
        placeholder="Enter filter term (leave empty to show all)",
    )
    async def summoning_status_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[summoning_manager] Getting status, filter: {value}")
                result = self.run_js_export('get_summoning_status_js', self.injector, filter_query=value or "")
                return result
            except Exception as e:
                if self.debug:
                    console.print(f"[summoning_manager] Error getting status: {e}")
                return f"ERROR: Error getting status: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["filter_query"])
    def get_summoning_status_js(self, filter_query=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const summon = bEngine.getGameAttribute("Summon");
            const cl = bEngine.getGameAttribute("CustomLists");
            const upgList = cl?.h?.SummonUPG;
            if (!summon || !upgList) return "Error: Summoning data not found";

            const levels = summon[0] || [];
            const resources = summon[2] || [];
            const filterQuery = (filter_query || "").toLowerCase();

            const getMax = (row) => {
                const cap = Number(row[8] || 0);
                if (cap > 0) return cap;
                const v4 = Number(row[4] || 0);
                const v6 = Number(row[6] || 0);
                if (v4 >= 1000 && v6 > 0) return v6;
                if (v4 > 0 && v4 <= 1000) return v4;
                if (v6 > 0) return v6;
                return Math.max(cap, v4, v6, 0);
            };

            const isUncapped = (maxLevel) => maxLevel >= 9999;

            let total = 0;
            let unlocked = 0; // capped-only
            let maxed = 0; // capped-only
            const lockedItems = [];
            const unlockedItems = [];
            const maxedItems = [];
            const infiniteItems = [];

            for (let i = 0; i < upgList.length; i++) {
                const row = upgList[i];
                if (!row) continue;
                const name = (row[3] || "").replace(/_/g, ' ');
                const maxLevel = getMax(row);
                const level = Number((levels[i] || 0));
                total++;

                if (isUncapped(maxLevel)) {
                    infiniteItems.push({ name, level, maxLevel, index: i });
                    continue;
                }

                if (level >= maxLevel && maxLevel > 0) {
                    maxed++;
                    maxedItems.push({ name, level, maxLevel, index: i });
                } else if (level > 0) {
                    unlocked++;
                    unlockedItems.push({ name, level, maxLevel, index: i });
                } else {
                    lockedItems.push({ name, level, maxLevel, index: i });
                }
            }

            function section(title, items, color) {
                const list = items.filter(it => !filterQuery || it.name.toLowerCase().includes(filterQuery));
                if (list.length === 0) return "";
                let out = `<div style='font-weight: bold; margin: 10px 0 5px 0; color: ${color};'>${title} (${list.length})</div>`;
                for (const it of list) {
                    const maxDisp = (it.maxLevel >= 9999) ? '∞' : it.maxLevel;
                    let progress = '';
                    if (it.maxLevel > 0 && it.maxLevel < 9999) {
                        const pct = Math.round(it.level / it.maxLevel * 100);
                        progress = ` (${pct}%)`;
                    }
                    out += `<div style='margin: 2px 0; padding: 3px 8px; background: rgba(255,255,255,0.04); border-left: 3px solid ${color};'>${it.name} | Level: ${it.level}/${maxDisp}${progress}</div>`;
                }
                return out;
            }

            let output = "";
            output += section("Infinite Upgrades", infiniteItems, "#9aa0a6");
            output += section("Locked", lockedItems, "#cc6666");
            output += section("Unlocked", unlockedItems, "#d6c26e");
            output += section("Max Level", maxedItems, "#6bcf7f");

            if (!filterQuery) {
                const cappedTotal = total - infiniteItems.length;
                output += `<div style='margin-top: 15px; padding: 10px; background: rgba(0,0,0,0.1); border-radius: 5px;'>`;
                output += `<div style='font-weight: bold; margin-bottom: 5px;'>Summary</div>`;
                output += `<div>Total Upgrades: ${total}</div>`;
                output += `<div>Infinite Upgrades: ${infiniteItems.length}</div>`;
                output += `<div>Maxed (capped only): ${maxed}/${cappedTotal}</div>`;
                if (Array.isArray(resources) && resources.length > 0) {
                    output += `<div style='margin-top: 8px;'>Essences: ${resources.map((v,i)=>`[${i}]: ${v}`).join(' | ')}</div>`;
                }
                output += `</div>`;
            }

            return output;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @ui_autocomplete_input(
        label="Set Summoning Upgrade Level",
        description="Set a specific summoning upgrade to a specific level. Syntax: 'upgrade_name level'",
        button_text="Set Level",
        placeholder="Enter: upgrade_name level",
    )
    async def set_upgrade_level_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[summoning_manager] Setting upgrade level, input: {value}")

                if not value or not value.strip():
                    return "Please provide upgrade name and level (e.g., 'Unit Health 10')"

                parts = value.strip().split()
                if len(parts) < 2:
                    return "Syntax: 'upgrade_name level'"

                levelStr = parts[-1]
                upgradeName = ' '.join(parts[:-1])

                try:
                    levelInt = int(levelStr)
                    if levelInt < 0:
                        return "Level must be 0 or higher"
                except ValueError:
                    return "Level must be a valid number"

                result = await self.set_upgrade_level(upgradeName, levelInt)
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[summoning_manager] Error setting level: {e}")
                return f"ERROR: Error setting upgrade level: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    async def get_cached_upgrade_list(self):
        import time
        if (not hasattr(self, '_upgrade_cache') or 
            not hasattr(self, '_cache_timestamp') or 
            not hasattr(self, '_cache_duration') or
            time.time() - self._cache_timestamp > self._cache_duration):
            try:
                if not hasattr(self, 'injector') or not self.injector:
                    return []
                raw = self.run_js_export('get_upgrade_names_js', self.injector)
                if not raw or raw.startswith("Error:"):
                    return []
                names = []
                for line in raw.strip().split('\n'):
                    line = line.strip()
                    if line and '|' in line:
                        parts = line.split('|')
                        if len(parts) >= 2:
                            name = parts[0].strip()
                            if name and name != "Upgrade":
                                names.append(name)
                self._upgrade_cache = names
                self._cache_timestamp = time.time()
                self._cache_duration = 300
                return names
            except Exception:
                return []
        else:
            return self._upgrade_cache

    async def get_set_upgrade_level_ui_autocomplete(self, query: str = ""):
        try:
            if not hasattr(self, 'injector') or not self.injector:
                return []
            upgrades = await self.get_cached_upgrade_list()
            if not upgrades:
                return []
            ql = query.lower()
            results = [n for n in upgrades if ql in n.lower()]
            return results[:10]
        except Exception:
            return []

    @plugin_command(
        help="Set a specific summoning upgrade to a specific level.",
        params=[
            {"name": "upgrade_name", "type": str, "help": "Name of the upgrade"},
            {"name": "level", "type": int, "help": "Level to set (0 or higher)"},
        ],
    )
    async def set_upgrade_level(self, upgrade_name: str, level: int, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('set_upgrade_level_js', self.injector, upgrade_name=upgrade_name, level=level)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["upgrade_name", "level"])
    def set_upgrade_level_js(self, upgrade_name=None, level=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const summon = bEngine.getGameAttribute("Summon");
            const upgList = bEngine.getGameAttribute("CustomLists")?.h?.SummonUPG;
            if (!summon || !upgList) return "Error: Summoning data not found";
            if (!upgrade_name || level === undefined || level === null) return "Error: Upgrade name and level are required";
            if (level < 0) return "Error: Level must be 0 or higher";

            const levels = summon[0] || [];
            let foundIndex = -1;
            let foundName = "";
            const search = String(upgrade_name).toLowerCase().replace(/[^a-z0-9]/g, '');

            for (let i = 0; i < upgList.length; i++) {
                const row = upgList[i];
                if (!row) continue;
                const name = (row[3] || "").replace(/_/g, ' ');
                const clean = name.toLowerCase().replace(/[^a-z0-9]/g, '');
                if (clean.includes(search) || search.includes(clean)) {
                    foundIndex = i;
                    foundName = name;
                    break;
                }
            }

            if (foundIndex === -1) return `Error: Summoning upgrade '${upgrade_name}' not found`;

            const cap = Number(upgList[foundIndex][8] || 0);
            const v4 = Number(upgList[foundIndex][4] || 0);
            const v6 = Number(upgList[foundIndex][6] || 0);
            const maxLevel = cap > 0 ? cap : ((v4 >= 1000 && v6 > 0) ? v6 : (v4 > 0 && v4 <= 1000 ? v4 : (v6 > 0 ? v6 : Math.max(cap, v4, v6, 0))));
            const oldLevel = Number(levels[foundIndex] || 0);
            if (maxLevel > 0 && maxLevel < 9999 && level > maxLevel) return `Error: Level ${level} exceeds maximum level ${maxLevel} for '${foundName}'`;

            summon[0][foundIndex] = level;
            if (level === 0) return `Reset '${foundName}' to level 0 (was ${oldLevel})`;
            if (maxLevel > 0 && level === maxLevel) return `Set '${foundName}' to maximum level ${maxLevel} (was ${oldLevel})`;
            const maxDisp = maxLevel >= 9999 ? '∞' : maxLevel;
            return `Set '${foundName}' to level ${level} (was ${oldLevel}${maxLevel>0?`, max ${maxDisp}`:''})`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @plugin_command(
        help="Get list of summoning upgrade names for autocomplete.",
        params=[],
    )
    async def get_upgrade_names(self, injector=None, **kwargs):
        result = self.run_js_export('get_upgrade_names_js', injector)
        return result

    @js_export()
    def get_upgrade_names_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const summon = bEngine.getGameAttribute("Summon");
            const upgList = bEngine.getGameAttribute("CustomLists")?.h?.SummonUPG;
            if (!summon || !upgList) return "Error: Summoning data not found";

            const levels = summon[0] || [];
            const header = [
                'Upgrade | Level | Max Level | Status',
                '--------|-------|-----------|--------'
            ].join('\\n');
            let output = header + '\\n';
            for (let i = 0; i < upgList.length; i++) {
                const row = upgList[i];
                if (!row) continue;
                const name = (row[3] || "").replace(/_/g, ' ');
                const level = Number(levels[i] || 0);
                const cap = Number(row[8] || 0);
                const v4 = Number(row[4] || 0);
                const v6 = Number(row[6] || 0);
                const maxLevel = cap > 0 ? cap : ((v4 >= 1000 && v6 > 0) ? v6 : (v4 > 0 && v4 <= 1000 ? v4 : (v6 > 0 ? v6 : Math.max(cap, v4, v6, 0))));
                const maxDisp = maxLevel >= 9999 ? '∞' : maxLevel;
                let status = "LOCKED";
                if (maxLevel > 0 && maxLevel < 9999 && level >= maxLevel) status = "MAX";
                else if (level > 0) status = "UNLOCKED";
                output += `${name} | ${level} | ${maxDisp} | ${status}\\n`;
            }
            return output;
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @ui_button(
        label="Max Level All Upgrades",
        description="Set all summoning upgrades (with a finite cap) to maximum level, uncapped to 200",
        category="Actions",
        order=1
    )
    async def max_all_upgrades_ui(self):
        result = await self.max_all_upgrades(self.injector)
        return f"SUCCESS: {result}"

    @plugin_command(
        help="Set all summoning upgrades (with a finite cap) to maximum level; uncapped go to 200.",
        params=[],
    )
    async def max_all_upgrades(self, injector=None, **kwargs):
        result = self.run_js_export('max_all_upgrades_js', injector)
        return result

    @js_export()
    def max_all_upgrades_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const summon = bEngine.getGameAttribute("Summon");
            const upgList = bEngine.getGameAttribute("CustomLists")?.h?.SummonUPG;
            if (!summon || !upgList) return "Error: Summoning data not found";

            const levels = summon[0] || [];
            let cappedChanged = 0;
            let cappedAlready = 0;
            let uncappedSet200 = 0;
            let uncappedAlready = 0;
            for (let i = 0; i < upgList.length; i++) {
                const row = upgList[i];
                if (!row) continue;
                const cap = Number(row[8] || 0);
                const v4 = Number(row[4] || 0);
                const v6 = Number(row[6] || 0);
                const maxLevel = cap > 0 ? cap : ((v4 >= 1000 && v6 > 0) ? v6 : (v4 > 0 && v4 <= 1000 ? v4 : (v6 > 0 ? v6 : Math.max(cap, v4, v6, 0))));
                const cur = Number(levels[i] || 0);
                if (maxLevel > 0 && maxLevel < 9999) {
                    if (cur < maxLevel) { summon[0][i] = maxLevel; cappedChanged++; } else { cappedAlready++; }
                } else {
                    if (cur < 200) { summon[0][i] = 200; uncappedSet200++; } else { uncappedAlready++; }
                }
            }
            return `Capped: set ${cappedChanged}, already max ${cappedAlready}; Uncapped: set 200 for ${uncappedSet200}, already ≥200 ${uncappedAlready}`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @ui_button(
        label="Reset All Upgrades",
        description="Reset all summoning upgrades to level 0",
        category="Actions",
        order=2
    )
    async def reset_all_upgrades_ui(self):
        result = await self.reset_all_upgrades(self.injector)
        return f"SUCCESS: {result}"

    @plugin_command(
        help="Reset all summoning upgrades to level 0.",
        params=[],
    )
    async def reset_all_upgrades(self, injector=None, **kwargs):
        result = self.run_js_export('reset_all_upgrades_js', injector)
        return result

    @js_export()
    def reset_all_upgrades_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const summon = bEngine.getGameAttribute("Summon");
            const upgList = bEngine.getGameAttribute("CustomLists")?.h?.SummonUPG;
            if (!summon || !upgList) return "Error: Summoning data not found";

            const levels = summon[0] || [];
            let reset = 0;
            let already = 0;
            for (let i = 0; i < upgList.length; i++) {
                const cur = Number(levels[i] || 0);
                if (cur > 0) { summon[0][i] = 0; reset++; } else { already++; }
            }
            if (reset === 0) return `All summoning upgrades are already at level 0 (${already})`;
            return `Reset ${reset} summoning upgrades to level 0 (${already} already reset)`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @ui_autocomplete_input(
        label="Set Essence by Name",
        description="Set essence by name and amount. Syntax: 'name amount' (e.g., 'white 1000000')",
        button_text="Set Essence",
        placeholder="Enter: name amount",
        category="Essences",
        order=1
    )
    async def set_essence_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if not value or not value.strip():
                    return "Provide: name amount (e.g., 'white 1000000')"
                parts = value.strip().split()
                if len(parts) < 2:
                    return "Syntax: 'name amount'"
                try:
                    amt = int(parts[-1])
                except ValueError:
                    return "Amount must be a number"
                name = ' '.join(parts[:-1])
                if not name:
                    return "Provide a color name"
                result = await self.set_essence(name, amt)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "ERROR: No injector available - run 'inject' first to connect to the game"

    def get_set_essence_ui_autocomplete(self, query: str = ""):
        try:
            names = [
                "white", "green", "yellow", "blue", "purple", "orange", "light green"
            ]
            base = [f"{n} 1000000" for n in names]
            if not query:
                return base[:10]
            q = query.lower()
            return [s for s in base if q in s.lower()][:10]
        except Exception:
            return []

    @ui_autocomplete_input(
        label="Add Essence by Name",
        description="Add to essence by name. Syntax: 'name amount' (e.g., 'white 500000')",
        button_text="Add Essence",
        placeholder="Enter: name amount",
        category="Essences",
        order=2
    )
    async def add_essence_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if not value or not value.strip():
                    return "Provide: name amount (e.g., 'white 500000')"
                parts = value.strip().split()
                if len(parts) < 2:
                    return "Syntax: 'name amount'"
                try:
                    amt = int(parts[-1])
                except ValueError:
                    return "Amount must be a number"
                name = ' '.join(parts[:-1])
                if not name:
                    return "Provide a color name"
                result = await self.add_essence(name, amt)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "ERROR: No injector available - run 'inject' first to connect to the game"

    def get_add_essence_ui_autocomplete(self, query: str = ""):
        try:
            names = [
                "white", "green", "yellow", "blue", "purple", "orange", "light green"
            ]
            base = [f"{n} 500000" for n in names]
            if not query:
                return base[:10]
            q = query.lower()
            return [s for s in base if q in s.lower()][:10]
        except Exception:
            return []

    @ui_autocomplete_input(
        label="Set All Essences to",
        description="Set all essence entries to a specific amount (e.g., '1000000')",
        button_text="Set All",
        placeholder="Enter amount",
        category="Essences",
        order=3
    )
    async def set_all_essences_value_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if not value or not value.strip():
                    return "Provide an amount (e.g., '1000000')"
                try:
                    amt = int(value.strip())
                except ValueError:
                    return "Amount must be a number"
                result = await self.set_all_essences_value(amt)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "ERROR: No injector available - run 'inject' first to connect to the game"

    def get_set_all_essences_value_ui_autocomplete(self, query: str = ""):
        return ["100000", "500000", "1000000", "5000000", "10000000"]

    @ui_button(
        label="Reset All Essences",
        description="Set all essence entries to 0",
        category="Essences",
        order=4
    )
    async def reset_all_essences_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.reset_all_essences()
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "ERROR: No injector available - run 'inject' first to connect to the game"

    @plugin_command(
        help="Set a specific essence value by name (e.g., white, green, yellow, blue, purple, orange, light green)",
        params=[
            {"name": "name", "type": str, "help": "Essence name"},
            {"name": "amount", "type": int, "help": "Amount to set"},
        ],
    )
    async def set_essence(self, name: str, amount: int, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            return self.run_js_export('set_essence_js', self.injector, name=name, amount=amount)
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @plugin_command(
        help="Add to a specific essence by name",
        params=[
            {"name": "name", "type": str, "help": "Essence name"},
            {"name": "amount", "type": int, "help": "Amount to add"},
        ],
    )
    async def add_essence(self, name: str, amount: int, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            return self.run_js_export('add_essence_js', self.injector, name=name, amount=amount)
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @plugin_command(
        help="Set all essence entries to a value",
        params=[
            {"name": "amount", "type": int, "help": "Amount to set for each essence"},
        ],
    )
    async def set_all_essences_value(self, amount: int, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            return self.run_js_export('set_all_essences_js', self.injector, amount=amount)
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @plugin_command(
        help="Reset all essence entries to 0",
        params=[],
    )
    async def reset_all_essences(self, injector=None, **kwargs):
        return self.run_js_export('reset_all_essences_js', injector)

    @js_export(params=["name", "amount"])
    def set_essence_js(self, name=None, amount=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const summon = bEngine.getGameAttribute("Summon");
            if (!summon) return "Error: Summoning data not found";
            const amt = Math.floor(parseInt(arguments[1]) || 0);
            const raw = String(arguments[0] || '').toLowerCase();
            const canon = raw.replace(/[^a-z]/g, '');
            const names = ['white','green','yellow','blue','purple','orange','lightgreen'];
            let idx = names.indexOf(canon);
            if (idx === -1 && /^\\d+$/.test(raw)) idx = Math.floor(parseInt(raw));
            if (!Array.isArray(summon[2])) return "Error: Essence data not found";
            if (idx < 0 || idx >= summon[2].length) return `Error: Invalid index ${idx}`;
            const old = Number(summon[2][idx] || 0);
            summon[2][idx] = Math.max(0, amt);
            const dispName = ['White','Green','Yellow','Blue','Purple','Orange','Light Green'][idx] || `Index ${idx}`;
            return `${dispName} essence set to ${summon[2][idx]} (was ${old})`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export(params=["name", "amount"])
    def add_essence_js(self, name=None, amount=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const summon = bEngine.getGameAttribute("Summon");
            if (!summon) return "Error: Summoning data not found";
            const amt = Math.floor(parseInt(arguments[1]) || 0);
            const raw = String(arguments[0] || '').toLowerCase();
            const canon = raw.replace(/[^a-z]/g, '');
            const names = ['white','green','yellow','blue','purple','orange','lightgreen'];
            let idx = names.indexOf(canon);
            if (idx === -1 && /^\\d+$/.test(raw)) idx = Math.floor(parseInt(raw));
            if (!Array.isArray(summon[2])) return "Error: Essence data not found";
            if (idx < 0 || idx >= summon[2].length) return `Error: Invalid index ${idx}`;
            const old = Number(summon[2][idx] || 0);
            summon[2][idx] = Math.max(0, old + amt);
            const dispName = ['White','Green','Yellow','Blue','Purple','Orange','Light Green'][idx] || `Index ${idx}`;
            return `${dispName} essence changed by ${amt} to ${summon[2][idx]} (was ${old})`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export(params=["amount"])
    def set_all_essences_js(self, amount=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const summon = bEngine.getGameAttribute("Summon");
            if (!summon) return "Error: Summoning data not found";
            const amt = Math.floor(parseInt(arguments[0]) || 0);
            if (!Array.isArray(summon[2])) return "Error: Essence data not found";
            let changed = 0;
            for (let i = 0; i < summon[2].length; i++) {
                const old = Number(summon[2][i] || 0);
                summon[2][i] = Math.max(0, amt);
                if (summon[2][i] !== old) changed++;
            }
            return `Set ${changed} essence entries to ${amt}`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def reset_all_essences_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const summon = bEngine.getGameAttribute("Summon");
            if (!summon) return "Error: Summoning data not found";
            if (!Array.isArray(summon[2])) return "Error: Essence data not found";
            let reset = 0;
            for (let i = 0; i < summon[2].length; i++) {
                if (summon[2][i] !== 0) { summon[2][i] = 0; reset++; }
            }
            return `Reset ${reset} essence entries to 0`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @plugin_command(
        help="Get summoning status showing all upgrades and their levels.",
        params=[],
    )
    async def get_summoning_status(self, injector=None, **kwargs):
        result = self.run_js_export('get_summoning_status_js', injector)
        return result


plugin_class = SummoningManagerPlugin


