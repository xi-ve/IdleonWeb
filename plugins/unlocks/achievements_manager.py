from typing import Optional
from plugin_system import PluginBase, js_export, ui_button, ui_input_with_button, ui_search_with_results

class AchievementsPlugin(PluginBase):
    VERSION = "1.0.0"
    DESCRIPTION = "Achievements tools: unlock all, unlock by ID/range, and overview per world."
    PLUGIN_ORDER = 6
    CATEGORY = "Unlocks"

    def __init__(self, config=None):
        super().__init__(config or {})
        self.name = 'achievements_manager'

    async def cleanup(self):
        pass

    async def update(self):
        pass

    async def on_config_changed(self, config):
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)

    async def on_game_ready(self):
        pass

    @ui_button(
        label="Unlock All Achievements",
        description="Sets every achievement as obtained (SteamAchieve=1; sets AchieveReg=-1).",
        category="Actions",
        order=1
    )
    async def unlock_all_achievements_ui(self):
        if hasattr(self, 'injector') and self.injector:
            return self.run_js_export('unlock_all_achievements_js', self.injector)
        return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_button(
        label="Lock All Achievements",
        description="Locks every achievement (SteamAchieve=0; sets AchieveReg=0).",
        category="Actions",
        order=2
    )
    async def lock_all_achievements_ui(self):
        if hasattr(self, 'injector') and self.injector:
            return self.run_js_export('lock_all_achievements_js', self.injector)
        return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_input_with_button(
        label="Unlock Achievements by ID(s)",
        description="Comma-separated IDs, ranges, or world-index. Examples: 5, 12-20, 33, W2, W3#4-9.",
        button_text="Unlock IDs",
        placeholder="e.g. 1,5-10,42 or W2#5-12",
        category="Actions",
        order=3
    )
    async def unlock_achievements_by_id_ui(self, value: Optional[str] = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                return self.run_js_export('unlock_achievements_by_id_js', self.injector, ids_text=value or "")
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_input_with_button(
        label="Lock Achievements by ID(s)",
        description="Comma-separated IDs, ranges, or world-index. Examples: 5, 12-20, 33, W2, W3#4-9.",
        button_text="Lock IDs",
        placeholder="e.g. 1,5-10,42 or W2#5-12",
        category="Actions",
        order=4
    )
    async def lock_achievements_by_id_ui(self, value: Optional[str] = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                return self.run_js_export('lock_achievements_by_id_js', self.injector, ids_text=value or "")
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_search_with_results(
        label="Achievement Status Overview",
        description="Show per-world achievement status with filters.",
        button_text="Show Achievement Status",
        placeholder="Filter: 'world 3', 'locked', 'unlocked', 'steam', 'reg', id (e.g. 123)",
        category="Search",
        order=0
    )
    async def achievement_status_overview_ui(self, value: Optional[str] = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                return self.run_js_export('get_achievement_status_js', self.injector, filter_query=value or "")
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export()
    def unlock_all_achievements_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const eng = ctx["com.stencyl.Engine"].engine;

            let steam = eng.getGameAttribute("SteamAchieve");
            let reg = eng.getGameAttribute("AchieveReg");
            const n = Math.max(Array.isArray(steam) ? steam.length : 0, Array.isArray(reg) ? reg.length : 0, 100);
            if (!Array.isArray(steam)) steam = new Array(n).fill(0);
            if (!Array.isArray(reg)) reg = new Array(n).fill(0);

            let changed = 0, already = 0;
            for (let i = 0; i < n; i++) {
                const had = (steam[i] === 1) || (reg[i] === -1);
                if (had) { already++; } else { changed++; }
                steam[i] = 1;
                reg[i] = -1;
            }

            eng.setGameAttribute && eng.setGameAttribute("SteamAchieve", steam);
            eng.setGameAttribute && eng.setGameAttribute("AchieveReg", reg);
            try { if (typeof eng.saveGame === "function") eng.saveGame(); } catch {}
            return `Unlocked all achievements. Changed: ${changed}, already obtained: ${already}.`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def lock_all_achievements_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const eng = ctx["com.stencyl.Engine"].engine;

            let steam = eng.getGameAttribute("SteamAchieve");
            let reg = eng.getGameAttribute("AchieveReg");
            const n = Math.max(Array.isArray(steam) ? steam.length : 0, Array.isArray(reg) ? reg.length : 0, 100);
            if (!Array.isArray(steam)) steam = new Array(n).fill(0);
            if (!Array.isArray(reg)) reg = new Array(n).fill(0);

            let changed = 0, already = 0;
            for (let i = 0; i < n; i++) {
                const wasUnlocked = (steam[i] === 1) || (reg[i] === -1);
                if (wasUnlocked) { changed++; } else { already++; }
                steam[i] = 0;
                reg[i] = 0;
            }

            eng.setGameAttribute && eng.setGameAttribute("SteamAchieve", steam);
            eng.setGameAttribute && eng.setGameAttribute("AchieveReg", reg);
            try { if (typeof eng.saveGame === "function") eng.saveGame(); } catch {}
            return `Locked all achievements. Changed: ${changed}, already locked: ${already}.`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export(params=["ids_text"])
    def unlock_achievements_by_id_js(self, ids_text: str = ""):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const eng = ctx["com.stencyl.Engine"].engine;

            let steam = eng.getGameAttribute("SteamAchieve");
            let reg = eng.getGameAttribute("AchieveReg");
            const n = Math.max(Array.isArray(steam) ? steam.length : 0, Array.isArray(reg) ? reg.length : 0, 100);

            const CL = eng.getGameAttribute("CustomLists");
            const namesSrc = CL?.h?.RegAchieves;
            const achName = i => { try { const row = Array.isArray(namesSrc) ? namesSrc[i] : null; return row ? String(row[0]) : `Ach ${i}`; } catch { return `Ach ${i}`; } };
            const norm = s => String(s || '').toLowerCase().replace(/_/g, ' ').replace(/\\s+/g, ' ').trim();
            const findByName = (needle) => {
                const t = norm(needle); if (!t) return -1;
                const L = Array.isArray(namesSrc) ? namesSrc.length : 0;
                for (let i = 0; i < L; i++) { if (norm(achName(i)) === t) return i; }
                for (let i = 0; i < L; i++) { if (norm(achName(i)).includes(t)) return i; }
                return -1;
            };

            const computeWorldIds = () => {
                const total = Math.max(n, Array.isArray(namesSrc) ? namesSrc.length : 0);
                const boundaries = [
                    { start: 0, endName: "Big_Frog_Big_Mad" },
                    { startName: "Down by the Desert", endName: "Skill Master" },
                    { startName: "Snowy Wonderland", endName: "Equinox Visitor" },
                    { startName: "Milky Wayfarer", endName: "Veritable Master" },
                    { startName: "The Plateauourist", endName: "Hug from Timmy" },
                    { startName: "Valley Visitor", endName: "Straw Hat Stacking" }
                ];
                const worlds = [];
                let lastEnd = -1;
                for (let w = 0; w < boundaries.length; w++) {
                    let { start, startName, endName } = boundaries[w];
                    if (!Number.isFinite(start)) start = findByName(startName);
                    let end = findByName(endName);
                    if (!Number.isFinite(start) || start < 0) start = lastEnd + 1;
                    if (!Number.isFinite(end) || end < start) end = start;
                    const arr = [];
                    for (let i = start; i <= Math.min(end, total - 1); i++) arr.push(i);
                    worlds.push(arr);
                    lastEnd = end;
                }
                return worlds;
            };

            const worldIdsList = computeWorldIds();

            const raw = String(ids_text ?? '').trim();
            if (!raw) return "";

            const candidateIds = new Set();
            const addCandidate = (x) => { if (Number.isFinite(x) && x >= 0) candidateIds.add(x | 0); };
            const addWorld = (wIdx) => { const arr = worldIdsList[wIdx] || []; for (const aId of arr) addCandidate(aId); };

            const tokens = raw.split(/[ ,\\s]+/).map(t => t.trim()).filter(Boolean);
            for (const tRaw of tokens) {
                const t = tRaw.toLowerCase();
                let m = t.match(/^(?:w|world)\\s*(\\d+)[#:\\-\\.]?\\s*(\\d+)\\s*\\-\\s*(\\d+)$/);
                if (m) {
                    const wNum = parseInt(m[1], 10), a = parseInt(m[2], 10), b = parseInt(m[3], 10);
                    const arr = worldIdsList[(wNum | 0) - 1] || [];
                    if (Number.isFinite(a) && Number.isFinite(b) && arr.length) {
                        let start = Math.max(1, Math.min(a, b)), end = Math.min(arr.length, Math.max(a, b));
                        for (let k = start; k <= end; k++) addCandidate(arr[k - 1]);
                    }
                    continue;
                }
                m = t.match(/^(?:w|world)\\s*(\\d+)[#:\\-\\.]?\\s*(\\d+)$/);
                if (m) {
                    const wNum = parseInt(m[1], 10), idx = parseInt(m[2], 10);
                    const arr = worldIdsList[(wNum | 0) - 1] || [];
                    if (Number.isFinite(idx) && idx >= 1 && idx <= arr.length) addCandidate(arr[idx - 1]);
                    continue;
                }
                m = t.match(/^(?:w|world)\\s*(\\d+)$/);
                if (m) { const wNum = parseInt(m[1], 10); if (Number.isFinite(wNum) && wNum > 0) addWorld(wNum - 1); continue; }
                m = t.match(/^(\\d+)-(\\d+)$/);
                if (m) { let a = parseInt(m[1], 10), b = parseInt(m[2], 10); if (Number.isFinite(a) && Number.isFinite(b)) { if (a > b) { const tmp = a; a = b; b = tmp; } for (let i = a; i <= b; i++) addCandidate(i); } continue; }
                const num = parseInt(t, 10); if (Number.isFinite(num)) { addCandidate(num); continue; }
            }

            if (candidateIds.size === 0) return "No valid IDs parsed.";

            const flatIds = worldIdsList.flat().filter(x => Number.isFinite(x));
            const maxWorldId = flatIds.length ? Math.max(...flatIds) : -1;
            const maxCandidate = Math.max(...Array.from(candidateIds));
            const N = Math.max(n, maxWorldId + 1, (Number.isFinite(maxCandidate) ? (maxCandidate + 1) : 0));
            if (!Array.isArray(steam) || steam.length < N) {
                const tmp = new Array(N).fill(0);
                if (Array.isArray(steam)) { for (let i = 0; i < steam.length; i++) tmp[i] = steam[i] ?? 0; }
                steam = tmp;
            }
            if (!Array.isArray(reg) || reg.length < N) {
                const tmp = new Array(N).fill(0);
                if (Array.isArray(reg)) { for (let i = 0; i < reg.length; i++) tmp[i] = Number.isFinite(reg[i]) ? reg[i] : 0; }
                reg = tmp;
            }

            let changed = 0, already = 0;
            const applied = [];
            for (const i of candidateIds) {
                if (!(i >= 0 && i < N)) continue;
                const had = (steam[i] === 1) || (reg[i] === -1);
                if (had) { already++; } else { changed++; }
                steam[i] = 1;
                reg[i] = -1;
                applied.push(i);
            }

            eng.setGameAttribute && eng.setGameAttribute("SteamAchieve", steam);
            eng.setGameAttribute && eng.setGameAttribute("AchieveReg", reg);
            try { if (typeof eng.saveGame === "function") eng.saveGame(); } catch {}

            const preview = applied.sort((a,b)=>a-b).slice(0, 8).join(', ');
            return `Unlocked ${changed} achievement(s), ${already} already obtained. IDs: ${preview}${applied.length>8? ', ...':''}`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export(params=["ids_text"])
    def lock_achievements_by_id_js(self, ids_text: str = ""):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const eng = ctx["com.stencyl.Engine"].engine;

            let steam = eng.getGameAttribute("SteamAchieve");
            let reg = eng.getGameAttribute("AchieveReg");
            const n = Math.max(Array.isArray(steam) ? steam.length : 0, Array.isArray(reg) ? reg.length : 0, 100);

            const CL = eng.getGameAttribute("CustomLists");
            const namesSrc = CL?.h?.RegAchieves;
            const achName = i => { try { const row = Array.isArray(namesSrc) ? namesSrc[i] : null; return row ? String(row[0]) : `Ach ${i}`; } catch { return `Ach ${i}`; } };
            const norm = s => String(s || '').toLowerCase().replace(/_/g, ' ').replace(/\\s+/g, ' ').trim();
            const findByName = (needle) => {
                const t = norm(needle); if (!t) return -1;
                const L = Array.isArray(namesSrc) ? namesSrc.length : 0;
                for (let i = 0; i < L; i++) { if (norm(achName(i)) === t) return i; }
                for (let i = 0; i < L; i++) { if (norm(achName(i)).includes(t)) return i; }
                return -1;
            };

            const computeWorldIds = () => {
                const total = Math.max(n, Array.isArray(namesSrc) ? namesSrc.length : 0);
                const boundaries = [
                    { start: 0, endName: "Big_Frog_Big_Mad" },
                    { startName: "Down by the Desert", endName: "Skill Master" },
                    { startName: "Snowy Wonderland", endName: "Equinox Visitor" },
                    { startName: "Milky Wayfarer", endName: "Veritable Master" },
                    { startName: "The Plateauourist", endName: "Hug from Timmy" },
                    { startName: "Valley Visitor", endName: "Straw Hat Stacking" }
                ];
                const worlds = [];
                let lastEnd = -1;
                for (let w = 0; w < boundaries.length; w++) {
                    let { start, startName, endName } = boundaries[w];
                    if (!Number.isFinite(start)) start = findByName(startName);
                    let end = findByName(endName);
                    if (!Number.isFinite(start) || start < 0) start = lastEnd + 1;
                    if (!Number.isFinite(end) || end < start) end = start;
                    const arr = [];
                    for (let i = start; i <= Math.min(end, total - 1); i++) arr.push(i);
                    worlds.push(arr);
                    lastEnd = end;
                }
                return worlds;
            };

            const worldIdsList = computeWorldIds();

            const raw = String(ids_text ?? '').trim();
            if (!raw) return "";

            const candidateIds = new Set();
            const addCandidate = (x) => { if (Number.isFinite(x) && x >= 0) candidateIds.add(x | 0); };
            const addWorld = (wIdx) => { const arr = worldIdsList[wIdx] || []; for (const aId of arr) addCandidate(aId); };

            const tokens = raw.split(/[ ,\\s]+/).map(t => t.trim()).filter(Boolean);
            for (const tRaw of tokens) {
                const t = tRaw.toLowerCase();
                let m = t.match(/^(?:w|world)\\s*(\\d+)[#:\\-\\.]?\\s*(\\d+)\\s*\\-\\s*(\\d+)$/);
                if (m) {
                    const wNum = parseInt(m[1], 10), a = parseInt(m[2], 10), b = parseInt(m[3], 10);
                    const arr = worldIdsList[(wNum | 0) - 1] || [];
                    if (Number.isFinite(a) && Number.isFinite(b) && arr.length) {
                        let start = Math.max(1, Math.min(a, b)), end = Math.min(arr.length, Math.max(a, b));
                        for (let k = start; k <= end; k++) addCandidate(arr[k - 1]);
                    }
                    continue;
                }
                m = t.match(/^(?:w|world)\\s*(\\d+)[#:\\-\\.]?\\s*(\\d+)$/);
                if (m) {
                    const wNum = parseInt(m[1], 10), idx = parseInt(m[2], 10);
                    const arr = worldIdsList[(wNum | 0) - 1] || [];
                    if (Number.isFinite(idx) && idx >= 1 && idx <= arr.length) addCandidate(arr[idx - 1]);
                    continue;
                }
                m = t.match(/^(?:w|world)\\s*(\\d+)$/);
                if (m) { const wNum = parseInt(m[1], 10); if (Number.isFinite(wNum) && wNum > 0) addWorld(wNum - 1); continue; }
                m = t.match(/^(\\d+)-(\\d+)$/);
                if (m) { let a = parseInt(m[1], 10), b = parseInt(m[2], 10); if (Number.isFinite(a) && Number.isFinite(b)) { if (a > b) { const tmp = a; a = b; b = tmp; } for (let i = a; i <= b; i++) addCandidate(i); } continue; }
                const num = parseInt(t, 10); if (Number.isFinite(num)) { addCandidate(num); continue; }
            }

            if (candidateIds.size === 0) return "No valid IDs parsed.";

            const flatIds = worldIdsList.flat().filter(x => Number.isFinite(x));
            const maxWorldId = flatIds.length ? Math.max(...flatIds) : -1;
            const maxCandidate = Math.max(...Array.from(candidateIds));
            const N = Math.max(n, maxWorldId + 1, (Number.isFinite(maxCandidate) ? (maxCandidate + 1) : 0));
            if (!Array.isArray(steam) || steam.length < N) {
                const tmp = new Array(N).fill(0);
                if (Array.isArray(steam)) { for (let i = 0; i < steam.length; i++) tmp[i] = steam[i] ?? 0; }
                steam = tmp;
            }
            if (!Array.isArray(reg) || reg.length < N) {
                const tmp = new Array(N).fill(0);
                if (Array.isArray(reg)) { for (let i = 0; i < reg.length; i++) tmp[i] = Number.isFinite(reg[i]) ? reg[i] : 0; }
                reg = tmp;
            }

            let changed = 0, already = 0;
            const applied = [];
            for (const i of candidateIds) {
                if (!(i >= 0 && i < N)) continue;
                const had = (steam[i] === 1) || (reg[i] === -1);
                if (had) { changed++; } else { already++; }
                steam[i] = 0;
                reg[i] = 0;
                applied.push(i);
            }

            eng.setGameAttribute && eng.setGameAttribute("SteamAchieve", steam);
            eng.setGameAttribute && eng.setGameAttribute("AchieveReg", reg);
            try { if (typeof eng.saveGame === "function") eng.saveGame(); } catch {}

            const preview = applied.sort((a,b)=>a-b).slice(0, 8).join(', ');
            return `Locked ${changed} achievement(s), ${already} already locked. IDs: ${preview}${applied.length>8? ', ...':''}`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export(params=["filter_query"])
    def get_achievement_status_js(self, filter_query: str = ""):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const eng = ctx["com.stencyl.Engine"].engine;

            const steam = eng.getGameAttribute("SteamAchieve");
            const reg = eng.getGameAttribute("AchieveReg");
            const n = Math.max(Array.isArray(steam) ? steam.length : 0, Array.isArray(reg) ? reg.length : 0, 100);

            const CL = eng.getGameAttribute("CustomLists");
            const namesSrc = CL?.h?.RegAchieves;
            const achName = i => { try { const row = Array.isArray(namesSrc) ? namesSrc[i] : null; return row ? String(row[0]) : `Ach ${i}`; } catch { return `Ach ${i}`; } };
            const norm = s => String(s || '').toLowerCase().replace(/_/g, ' ').replace(/\\s+/g, ' ').trim();
            const findByName = (needle) => {
                const t = norm(needle); if (!t) return -1;
                const L = Array.isArray(namesSrc) ? namesSrc.length : 0;
                for (let i = 0; i < L; i++) { if (norm(achName(i)) === t) return i; }
                for (let i = 0; i < L; i++) { if (norm(achName(i)).includes(t)) return i; }
                return -1;
            };

            const computeWorldIds = () => {
                const total = Math.max(n, Array.isArray(namesSrc) ? namesSrc.length : 0);
                const boundaries = [
                    { start: 0, endName: "Big_Frog_Big_Mad" },
                    { startName: "Down by the Desert", endName: "Skill Master" },
                    { startName: "Snowy Wonderland", endName: "Equinox Visitor" },
                    { startName: "Milky Wayfarer", endName: "Veritable Master" },
                    { startName: "The Plateauourist", endName: "Hug from Timmy" },
                    { startName: "Valley Visitor", endName: "Straw Hat Stacking" }
                ];
                const worlds = []; let lastEnd = -1;
                for (let w = 0; w < boundaries.length; w++) {
                    let { start, startName, endName } = boundaries[w];
                    if (!Number.isFinite(start)) start = findByName(startName);
                    let end = findByName(endName);
                    if (!Number.isFinite(start) || start < 0) start = lastEnd + 1;
                    if (!Number.isFinite(end) || end < start) end = start;
                    const arr = []; for (let i = start; i <= Math.min(end, total - 1); i++) arr.push(i);
                    worlds.push(arr); lastEnd = end;
                }
                return worlds;
            };

            const worldIdsList = computeWorldIds();
            const totalWorlds = worldIdsList.length || 1;

            const filter = (filter_query || '').toLowerCase().trim();
            const mWorldIdx = filter.match(/^(?:w|world)\\s*(\\d+)[#:\\-\\.]?\\s*(\\d+)$/);
            let onlyId = null;
            if (mWorldIdx) {
                const wNum = parseInt(mWorldIdx[1], 10), idx = parseInt(mWorldIdx[2], 10);
                const arr = worldIdsList[(wNum|0) - 1] || [];
                if (Number.isFinite(idx) && idx >= 1 && idx <= arr.length) onlyId = arr[idx - 1];
            } else {
                const idOnlyMatch = filter && filter.match(/^(\\d{1,4})$/);
                onlyId = idOnlyMatch ? parseInt(idOnlyMatch[1], 10) : null;
            }
            const filterWorldMatch = filter.match(/world\\s*(\\d+)/);
            const filterWorld = filterWorldMatch ? (parseInt(filterWorldMatch[1], 10) - 1) : null;
            const wantLocked = filter.includes('locked');
            const wantUnlocked = filter.includes('unlocked');
            const wantSteamOnly = filter.includes('steam');
            const wantRegOnly = filter.includes('reg');

            let html = '';
            html += `<div style=\"font-weight:bold;font-size:16px;margin-bottom:8px;\">🏆 Achievement Status Overview</div>`;

            let grandTotal = 0, grandObtained = 0, shownWorlds = 0;

            for (let w = 0; w < totalWorlds; w++) {
                if (filterWorld !== null && w !== filterWorld) continue;
                const ids = (worldIdsList[w] || []).filter(i => Number.isFinite(i));
                if (!ids.length) continue;

                let obtained = 0, total = 0;
                const rows = [];

                for (const i of ids) {
                    if (onlyId !== null && i !== onlyId) continue;
                    const s = (Array.isArray(steam) && i < steam.length) ? ((steam[i] ?? 0) | 0) : 0;
                    const rRaw = (Array.isArray(reg) && i < reg.length) ? reg[i] : 0;
                    const r = Number.isFinite(rRaw) ? (rRaw | 0) : 0;
                    const has = (s === 1) || (r === -1);
                    if (wantLocked && has) continue;
                    if (wantUnlocked && !has) continue;
                    if (wantSteamOnly && s !== 1) continue;
                    if (wantRegOnly && r !== -1) continue;

                    total++;
                    if (has) obtained++;

                    const badgeColor = has ? '#4CAF50' : '#f44336';
                    const textColor = '#fff';
                    const label = has ? 'Obtained' : 'Locked';
                    const nm = achName(i).replace(/</g, '&lt;').replace(/>/g, '&gt;');
                    const localIdx = Math.max(0, (worldIdsList[w] || []).indexOf(i)) + 1;
                    rows.push(`<div style=\\"padding:6px 8px;margin:4px 0;background:rgba(255,255,255,0.03);border-left:3px solid #555;\\">`
                        + `<div style=\\"display:flex;align-items:center;gap:8px;flex-wrap:wrap;\\">`
                        + `<strong>#${i} (W${w + 1}-${localIdx})</strong><span>${nm}</span>`
                        + `<span style=\\"display:inline-block;padding:2px 6px;margin-left:auto;border-radius:4px;background:${badgeColor};color:${textColor};font-size:11px;\\">${label}</span>`
                        + `</div>`
                        + `</div>`);
                }

                if (rows.length === 0) continue;

                shownWorlds++;
                grandTotal += total;
                grandObtained += obtained;
                const pct = total > 0 ? Math.round(obtained / total * 100) : 0;

                html += `
                <div style=\"margin:12px 0 16px 0;padding:10px;border:1px solid #333;border-radius:8px;background:linear-gradient(135deg,#1e1e1e,#262626);\">\n\
                    <div style=\"display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;\">\n\
                        <div style=\"font-weight:bold;color:#9ad;\">🌍 World ${w + 1}</div>\n\
                        <div style=\"color:#ccc;\">Obtained: ${obtained}/${total} (${pct}%)</div>\n\
                    </div>\n\
                    <div style=\"margin-top:8px;\">${rows.join('')}</div>\n\
                </div>`;
            }

            if (!html) { return `<div>No results${filter ? ` for \\\"${filter}\\\"` : ''}.</div>`; }

            const grandPct = grandTotal > 0 ? Math.round(grandObtained / grandTotal * 100) : 0;
            html = html + `
                <div style=\"margin-top:12px;padding:10px;background:rgba(0,0,0,0.2);border-radius:6px;\">\n\
                    <div style=\"font-weight:bold;margin-bottom:4px;\">📊 Summary</div>\n\
                    <div>Worlds shown: ${shownWorlds}</div>\n\
                    <div>Achievements obtained (shown): ${grandObtained}/${grandTotal} (${grandPct}%)</div>\n\
                </div>`;

            return html;
        } catch (e) { return `Error: ${e.message}`; }
        '''

plugin_class = AchievementsPlugin
