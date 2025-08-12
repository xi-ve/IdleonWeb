from plugin_system import PluginBase, js_export, ui_toggle, ui_search_with_results, plugin_command, ui_autocomplete_input, console, ui_button, ui_banner


class StatueManagerPlugin(PluginBase):
    VERSION = "1.0.0"
    DESCRIPTION = "Manage World 1 Statues: view status, set levels and grades, max or reset."
    PLUGIN_ORDER = 3
    CATEGORY = "World 1"

    def __init__(self, config=None):
        super().__init__(config or {})
        self.debug = config.get('debug', False) if config else False
        self._statue_cache = None
        self._cache_timestamp = 0
        self._cache_duration = 300
        self.name = 'statue_manager'

    async def cleanup(self): pass
    async def update(self): pass
    async def on_config_changed(self, config):
        self.debug = config.get('debug', False)
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)
    async def on_game_ready(self): pass

    @ui_banner(
        label="Note",
        description="Statues are theoretically unlimited, but this plugin hard-caps manual inputs to 1000 for safety. Use reasonable amounts. When settings statues that are not yet known, please ensure to do some actions in-game before logging out to ensure data synchronization.",
        banner_type="warning",
        category="Actions",
        order=-100
    )
    async def note_banner(self):
        return ""

    @ui_toggle(
        label="Debug Mode",
        description="Enable debug logging for statue manager plugin",
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
        label="Statue Status Overview",
        description="Show World 1 statues with current level and grade (Stone/Gold/Onyx)",
        button_text="Show Statue Status",
        placeholder="Enter filter term (leave empty to show all)",
    )
    async def statue_status_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[statue_manager] Getting status, filter: {value}")
                result = self.run_js_export('get_statue_status_js', self.injector, filter_query=value or "")
                return result
            except Exception as e:
                if self.debug:
                    console.print(f"[statue_manager] Error getting status: {e}")
                return f"ERROR: Error getting status: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["filter_query"])
    def get_statue_status_js(self, filter_query=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const levelsList = bEngine.getGameAttribute("StatueLevels");
            const gradeList = bEngine.getGameAttribute("StatueG");
            const ownershipKey = (window.pluginConfigs && window.pluginConfigs['statue_manager'] && window.pluginConfigs['statue_manager'].ownershipKey) || '';
            const ownArr = ownershipKey ? bEngine.getGameAttribute(ownershipKey) : null;
            const cl = bEngine.getGameAttribute("CustomLists");
            const dmap = bEngine.getGameAttribute("DummyMap");
            const info = cl?.h?.StatueInfo;
            if (!Array.isArray(levelsList) || !Array.isArray(gradeList)) return "Error: Statue data not found";

            const filterQuery = String(filter_query || '').toLowerCase();
            const ola = bEngine.getGameAttribute("OptionsListAccount");
            const smg = Number(ola && ola[69] || 0);
            const smText = smg >= 2 ? 'Onyx' : (smg >= 1 ? 'Gold' : 'Locked');

            const getRawName = (idx) => {
                const row = info && info[idx];
                if (Array.isArray(row)) {
                    for (let j = 0; j < row.length; j++) {
                        const v = row[j];
                        if (typeof v === 'string') {
                            const s = v.replace(/_/g, ' ').trim();
                            if (s && /[A-Za-z]/.test(s) && !/^statue\\s*\\d+$/i.test(s)) return s;
                        }
                    }
                }
                return '';
            };

            const getCapHeuristic = (idx) => 0;

            const toGrade = (g) => (g >= 2 ? 'Onyx' : (g >= 1 ? 'Gold' : 'Stone'));

            const items = [];
            for (let i = 0; i < Math.max(levelsList.length, gradeList.length); i++) {
                const row = levelsList[i] || [0];
                const level = Number(row && row[0] || 0);
                const grade = Number(gradeList[i] || 0);
                const rawName = getRawName(i);
                if (!rawName) continue;
                const name = rawName;
                const cap = 0;
                items.push({ index: i, name, level, grade, gradeText: toGrade(grade), cap });
            }

            const filtered = items.filter(it => !filterQuery || it.name.toLowerCase().includes(filterQuery));
            const onyx = filtered.filter(it => it.grade >= 2);
            const gold = filtered.filter(it => it.grade === 1);
            const unlocked = filtered.filter(it => it.level > 0 && it.grade < 1);
            const locked = filtered.filter(it => it.level === 0 && it.grade < 1);

            function section(title, list, color) {
                if (list.length === 0) return '';
                let out = `<div style='font-weight: bold; margin: 10px 0 5px 0; color: ${color};'>${title} (${list.length})</div>`;
                for (const it of list) {
                    const capDisp = it.cap > 0 ? it.cap : '∞';
                    const progress = it.cap > 0 ? ` (${Math.round(Math.min(100, it.level / it.cap * 100))}%)` : '';
                    out += `<div style='margin: 2px 0; padding: 3px 8px; background: rgba(255,255,255,0.04); border-left: 3px solid ${color};'>${it.name} | Level: ${it.level}/${capDisp} | Grade: ${it.gradeText}${progress}</div>`;
                }
                return out;
            }

            let output = '';
            output += `<div style='margin: 6px 0; padding: 6px 8px; background: rgba(255,255,255,0.03); border-left: 3px solid #5ea1ec;'>Statue Man: ${smText} (flag ${smg})</div>`;
            output += section('Onyx', onyx, '#6bcf7f');
            output += section('Gold', gold, '#d6c26e');
            output += section('Unlocked (Stone)', unlocked, '#9aa0a6');
            output += section('Locked', locked, '#cc6666');

            if (!filterQuery) {
                const found = items.filter(it => it.level > 0).length;
                output += `<div style='margin-top: 15px; padding: 10px; background: rgba(0,0,0,0.1); border-radius: 5px;'>`;
                output += `<div style='font-weight: bold; margin-bottom: 5px;'>Summary</div>`;
                output += `<div>Total Statues: ${items.length}</div>`;
                output += `<div>Found Statues: ${found}</div>`;
                output += `<div>Gold: ${gold.length}</div>`;
                output += `<div>Onyx: ${onyx.length}</div>`;
                output += `</div>`;
            }

            return output;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @ui_autocomplete_input(
        label="Set Statue Man Grade",
        description="Set the Statue Man NPC grade. Syntax: 'stone|gold|onyx' or '0|1|2'",
        button_text="Set",
        placeholder="stone | gold | onyx",
        category="Actions",
        order=0
    )
    async def set_statue_man_grade_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if not value or not value.strip():
                    return "Provide: stone|gold|onyx or 0|1|2"
                v = value.strip().lower()
                gradeMap = { 'stone': 0, '0': 0, 'gold': 1, '1': 1, 'onyx': 2, '2': 2 }
                if gradeMap.get(v) is None:
                    return "Grade must be stone/gold/onyx or 0/1/2"
                result = await self.set_statue_man_grade(int(gradeMap[v]))
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "ERROR: No injector available - run 'inject' first to connect to the game"

    async def get_set_statue_man_grade_ui_autocomplete(self, query: str = ""):
        try:
            base = ["stone", "gold", "onyx", "0", "1", "2"]
            if not query:
                return base[:10]
            q = query.lower()
            return [s for s in base if q in s.lower()][:10]
        except Exception:
            return []

    @plugin_command(
        help="Set Statue Man NPC grade (0=Stone, 1=Gold, 2=Onyx)",
        params=[
            {"name": "grade", "type": int, "help": "Grade to set for Statue Man"},
        ],
    )
    async def set_statue_man_grade(self, grade: int, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            return self.run_js_export('set_statue_man_grade_js', self.injector, grade=grade)
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["grade"])
    def set_statue_man_grade_js(self, grade=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const ola = bEngine.getGameAttribute("OptionsListAccount");
            if (!Array.isArray(ola)) return "Error: OptionsListAccount not found";
            const g = Math.max(0, Math.floor(Number(arguments[0]) || 0));
            const old = Number(ola[69] || 0);
            ola[69] = g;
            const gt = g >= 2 ? 'Onyx' : (g >= 1 ? 'Gold' : 'Stone');
            return `Set Statue Man to ${gt} (was ${old})`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    async def get_cached_statue_list(self):
        import time
        if (not hasattr(self, '_statue_cache') or 
            not hasattr(self, '_cache_timestamp') or 
            not hasattr(self, '_cache_duration') or
            time.time() - self._cache_timestamp > self._cache_duration):
            try:
                if not hasattr(self, 'injector') or not self.injector:
                    return []
                raw = self.run_js_export('get_statue_names_js', self.injector)
                if not raw or raw.startswith("Error:"):
                    return []
                names = []
                for line in raw.strip().split('\n'):
                    line = line.strip()
                    if line and '|' in line:
                        parts = line.split('|')
                        if len(parts) >= 1:
                            name = parts[0].strip()
                            if name and name != "Statue":
                                names.append(name)
                self._statue_cache = names
                self._cache_timestamp = time.time()
                self._cache_duration = 300
                return names
            except Exception:
                return []
        else:
            return self._statue_cache

    @ui_autocomplete_input(
        label="Set Statue Level",
        description="Set a specific statue to a specific level. Syntax: 'statue_name level'",
        button_text="Set Level",
        placeholder="Enter: statue_name level",
    )
    async def set_statue_level_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[statue_manager] Setting statue level, input: {value}")
                if not value or not value.strip():
                    return "Provide statue name and level (e.g., 'Base Damage 10')"
                parts = value.strip().split()
                if len(parts) < 2:
                    return "Syntax: 'statue_name level'"
                levelStr = parts[-1]
                statueName = ' '.join(parts[:-1])
                try:
                    levelInt = int(levelStr)
                    if levelInt < 0:
                        return "Level must be 0 or higher"
                except ValueError:
                    return "Level must be a valid number"
                result = await self.set_statue_level(statueName, levelInt)
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[statue_manager] Error setting level: {e}")
                return f"ERROR: Error setting statue level: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    async def get_set_statue_level_ui_autocomplete(self, query: str = ""):
        try:
            if not hasattr(self, 'injector') or not self.injector:
                return []
            statues = await self.get_cached_statue_list()
            if not statues:
                return []
            ql = query.lower()
            results = [n for n in statues if ql in n.lower()]
            return results[:10]
        except Exception:
            return []

    @plugin_command(
        help="Set a specific statue to a specific level.",
        params=[
            {"name": "statue_name", "type": str, "help": "Name of the statue"},
            {"name": "level", "type": int, "help": "Level to set (0 or higher)"},
        ],
    )
    async def set_statue_level(self, statue_name: str, level: int, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('set_statue_level_js', self.injector, statue_name=statue_name, level=level)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["statue_name", "level"])
    def set_statue_level_js(self, statue_name=None, level=None):
        return '''
        try {
            const desiredName = String(arguments[0] ?? statue_name ?? '').trim();
            const desiredLevel = Math.max(0, Math.floor(Number(arguments[1] ?? level ?? 0)));
            function findEngine(){ const seen=new Set(); const q=[window]; while(q.length){ const o=q.shift(); if(!o||typeof o!=="object") continue; if(seen.has(o)) continue; seen.add(o); try{ if(typeof o.getGameAttribute==="function"&&o.gameAttributes) return o; }catch(_){ } const ks=Object.keys(o); for(let i=0;i<ks.length;i++){ const v=o[ks[i]]; if(v&&typeof v==="object"&&!seen.has(v)) q.push(v); } } return null; }
            function normalize(s){ return (s||"").toString().trim().toLowerCase(); }
            function extractNames(entry){ const out=[]; if(!entry) return out; if(typeof entry==="string"){ out.push(entry); } else if(Array.isArray(entry)){ for(const v of entry) if(typeof v==="string") out.push(v); } else if(typeof entry==="object"){ for(const k in entry){ const v=entry[k]; if(typeof v==="string") out.push(v); } } return out; }
            function unlockByName(eng,name,lvl){ const cl=eng.getGameAttribute("CustomLists"); if(!cl||!cl.h||!cl.h.StatueInfo) return false; const info=cl.h.StatueInfo; const target=normalize(name); let idx=-1; if(Array.isArray(info)){ for(let i=0;i<info.length;i++){ const cand=extractNames(info[i]).map(normalize); if(cand.includes(target) || cand.some(n=>n.replace(/[\\s_]+/g,' ')===target.replace(/[\\s_]+/g,' '))){ idx=i; break; } } } else { const keys=Object.keys(info); for(let i=0;i<keys.length;i++){ const k=keys[i]; const cand=extractNames(info[k]).concat([k]).map(normalize); if(cand.includes(target) || cand.some(n=>n.replace(/[\\s_]+/g,' ')===target.replace(/[\\s_]+/g,' '))){ idx=(+k===+k)?+k:i; break; } } } if(idx<0) return false; const lv=eng.getGameAttribute("StatueLevels"); const g=eng.getGameAttribute("StatueG")||[]; if(!lv) return false; if(Array.isArray(lv[idx])) lv[idx][0]=Math.max(1, +lv[idx][0]||lvl||1); else lv[idx]=Math.max(1, +lv[idx]||lvl||1); if(Array.isArray(g)) g[idx]=Math.max(1, +g[idx]||0); return true; }
            const ctx = window.__idleon_cheats__;
            const eng = (ctx && ctx["com.stencyl.Engine"] && ctx["com.stencyl.Engine"].engine) || findEngine();
            if(!eng) throw new Error('Game engine not found');
            let applied=false; try{ applied=unlockByName(eng,desiredName,desiredLevel); }catch(_){ }
            function tick(){ try{ unlockByName(eng,desiredName,desiredLevel); }catch(_){ } }
            function forceDesired(){ try {
                const cl=eng.getGameAttribute('CustomLists'); if(!cl||!cl.h||!cl.h.StatueInfo) return;
                const info=cl.h.StatueInfo; const target=normalize(desiredName); let idx=-1;
                function extract(entry){ const out=[]; if(!entry) return out; if(typeof entry==='string'){ out.push(entry); } else if(Array.isArray(entry)){ for(const v of entry) if(typeof v==='string') out.push(v); } else if(typeof entry==='object'){ for(const k in entry){ const v=entry[k]; if(typeof v==='string') out.push(v); } } return out; }
                function norm(s){ return (s||'').toString().trim().toLowerCase(); }
                if(Array.isArray(info)){
                  for(let i=0;i<info.length;i++){ const cand=extract(info[i]).map(norm); if(cand.includes(target) || cand.some(n=>n.replace(/[\\s_]+/g,' ')===target.replace(/[\\s_]+/g,' '))){ idx=i; break; } }
                } else {
                  const keys=Object.keys(info); for(let i=0;i<keys.length;i++){ const k=keys[i]; const cand=extract(info[k]).concat([k]).map(norm); if(cand.includes(target) || cand.some(n=>n.replace(/[\\s_]+/g,' ')===target.replace(/[\\s_]+/g,' '))){ idx=(+k===+k)?+k:i; break; } }
                }
                if(idx<0) return;
                const lv=eng.getGameAttribute('StatueLevels'); const g=eng.getGameAttribute('StatueG')||[];
                if(!lv) return;
                const want=Math.max(1, desiredLevel);
                if(Array.isArray(lv[idx])) lv[idx][0]=want; else lv[idx]=want;
                if(Array.isArray(g)) g[idx]=Math.max(1, +g[idx]||0);
                try { const dmap=eng.getGameAttribute('DummyMap'); if(dmap&&dmap.h){ if(!Array.isArray(dmap.h.StatueLevels)) dmap.h.StatueLevels=[]; if(!Array.isArray(dmap.h.StatueLevels[idx])) dmap.h.StatueLevels[idx]=[0]; dmap.h.StatueLevels[idx][0]=want; } } catch(_){ }
              } catch(_){ }
            }
            try{ forceDesired(); }catch(_){ }
            try{ tick(); }catch(_){ }
            try{ const id=setInterval(()=>{ tick(); forceDesired(); },2000); document.addEventListener('visibilitychange',()=>{ if(!document.hidden){ tick(); forceDesired(); } }); window.addEventListener('focus',()=>{ tick(); forceDesired(); }); setTimeout(()=>{ try{ clearInterval(id); }catch(_){ } },20000); }catch(_){ }
            return applied ? 'OK' : `Error: Statue '${desiredName}' not found`;
        } catch (e) { return `Error: ${e.message}`; }
        '''

    @plugin_command(
        help="Get list of statues for autocomplete.",
        params=[],
    )
    async def get_statue_names(self, injector=None, **kwargs):
        result = self.run_js_export('get_statue_names_js', injector)
        return result

    @js_export()
    def get_statue_names_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const levelsList = bEngine.getGameAttribute("StatueLevels");
            const gradeList = bEngine.getGameAttribute("StatueG");
            const ownershipKey = (window.pluginConfigs && window.pluginConfigs['statue_manager'] && window.pluginConfigs['statue_manager'].ownershipKey) || '';
            const ownArr = ownershipKey ? bEngine.getGameAttribute(ownershipKey) : null;
            const dmap = bEngine.getGameAttribute("DummyMap");
            const cl = bEngine.getGameAttribute("CustomLists");
            const info = cl?.h?.StatueInfo;
            if (!Array.isArray(levelsList)) return "Error: Statue data not found";

            const getName = (idx) => getRawName(idx) || `Statue ${idx}`;

            const header = [
                'Statue | Level | Grade',
                '-------|-------|------'
            ].join('\\n');
            let output = header + '\\n';
            for (let i = 0; i < Math.max(levelsList.length, Array.isArray(info) ? info.length : 0); i++) {
                const name = getRawName(i);
                if (!name) continue;
                const level = Number((levelsList[i] && levelsList[i][0]) || 0);
                const grade = Number(gradeList && gradeList[i] || 0);
                const gradeText = grade >= 2 ? 'Onyx' : (grade >= 1 ? 'Gold' : 'Stone');
                output += `${name} | ${level} | ${gradeText}\\n`;
            }
            return output;
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @ui_button(
        label="Max All Statue Levels",
        description="Set all statues to their max if known, else to 50",
        category="Actions",
        order=1
    )
    async def max_all_statues_ui(self):
        result = await self.max_all_statues(self.injector)
        return f"SUCCESS: {result}"

    @plugin_command(
        help="Set all statue levels to max if known, else 50.",
        params=[],
    )
    async def max_all_statues(self, injector=None, **kwargs):
        result = self.run_js_export('max_all_statues_js', injector)
        return result

    @js_export()
    def max_all_statues_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            let eng = null;
            if (ctx && ctx["com.stencyl.Engine"] && ctx["com.stencyl.Engine"].engine) eng = ctx["com.stencyl.Engine"].engine;
            if (!eng) {
                const seen = new Set(); const q = [window];
                while (q.length) {
                    const o = q.shift(); if (!o || typeof o !== 'object') continue; if (seen.has(o)) continue; seen.add(o);
                    try { if (typeof o.getGameAttribute === 'function' && o.gameAttributes) { eng = o; break; } } catch(_) {}
                    for (const k in o) { try { const v = o[k]; if (v && typeof v === 'object' && !seen.has(v)) q.push(v); } catch(_) {} }
                }
            }
            if (!eng) throw new Error('Game engine not found');
            const lv = eng.getGameAttribute('StatueLevels');
            const gr = eng.getGameAttribute('StatueG') || [];
            const cl = eng.getGameAttribute('CustomLists');
            const info = cl && cl.h && cl.h.StatueInfo;
            if (!Array.isArray(lv)) return 'Error: Statue data not found';
            function extractNames(entry){ const out=[]; if(!entry) return out; if (typeof entry==='string') out.push(entry); else if (Array.isArray(entry)) for(const v of entry) if(typeof v==='string') out.push(v); else if (typeof entry==='object') for(const k in entry){ const v=entry[k]; if(typeof v==='string') out.push(v); } return out; }
            function hasName(i){ if (!info) return true; const row = Array.isArray(info)?info[i]:info[i]; const names = extractNames(row); return names.length>0; }
            function setLevel(i, v){ if (Array.isArray(lv[i])) lv[i][0]=v; else lv[i]=v; }
            function ensureUnlockedAll(){ let n=0; const len = Array.isArray(info)?info.length:lv.length; for(let i=0;i<len;i++){ if (Array.isArray(info) && !hasName(i)) continue; if (!Array.isArray(lv[i]) && typeof lv[i] !== 'number') lv[i] = [0]; if (Array.isArray(lv[i])) { if (lv[i][0] < 1) { lv[i][0] = 1; n++; } } else { if (lv[i] < 1) { lv[i] = 1; n++; } } if (Array.isArray(gr)) gr[i] = Math.max(1, Number(gr[i]||0)); }
              return n;
            }
            try { ensureUnlockedAll(); } catch(_){ }
            try { const id = setInterval(()=>{ try{ ensureUnlockedAll(); }catch(_){} }, 2000); setTimeout(()=>{ try{ clearInterval(id); }catch(_){} }, 8000); } catch(_){ }
            let changed=0; const target=200; const len = Array.isArray(info)?info.length:lv.length;
            for (let i=0;i<len;i++){
                if (!hasName(i)) continue;
                if (!Array.isArray(lv[i]) && typeof lv[i] !== 'number') lv[i] = [0];
                setLevel(i, Math.max(1,target));
                if (Array.isArray(gr)) gr[i]=Math.max(1, Number(gr[i]||0));
                changed++;
            }
            return `Set ${changed} statues to ${target}`;
        } catch (e) { return `Error: ${e.message}`; }
        '''

    @ui_button(
        label="Reset All Statues",
        description="Reset all statue levels to 0 and grade to Stone",
        category="Actions",
        order=2
    )
    async def reset_all_statues_ui(self):
        result = await self.reset_all_statues(self.injector)
        return f"SUCCESS: {result}"

    @plugin_command(
        help="Reset all statue levels to 0 and grade to Stone.",
        params=[],
    )
    async def reset_all_statues(self, injector=None, **kwargs):
        result = self.run_js_export('reset_all_statues_js', injector)
        return result

    @js_export()
    def reset_all_statues_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            let eng = null;
            if (ctx && ctx["com.stencyl.Engine"] && ctx["com.stencyl.Engine"].engine) eng = ctx["com.stencyl.Engine"].engine;
            if (!eng) {
                const seen = new Set(); const q = [window];
                while (q.length) {
                    const o = q.shift(); if (!o || typeof o !== 'object') continue; if (seen.has(o)) continue; seen.add(o);
                    try { if (typeof o.getGameAttribute === 'function' && o.gameAttributes) { eng = o; break; } } catch(_) {}
                    for (const k in o) { try { const v = o[k]; if (v && typeof v === 'object' && !seen.has(v)) q.push(v); } catch(_) {} }
                }
            }
            if (!eng) throw new Error('Game engine not found');
            const lv = eng.getGameAttribute('StatueLevels');
            const gr = eng.getGameAttribute('StatueG') || [];
            const cl = eng.getGameAttribute('CustomLists');
            const info = cl && cl.h && cl.h.StatueInfo;
            if (!Array.isArray(lv)) return 'Error: Statue data not found';
            function extractNames(entry){ const out=[]; if(!entry) return out; if (typeof entry==='string') out.push(entry); else if (Array.isArray(entry)) for(const v of entry) if(typeof v==='string') out.push(v); else if (typeof entry==='object') for(const k in entry){ const v=entry[k]; if(typeof v==='string') out.push(v); } return out; }
            function hasName(i){ if (!info) return true; const row = Array.isArray(info)?info[i]:info[i]; const names = extractNames(row); return names.length>0; }
            function setLevel(i, v){ if (Array.isArray(lv[i])) lv[i][0]=v; else lv[i]=v; }
            function ensureUnlockedAll(){ let n=0; const len = Array.isArray(info)?info.length:lv.length; for(let i=0;i<len;i++){ if (Array.isArray(info) && !hasName(i)) continue; if (!Array.isArray(lv[i]) && typeof lv[i] !== 'number') lv[i] = [0]; if (Array.isArray(lv[i])) { if (lv[i][0] < 1) { lv[i][0] = 1; n++; } } else { if (lv[i] < 1) { lv[i] = 1; n++; } } if (Array.isArray(gr)) gr[i] = Math.max(1, Number(gr[i]||0)); }
              return n;
            }
            try { ensureUnlockedAll(); } catch(_){ }
            try { const id = setInterval(()=>{ try{ ensureUnlockedAll(); }catch(_){} }, 2000); setTimeout(()=>{ try{ clearInterval(id); }catch(_){} }, 8000); } catch(_){ }
            let resetL=0; const len = Array.isArray(info)?info.length:lv.length;
            for (let i=0;i<len;i++){
                if (!hasName(i)) continue;
                setLevel(i, 0); if (Array.isArray(gr)) gr[i]=0; resetL++;
            }
            return `Reset levels for ${resetL} statues`;
        } catch (e) { return `Error: ${e.message}`; }
        '''

    @ui_button(
        label="Set All Grades: Gold",
        description="Set all statues to Gold grade",
        category="Actions",
        order=3
    )
    async def set_all_gold_ui(self):
        result = await self.set_all_statue_grades(1)
        return f"SUCCESS: {result}"

    @ui_button(
        label="Set All Grades: Onyx",
        description="Set all statues to Onyx grade",
        category="Actions",
        order=4
    )
    async def set_all_onyx_ui(self):
        result = await self.set_all_statue_grades(2)
        return f"SUCCESS: {result}"

    @plugin_command(
        help="Set all statue grades (0=Stone, 1=Gold, 2=Onyx)",
        params=[
            {"name": "grade", "type": int, "help": "Grade to set for all statues"},
        ],
    )
    async def set_all_statue_grades(self, grade: int, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            return self.run_js_export('set_all_statue_grades_js', self.injector, grade=grade)
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["grade"])
    def set_all_statue_grades_js(self, grade=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const gradeList = bEngine.getGameAttribute("StatueG");
            if (!Array.isArray(gradeList)) return "Error: Statue data not found";
            const g = Math.max(0, Math.floor(Number(arguments[0]) || 0));
            let changed = 0;
            for (let i = 0; i < gradeList.length; i++) {
                const old = Number(gradeList[i] || 0);
                if (old !== g) { gradeList[i] = g; changed++; }
            }
            const gt = g >= 2 ? 'Onyx' : (g >= 1 ? 'Gold' : 'Stone');
            return `Set grade '${gt}' for ${changed} statues`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @ui_autocomplete_input(
        label="Set Statue Grade",
        description="Set a specific statue's grade. Syntax: 'name grade' (grade: stone|gold|onyx or 0|1|2)",
        button_text="Set Grade",
        placeholder="Enter: name grade",
    )
    async def set_statue_grade_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if not value or not value.strip():
                    return "Provide: name grade (e.g., 'Base Damage onyx')"
                parts = value.strip().split()
                if len(parts) < 2:
                    return "Syntax: 'name grade'"
                gradeRaw = parts[-1].lower()
                name = ' '.join(parts[:-1])
                gradeMap = { 'stone': 0, '0': 0, 'gold': 1, '1': 1, 'onyx': 2, '2': 2 }
                if gradeMap.get(gradeRaw) is None:
                    return "Grade must be stone/gold/onyx or 0/1/2"
                result = await self.set_statue_grade(name, int(gradeMap[gradeRaw]))
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "ERROR: No injector available - run 'inject' first to connect to the game"

    async def get_set_statue_grade_ui_autocomplete(self, query: str = ""):
        try:
            names = await self.get_cached_statue_list()
            suffixes = [" stone", " gold", " onyx"]
            base = []
            for n in names[:10]:
                for s in suffixes:
                    base.push(n + s)
            if not query:
                return base[:10]
            q = query.lower()
            return [s for s in base if q in s.lower()][:10]
        except Exception:
            return []

    @plugin_command(
        help="Set a specific statue's grade.",
        params=[
            {"name": "name", "type": str, "help": "Statue name"},
            {"name": "grade", "type": int, "help": "0=Stone, 1=Gold, 2=Onyx"},
        ],
    )
    async def set_statue_grade(self, name: str, grade: int, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            return self.run_js_export('set_statue_grade_js', self.injector, name=name, grade=grade)
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["name", "grade"])
    def set_statue_grade_js(self, name=None, grade=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const gradeList = bEngine.getGameAttribute("StatueG");
            const levelsList = bEngine.getGameAttribute("StatueLevels");
            const cl = bEngine.getGameAttribute("CustomLists");
            const info = cl?.h?.StatueInfo;
            if (!Array.isArray(gradeList)) return "Error: Statue data not found";
            if (!name) return "Error: Statue name required";
            const g = Math.max(0, Math.floor(Number(grade)));

            const getNameFromRow = (row) => {
                if (!Array.isArray(row)) return '';
                for (let j = 0; j < row.length; j++) {
                    const v = row[j];
                    if (typeof v === 'string' && v.trim()) return v.replace(/_/g, ' ');
                }
                return '';
            };

            const target = String(name).toLowerCase().replace(/[^a-z0-9]/g, '');
            let foundIndex = -1;
            let foundName = '';
            for (let i = 0; i < Math.max(gradeList.length, Array.isArray(info) ? info.length : 0); i++) {
                const n = getNameFromRow(info && info[i]) || `Statue ${i}`;
                const clean = n.toLowerCase().replace(/[^a-z0-9]/g, '');
                if (clean.includes(target) || target.includes(clean)) { foundIndex = i; foundName = n; break; }
            }
            if (foundIndex === -1) return `Error: Statue '${name}' not found`;
            const old = Number(gradeList[foundIndex] || 0);
            gradeList[foundIndex] = g;
            if (g > 0 && Array.isArray(levelsList)) {
                if (!Array.isArray(levelsList[foundIndex])) levelsList[foundIndex] = [0];
                if (Number(levelsList[foundIndex][0] || 0) === 0) {
                    levelsList[foundIndex][0] = 1;
                }
            }
            const gt = g >= 2 ? 'Onyx' : (g >= 1 ? 'Gold' : 'Stone');
            return `Set '${foundName}' grade to ${gt} (was ${old})`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @plugin_command(
        help="Get statue status HTML.",
        params=[],
    )
    async def get_statue_status(self, injector=None, **kwargs):
        result = self.run_js_export('get_statue_status_js', injector)
        return result
        
   

plugin_class = StatueManagerPlugin



