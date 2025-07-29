from plugin_system import PluginBase, js_export, ui_search_with_results, ui_toggle, plugin_command
from config_manager import config_manager

class QuestHelperPlugin(PluginBase):
    VERSION = "1.0.0"
    DESCRIPTION = "Lists all ongoing quests and allows instant completion by clicking quest names."
    PLUGIN_ORDER = 5
    CATEGORY = "Character"

    def __init__(self, config=None):
        super().__init__(config or {})
        self.name = 'quest_helper'
        self.debug = config.get('debug', False) if config else False

    async def cleanup(self): pass
    async def update(self): pass
    async def on_config_changed(self, config): 
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)
        self.debug = config.get('debug', False) if config else False
    async def on_game_ready(self): pass

    @ui_search_with_results(
        label="Quest Helper",
        description="List all ongoing quests and complete them instantly",
        button_text="Refresh Quest List",
        placeholder="Search quests (leave empty to show all)",
        category="Gameplay Enhancements",
        order=0
    )
    async def quest_helper_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                result = await self.get_quest_list(self.injector)
                if value and value.strip():
                    # Filter results based on input
                    lines = result.split('\n')
                    filtered_lines = []
                    query_lower = value.lower()
                    for line in lines:
                        if query_lower in line.lower():
                            filtered_lines.append(line)
                    return '\n'.join(filtered_lines) if filtered_lines else f"No quests found matching: {value}"
                else:
                    return result
            except Exception as e:
                return f"ERROR: Error getting quest list: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_toggle(
        label="Auto-Complete All Quests",
        description="Instantly complete all ongoing quests",
        config_key="auto_complete_all",
        default_value=False
    )
    async def auto_complete_all_ui(self, value: bool = None):
        if value is not None:
            self.config["auto_complete_all"] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector and value:
                try:
                    result = await self.auto_complete_all_quests(self.injector)
                    return f"SUCCESS: {result}"
                except Exception as e:
                    return f"ERROR: Error auto-completing quests: {str(e)}"
        return f"Auto-complete all quests {'enabled' if self.config.get('auto_complete_all', False) else 'disabled'}"

    @ui_toggle("Fix Character Quest Requirements", "Fixes all completed quests to have their requirements properly set as fulfilled")
    async def fix_character_ui(self, value: bool = None):
        if value:
            result = await self.fix_character_requirements()
            return f"Character fixed! {result}"
        return "Character fixer ready. Enable to fix quest requirements."

    @ui_toggle("Reset All Quests to Uncompleted", "Resets all quests to uncompleted status")
    async def reset_quests_ui(self, value: bool = None):
        if value:
            result = await self.reset_all_quests()
            return f"Quests reset! {result}"
        return "Quest resetter ready. Enable to reset all quests to uncompleted."

    @plugin_command(
        help="Get list of all ongoing quests with completion options.",
        params=[],
    )
    async def get_quest_list(self, injector=None, **kwargs):
        if self.debug:
            console.print("[quest_helper] Getting quest list...")
        result = self.run_js_export('get_quest_list_js', injector)
        if self.debug:
            console.print(f"[quest_helper] Result: {result}")
        return result

    @plugin_command(
        help="Complete a specific quest by name.",
        params=["quest_name"],
    )
    async def complete_quest(self, injector=None, quest_name=None, **kwargs):
        if self.debug:
            console.print(f"[quest_helper] Completing quest: {quest_name}")
        result = self.run_js_export('complete_quest_js', injector, quest_name)
        if self.debug:
            console.print(f"[quest_helper] Result: {result}")
        return result

    @plugin_command(
        help="Auto-complete all ongoing quests.",
        params=[],
    )
    async def auto_complete_all_quests(self, injector=None, **kwargs):
        if self.debug:
            console.print("[quest_helper] Auto-completing all quests...")
        result = self.run_js_export('auto_complete_all_quests_js', injector)
        if self.debug:
            console.print(f"[quest_helper] Result: {result}")
        return result

    @plugin_command("Fix character quest requirements")
    async def fix_character_requirements(self, injector=None, **kwargs):
        result = self.run_js_export('fix_character_requirements_js', injector)
        return result if result else "No result returned from character fix"

    @plugin_command("Reset all quests to uncompleted")
    async def reset_all_quests(self, injector=None, **kwargs):
        result = self.run_js_export('reset_all_quests_js', injector)
        return result if result else "No result returned from quest reset"

    @js_export()
    def fix_character_requirements_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const questComplete = bEngine.getGameAttribute("QuestComplete").h;
            const questStatus = bEngine.getGameAttribute("QuestStatus").h;
            const npcDialogue = bEngine.getGameAttribute("NPCdialogue").h;
            const dialogueDefGET = bEngine.getGameAttribute("DialogueDefGET").h;
            
            let fixed_count = 0;
            let total_quests = 0;
            let requirements_filled = 0;
            
            // Process ALL quests (not just completed ones)
            for (const [questKey, isCompleted] of Object.entries(questComplete)) {
                total_quests++;
                
                // Ensure questStatus entry exists for this quest
                if (!questStatus[questKey]) {
                    questStatus[questKey] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; // Create with 10 requirement slots
                    fixed_count++;
                }
                
                let quest_needs_fixing = false;
                
                // Set quest status to completed (2) regardless of current status
                if (questStatus[questKey][0] !== 2) {
                    questStatus[questKey][0] = 2; // Set to completed
                    quest_needs_fixing = true;
                }
                
                // Set ALL requirement slots to fulfilled (1) - maximum requirements
                for (let i = 1; i < questStatus[questKey].length; i++) {
                    if (questStatus[questKey][i] !== 1) {
                        questStatus[questKey][i] = 1; // Fulfill requirement
                        requirements_filled++;
                        quest_needs_fixing = true;
                    }
                }
                
                // Also set the quest as completed in QuestComplete
                if (questComplete[questKey] !== 1) {
                    questComplete[questKey] = 1; // Mark as completed
                    quest_needs_fixing = true;
                }
                
                if (quest_needs_fixing) {
                    fixed_count++;
                }
            }
            
            // Update NPC dialogue to maximum for all NPCs
            let npc_dialogue_updated = 0;
            try {
                for (const [npcName, dialogueState] of Object.entries(npcDialogue)) {
                    if (dialogueDefGET[npcName] && dialogueDefGET[npcName][1]) {
                        const maxDialogue = dialogueDefGET[npcName][1].length - 1;
                        if (dialogueState < maxDialogue) {
                            npcDialogue[npcName] = maxDialogue;
                            npc_dialogue_updated++;
                        }
                    }
                }
            } catch (e) {
                console.log("NPC dialogue update error:", e);
            }
            
            // Trigger UI refresh
            try {
                const pixelHelper = bEngine.getGameAttribute("PixelHelperActor");
                if (pixelHelper && pixelHelper[5]) {
                    pixelHelper[5].shout("_customEvent_QuestComplete");
                }
                if (pixelHelper && pixelHelper[1]) {
                    pixelHelper[1].shout("_customEvent_QuestComplete");
                }
                
                // Additional quest popup triggers
                try {
                    // Trigger quest helper menu update
                    if (pixelHelper && pixelHelper[23]) {
                        pixelHelper[23].shout("_customEvent_QuestHelperUpdate");
                    }
                    
                    // Trigger NPC dialogue refresh
                    if (pixelHelper && pixelHelper[38]) {
                        pixelHelper[38].shout("_customEvent_DialogueRefresh");
                    }
                    
                    // Force quest UI refresh
                    bEngine.gameAttributes.h.QuestHelperMenu = bEngine.gameAttributes.h.QuestHelperMenu || [];
                    
                } catch (e) {
                    console.log("Additional quest popup trigger error:", e);
                }
                
                // Force UI refresh
                bEngine.gameAttributes.h.DummyText = "CharacterFixed";
                
            } catch (e) {
                console.log("Character fix event error:", e);
            }
            
            if (fixed_count === 0) {
                return `✅ All quests already have maximum requirements set! Total quests: ${total_quests}`;
            } else {
                return `🔧 Character fixed! Updated ${fixed_count} quests with ${requirements_filled} requirement slots filled. Updated ${npc_dialogue_updated} NPC dialogues. Total quests: ${total_quests}`;
            }
            
        } catch (e) {
            return `Error fixing character: ${e.message}`;
        }
        '''

    @js_export()
    def reset_all_quests_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const questComplete = bEngine.getGameAttribute("QuestComplete").h;
            const questStatus = bEngine.getGameAttribute("QuestStatus").h;
            const npcDialogue = bEngine.getGameAttribute("NPCdialogue").h;
            
            let reset_count = 0;
            let total_quests = 0;
            
            // Reset ALL quests to uncompleted
            for (const [questKey, isCompleted] of Object.entries(questComplete)) {
                total_quests++;
                
                // Reset quest completion status
                if (questComplete[questKey] !== 0) {
                    questComplete[questKey] = 0; // Mark as uncompleted
                    reset_count++;
                }
                
                // Reset quest status and requirements
                if (questStatus[questKey]) {
                    // Set quest status to not met (0)
                    if (questStatus[questKey][0] !== 0) {
                        questStatus[questKey][0] = 0; // Set to not met
                        reset_count++;
                    }
                    
                    // Reset ALL requirement slots to unfulfilled (0)
                    for (let i = 1; i < questStatus[questKey].length; i++) {
                        if (questStatus[questKey][i] !== 0) {
                            questStatus[questKey][i] = 0; // Reset requirement
                            reset_count++;
                        }
                    }
                }
            }
            
            // Reset NPC dialogue to initial state
            try {
                for (const [npcName, dialogueState] of Object.entries(npcDialogue)) {
                    if (dialogueState > 0) {
                        npcDialogue[npcName] = 0; // Reset to initial dialogue
                        reset_count++;
                    }
                }
            } catch (e) {
                console.log("NPC dialogue reset error:", e);
            }
            
            // Trigger UI refresh
            try {
                const pixelHelper = bEngine.getGameAttribute("PixelHelperActor");
                if (pixelHelper && pixelHelper[5]) {
                    pixelHelper[5].shout("_customEvent_QuestComplete");
                }
                if (pixelHelper && pixelHelper[1]) {
                    pixelHelper[1].shout("_customEvent_QuestComplete");
                }
                
                // Force UI refresh
                bEngine.gameAttributes.h.DummyText = "QuestsReset";
                
            } catch (e) {
                console.log("Quest reset event error:", e);
            }
            
            if (reset_count === 0) {
                return `✅ All quests are already reset to uncompleted! Total quests: ${total_quests}`;
            } else {
                return `🔄 Quests reset! Reset ${reset_count} quest elements across ${total_quests} total quests to uncompleted status.`;
            }
            
        } catch (e) {
            return `Error resetting quests: ${e.message}`;
        }
        '''

    @js_export()
    def get_quest_list_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const questComplete = bEngine.getGameAttribute("QuestComplete").h;
            const questStatus = bEngine.getGameAttribute("QuestStatus").h;
            const questHelperMenu = bEngine.getGameAttribute("QuestHelperMenu");
            const dialogueDefGET = bEngine.getGameAttribute("DialogueDefGET").h;
            
            const results = [];
            results.push(`<div style="font-weight: bold; font-size: 16px; margin-bottom: 10px; color: inherit;">📋 ALL QUESTS</div>`);
            results.push(`<br>`);
            
            let ongoing_count = 0;
            let completed_count = 0;
            let locked_count = 0;
            let total_count = 0;
            
            // Count all quests first
            for (const [questKey, isCompleted] of Object.entries(questComplete)) {
                total_count++;
                if (isCompleted === 0) ongoing_count++;
                else if (isCompleted === 1) completed_count++;
                else locked_count++;
            }
            
            // ACTIVE QUESTS SECTION
            results.push(`<div style="font-weight: bold; color: #ffa500; margin: 10px 0;">🟡 ACTIVE QUESTS (${ongoing_count})</div>`);
            results.push(`<div style="margin-left: 10px;">`);
            
            if (ongoing_count === 0) {
                results.push(`<div style="color: #888; font-style: italic;">No active quests found</div>`);
            } else {
                for (const [questKey, isCompleted] of Object.entries(questComplete)) {
                    if (isCompleted === 0) {
                        const questName = questKey.replace(/_/g, ' ');
                        results.push(`<div style="margin: 5px 0; padding: 5px; border-left: 3px solid #ffa500;">`);
                        results.push(`🟡 <strong>${questName}</strong> | <a href="#" onclick="window.complete_quest('${questKey}'); return false;">[CLICK TO COMPLETE]</a>`);
                        results.push(`</div>`);
                    }
                }
            }
            results.push(`</div><br>`);
            
            // COMPLETED QUESTS SECTION
            results.push(`<div style="font-weight: bold; color: #28a745; margin: 10px 0;">✅ COMPLETED QUESTS (${completed_count})</div>`);
            results.push(`<div style="margin-left: 10px;">`);
            
            let completed_shown = 0;
            for (const [questKey, isCompleted] of Object.entries(questComplete)) {
                if (isCompleted === 1 && completed_shown < 15) {
                    const questName = questKey.replace(/_/g, ' ');
                    results.push(`<div style="margin: 3px 0; padding: 3px;">`);
                    results.push(`✅ ${questName} | <a href="#" onclick="window.complete_quest('${questKey}'); return false;">[CLICK TO COMPLETE]</a>`);
                    results.push(`</div>`);
                    completed_shown++;
                }
            }
            
            if (completed_count > 15) {
                results.push(`<div style="color: #888; font-style: italic;">... and ${completed_count - 15} more completed quests</div>`);
            }
            results.push(`</div><br>`);
            
            // LOCKED QUESTS SECTION
            results.push(`<div style="font-weight: bold; color: #6c757d; margin: 10px 0;">🔒 LOCKED QUESTS (${locked_count})</div>`);
            results.push(`<div style="margin-left: 10px;">`);
            
            let locked_shown = 0;
            for (const [questKey, isCompleted] of Object.entries(questComplete)) {
                if (isCompleted !== 0 && isCompleted !== 1 && locked_shown < 15) {
                    const questName = questKey.replace(/_/g, ' ');
                    results.push(`<div style="margin: 3px 0; padding: 3px;">`);
                    results.push(`🔒 ${questName} | <a href="#" onclick="window.complete_quest('${questKey}'); return false;">[CLICK TO COMPLETE]</a>`);
                    results.push(`</div>`);
                    locked_shown++;
                }
            }
            
            if (locked_count > 15) {
                results.push(`<div style="color: #888; font-style: italic;">... and ${locked_count - 15} more locked quests</div>`);
            }
            results.push(`</div><br>`);
            
            // SUMMARY SECTION
            results.push(`<div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin: 10px 0;">`);
            results.push(`<div style="font-weight: bold; margin-bottom: 5px; color: inherit;">📊 SUMMARY</div>`);
            results.push(`<div style="color: inherit;">Active Quests: ${ongoing_count}</div>`);
            results.push(`<div style="color: inherit;">Completed Quests: ${completed_count}</div>`);
            results.push(`<div style="color: inherit;">Locked Quests: ${locked_count}</div>`);
            results.push(`<div style="color: inherit;">Total Quests: ${total_count}</div>`);
            results.push(`</div>`);
            
            // TIPS SECTION
            results.push(`<div style="border: 1px solid #007bff; padding: 10px; border-radius: 5px; margin: 10px 0;">`);
            results.push(`<div style="font-weight: bold; margin-bottom: 5px; color: inherit;">💡 TIPS</div>`);
            results.push(`<div style="color: inherit;">• Click any quest name to instantly complete it!</div>`);
            results.push(`<div style="color: inherit;">• Use "Auto Complete All" to finish all available quests at once!</div>`);
            results.push(`</div>`);
            
            return results.join("");
        } catch (e) {
            return `<div style="color: red;">Error: ${e.message}</div>`;
        }
        '''

    @js_export(params=["questKey"])
    def complete_quest_js(self, questKey=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const questComplete = bEngine.getGameAttribute("QuestComplete").h;
            const questStatus = bEngine.getGameAttribute("QuestStatus").h;
            const npcDialogue = bEngine.getGameAttribute("NPCdialogue").h;
            const dialogueDefGET = bEngine.getGameAttribute("DialogueDefGET").h;
            
            if (!questComplete.hasOwnProperty(questKey)) {
                return `Error: Quest '${questKey}' not found`;
            }
            
            const questName = questKey.replace(/_/g, ' ');
            
            // Check if quest is already completed
            if (questComplete[questKey] === 1) {
                return `Quest '${questName}' is already completed`;
            }
            
            // Check if quest is locked (status -1 or other negative values)
            if (questComplete[questKey] < 0) {
                return `Quest '${questName}' is locked and cannot be completed`;
            }
            
            // Ensure questStatus entry exists for this quest
            if (!questStatus[questKey]) {
                questStatus[questKey] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; // Create with 10 requirement slots
            }
            
            // Set quest requirements as fulfilled first
            if (questStatus[questKey]) {
                // Set quest as active/requirements met
                questStatus[questKey][0] = 1;
                
                // Set ALL requirement slots to fulfilled (1) - maximum requirements
                for (let i = 1; i < questStatus[questKey].length; i++) {
                    questStatus[questKey][i] = 1; // Fulfill all requirements
                }
            }
            
            // Complete the quest
            questComplete[questKey] = 1;
            
            // Update QuestStatus to completed
            if (questStatus[questKey]) {
                questStatus[questKey][0] = 2; // Completed status
            }
            
            // Find the NPC associated with this quest and update their dialogue
            try {
                // Extract NPC name from quest key (e.g., "Scripticus1" -> "Scripticus")
                const npcName = questKey.replace(/\\d+$/, '');
                
                if (npcDialogue[npcName] !== undefined) {
                    // Advance NPC dialogue to next stage
                    const currentDialogue = npcDialogue[npcName];
                    if (dialogueDefGET[npcName] && dialogueDefGET[npcName][1]) {
                        const maxDialogue = dialogueDefGET[npcName][1].length - 1;
                        if (currentDialogue < maxDialogue) {
                            npcDialogue[npcName] = currentDialogue + 1;
                        }
                    }
                }
            } catch (e) {
                console.log("NPC dialogue update error:", e);
            }
            
            // Trigger quest completion events
            try {
                // Trigger the quest completion event
                const pixelHelper = bEngine.getGameAttribute("PixelHelperActor");
                if (pixelHelper && pixelHelper[5]) {
                    pixelHelper[5].shout("_customEvent_QuestComplete");
                }
                
                // Also trigger on other relevant actors
                if (pixelHelper && pixelHelper[1]) {
                    pixelHelper[1].shout("_customEvent_QuestComplete");
                }
                
                // Update quest helper menu if it exists
                const questHelperMenu = bEngine.getGameAttribute("QuestHelperMenu");
                if (questHelperMenu && questHelperMenu.length > 0) {
                    // Remove completed quest from helper menu
                    for (let i = questHelperMenu.length - 1; i >= 0; i--) {
                        if (questHelperMenu[i] && questHelperMenu[i][0] === questKey) {
                            questHelperMenu.splice(i, 1);
                            break;
                        }
                    }
                }
                
                // Force UI refresh and trigger quest popup updates
                bEngine.gameAttributes.h.DummyText = "QuestCompleted";
                
                // Additional quest popup triggers
                try {
                    // Trigger quest helper menu update
                    if (pixelHelper && pixelHelper[23]) {
                        pixelHelper[23].shout("_customEvent_QuestHelperUpdate");
                    }
                    
                    // Trigger NPC dialogue refresh
                    if (pixelHelper && pixelHelper[38]) {
                        pixelHelper[38].shout("_customEvent_DialogueRefresh");
                    }
                    
                    // Force quest UI refresh
                    bEngine.gameAttributes.h.QuestHelperMenu = bEngine.gameAttributes.h.QuestHelperMenu || [];
                    
                } catch (e) {
                    console.log("Additional quest popup trigger error:", e);
                }
                
            } catch (e) {
                console.log("Quest completion event error:", e);
            }
            
            return `✅ Quest '${questName}' completed successfully with all requirements fulfilled!`;
        } catch (e) {
            return `Error completing quest: ${e.message}`;
        }
        '''

    @js_export()
    def auto_complete_all_quests_js(self):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const questComplete = bEngine.getGameAttribute("QuestComplete").h;
            const questStatus = bEngine.getGameAttribute("QuestStatus").h;
            const npcDialogue = bEngine.getGameAttribute("NPCdialogue").h;
            const dialogueDefGET = bEngine.getGameAttribute("DialogueDefGET").h;
            
            const results = [];
            let completed_count = 0;
            let skipped_locked = 0;
            let requirements_filled = 0;
            
            // Complete ALL quests (not just active ones, but skip locked ones)
            for (const [questKey, isCompleted] of Object.entries(questComplete)) {
                // Skip locked quests (status -1 or other negative values)
                if (isCompleted < 0) {
                    skipped_locked++;
                    continue;
                }
                
                if (isCompleted !== 1) { // Not already completed
                    const questName = questKey.replace(/_/g, ' ');
                    
                    // Ensure questStatus entry exists for this quest
                    if (!questStatus[questKey]) {
                        questStatus[questKey] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; // Create with 10 requirement slots
                    }
                    
                    // Set quest requirements as fulfilled first
                    if (questStatus[questKey]) {
                        // Set quest as active/requirements met
                        questStatus[questKey][0] = 1;
                        
                        // Set ALL requirement slots to fulfilled (1) - maximum requirements
                        for (let i = 1; i < questStatus[questKey].length; i++) {
                            questStatus[questKey][i] = 1; // Fulfill all requirements
                            requirements_filled++;
                        }
                    }
                    
                    // Complete the quest
                    questComplete[questKey] = 1;
                    
                    // Update QuestStatus to completed
                    if (questStatus[questKey]) {
                        questStatus[questKey][0] = 2;
                    }
                    
                    // Update NPC dialogue
                    try {
                        const npcName = questKey.replace(/\\d+$/, '');
                        if (npcDialogue[npcName] !== undefined) {
                            const currentDialogue = npcDialogue[npcName];
                            if (dialogueDefGET[npcName] && dialogueDefGET[npcName][1]) {
                                const maxDialogue = dialogueDefGET[npcName][1].length - 1;
                                if (currentDialogue < maxDialogue) {
                                    npcDialogue[npcName] = currentDialogue + 1;
                                }
                            }
                        }
                    } catch (e) {
                        console.log("NPC dialogue update error for", questKey, ":", e);
                    }
                    
                    results.push(`✅ Completed: ${questName}`);
                    completed_count++;
                }
            }
            
            // Trigger completion events
            try {
                const pixelHelper = bEngine.getGameAttribute("PixelHelperActor");
                if (pixelHelper && pixelHelper[5]) {
                    pixelHelper[5].shout("_customEvent_QuestComplete");
                }
                if (pixelHelper && pixelHelper[1]) {
                    pixelHelper[1].shout("_customEvent_QuestComplete");
                }
                
                // Update quest helper menu
                const questHelperMenu = bEngine.getGameAttribute("QuestHelperMenu");
                if (questHelperMenu && questHelperMenu.length > 0) {
                    // Remove all completed quests from helper menu
                    for (let i = questHelperMenu.length - 1; i >= 0; i--) {
                        if (questHelperMenu[i] && questComplete[questHelperMenu[i][0]] === 1) {
                            questHelperMenu.splice(i, 1);
                        }
                    }
                }
                
                // Force UI refresh and trigger quest popup updates
                bEngine.gameAttributes.h.DummyText = "AllQuestsCompleted";
                
                // Additional quest popup triggers
                try {
                    // Trigger quest helper menu update
                    if (pixelHelper && pixelHelper[23]) {
                        pixelHelper[23].shout("_customEvent_QuestHelperUpdate");
                    }
                    
                    // Trigger NPC dialogue refresh
                    if (pixelHelper && pixelHelper[38]) {
                        pixelHelper[38].shout("_customEvent_DialogueRefresh");
                    }
                    
                    // Force quest UI refresh
                    bEngine.gameAttributes.h.QuestHelperMenu = bEngine.gameAttributes.h.QuestHelperMenu || [];
                    
                } catch (e) {
                    console.log("Additional quest popup trigger error:", e);
                }
                
            } catch (e) {
                console.log("Quest completion event error:", e);
            }
            
            if (completed_count === 0) {
                return `All available quests are already completed! (Skipped ${skipped_locked} locked quests)`;
            }
            
            results.unshift(`🎉 **AUTO-COMPLETED ${completed_count} QUESTS**`);
            results.push(`📊 Filled ${requirements_filled} requirement slots`);
            if (skipped_locked > 0) {
                results.push(`🔒 Skipped ${skipped_locked} locked quests`);
            }
            return results.join("\\n");
        } catch (e) {
            return `Error auto-completing quests: ${e.message}`;
        }
        '''

plugin_class = QuestHelperPlugin 