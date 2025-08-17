from plugin_system import PluginBase, js_export, ui_banner, ui_toggle, ui_button, ui_search_with_results, ui_autocomplete_input, plugin_command, console
from config_manager import config_manager

class QuestManagerPlugin(PluginBase):
    VERSION = "1.0.0"
    DESCRIPTION = "Comprehensive quest management system to view, unlock, and manage all quests. Provides status overview, individual quest unlocking with autocomplete, and quest reset functionality. ⚠️ MODERATE RISK: Use with caution as quest manipulation can affect game progression."
    PLUGIN_ORDER = 6
    CATEGORY = "Character"

    def __init__(self, config=None):
        super().__init__(config or {})        
        self.debug = config.get('debug', False) if config else False
        self.name = 'quest_manager'
        self._quest_cache = None
        self._cache_timestamp = 0
        self._cache_duration = 300

    async def cleanup(self): pass
    async def update(self): pass
    async def on_config_changed(self, config): 
        self.debug = config.get('debug', False)
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)
    async def on_game_ready(self): pass

    async def get_cached_quest_list(self):
        import time
        if (not hasattr(self, '_quest_cache') or 
            not hasattr(self, '_cache_timestamp') or 
            not hasattr(self, '_cache_duration') or
            time.time() - self._cache_timestamp > self._cache_duration):
            
            if self.debug:
                console.print("[quest_manager] Cache expired or missing, fetching quest list...")
            try:
                if not hasattr(self, 'injector') or not self.injector:
                    if self.debug:
                        console.print("[quest_manager] No injector available")
                    return []
                
                raw_result = self.run_js_export('get_quest_names_js', self.injector)
                if self.debug:
                    console.print(f"[quest_manager] Raw JS result: {raw_result}")
                
                if not raw_result or raw_result.startswith("Error:"):
                    if self.debug:
                        console.print(f"[quest_manager] No valid result from JS: {raw_result}")
                    return []
                
                quest_items = []
                lines = raw_result.strip().split('\n')
                if self.debug:
                    console.print(f"[quest_manager] Processing {len(lines)} lines")
                
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('Error:') and not line.startswith('['):
                        quest_items.append(line)
                
                self._quest_cache = quest_items
                self._cache_timestamp = time.time()
                self._cache_duration = 300
                if self.debug:
                    console.print(f"[quest_manager] Cached {len(quest_items)} quests")
                return quest_items
            except Exception as e:
                if self.debug:
                    console.print(f"[quest_manager] Error fetching quest list: {e}")
                return []
        else:
            if self.debug:
                console.print(f"[quest_manager] Using cached quest list ({len(self._quest_cache)} items)")
            return self._quest_cache

    async def get_unlock_quest_ui_autocomplete(self, query: str = ""):
        if self.debug:
            console.print(f"[quest_manager] get_unlock_quest_ui_autocomplete called with query: '{query}'")
        try:
            if not hasattr(self, 'injector') or not self.injector:
                if self.debug:
                    console.print("[quest_manager] No injector available for autocomplete")
                return []
            
            quest_items = await self.get_cached_quest_list()
            if self.debug:
                console.print(f"[quest_manager] Got {len(quest_items)} quest items from cache")
            
            if not quest_items:
                if self.debug:
                    console.print("[quest_manager] No quest items found")
                return []
            
            query_lower = query.lower()
            suggestions = []
            
            for item in quest_items:
                if query_lower in item.lower():
                    suggestions.append(item)
                    if self.debug:
                        console.print(f"[quest_manager] Added suggestion: {item}")
            
            if self.debug:
                console.print(f"[quest_manager] Returning {len(suggestions)} suggestions: {suggestions}")
            return suggestions[:20]
        except Exception as e:
            if self.debug:
                console.print(f"[quest_manager] Error in get_unlock_quest_ui_autocomplete: {e}")
            return []

    @ui_banner(
        label="⚠️ Quest Manager",
        description="Comprehensive quest management system. Use with caution as quest manipulation can affect game progression.",
        banner_type="warning",
        category="Quest Actions",
        order=-1
    )
    async def warning_banner(self):
        return "Quest Manager active"

    @ui_search_with_results(
        label="Quest Status Overview",
        description="Show all quests with their current status, completion state, and requirements",
        button_text="Show Quest Status",
        placeholder="Enter filter term (leave empty to show all)",
        category="Quest Overview",
        order=1
    )
    async def quest_status_overview_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[quest_manager] Getting quest status overview, filter: {value}")
                result = self.run_js_export('get_quest_status_overview_js', self.injector, filter_query=value or "")
                return result
            except Exception as e:
                if self.debug:
                    console.print(f"[quest_manager] Error getting quest status overview: {e}")
                return f"ERROR: Error getting quest status overview: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_search_with_results(
        label="Quest Helper Status",
        description="Show quests currently in the quest helper menu",
        button_text="Show Quest Helper",
        placeholder="Enter filter term (leave empty to show all)",
        category="Quest Overview",
        order=2
    )
    async def quest_helper_status_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[quest_manager] Getting quest helper status, filter: {value}")
                result = self.run_js_export('get_quest_helper_status_js', self.injector, filter_query=value or "")
                return result
            except Exception as e:
                if self.debug:
                    console.print(f"[quest_manager] Error getting quest helper status: {e}")
                return f"ERROR: Error getting quest helper status: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_autocomplete_input(
        label="Unlock Quest by Name",
        description="Unlock a specific quest by name (with autocomplete). Makes the quest available/active.",
        button_text="Unlock Quest",
        placeholder="Start typing quest name...",
        category="Quest Actions",
        order=3
    )
    async def unlock_quest_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[quest_manager] Unlocking quest, input: {value}")
                if not value or not value.strip():
                    return "Please provide a quest name"
                quest_name = value.strip()
                if self.debug:
                    console.print(f"[quest_manager] Parsed quest name: '{quest_name}'")
                result = await self.unlock_quest(quest_name)
                if self.debug:
                    console.print(f"[quest_manager] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[quest_manager] Error unlocking quest: {e}")
                return f"ERROR: Error unlocking quest: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_autocomplete_input(
        label="Complete Quest by Name",
        description="Complete a specific quest by name (with autocomplete). Sets quest to completed state.",
        button_text="Complete Quest",
        placeholder="Start typing quest name...",
        category="Quest Actions",
        order=4
    )
    async def complete_quest_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[quest_manager] Completing quest, input: {value}")
                if not value or not value.strip():
                    return "Please provide a quest name"
                quest_name = value.strip()
                if self.debug:
                    console.print(f"[quest_manager] Parsed quest name: '{quest_name}'")
                result = await self.complete_quest(quest_name)
                if self.debug:
                    console.print(f"[quest_manager] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[quest_manager] Error completing quest: {e}")
                return f"ERROR: Error completing quest: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_autocomplete_input(
        label="Complete Quest Requirements Only",
        description="Complete all requirements for a specific quest (with autocomplete) without marking quest as completed.",
        button_text="Complete Requirements",
        placeholder="Start typing quest name...",
        category="Quest Actions",
        order=4.5
    )
    async def complete_quest_requirements_only_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[quest_manager] Completing quest requirements only, input: {value}")
                if not value or not value.strip():
                    return "Please provide a quest name"
                quest_name = value.strip()
                if self.debug:
                    console.print(f"[quest_manager] Parsed quest name: '{quest_name}'")
                result = await self.complete_quest_requirements_only(quest_name)
                if self.debug:
                    console.print(f"[quest_manager] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[quest_manager] Error completing quest requirements: {e}")
                return f"ERROR: Error completing quest requirements: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_autocomplete_input(
        label="Set Quest to Ongoing",
        description="Set a specific quest to ongoing/active status (with autocomplete). Makes the quest active without completing it.",
        button_text="Set Ongoing",
        placeholder="Start typing quest name...",
        category="Quest Actions",
        order=4.7
    )
    async def set_quest_ongoing_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[quest_manager] Setting quest to ongoing, input: {value}")
                if not value or not value.strip():
                    return "Please provide a quest name"
                quest_name = value.strip()
                if self.debug:
                    console.print(f"[quest_manager] Parsed quest name: '{quest_name}'")
                result = await self.set_quest_ongoing(quest_name)
                if self.debug:
                    console.print(f"[quest_manager] Result: {result}")
                return f"SUCCESS: {result}"
            except Exception as e:
                if self.debug:
                    console.print(f"[quest_manager] Error setting quest to ongoing: {e}")
                return f"ERROR: Error setting quest to ongoing: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_button(
        label="🔓 Unlock All Quests",
        description="Unlock all quests in the game (makes them available/active)",
        category="Quest Actions",
        order=5
    )
    async def unlock_all_quests_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.unlock_all_quests()
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: Error unlocking all quests: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_button(
        label="🔄 Reset All Quests",
        description="Reset all quests to their initial state (removes completion and progress)",
        category="Quest Actions",
        order=6
    )
    async def reset_all_quests_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.reset_all_quests()
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: Error resetting all quests: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_button(
        label="🎯 Reset Quest Requirements",
        description="Reset all quest requirements/progress to zero (keeps quest completion status)",
        category="Quest Actions",
        order=7
    )
    async def reset_quest_requirements_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.reset_quest_requirements()
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: Error resetting quest requirements: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_button(
        label="✅ Complete All Quest Requirements",
        description="Set all quest requirements to completed for all completed quests (fixes quest progress)",
        category="Quest Actions",
        order=8
    )
    async def complete_all_quest_requirements_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.complete_all_quest_requirements()
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: Error completing quest requirements: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_button(
        label="🎯 Complete ALL Quests & Requirements",
        description="Complete all quests in the game AND set all their requirements to completed (ultimate completion)",
        category="Quest Actions",
        order=9
    )
    async def complete_all_quests_and_requirements_ui(self):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.complete_all_quests_and_requirements()
                return f"SUCCESS: {result}"
            except Exception as e:
                return f"ERROR: Error completing all quests and requirements: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @plugin_command(
        help="Get quest status overview.",
        params=[],
    )
    async def get_quest_status_overview(self, injector=None, **kwargs):
        result = self.run_js_export('get_quest_status_overview_js', injector)
        return result

    @plugin_command(
        help="Get quest helper menu status.",
        params=[],
    )
    async def get_quest_helper_status(self, injector=None, **kwargs):
        result = self.run_js_export('get_quest_helper_status_js', injector)
        return result

    @plugin_command(
        help="Unlock a specific quest by name.",
        params=[
            {"name": "quest_name", "type": str, "help": "Name of the quest to unlock"},
        ],
    )
    async def unlock_quest(self, quest_name: str, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('unlock_quest_js', self.injector, quest_name=quest_name)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @plugin_command(
        help="Complete a specific quest by name.",
        params=[
            {"name": "quest_name", "type": str, "help": "Name of the quest to complete"},
        ],
    )
    async def complete_quest(self, quest_name: str, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('complete_quest_js', self.injector, quest_name=quest_name)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @plugin_command(
        help="Complete all requirements for a specific quest without marking quest as completed.",
        params=[
            {"name": "quest_name", "type": str, "help": "Name of the quest to complete requirements for"},
        ],
    )
    async def complete_quest_requirements_only(self, quest_name: str, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('complete_quest_requirements_only_js', self.injector, quest_name=quest_name)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @plugin_command(
        help="Set a specific quest to ongoing/active status.",
        params=[
            {"name": "quest_name", "type": str, "help": "Name of the quest to set to ongoing"},
        ],
    )
    async def set_quest_ongoing(self, quest_name: str, **kwargs):
        if hasattr(self, 'injector') and self.injector:
            result = self.run_js_export('set_quest_ongoing_js', self.injector, quest_name=quest_name)
            return result
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @plugin_command(
        help="Unlock all quests in the game.",
        params=[],
    )
    async def unlock_all_quests(self, injector=None, **kwargs):
        result = self.run_js_export('unlock_all_quests_js', injector)
        return result

    @plugin_command(
        help="Reset all quests to their initial state.",
        params=[],
    )
    async def reset_all_quests(self, injector=None, **kwargs):
        result = self.run_js_export('reset_all_quests_js', injector)
        return result

    @plugin_command(
        help="Reset all quest requirements/progress.",
        params=[],
    )
    async def reset_quest_requirements(self, injector=None, **kwargs):
        result = self.run_js_export('reset_quest_requirements_js', injector)
        return result

    @plugin_command(
        help="Complete all quest requirements for all completed quests.",
        params=[],
    )
    async def complete_all_quest_requirements(self, injector=None, **kwargs):
        result = self.run_js_export('complete_all_quest_requirements_js', injector)
        return result

    @plugin_command(
        help="Complete all quests in the game AND set all their requirements to completed.",
        params=[],
    )
    async def complete_all_quests_and_requirements(self, injector=None, **kwargs):
        result = self.run_js_export('complete_all_quests_and_requirements_js', injector)
        return result

    # JavaScript export functions
    @js_export()
    def get_quest_names_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            
            const questComplete = bEngine.getGameAttribute("QuestComplete");
            if (!questComplete || !questComplete.h) {
                return "Error: Quest data not found";
            }
            
            const questNames = Object.keys(questComplete.h);
            return questNames.join('\\n');
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export(params=["filter_query"])
    def get_quest_status_overview_js(self, filter_query=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            
            const questComplete = bEngine.getGameAttribute("QuestComplete");
            const questStatus = bEngine.getGameAttribute("QuestStatus");
            
            if (!questComplete || !questComplete.h) {
                return "Error: Quest completion data not found";
            }
            
            let output = "";
            output += "<div style='font-weight: bold; font-size: 16px; margin-bottom: 10px;'>QUEST STATUS OVERVIEW</div>";
            
            const questNames = Object.keys(questComplete.h);
            const filterQuery = filter_query ? filter_query.toLowerCase() : "";
            
            let totalQuests = 0;
            let activeQuests = 0;
            let completedQuests = 0;
            let lockedQuests = 0;
            
            const activeQuestsList = [];
            const completedQuestsList = [];
            const lockedQuestsList = [];
            
            // Categorize all quests
            for (const questName of questNames) {
                if (filterQuery && !questName.toLowerCase().includes(filterQuery)) continue;
                
                totalQuests++;
                const completionStatus = questComplete.h[questName];
                const questProgress = questStatus && questStatus.h && questStatus.h[questName] ? questStatus.h[questName] : null;
                
                if (completionStatus === 1) {
                    completedQuests++;
                    completedQuestsList.push({name: questName, progress: questProgress});
                } else if (completionStatus === 0) {
                    activeQuests++;
                    activeQuestsList.push({name: questName, progress: questProgress});
                } else if (completionStatus === -1) {
                    lockedQuests++;
                    lockedQuestsList.push({name: questName, progress: questProgress});
                }
            }
            
            output += "<div style='margin: 10px 0; padding: 10px; background: rgba(0, 0, 0, 0.1); border-radius: 5px;'>";
            output += "<div style='font-weight: bold; margin-bottom: 5px;'>SUMMARY</div>";
            output += "<div>Total Quests: " + totalQuests + "</div>";
            output += "<div>Active: " + activeQuests + " | Completed: " + completedQuests + " | Locked: " + lockedQuests + "</div>";
            if (totalQuests > 0) {
                output += "<div>Completion Rate: " + Math.round(completedQuests/totalQuests*100) + "%</div>";
            }
            output += "</div>";
            
            if (activeQuests > 0) {
                output += "<div style='margin: 10px 0; padding: 10px; background: rgba(255, 217, 61, 0.05); border-radius: 5px;'>";
                output += "<div style='font-weight: bold; margin-bottom: 5px; color: #ffd93d;'>🔄 ACTIVE QUESTS (" + activeQuests + ")</div>";
                for (const quest of activeQuestsList) {
                    output += "<div style='margin: 2px 0; padding: 3px 8px; background: rgba(255, 217, 61, 0.1); border-left: 3px solid #ffd93d;'>";
                    output += quest.name;
                    if (quest.progress && Array.isArray(quest.progress) && quest.progress.length > 0) {
                        output += " | Progress: [" + quest.progress.join(', ') + "]";
                    }
                    output += "</div>";
                }
                output += "</div>";
            }
            
            if (completedQuests > 0) {
                output += "<div style='margin: 10px 0; padding: 10px; background: rgba(107, 207, 127, 0.05); border-radius: 5px;'>";
                output += "<div style='font-weight: bold; margin-bottom: 5px; color: #6bcf7f;'>✅ COMPLETED QUESTS (" + completedQuests + ")</div>";
                for (const quest of completedQuestsList) {
                    output += "<div style='margin: 2px 0; padding: 3px 8px; background: rgba(107, 207, 127, 0.1); border-left: 3px solid #6bcf7f;'>";
                    output += quest.name;
                    if (quest.progress && Array.isArray(quest.progress) && quest.progress.length > 0) {
                        output += " | Requirements: [" + quest.progress.join(', ') + "]";
                    }
                    output += "</div>";
                }
                output += "</div>";
            }
            
            if (lockedQuests > 0) {
                output += "<div style='margin: 10px 0; padding: 10px; background: rgba(255, 107, 107, 0.05); border-radius: 5px;'>";
                output += "<div style='font-weight: bold; margin-bottom: 5px; color: #ff6b6b;'>🔒 LOCKED QUESTS (" + lockedQuests + ")</div>";
                for (const quest of lockedQuestsList) {
                    output += "<div style='margin: 2px 0; padding: 3px 8px; background: rgba(255, 107, 107, 0.1); border-left: 3px solid #ff6b6b;'>";
                    output += quest.name;
                    if (quest.progress && Array.isArray(quest.progress) && quest.progress.length > 0) {
                        output += " | Requirements: [" + quest.progress.join(', ') + "]";
                    }
                    output += "</div>";
                }
                output += "</div>";
            }
            
            return output;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export(params=["filter_query"])
    def get_quest_helper_status_js(self, filter_query=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            
            const questHelperMenu = bEngine.getGameAttribute("QuestHelperMenu");
            
            let output = "";
            output += "<div style='font-weight: bold; font-size: 16px; margin-bottom: 10px;'>QUEST HELPER STATUS</div>";
            
            if (!questHelperMenu || !Array.isArray(questHelperMenu)) {
                output += "<div style='margin: 10px 0; padding: 10px; background: rgba(255, 107, 107, 0.1); border-radius: 5px;'>";
                output += "<div>No Quest Helper data found or Quest Helper is empty</div>";
                output += "</div>";
                return output;
            }
            
            const filterQuery = filter_query ? filter_query.toLowerCase() : "";
            
            output += "<div style='margin: 10px 0; padding: 10px; background: rgba(0, 0, 0, 0.1); border-radius: 5px;'>";
            output += "<div style='font-weight: bold; margin-bottom: 5px;'>ACTIVE QUEST HELPER ENTRIES (" + questHelperMenu.length + ")</div>";
            
            if (questHelperMenu.length === 0) {
                output += "<div>Quest Helper is empty - no quests currently tracked</div>";
            } else {
                for (let i = 0; i < questHelperMenu.length; i++) {
                    const helperEntry = questHelperMenu[i];
                    if (!helperEntry || !Array.isArray(helperEntry)) continue;
                    
                    const questName = helperEntry[0] || "Unknown Quest";
                    if (filterQuery && !questName.toLowerCase().includes(filterQuery)) continue;
                    
                    output += "<div style='margin: 2px 0; padding: 3px 8px; background: rgba(255, 217, 61, 0.1); border-left: 3px solid #ffd93d;'>";
                    output += `Quest Helper ${i + 1}: ${questName}`;
                    
                    if (helperEntry.length > 1) {
                        output += " | Items: [";
                        for (let j = 1; j < helperEntry.length; j++) {
                            if (j > 1) output += ", ";
                            output += helperEntry[j];
                        }
                        output += "]";
                    }
                    output += "</div>";
                }
            }
            output += "</div>";
            
            return output;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export(params=["quest_name"])
    def unlock_quest_js(self, quest_name=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            
            const questComplete = bEngine.getGameAttribute("QuestComplete");
            const questStatus = bEngine.getGameAttribute("QuestStatus");
            
            if (!questComplete || !questComplete.h) {
                return "Error: Quest completion data not found";
            }
            
            if (!quest_name || quest_name.trim() === "") {
                return "Error: Quest name is required";
            }
            
            const questName = quest_name.trim();
            
            if (!(questName in questComplete.h)) {
                return `Error: Quest '${questName}' not found. Available quests: ${Object.keys(questComplete.h).slice(0, 10).join(', ')}...`;
            }
            
            const currentStatus = questComplete.h[questName];
            
            questComplete.h[questName] = 0;
            
            if (questStatus && questStatus.h && !(questName in questStatus.h)) {
                questStatus.h[questName] = [0]; // Initialize with basic progress array
            }
            
            let statusText = "unknown";
            if (currentStatus === 1) statusText = "completed";
            else if (currentStatus === 0) statusText = "already active";
            else if (currentStatus === -1) statusText = "locked";
            
            return `✅ Unlocked quest '${questName}' (was ${statusText})`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export(params=["quest_name"])
    def complete_quest_js(self, quest_name=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            
            const questComplete = bEngine.getGameAttribute("QuestComplete");
            
            if (!questComplete || !questComplete.h) {
                return "Error: Quest completion data not found";
            }
            
            if (!quest_name || quest_name.trim() === "") {
                return "Error: Quest name is required";
            }
            
            const questName = quest_name.trim();
            
            if (!(questName in questComplete.h)) {
                return `Error: Quest '${questName}' not found. Available quests: ${Object.keys(questComplete.h).slice(0, 10).join(', ')}...`;
            }
            
            const currentStatus = questComplete.h[questName];
            
            questComplete.h[questName] = 1;
            
            let statusText = "unknown";
            if (currentStatus === 1) statusText = "already completed";
            else if (currentStatus === 0) statusText = "active";
            else if (currentStatus === -1) statusText = "locked";
            
            return `🎯 Completed quest '${questName}' (was ${statusText})`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export(params=["quest_name"])
    def complete_quest_requirements_only_js(self, quest_name=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;

            if (!quest_name || !quest_name.trim()) return "Error: Quest name is required";
            const questName = quest_name.trim();

            const questHelperMenu = bEngine.getGameAttribute("QuestHelperMenu");
            if (!Array.isArray(questHelperMenu)) return "Error: QuestHelperMenu not found";

            const helperEntry = questHelperMenu.find(e => Array.isArray(e) && e[0] === questName);
            if (!helperEntry) return `Error: Quest '${questName}' is not active in QuestHelperMenu`;

            const triples = [];
            for (let i = 1; i + 2 < helperEntry.length; i += 3) {
                const id = helperEntry[i];
                const cur = Number(helperEntry[i + 1]) || 0;
                const tgt = Number(helperEntry[i + 2]) || 0;
                triples.push({ id, cur, tgt });
            }
            const reqCount = triples.length;
            if (reqCount === 0) return `Error: No requirements parsed for '${questName}'`;

            const candidateKeys = Object.keys(bEngine._gameAttributes || {}).filter(k => /quest/i.test(k));
            const updated = [];
            let bestHit = null;

            for (const key of candidateKeys) {
                const v = bEngine.getGameAttribute(key);
                if (!v || !v.h || !(questName in v.h)) continue;
                const entry = v.h[questName];
                if (!Array.isArray(entry)) continue;

                if (entry.length === reqCount || entry.length >= reqCount) {
                    for (let i = 0; i < reqCount; i++) {
                        entry[i] = Number.isFinite(entry[i]) ? Math.max(entry[i], triples[i].tgt) : triples[i].tgt;
                    }
                    updated.push(key);
                    if (entry.length === reqCount && !bestHit) bestHit = key;
                }
            }

            if (updated.length === 0) {
                const questStatus = bEngine.getGameAttribute("QuestStatus");
                if (questStatus && questStatus.h) {
                    questStatus.h[questName] = triples.map(t => t.tgt);
                    bestHit = "QuestStatus";
                } else {
                    return "Error: No quest progress container matched and QuestStatus missing";
                }
            }

            const questComplete = bEngine.getGameAttribute("QuestComplete");
            if (questComplete?.h && (questName in questComplete.h) && questComplete.h[questName] !== 1) {
                questComplete.h[questName] = 0;
            }

            return `✅ Set ${reqCount} requirements to target for '${questName}' in ${bestHit || updated[0]}${updated.length > 1 ? " (+ " + (updated.length - 1) + " mirrors)" : ""}`;
        } catch (e) {
            return "Error: " + e.message;
        }
        '''

    @js_export(params=["quest_name"])
    def set_quest_ongoing_js(self, quest_name=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            
            const questComplete = bEngine.getGameAttribute("QuestComplete");
            const questStatus = bEngine.getGameAttribute("QuestStatus");
            
            if (!questComplete || !questComplete.h) {
                return "Error: Quest completion data not found";
            }
            
            if (!quest_name || quest_name.trim() === "") {
                return "Error: Quest name is required";
            }
            
            const questName = quest_name.trim();
            
            if (!(questName in questComplete.h)) {
                return `Error: Quest '${questName}' not found. Available quests: ${Object.keys(questComplete.h).slice(0, 10).join(', ')}...`;
            }
            
            const currentStatus = questComplete.h[questName];
            let previousStatusText = "unknown";
            if (currentStatus === 1) previousStatusText = "completed";
            else if (currentStatus === 0) previousStatusText = "already ongoing";
            else if (currentStatus === -1) previousStatusText = "locked";
            
            // Set quest to ongoing (status 0)
            questComplete.h[questName] = 0;
            
            // Initialize quest status/progress if it doesn't exist
            if (questStatus && questStatus.h && !(questName in questStatus.h)) {
                questStatus.h[questName] = [0]; // Initialize with basic progress array
            }
            
            if (currentStatus === 0) {
                return `🔄 Quest '${questName}' is already ongoing/active!`;
            } else {
                return `🔄 Set quest '${questName}' to ongoing/active status (was ${previousStatusText})`;
            }
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def unlock_all_quests_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            
            const questComplete = bEngine.getGameAttribute("QuestComplete");
            const questStatus = bEngine.getGameAttribute("QuestStatus");
            
            if (!questComplete || !questComplete.h) {
                return "Error: Quest completion data not found";
            }
            
            const questNames = Object.keys(questComplete.h);
            let unlockedCount = 0;
            let alreadyActiveCount = 0;
            
            for (const questName of questNames) {
                const currentStatus = questComplete.h[questName];
                
                if (currentStatus !== 0) {
                    questComplete.h[questName] = 0;
                    unlockedCount++;
                    
                    if (questStatus && questStatus.h && !(questName in questStatus.h)) {
                        questStatus.h[questName] = [0];
                    }
                } else {
                    alreadyActiveCount++;
                }
            }
            
            if (unlockedCount === 0) {
                return `✅ All ${questNames.length} quests are already unlocked!`;
            } else {
                return `🔓 Unlocked ${unlockedCount} quests! (${alreadyActiveCount} were already active, total: ${questNames.length})`;
            }
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def reset_all_quests_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            
            const questComplete = bEngine.getGameAttribute("QuestComplete");
            const questStatus = bEngine.getGameAttribute("QuestStatus");
            
            if (!questComplete || !questComplete.h) {
                return "Error: Quest completion data not found";
            }
            
            const questNames = Object.keys(questComplete.h);
            let resetCount = 0;
            
            for (const questName of questNames) {
                questComplete.h[questName] = -1;
                resetCount++;
                
                if (questStatus && questStatus.h && questName in questStatus.h) {
                    if (Array.isArray(questStatus.h[questName])) {
                        for (let i = 0; i < questStatus.h[questName].length; i++) {
                            questStatus.h[questName][i] = 0;
                        }
                    }
                }
            }
            
            return `🔄 Reset ${resetCount} quests to locked state and cleared all progress!`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def reset_quest_requirements_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            
            const questStatus = bEngine.getGameAttribute("QuestStatus");
            
            if (!questStatus || !questStatus.h) {
                return "Error: Quest status data not found";
            }
            
            const questNames = Object.keys(questStatus.h);
            let resetCount = 0;
            
            for (const questName of questNames) {
                const questProgress = questStatus.h[questName];
                
                if (Array.isArray(questProgress)) {
                    let hasProgress = false;
                    for (let i = 0; i < questProgress.length; i++) {
                        if (questProgress[i] !== 0) {
                            questProgress[i] = 0;
                            hasProgress = true;
                        }
                    }
                    if (hasProgress) resetCount++;
                }
            }
            
            return `🎯 Reset progress/requirements for ${resetCount} quests (kept completion status)!`;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def complete_all_quest_requirements_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            
            const questComplete = bEngine.getGameAttribute("QuestComplete");
            const questStatus = bEngine.getGameAttribute("QuestStatus");
            
            if (!questComplete || !questComplete.h) {
                return "Error: Quest completion data not found";
            }
            
            if (!questStatus || !questStatus.h) {
                return "Error: Quest status data not found";
            }
            
            const questNames = Object.keys(questComplete.h);
            let completedCount = 0;
            let processedQuests = 0;
            
            for (const questName of questNames) {
                const completionStatus = questComplete.h[questName];
                
                if (completionStatus === 1) {
                    processedQuests++;
                    
                    // Initialize quest status if it doesn't exist
                    if (!(questName in questStatus.h)) {
                        questStatus.h[questName] = [9999];
                        completedCount++;
                    } else {
                        const questProgress = questStatus.h[questName];
                        
                        if (Array.isArray(questProgress)) {
                            let wasIncomplete = false;
                            for (let i = 0; i < questProgress.length; i++) {
                                // Set all requirements to a high value (9999) to indicate completion
                                if (questProgress[i] < 9999) {
                                    questProgress[i] = 9999;
                                    wasIncomplete = true;
                                }
                            }
                            if (wasIncomplete) completedCount++;
                        }
                    }
                }
            }
            
            if (completedCount === 0) {
                return `✅ All requirements for ${processedQuests} completed quests are already fulfilled!`;
            } else {
                return `✅ Set requirements to completed for ${completedCount} out of ${processedQuests} completed quests!`;
            }
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

    @js_export()
    def complete_all_quests_and_requirements_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            const bEngine = ctx["com.stencyl.Engine"].engine;
            
            const questComplete = bEngine.getGameAttribute("QuestComplete");
            const questStatus = bEngine.getGameAttribute("QuestStatus");
            
            if (!questComplete || !questComplete.h) {
                return "Error: Quest completion data not found";
            }
            
            if (!questStatus || !questStatus.h) {
                return "Error: Quest status data not found";
            }
            
            const questNames = Object.keys(questComplete.h);
            let completedCount = 0;
            let requirementsSetCount = 0;
            let alreadyCompletedCount = 0;
            
            for (const questName of questNames) {
                const currentCompletionStatus = questComplete.h[questName];
                
                if (currentCompletionStatus !== 1) {
                    questComplete.h[questName] = 1;
                    completedCount++;
                } else {
                    alreadyCompletedCount++;
                }
                
                if (!(questName in questStatus.h)) {
                    questStatus.h[questName] = [9999]; // Initialize with high completion value
                    requirementsSetCount++;
                } else {
                    const questProgress = questStatus.h[questName];
                    
                    if (Array.isArray(questProgress)) {
                        let wasIncomplete = false;
                        for (let i = 0; i < questProgress.length; i++) {
                            // Set all requirements to a high value (9999) to indicate completion
                            if (questProgress[i] < 9999) {
                                questProgress[i] = 9999;
                                wasIncomplete = true;
                            }
                        }
                        if (wasIncomplete) requirementsSetCount++;
                    }
                }
            }
            
            let message = "🎯 COMPLETE QUEST OVERHAUL:\\n";
            message += `📋 Total quests processed: ${questNames.length}\\n`;
            message += `✅ Newly completed quests: ${completedCount}\\n`;
            message += `⚡ Already completed quests: ${alreadyCompletedCount}\\n`;
            message += `🔧 Quest requirements fixed: ${requirementsSetCount}\\n`;
            message += `🏆 ALL QUESTS ARE NOW COMPLETED WITH FULFILLED REQUIREMENTS!`;
            
            return message;
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

plugin_class = QuestManagerPlugin
