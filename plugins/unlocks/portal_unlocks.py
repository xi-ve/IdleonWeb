from typing import Optional
from plugin_system import PluginBase, js_export, ui_button, console, ui_search_with_results
from plugin_system import ui_autocomplete_input

class PortalUnlocksPlugin(PluginBase):
    VERSION = "1.0.0"
    DESCRIPTION = "Portal unlock tools: auto-kill to unlock current portal and zero all portal requirements in current world."
    PLUGIN_ORDER = 5
    CATEGORY = "Unlocks"

    def __init__(self, config=None):
        super().__init__(config or {})
        self.name = 'portal_unlocks'

    async def cleanup(self): pass
    async def update(self): pass
    async def on_config_changed(self, config): 
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)
    async def on_game_ready(self): pass

    @ui_button(
        label="Auto-kill to Unlock Current Portal",
        description="Repeatedly kills mobs until the first portal on the current map unlocks. Stops when you teleport/change maps for safety.",
        category="Actions",
        order=1
    )
    async def autokill_current_portal_ui(self):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('autokill_current_portal_js', self.injector)
            return result
        return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_button(
        label="Unlock All Portals in Current World",
        description="Zero all portal kill requirements for maps in the current world and set related quest flags where needed.",
        category="Actions",
        order=2
    )
    async def unlock_all_portals_world_ui(self):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('unlock_all_portals_world_js', self.injector)
            return result
        return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_autocomplete_input(
        label="Unlock Map Portals (Wn Map m)",
        description="Unlock all portals on a specific map. Enter 'W1 Map 3' (World 1, Map 3).",
        button_text="Unlock Map Portals",
        placeholder="e.g. W1 Map 3",
        category="Actions",
        order=3
    )
    async def unlock_portals_by_world_map_ui(self, value: Optional[str] = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = self.run_js_export('unlock_portals_by_world_map_js', self.injector, input_text=value or "")
                return result
            except Exception as e:
                return f"ERROR: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    def get_unlock_portals_by_world_map_ui_autocomplete(self, query: str = ""):
        """Provide autocomplete suggestions like 'W1 Map 3' for maps that still have locked portals."""
        try:
            if not hasattr(self, 'injector') or not self.injector:
                return []
            suggestions = self.run_js_export('get_locked_portal_maps_js', self.injector)
            if not isinstance(suggestions, list):
                return []
            q = (query or '').lower().strip()
            if not q:
                return suggestions[:20]
            return [s for s in suggestions if q in s.lower()][:20]
        except Exception:
            return []

    @ui_search_with_results(
        label="Portal Status Overview",
        description="Show each world with per-map portal unlock status.",
        button_text="Show Portal Status",
        placeholder="Filter: 'world 3', 'locked', 'unlocked', map id (e.g. 123)",
        category="Search",
        order=0
    )
    async def portal_status_overview_ui(self, value: Optional[str] = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = self.run_js_export('get_portal_status_js', self.injector, filter_query=value or "")
                return result
            except Exception as e:
                return f"ERROR: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["input_text"])
    def unlock_portals_by_world_map_js(self, input_text=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const eng = ctx["com.stencyl.Engine"].engine;

            const kills = eng.getGameAttribute("KillsLeft2Advance");
            if (!Array.isArray(kills)) return "Error: KillsLeft2Advance missing";

            const raw = (input_text || '').trim();
            if (!raw) return "Enter input like 'W1 Map 3'";
            const s = raw.toLowerCase();

            // Parse world and map numbers from inputs like "W1 Map 3", "w1map3", "world 2 map 10"
            const wMatch = s.match(/\\bw\\s*(\\d+)\\b|\\bworld\\s*(\\d+)\\b/);
            const mapMatch = s.match(/\\bmap\\s*(\\d+)\\b|\\bmap(\\d+)\\b/);
            const wNum = wMatch ? parseInt(wMatch[1] || wMatch[2], 10) : null;
            let mapNum = mapMatch ? parseInt(mapMatch[1] || mapMatch[2], 10) : null;

            if (wNum === null || mapNum === null || !Number.isFinite(wNum) || !Number.isFinite(mapNum)) {
                return "Invalid input. Use 'W1 Map 3'";
            }

            const worldIdx = wNum - 1;
            if (!(Number.isFinite(worldIdx)) || worldIdx < 0) return `Invalid world: ${wNum}`;

            // Try multiple interpretations:
            // A) local index within world (worldIdx*50 + mapNum)
            // B) global map id (mapNum)
            // C) local index is 1-based (worldIdx*50 + (mapNum-1))
            const candA = worldIdx * 50 + mapNum;
            const candB = mapNum;
            const candC = worldIdx * 50 + (mapNum - 1);

            let mapId = null;
            if (candA >= 0 && candA < kills.length && Array.isArray(kills[candA])) {
                mapId = candA;
            } else if (candC >= 0 && candC < kills.length && Array.isArray(kills[candC])) {
                mapId = candC;
                mapNum = mapNum - 1; // adjust local for messaging
            } else if (candB >= 0 && candB < kills.length && Array.isArray(kills[candB])) {
                // Accept global map id when it matches
                mapId = candB;
                // Recompute mapNum as local for messaging
                mapNum = mapId - worldIdx * 50;
            } else {
                return `Could not resolve map from input. Tried IDs: ${candA}, ${candC}, ${candB}`;
            }

            const arr = kills[mapId];
            if (!Array.isArray(arr) || arr.length === 0) return `Map ${mapId} has no portals.`;

            let changed = 0, already = 0;
            for (let i = 0; i < arr.length; i++) {
                if ((arr[i] | 0) > 0) { arr[i] = 0; changed++; } else { already++; }
            }

            const localIdx = mapNum;
            if (changed === 0) return `W${worldIdx + 1} Map ${localIdx}: all portals already unlocked (${already}/${arr.length}).`;
            return `Unlocked ${changed} portal(s) on W${worldIdx + 1} Map ${localIdx} (global Map ${mapId}).`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def get_locked_portal_maps_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const eng = ctx["com.stencyl.Engine"].engine;

            const kills = eng.getGameAttribute("KillsLeft2Advance");
            if (!Array.isArray(kills)) return [];

            const suggestions = [];
            for (let m = 0; m < kills.length; m++) {
                const arr = kills[m];
                if (!Array.isArray(arr) || arr.length === 0) continue;
                const locked = arr.some(v => (v | 0) > 0);
                if (!locked) continue;
                const w = Math.floor(m / 50);
                const local = m - w * 50;
                suggestions.push(`W${w + 1} Map ${local}`);
            }
            return suggestions;
        } catch (e) {
            return [];
        }
        '''

    @js_export()
    def autokill_current_portal_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const eng = ctx["com.stencyl.Engine"].engine;

            const currentMap = (eng.getGameAttribute("CurrentMap") | 0) >>> 0;
            const killsList = eng.getGameAttribute("KillsLeft2Advance");
            if (!Array.isArray(killsList)) return "Error: Portal kill requirements not found";
            const killReqs = killsList[currentMap];
            if (!Array.isArray(killReqs) || killReqs.length === 0) return "Error: No portal data for this map";

            const portalIndex = 0; // target the first portal on this map

            function killAllMobsOnce() {
                const mobs = eng.getGameAttribute("MapMonstersList");
                const hp   = eng.getGameAttribute("MonsterHP");
                const alive = eng.getGameAttribute("MonsterAlive");
                const willDie = eng.getGameAttribute("MonsterWillDie");
                if (!Array.isArray(mobs) || !Array.isArray(hp) || !Array.isArray(alive)) return 0;
                let killedCount = 0;
                for (let i = 0; i < mobs.length; i++) {
                    const actor = mobs[i];
                    const behav = actor?.behaviors?.getBehavior?.("ActorEvents_1");
                    if (!behav) continue;
                    const id = (behav._MonsterID | 0) >>> 0;
                    if (!(id >= 0)) continue;
                    if (alive[id] !== 1) continue;
                    if (hp[id] <= 0) continue;
                    hp[id] = 0;
                    if (Array.isArray(willDie)) willDie[id] = 1;
                    killedCount++;
                }
                return killedCount;
            }

            // Avoid multiple simultaneous loops
            if (!window.__portalUnlock) window.__portalUnlock = {};
            if (window.__portalUnlock.autoKillActive) {
                return "Auto-kill is already running for the current session. Check console for progress.";
            }
            window.__portalUnlock.autoKillActive = true;

            const tickDelayMs = 15;
            let ticks = 0;
            const maxTicks = 60000; // safety cap

            (function autoKillUntilPortal(){
                try {
                    // Abort if the player changed maps
                    const liveMap = (eng.getGameAttribute("CurrentMap") | 0) >>> 0;
                    if (liveMap !== currentMap) {
                        console.log("[portal_unlocks] Map changed; aborting auto-kill.");
                        window.__portalUnlock.autoKillActive = false;
                        return;
                    }

                    const remaining = (eng.getGameAttribute("KillsLeft2Advance")[currentMap] || [])[portalIndex] | 0;
                    if (remaining <= 0) {
                        console.log("[portal_unlocks] Portal unlocked or no kills needed.");
                        window.__portalUnlock.autoKillActive = false;
                        return;
                    }
                    const justKilled = killAllMobsOnce();
                    const newRemaining = ((eng.getGameAttribute("KillsLeft2Advance")[currentMap] || [])[portalIndex] | 0);
                    console.log(`[portal_unlocks] Killed ${justKilled} mobs. ${newRemaining} kills left for portal...`);
                    ticks++;
                    if (ticks < maxTicks && window.__portalUnlock.autoKillActive) {
                        setTimeout(autoKillUntilPortal, tickDelayMs);
                    } else if (ticks >= maxTicks) {
                        console.warn('[portal_unlocks] Stopped after safety cap.');
                        window.__portalUnlock.autoKillActive = false;
                    }
                } catch (e) {
                    console.error('[portal_unlocks] Error in auto-kill loop:', e);
                    window.__portalUnlock.autoKillActive = false;
                }
            })();

            const startRemaining = (eng.getGameAttribute("KillsLeft2Advance")[currentMap] || [])[portalIndex] | 0;
            return `Started auto-kill for map ${currentMap}, portal #${portalIndex + 1}. Remaining: ${startRemaining}. Progress logged in console.`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def unlock_all_portals_world_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const eng = ctx["com.stencyl.Engine"].engine;

            const curMap = eng.getGameAttribute("CurrentMap") | 0;
            const world = Math.floor(curMap / 50);
            const s = world * 50, e = s + 49;

            const kills = eng.getGameAttribute("KillsLeft2Advance");
            if (!Array.isArray(kills)) return "Error: KillsLeft2Advance missing";

            let portalsZeroed = 0, mapsTouched = 0;
            for (let m = s; m <= e; m++) {
                const a = kills[m];
                if (!Array.isArray(a) || a.length === 0) continue;
                mapsTouched++;
                for (let i = 0; i < a.length; i++) {
                    if (a[i] !== 0) { a[i] = 0; portalsZeroed++; }
                }
            }

            const QS = eng.getGameAttribute("QuestStatus");
            const setReq = (name) => {
                const q = QS?.h?.[name];
                if (!q || !Array.isArray(q)) return 0;
                const before0 = q[0] | 0;
                q[0] = 1;
                return (before0 !== 1) | 0;
            };

            let reqSet = 0;
            if (QS && QS.h) {
                if (world === 3) {
                    for (let i = 11; i <= 15; i++) reqSet += setReq("Gobo" + i);
                }
                if (world === 5) {
                    for (let i = 1; i <= 6; i++) {
                        reqSet += setReq("Lafu_Shi" + i) || setReq("LafuShi" + i);
                    }
                }
            }

            return `World ${world + 1}: maps touched ${mapsTouched}, portals zeroed ${portalsZeroed}, quest reqs set ${reqSet}`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export(params=["filter_query"])
    def get_portal_status_js(self, filter_query=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const eng = ctx["com.stencyl.Engine"].engine;

            const kills = eng.getGameAttribute("KillsLeft2Advance");
            if (!Array.isArray(kills)) return "Error: KillsLeft2Advance missing";

            const curMap = eng.getGameAttribute("CurrentMap") | 0;
            const curWorld = Math.floor(curMap / 50);

            const filter = (filter_query || '').toLowerCase().trim();
            const filterWorldMatch = filter.match(/world\\s*(\\d+)/);
            const filterWorld = filterWorldMatch ? (parseInt(filterWorldMatch[1], 10) - 1) : null;
            const wantLocked = filter.includes('locked');
            const wantUnlocked = filter.includes('unlocked');
            const mapIdMatch = filter && filter.match(/^(\\d{1,4})$/);
            const onlyMapId = mapIdMatch ? parseInt(mapIdMatch[1], 10) : null;

            const totalMaps = kills.length;
            const totalWorlds = Math.max(1, Math.floor((totalMaps - 1) / 50) + 1);

            let html = '';
            html += `<div style="font-weight:bold;font-size:16px;margin-bottom:8px;">🌀 Portal Status Overview</div>`;
            html += `<div style="margin:8px 0 12px 0;color:#ccc;">`+
                    `Worlds: ${totalWorlds} • Current World: ${curWorld + 1} • Total Maps: ${totalMaps}`+
                    `</div>`;

            let grandTotalPortals = 0;
            let grandUnlocked = 0;
            let grandMapsWithPortals = 0;

            for (let w = 0; w < totalWorlds; w++) {
                if (filterWorld !== null && w !== filterWorld) continue;
                const start = w * 50;
                const end = Math.min(start + 49, totalMaps - 1);

                let mapsWithPortals = 0;
                let totalPortals = 0;
                let unlockedPortals = 0;

                const mapRows = [];

                for (let m = start; m <= end; m++) {
                    if (onlyMapId !== null && m !== onlyMapId) continue;
                    const arr = kills[m];
                    if (!Array.isArray(arr) || arr.length === 0) continue;
                    mapsWithPortals++;

                    const parts = [];
                    for (let i = 0; i < arr.length; i++) {
                        const val = arr[i] | 0;
                        const isUnlocked = val <= 0;
                        totalPortals++;
                        if (isUnlocked) unlockedPortals++;
                        const badgeColor = isUnlocked ? '#4CAF50' : '#f44336';
                        const textColor = '#fff';
                        const label = isUnlocked ? 'Unlocked' : `${val}`;
                        parts.push(`<span style=\"display:inline-block;padding:2px 6px;margin:0 4px 4px 0;`+
                                   `border-radius:4px;background:${badgeColor};color:${textColor};font-size:11px;\">P${i+1}: ${label}</span>`);
                    }

                    const mapState = (arr.every(v => (v|0) <= 0)) ? '🟢' : (arr.some(v => (v|0) <= 0) ? '🟡' : '🔴');
                    const rowLockedCount = arr.filter(v => (v|0) > 0).length;
                    const rowUnlockedCount = arr.length - rowLockedCount;

                    if (wantLocked && rowLockedCount === 0) continue;
                    if (wantUnlocked && rowUnlockedCount === 0) continue;

                    const isCurrent = (m === curMap);
                    mapRows.push(`
                        <div style=\"padding:6px 8px;margin:4px 0;background:rgba(255,255,255,0.03);`+
                                     `border-left:3px solid ${isCurrent ? '#ffd700' : '#555'};\">`+
                            `<div style=\"display:flex;align-items:center;gap:8px;flex-wrap:wrap;\">`+
                                `<span>${mapState}</span>`+
                                `<strong>Map ${m}</strong>`+
                                `${isCurrent ? '<span style=\\"color:#ffd700;\\">(current)</span>' : ''}`+
                            `</div>`+
                            `<div style=\"margin-top:4px;\">${parts.join(' ')}</div>`+
                        `</div>`
                    );
                }

                if (mapRows.length === 0) continue;

                grandTotalPortals += totalPortals;
                grandUnlocked += unlockedPortals;
                grandMapsWithPortals += mapsWithPortals;

                const pct = totalPortals > 0 ? Math.round(unlockedPortals / totalPortals * 100) : 0;

                html += `
                <div style="margin:12px 0 16px 0;padding:10px;border:1px solid #333;border-radius:8px;`+
                         `background:linear-gradient(135deg,#1e1e1e,#262626);">
                    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                        <div style="font-weight:bold;color:#9ad;">🌍 World ${w + 1}</div>
                        <div style="color:#ccc;">Maps with portals: ${mapsWithPortals} · Portals unlocked: ${unlockedPortals}/${totalPortals} (${pct}%)</div>
                    </div>
                    <div style="margin-top:8px;">${mapRows.join('')}</div>
                </div>`;
            }

            if (!html) {
                return `<div>No results${filter ? ` for \"${filter}\"` : ''}.</div>`;
            }

            const grandPct = grandTotalPortals > 0 ? Math.round(grandUnlocked / grandTotalPortals * 100) : 0;
            html = html + `
                <div style="margin-top:12px;padding:10px;background:rgba(0,0,0,0.2);border-radius:6px;">
                    <div style="font-weight:bold;margin-bottom:4px;">📊 Summary</div>
                    <div>Total Worlds: ${totalWorlds}</div>
                    <div>Worlds shown: ${filterWorld !== null ? 1 : totalWorlds}</div>
                    <div>Maps with portals (shown): ${grandMapsWithPortals}</div>
                    <div>Unlocked portals (shown): ${grandUnlocked}/${grandTotalPortals} (${grandPct}%)</div>
                </div>`;

            return html;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

plugin_class = PortalUnlocksPlugin
