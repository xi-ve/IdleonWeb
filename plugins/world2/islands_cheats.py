from plugin_system import PluginBase, js_export, ui_toggle, ui_search_with_results, plugin_command, ui_autocomplete_input, console, ui_button, ui_banner


class IslandsCheatsPlugin(PluginBase):
    VERSION = "1.0.0"
    DESCRIPTION = "World 2 Islands cheats: Trash, Bottles, Shimmers, Rando, Gambling, unlock islands, and counters."
    PLUGIN_ORDER = 2
    CATEGORY = "World 2"

    def __init__(self, config=None):
        super().__init__(config or {})
        self.debug = config.get('debug', False) if config else False
        self.name = 'islands_cheats'

    async def cleanup(self): pass
    async def update(self): pass
    async def on_config_changed(self, config):
        self.debug = config.get('debug', False)
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)
    async def on_game_ready(self): pass

    @ui_toggle(
        label="Debug Mode",
        description="Enable verbose logging for these islands cheats",
        config_key="debug",
        default_value=False,
        category="Settings",
        order=100
    )
    async def enable_debug(self, value: bool = None):
        if value is not None:
            self.config["debug"] = value
            self.save_to_global_config()
            self.debug = value
        return f"Debug mode {'enabled' if self.config.get('debug', False) else 'disabled'}"

    @ui_search_with_results(
        label="Islands Status Overview",
        description="Show islands, currencies, upgrades, and unlock state",
        button_text="Show Status",
        placeholder="Enter filter term (leave empty to show all)",
        category="Status",
        order=0
    )
    async def island_status_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[islands_cheats] Getting status, filter: {value}")
                result = self.run_js_export('get_islands_status_js', self.injector, filter_query=value or "")
                return result
            except Exception as e:
                if self.debug:
                    console.print(f"[islands_cheats] Error getting status: {e}")
                return f"ERROR: Error getting status: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["filter_query"])
    def get_islands_status_js(self, filter_query=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const eng = ctx["com.stencyl.Engine"].engine;
            const ola = eng.getGameAttribute("OptionsListAccount");
            if (!Array.isArray(ola)) return "Error: OptionsListAccount not found";

            const f = String(filter_query||'').toLowerCase();

            const get = (i) => Number(ola[i]||0);
            const getStr = (i) => String(ola[i]||'');

            const unlockStr = getStr(169);
            const islandOrder = [
                { key: 'trash',   code: '_', title: 'Trash Island' },
                { key: 'rando',   code: 'a', title: 'Rando Island' },
                { key: 'crystal', code: 'b', title: 'Crystal Island' },
                { key: 'seasalt', code: 'c', title: 'Seasalt Island' },
                { key: 'shimmer', code: 'd', title: 'Shimmer Island' },
                { key: 'fractal', code: 'e', title: 'Fractal Island' }
            ];
            const unlocked = Object.fromEntries(islandOrder.map(x => [x.key, unlockStr.includes(x.code)]));

            const vals = {
                garbage: get(161),
                bottles: get(162),
                shimmers: get(173),
                garbageUpg: { garbagePct: get(163), bottlesPct: get(164) },
                gamblingBribe: get(165),
                randoUpg: { lootPct: get(166), doubleBossPct: get(167) },
                unlockedIslands: unlockStr,
                uncollectedGroundGarbage: get(160),
                uncollectedDockBottles: get(170),
                shimmerStats: get(172),
                shimmerUpg: { str: get(174), agi: get(175), wis: get(176), luk: get(177), dmg: get(178), class: get(179), skill: get(180) },
                fractalAfkTime: Number(ola[184]||0)
            };

            const rows = [];
            function addRow(title, items){
                const id = title.toLowerCase();
                if (f && !id.includes(f)) return;
                let out = `<div style='font-weight:bold;margin:10px 0 5px 0;color:#5ea1ec;'>${title}</div>`;
                for (const [k,v] of items) {
                    out += `<div style='margin:2px 0;padding:3px 8px;background:rgba(255,255,255,0.04);border-left:3px solid #5ea1ec;'>${k}: ${v}</div>`;
                }
                rows.push(out);
            }

            addRow('Islands', islandOrder.map(x => [x.title, unlocked[x.key] ? 'Unlocked' : 'Locked']));
            addRow('Currencies', [
                ['Garbage', vals.garbage],
                ['Bottles', vals.bottles],
                ['Shimmers', vals.shimmers]
            ]);
            addRow('Garbage Island Upgrades', [
                ['+% Garbage', vals.garbageUpg.garbagePct],
                ['+% Bottles', vals.garbageUpg.bottlesPct]
            ]);
            addRow('Rando Island Upgrades', [
                ['+% Loot (events)', vals.randoUpg.lootPct],
                ['+% Double Boss', vals.randoUpg.doubleBossPct]
            ]);
            addRow('Gambling', [
                ['Bribe Unlock Flag', vals.gamblingBribe]
            ]);
            
            addRow('Uncollected Counters', [
                ['Ground Garbage', vals.uncollectedGroundGarbage],
                ['Dock Bottles', vals.uncollectedDockBottles]
            ]);
            addRow('Shimmer Island', [
                ['Char Stat Tracking', vals.shimmerStats]
            ]);
            addRow('Shimmer Upgrades', [
                ['Base STR', vals.shimmerUpg.str],
                ['Base AGI', vals.shimmerUpg.agi],
                ['Base WIS', vals.shimmerUpg.wis],
                ['Base LUK', vals.shimmerUpg.luk],
                ['% Total Damage', vals.shimmerUpg.dmg],
                ['% Class EXP', vals.shimmerUpg.class],
                ['% Skill Eff', vals.shimmerUpg.skill]
            ]);
            (function(){
                const t = Math.max(0, Number(vals.fractalAfkTime||0));
                const h = Math.floor(t / 3600);
                const m = Math.floor((t % 3600) / 60);
                const s = Math.floor(t % 60);
                addRow('Fractal Isle', [["AFK Time", `${t} sec (${h}h ${m}m ${s}s)`]]);
            })();

            return rows.join('');
        } catch (e) { return `Error: ${e.message}`; }
        '''

    @ui_autocomplete_input(
        label="Set Fractal AFK Time",
        description="Set Fractal Isle AFK timer seconds",
        button_text="Set",
        placeholder="3600",
        category="Actions",
        order=0
    )
    async def set_fractal_afk_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if not value or not value.strip():
                    return "Provide seconds, e.g., 3600"
                try:
                    secs = int(value.strip())
                    if secs < 0:
                        return "Value must be 0 or higher"
                except ValueError:
                    return "Value must be a valid number"
                result = await self.set_fractal_afk(secs)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "ERROR: No injector available - run 'inject' first to connect to the game"

    async def get_set_fractal_afk_ui_autocomplete(self, query: str = ""):
        try:
            base = ["3600", "86400", "43200"]
            if not query:
                return base[:10]
            q = query.lower()
            return [s for s in base if q in s.lower()][:10]
        except Exception:
            return []

    @plugin_command(
        help="Set Fractal Isle AFK timer seconds (OLA[184])",
        params=[
            {"name": "seconds", "type": int, "help": "Seconds to set (0 or higher)"},
        ],
    )
    async def set_fractal_afk(self, seconds: int, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            return self.run_js_export('set_fractal_afk_js', self.injector, seconds=seconds)
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["seconds"])
    def set_fractal_afk_js(self, seconds=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const eng = ctx["com.stencyl.Engine"].engine;
            const ola = eng.getGameAttribute("OptionsListAccount");
            if (!Array.isArray(ola)) return "Error: OptionsListAccount not found";
            const v = Math.max(0, Math.floor(Number(seconds||0)));
            const old = Number(ola[184]||0);
            ola[184] = v;
            try { if (typeof eng.saveGame === 'function') eng.saveGame(); } catch {}
            return `Set Fractal AFK to ${v} (was ${old})`;
        } catch (e) { return `Error: ${e.message}`; }
        '''

    @ui_autocomplete_input(
        label="Set Currency Amount",
        description="Set a currency. Examples: 'garbage 100000', 'bottles 50000', 'shimmers 25000'",
        button_text="Set",
        placeholder="garbage 100000 | bottles 50000 | shimmers 25000",
        category="Currencies",
        order=0
    )
    async def set_currency_amount_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if not value or not value.strip():
                    return "Provide: garbage|bottles|shimmers amount"
                parts = value.strip().split()
                if len(parts) < 2:
                    return "Syntax: 'name amount'"
                name = parts[0].lower()
                amtStr = parts[1]
                try:
                    amt = int(amtStr)
                    if amt < 0:
                        return "Amount must be 0 or higher"
                except ValueError:
                    return "Amount must be a valid number"
                result = await self.set_currency_amount(name, amt)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "ERROR: No injector available - run 'inject' first to connect to the game"

    async def get_set_currency_amount_ui_autocomplete(self, query: str = ""):
        try:
            base = ["garbage 100000", "bottles 100000", "shimmers 100000"]
            if not query:
                return base[:10]
            q = query.lower()
            return [s for s in base if q in s.lower()][:10]
        except Exception:
            return []

    @plugin_command(
        help="Set a currency amount for islands",
        params=[
            {"name": "name", "type": str, "help": "garbage|bottles|shimmers"},
            {"name": "amount", "type": int, "help": "Amount to set (0 or higher)"},
        ],
    )
    async def set_currency_amount(self, name: str, amount: int, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            return self.run_js_export('set_currency_amount_js', self.injector, name=name, amount=amount)
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["name", "amount"])
    def set_currency_amount_js(self, name=None, amount=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const eng = ctx["com.stencyl.Engine"].engine;
            const ola = eng.getGameAttribute("OptionsListAccount");
            if (!Array.isArray(ola)) return "Error: OptionsListAccount not found";
            const k = String(name||'').toLowerCase();
            const amt = Math.max(0, Math.floor(Number(amount||0)));
            let idx = -1, label = '';
            if (k === 'garbage') { idx = 161; label = 'Garbage'; }
            else if (k === 'bottles') { idx = 162; label = 'Bottles'; }
            else if (k === 'shimmers') { idx = 173; label = 'Shimmers'; }
            else return "Error: Unknown currency name";
            const old = Number(ola[idx]||0);
            ola[idx] = amt;
            try { if (typeof eng.saveGame === 'function') eng.saveGame(); } catch {}
            return `Set ${label} to ${amt} (was ${old})`;
        } catch (e) { return `Error: ${e.message}`; }
        '''

    @ui_autocomplete_input(
        label="Set Garbage Island Upgrades",
        description="Set '+% Garbage' and '+% Bottles'. Examples: 'both 100', 'garbage 100', 'bottles 100'",
        button_text="Set",
        placeholder="both 100 | garbage 100 | bottles 100",
        category="Upgrades",
        order=0
    )
    async def set_garbage_upgrades_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if not value or not value.strip():
                    return "Provide: both|garbage|bottles value"
                parts = value.strip().split()
                if len(parts) < 2:
                    return "Syntax: 'target value'"
                target = parts[0].lower()
                valStr = parts[1]
                try:
                    valInt = int(valStr)
                    if valInt < 0:
                        return "Value must be 0 or higher"
                except ValueError:
                    return "Value must be a valid number"
                result = await self.set_garbage_upgrades(target, valInt)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "ERROR: No injector available - run 'inject' first to connect to the game"

    async def get_set_garbage_upgrades_ui_autocomplete(self, query: str = ""):
        try:
            base = ["both 200", "garbage 200", "bottles 200"]
            if not query:
                return base[:10]
            q = query.lower()
            return [s for s in base if q in s.lower()][:10]
        except Exception:
            return []

    @plugin_command(
        help="Set Garbage Island upgrades",
        params=[
            {"name": "target", "type": str, "help": "both|garbage|bottles"},
            {"name": "value", "type": int, "help": "Value to set (0 or higher)"},
        ],
    )
    async def set_garbage_upgrades(self, target: str, value: int, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            return self.run_js_export('set_garbage_upgrades_js', self.injector, target=target, value=value)
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["target", "value"])
    def set_garbage_upgrades_js(self, target=None, value=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const eng = ctx["com.stencyl.Engine"].engine;
            const ola = eng.getGameAttribute("OptionsListAccount");
            if (!Array.isArray(ola)) return "Error: OptionsListAccount not found";
            const tgt = String(target||'').toLowerCase();
            const val = Math.max(0, Math.floor(Number(value||0)));
            let changed = 0;
            if (tgt === 'both' || tgt === 'garbage') { const old = Number(ola[163]||0); if (old !== val) { ola[163] = val; changed++; } }
            if (tgt === 'both' || tgt === 'bottles') { const old = Number(ola[164]||0); if (old !== val) { ola[164] = val; changed++; } }
            try { if (typeof eng.saveGame === 'function') eng.saveGame(); } catch {}
            return `Set ${changed} upgrade field(s) to ${val}`;
        } catch (e) { return `Error: ${e.message}`; }
        '''

    @ui_autocomplete_input(
        label="Set Rando Upgrades",
        description="Set Rando upgrades. Examples: 'both 100', 'loot 100', 'double 100'",
        button_text="Set",
        placeholder="both 100 | loot 100 | double 100",
        category="Upgrades",
        order=1
    )
    async def set_rando_upgrades_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if not value or not value.strip():
                    return "Provide: both|loot|double value"
                parts = value.strip().split()
                if len(parts) < 2:
                    return "Syntax: 'target value'"
                target = parts[0].lower()
                valStr = parts[1]
                try:
                    valInt = int(valStr)
                    if valInt < 0:
                        return "Value must be 0 or higher"
                except ValueError:
                    return "Value must be a valid number"
                result = await self.set_rando_upgrades(target, valInt)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "ERROR: No injector available - run 'inject' first to connect to the game"

    async def get_set_rando_upgrades_ui_autocomplete(self, query: str = ""):
        try:
            base = ["both 200", "loot 200", "double 200"]
            if not query:
                return base[:10]
            q = query.lower()
            return [s for s in base if q in s.lower()][:10]
        except Exception:
            return []

    @plugin_command(
        help="Set Rando Island upgrades",
        params=[
            {"name": "target", "type": str, "help": "both|loot|double"},
            {"name": "value", "type": int, "help": "Value to set (0 or higher)"},
        ],
    )
    async def set_rando_upgrades(self, target: str, value: int, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            return self.run_js_export('set_rando_upgrades_js', self.injector, target=target, value=value)
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["target", "value"])
    def set_rando_upgrades_js(self, target=None, value=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const eng = ctx["com.stencyl.Engine"].engine;
            const ola = eng.getGameAttribute("OptionsListAccount");
            if (!Array.isArray(ola)) return "Error: OptionsListAccount not found";
            const tgt = String(target||'').toLowerCase();
            const val = Math.max(0, Math.floor(Number(value||0)));
            let changed = 0;
            if (tgt === 'both' || tgt === 'loot') { const old = Number(ola[166]||0); if (old !== val) { ola[166] = val; changed++; } }
            if (tgt === 'both' || tgt === 'double') { const old = Number(ola[167]||0); if (old !== val) { ola[167] = val; changed++; } }
            try { if (typeof eng.saveGame === 'function') eng.saveGame(); } catch {}
            return `Set ${changed} Rando field(s) to ${val}`;
        } catch (e) { return `Error: ${e.message}`; }
        '''

    @ui_button(
        label="Unlock Gambling Bribe",
        description="Enable the Gambling Island bribe option",
        category="Islands",
        order=30
    )
    async def unlock_gambling_bribe_ui(self):
        result = await self.set_gambling_bribe(1)
        return f"SUCCESS: {result}"

    @plugin_command(
        help="Set Gambling Island bribe unlock flag",
        params=[
            {"name": "flag", "type": int, "help": "0 or 1"},
        ],
    )
    async def set_gambling_bribe(self, flag: int, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            return self.run_js_export('set_gambling_bribe_js', self.injector, flag=flag)
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["flag"])
    def set_gambling_bribe_js(self, flag=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const eng = ctx["com.stencyl.Engine"].engine;
            const ola = eng.getGameAttribute("OptionsListAccount");
            if (!Array.isArray(ola)) return "Error: OptionsListAccount not found";
            const f = Math.max(0, Math.min(1, Math.floor(Number(flag||0))));
            const old = Number(ola[165]||0);
            ola[165] = f;
            try { if (typeof eng.saveGame === 'function') eng.saveGame(); } catch {}
            return `Set Gambling bribe flag to ${f} (was ${old})`;
        } catch (e) { return `Error: ${e.message}`; }
        '''

    

    @plugin_command(
        help="Set unlocked islands string",
        params=[
            {"name": "unlock_str", "type": str, "help": "Islands unlock string"},
        ],
    )
    async def set_unlocked_islands(self, unlock_str: str, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            return self.run_js_export('set_unlocked_islands_js', self.injector, unlock_str=unlock_str)
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["unlock_str"])
    def set_unlocked_islands_js(self, unlock_str=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const eng = ctx["com.stencyl.Engine"].engine;
            const ola = eng.getGameAttribute("OptionsListAccount");
            if (!Array.isArray(ola)) return "Error: OptionsListAccount not found";
            const s = String(unlock_str||'');
            const old = String(ola[169]||'');
            ola[169] = s;
            try { if (typeof eng.saveGame === 'function') eng.saveGame(); } catch {}
            return `Set unlocked islands to '${s}' (was '${old}')`;
        } catch (e) { return `Error: ${e.message}`; }
        '''

    @ui_button(
        label="Unlock All Islands",
        description="Unlock all World 2 islands",
        category="Islands",
        order=10
    )
    async def unlock_all_islands_ui(self):
        result = await self.set_unlocked_islands("abcde_")
        return f"SUCCESS: {result}"

    @ui_button(
        label="Lock All Islands",
        description="Lock all World 2 islands",
        category="Islands",
        order=11
    )
    async def lock_all_islands_ui(self):
        result = await self.set_unlocked_islands("")
        return f"SUCCESS: {result}"

    @ui_autocomplete_input(
        label="Set Island Lock State",
        description="Type: 'unlock trash' or 'lock shimmer'",
        button_text="Apply",
        placeholder="unlock trash | lock rando | unlock crystal | lock seasalt | unlock shimmer | lock fractal",
        category="Islands",
        order=12
    )
    async def set_island_lock_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if not value or not value.strip():
                    return "Provide: unlock|lock islandName"
                parts = value.strip().split()
                if len(parts) < 2:
                    return "Syntax: 'unlock|lock name'"
                stateWord = parts[0].lower()
                name = ' '.join(parts[1:]).lower()
                if stateWord not in ('unlock','lock'):
                    return "First word must be unlock or lock"
                state = 1 if stateWord == 'unlock' else 0
                result = await self.set_island_lock(name, state)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "ERROR: No injector available - run 'inject' first to connect to the game"

    async def get_set_island_lock_ui_autocomplete(self, query: str = ""):
        try:
            base = [
                "unlock trash","lock trash",
                "unlock rando","lock rando",
                "unlock crystal","lock crystal",
                "unlock seasalt","lock seasalt",
                "unlock shimmer","lock shimmer",
                "unlock fractal","lock fractal"
            ]
            if not query:
                return base[:10]
            q = query.lower()
            return [s for s in base if q in s.lower()][:10]
        except Exception:
            return []

    @plugin_command(
        help="Unlock or lock a single island",
        params=[
            {"name": "name", "type": str, "help": "trash|rando|crystal|seasalt|shimmer|fractal"},
            {"name": "state", "type": int, "help": "1=unlock, 0=lock"},
        ],
    )
    async def set_island_lock(self, name: str, state: int, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            return self.run_js_export('set_island_lock_js', self.injector, name=name, state=state)
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["name","state"])
    def set_island_lock_js(self, name=None, state=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const eng = ctx["com.stencyl.Engine"].engine;
            const ola = eng.getGameAttribute("OptionsListAccount");
            if (!Array.isArray(ola)) return "Error: OptionsListAccount not found";
            const rawName = String(name||'').trim().toLowerCase();
            const want = Math.max(0, Math.min(1, Number(state||0)));
            const map = { trash:'_', rando:'a', crystal:'b', seasalt:'c', shimmer:'d', fractal:'e' };
            if (!map.hasOwnProperty(rawName)) return "Error: Unknown island name";
            const code = map[rawName];
            const order = ['a','b','c','d','e','_'];
            const cur = String(ola[169]||'');
            const set = new Set(cur.split('').filter(Boolean));
            if (want === 1) set.add(code); else set.delete(code);
            const next = order.filter(ch => set.has(ch)).join('');
            const old = String(ola[169]||'');
            ola[169] = next;
            try { if (typeof eng.saveGame === 'function') eng.saveGame(); } catch {}
            return `${want===1?'Unlocked':'Locked'} ${rawName} (was '${old}', now '${next}')`;
        } catch (e) { return `Error: ${e.message}`; }
        '''

    @ui_autocomplete_input(
        label="Set Uncollected Counters",
        description="Set uncollected amounts. Examples: 'garbage 100', 'bottles 100'",
        button_text="Set",
        placeholder="garbage 100 | bottles 100",
        category="Currencies",
        order=1
    )
    async def set_uncollected_counters_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if not value or not value.strip():
                    return "Provide: garbage|bottles value"
                parts = value.strip().split()
                if len(parts) < 2:
                    return "Syntax: 'name value'"
                name = parts[0].lower()
                valStr = parts[1]
                try:
                    valInt = int(valStr)
                    if valInt < 0:
                        return "Value must be 0 or higher"
                except ValueError:
                    return "Value must be a valid number"
                result = await self.set_uncollected_counters(name, valInt)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "ERROR: No injector available - run 'inject' first to connect to the game"

    async def get_set_uncollected_counters_ui_autocomplete(self, query: str = ""):
        try:
            base = ["garbage 100", "bottles 100", "garbage 0", "bottles 0"]
            if not query:
                return base[:10]
            q = query.lower()
            return [s for s in base if q in s.lower()][:10]
        except Exception:
            return []

    @plugin_command(
        help="Set uncollected counters",
        params=[
            {"name": "name", "type": str, "help": "garbage|bottles"},
            {"name": "value", "type": int, "help": "Value to set (0 or higher)"},
        ],
    )
    async def set_uncollected_counters(self, name: str, value: int, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            return self.run_js_export('set_uncollected_counters_js', self.injector, name=name, value=value)
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["name", "value"])
    def set_uncollected_counters_js(self, name=None, value=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const eng = ctx["com.stencyl.Engine"].engine;
            const ola = eng.getGameAttribute("OptionsListAccount");
            if (!Array.isArray(ola)) return "Error: OptionsListAccount not found";
            const k = String(name||'').toLowerCase();
            const val = Math.max(0, Math.floor(Number(value||0)));
            if (k === 'garbage') { const old = Number(ola[160]||0); ola[160] = val; return `Set uncollected ground garbage to ${val} (was ${old})`; }
            if (k === 'bottles') { const old = Number(ola[170]||0); ola[170] = val; return `Set uncollected dock bottles to ${val} (was ${old})`; }
            return "Error: Unknown counter name";
        } catch (e) { return `Error: ${e.message}`; }
        '''

    @ui_autocomplete_input(
        label="Set Shimmer Upgrades",
        description="Set Shimmer upgrades. Use 'all 100' or one of str|agi|wis|luk|dmg|class|skill",
        button_text="Set",
        placeholder="all 100 | str 100 | agi 100 | wis 100 | luk 100 | dmg 100 | class 100 | skill 100",
        category="Upgrades",
        order=2
    )
    async def set_shimmer_upgrades_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if not value or not value.strip():
                    return "Provide: all|str|agi|wis|luk|dmg|class|skill value"
                parts = value.strip().split()
                if len(parts) < 2:
                    return "Syntax: 'target value'"
                target = parts[0].lower()
                valStr = parts[1]
                try:
                    valInt = int(valStr)
                    if valInt < 0:
                        return "Value must be 0 or higher"
                except ValueError:
                    return "Value must be a valid number"
                result = await self.set_shimmer_upgrades(target, valInt)
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "ERROR: No injector available - run 'inject' first to connect to the game"

    async def get_set_shimmer_upgrades_ui_autocomplete(self, query: str = ""):
        try:
            base = [
                "all 200","str 200","agi 200","wis 200","luk 200","dmg 200","class 200","skill 200"
            ]
            if not query:
                return base[:10]
            q = query.lower()
            return [s for s in base if q in s.lower()][:10]
        except Exception:
            return []

    @plugin_command(
        help="Set Shimmer Island upgrades",
        params=[
            {"name": "target", "type": str, "help": "all|str|agi|wis|luk|dmg|class|skill"},
            {"name": "value", "type": int, "help": "Value to set (0 or higher)"},
        ],
    )
    async def set_shimmer_upgrades(self, target: str, value: int, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            return self.run_js_export('set_shimmer_upgrades_js', self.injector, target=target, value=value)
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["target", "value"])
    def set_shimmer_upgrades_js(self, target=None, value=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const eng = ctx["com.stencyl.Engine"].engine;
            const ola = eng.getGameAttribute("OptionsListAccount");
            if (!Array.isArray(ola)) return "Error: OptionsListAccount not found";
            const tgt = String(target||'').toLowerCase();
            const val = Math.max(0, Math.floor(Number(value||0)));
            const map = {
                str: 174,
                agi: 175,
                wis: 176,
                luk: 177,
                dmg: 178,
                class: 179,
                skill: 180
            };
            let changed = 0;
            if (tgt === 'all') {
                for (const k in map) { const idx = map[k]; const old = Number(ola[idx]||0); if (old !== val) { ola[idx] = val; changed++; } }
            } else if (map.hasOwnProperty(tgt)) {
                const idx = map[tgt]; const old = Number(ola[idx]||0); if (old !== val) { ola[idx] = val; changed++; }
            } else {
                return "Error: Unknown target";
            }
            try { if (typeof eng.saveGame === 'function') eng.saveGame(); } catch {}
            return `Set ${changed} Shimmer field(s) to ${val}`;
        } catch (e) { return `Error: ${e.message}`; }
        '''

    @plugin_command(
        help="Get islands status HTML.",
        params=[],
    )
    async def get_islands_status(self, injector=None, **kwargs):
        result = self.run_js_export('get_islands_status_js', injector)
        return result


plugin_class = IslandsCheatsPlugin


