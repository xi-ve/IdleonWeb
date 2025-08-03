from plugin_system import PluginBase, js_export, ui_toggle, ui_search_with_results, ui_autocomplete_input, console, ui_banner

class ClassUnlockPlugin(PluginBase):
    VERSION = "1.0.0"
    DESCRIPTION = "Set characters to any class, change characters classes, view class progression."
    PLUGIN_ORDER = 4
    CATEGORY = "Unlocks"

    def __init__(self, config=None):
        super().__init__(config or {})
        self.debug = config.get('debug', False) if config else False
        self.name = 'class_unlock'

    async def cleanup(self): 
        pass
    
    async def update(self): 
        pass
    
    async def on_config_changed(self, config): 
        self.debug = config.get('debug', False)
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)
    
    async def on_game_ready(self): 
        pass

    @ui_toggle(
        label="Debug Mode",
        description="Enable debug logging for class unlock plugin",
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
        label="Class Progression Banner",
        description="Show current class and all upgradeable subclasses in the progression chain",
        button_text="Show Progression Banner",
        placeholder="Enter filter term (leave empty to show all)",
    )
    async def class_progression_banner_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[class_unlock] Getting class progression banner, filter: {value}")
                result = self.run_js_export('get_class_progression_banner_js', self.injector, filter_query=value or "")
                return result
            except Exception as e:
                if self.debug:
                    console.print(f"[class_unlock] Error getting class progression banner: {e}")
                return f"ERROR: Error getting class progression banner: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @ui_banner(
        label="⚠️ Class Corruption Warning",
        description="⚠️ DANGER: Class changes can corrupt your character (infinite/invalid HP/MP/stats). Emergency recovery: Use 'Complete Class Redo Token' item.",
        category="Search",
        order=-5000
    )
    def banner_warning(self):
        return ''

    @ui_autocomplete_input(
        label="Set Character Class",
        description="Set your character to any class. The system will follow the proper progression chain to unlock all required classes. Available: 29 classes including Beginner, Warrior, Archer, Mage, Secret classes, and master classes like Death Bringer, Wind Walker, and Arcane Cultist.",
        button_text="Set Class",
        placeholder="Enter class name such as, Mage, Warrior, Archer, Blood Berserker ...",
    )
    async def set_character_class_ui(self, value: str = None):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[class_unlock] Setting character class to: {value}")
                result = self.run_js_export('set_character_class_js', self.injector, class_name=value)
                return result
            except Exception as e:
                if self.debug:
                    console.print(f"[class_unlock] Error setting character class: {e}")
                return f"ERROR: Error setting character class: {str(e)}"
        else:
            return "ERROR: No injector available - run 'inject' first to connect to the game"

    @js_export(params=["filter_query"])
    def get_class_progression_banner_js(self, filter_query=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            const currentClass = bEngine.getGameAttribute("CharacterClass") || 0;
            
            const classInfo = {
                0: "No Class", 1: "Beginner", 2: "Rocklyte", 3: "Cactolyte", 4: "Voidwalker",
                5: "Promotheus", 6: "Beginner (Max)", 7: "Warrior", 8: "Barbarian", 9: "Squire", 10: "Blood Berserker",
                11: "Death Bringer", 12: "Divine Knight", 13: "Royal Guardian", 14: "Journeyman",
                15: "Maestro", 19: "Archer", 20: "Hunter", 21: "Ranger", 22: "Bowman", 
                23: "Siege Breaker", 25: "Wind Walker", 26: "Beast Master", 28: "Elemental Sorcerer",
                29: "Voidwalker", 31: "Mage", 32: "Wizard", 33: "Shaman", 36: "Bubonic Conjuror", 
                37: "Arcane Cultist (Old)", 40: "Arcane Cultist"
            };
            
            const classProgression = {
                "journeyman": [1, 14],
                "maestro": [1, 14, 15],
                "voidwalker": [1, 14, 15, 29],
                "warrior": [1, 7],
                "barbarian": [1, 7, 8],
                "blood berserker": [1, 7, 8, 10],
                "death bringer": [1, 7, 8, 10, 11],
                "squire": [1, 7, 9],
                "divine knight": [1, 7, 9, 12],
                "royal guardian": [1, 7, 13],
                "archer": [1, 19],
                "bowman": [1, 19, 22],
                "siege breaker": [1, 19, 22, 23],
                "hunter": [1, 19, 20],
                "beast master": [1, 19, 20, 26],
                "wind walker": [1, 19, 20, 26, 25],
                "ranger": [1, 19, 21],
                "mayheim": [1, 19, 24],
                "mage": [1, 31],
                "wizard": [1, 31, 32],
                "elemental sorcerer": [1, 31, 32, 28],
                "elementalist": [1, 31, 32, 34],
                "shaman": [1, 31, 33],
                "bubonic conjuror": [1, 31, 33, 36],
                "arcane cultist": [1, 31, 33, 36, 40],
                "spiritual monk": [1, 31, 35],
                "ethereal form": [1, 31, 38],
                "druid": [1, 31, 39],
                "battle mage": [1, 31, 30],
                "virtuoso": [1, 14, 16],
                "infiltrator": [1, 14, 17],
                "shadow assassin": [1, 14, 18],
                "strat": [1, 27],
                "infinilyte": [1, 41]
            };
            
            let output = "";
            output += "<div style='font-weight: bold; font-size: 18px; margin-bottom: 15px; text-align: center; color: #ffd700;'>⚔️ CLASS PROGRESSION CHAIN</div>";
            
            const currentClassName = classInfo[currentClass] || `Unknown (${currentClass})`;
            output += `<div style='margin-bottom: 20px; padding: 15px; background: linear-gradient(135deg, #2a2a2a 0%, #3a3a3a 100%); border-radius: 8px; border: 2px solid #ffd700;'>`;
            output += `<div style='font-size: 16px; font-weight: bold; color: #ffd700; margin-bottom: 8px;'>Current Class:</div>`;
            output += `<div style='font-size: 20px; font-weight: bold; color: #ffffff;'>${currentClassName}</div>`;
            output += `<div style='font-size: 12px; color: #cccccc; margin-top: 5px;'>ID: ${currentClass}</div>`;
            output += "</div>";
            
            output += "<div style='font-weight: bold; font-size: 16px; margin: 20px 0 10px 0; color: #4CAF50;'>Available Upgrade Paths:</div>";
            
            const filterLower = (filter_query || "").toLowerCase();
            
            const renderProgressionChain = (chain, title, color) => {
                const chainNames = chain.map(id => classInfo[id] || `Unknown (${id})`);
                const filteredNames = chainNames.filter(name => 
                    !filterLower || name.toLowerCase().includes(filterLower)
                );
                
                if (filteredNames.length === 0) return "";
                
                let section = `<div style='margin: 15px 0;'>`;
                section += `<div style='font-weight: bold; font-size: 14px; color: ${color}; margin-bottom: 8px;'>${title}:</div>`;
                section += "<div style='display: flex; flex-wrap: wrap; gap: 8px;'>";
                
                filteredNames.forEach((name, index) => {
                    const isCurrent = chainNames.includes(currentClassName) && name === currentClassName;
                    const isUnlocked = chainNames.indexOf(name) <= chainNames.indexOf(currentClassName);
                    
                    let bgColor = "#2a2a2a";
                    let borderColor = "#555";
                    let textColor = "#cccccc";
                    
                    if (isCurrent) {
                        bgColor = "#ffd700";
                        borderColor = "#ffd700";
                        textColor = "#000000";
                    } else if (isUnlocked) {
                        bgColor = "#4CAF50";
                        borderColor = "#4CAF50";
                        textColor = "#ffffff";
                    } else {
                        bgColor = "#f44336";
                        borderColor = "#f44336";
                        textColor = "#ffffff";
                    }
                    
                    section += `<div style='padding: 8px 12px; background: ${bgColor}; border: 2px solid ${borderColor}; border-radius: 6px; color: ${textColor}; font-weight: bold; font-size: 12px;'>`;
                    section += `${name}</div>`;
                    
                    if (index < filteredNames.length - 1) {
                        section += `<div style='color: ${color}; font-weight: bold; margin: 0 4px;'>→</div>`;
                    }
                });
                
                section += "</div></div>";
                return section;
            };
            
            const secretChain = [1, 14, 15, 29];
            const warriorBarbarianChain = [1, 7, 8, 10, 11];
            const warriorSquireChain = [1, 7, 9, 12];
            const warriorRoyalGuardianChain = [1, 7, 13];
            const archerBowmanChain = [1, 19, 22, 23];
            const archerHunterChain = [1, 19, 20, 26, 25];
            const archerRangerChain = [1, 19, 21];
            const mageWizardChain = [1, 31, 32, 28];
            const mageShamanChain = [1, 31, 33, 36, 40];
            
            output += renderProgressionChain(secretChain, "Secret Path (Journeyman → Maestro → Voidwalker)", "#ff6b6b");
            output += renderProgressionChain(warriorBarbarianChain, "Warrior Path (Barbarian → Blood Berserker → Death Bringer)", "#4ecdc4");
            output += renderProgressionChain(warriorSquireChain, "Warrior Path (Squire → Divine Knight)", "#45b7d1");
            output += renderProgressionChain(warriorRoyalGuardianChain, "Warrior Path (Royal Guardian)", "#8e44ad");
            output += renderProgressionChain(archerBowmanChain, "Archer Path (Bowman → Siege Breaker)", "#96ceb4");
            output += renderProgressionChain(archerHunterChain, "Archer Path (Hunter → Beast Master → Wind Walker)", "#feca57");
            output += renderProgressionChain(archerRangerChain, "Archer Path (Ranger)", "#2ecc71");
            output += renderProgressionChain(mageWizardChain, "Mage Path (Wizard → Elemental Sorcerer)", "#ff9ff3");
            output += renderProgressionChain(mageShamanChain, "Mage Path (Shaman → Bubonic Conjuror → Arcane Cultist)", "#54a0ff");
            
            output += `<div style='margin-top: 20px; padding: 10px; background: #1a1a1a; border-radius: 5px; border-left: 4px solid #ffd700;'>`;
            output += `<div style='font-size: 12px; color: #cccccc;'>`;
            output += `<strong>Legend:</strong><br>`;
            output += `<span style='color: #ffd700;'>🟡 Current Class</span> | `;
            output += `<span style='color: #4CAF50;'>🟢 Unlocked</span> | `;
            output += `<span style='color: #f44336;'>🔴 Locked</span>`;
            output += "</div></div>";
            
            return output;
        } catch (error) {
            console.error("Error in class progression banner:", error);
            return "Error: " + error.message;
        }
        '''

    @js_export(params=["class_name"])
    def set_character_class_js(self, class_name=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            const bEngine = ctx["com.stencyl.Engine"].engine;
            
            const classMap = {
                "beginner": 1,
                "rocklyte": 2,
                "cactolyte": 3,
                "voidwalker": 4,
                "promotheus": 5,
                "warrior": 7,
                "barbarian": 8,
                "squire": 9,
                "blood berserker": 10,
                "death bringer": 11,
                "divine knight": 12,
                "royal guardian": 13,
                "journeyman": 14,
                "maestro": 15,
                "archer": 19,
                "hunter": 20,
                "ranger": 21,
                "bowman": 22,
                "siege breaker": 23,
                "wind walker": 25,
                "beast master": 26,
                "elemental sorcerer": 28,
                "mage": 31,
                "wizard": 32,
                "shaman": 33,
                "bubonic conjuror": 36,
                "arcane cultist": 37
            };
            
            if (!class_name) {
                return "Error: No class name provided";
            }
            
            const masterClasses = ["death bringer", "wind walker", "arcane cultist"];
            if (masterClasses.includes(class_name.toLowerCase())) {
                return "⚠️ MASTER CLASS: This is a master class that must be obtained through special NPCs in World 6. Setting this class directly may cause issues.";
            }
            
            const classId = classMap[class_name.toLowerCase()];
            if (!classId) {
                return `Error: Unknown class name '${class_name}'. Available classes: ${Object.keys(classMap).join(", ")}`;
            }
            
            const userInfo = bEngine.getGameAttribute("UserInfo");
            const currentPlayerId = userInfo ? userInfo[0] : null;
            
            if (!currentPlayerId) {
                return "Error: Could not determine current player ID";
            }
            
            const playerDatabase = bEngine.getGameAttribute("PlayerDATABASE");
            if (playerDatabase && playerDatabase.h && playerDatabase.h[currentPlayerId]) {
                const currentPlayer = playerDatabase.h[currentPlayerId];
                if (currentPlayer && currentPlayer.h) {
                    currentPlayer.h.CharacterClass = classId;
                }
            }
            
            bEngine.setGameAttribute("CharacterClass", classId);
            
            return `Successfully set current character to ${class_name} class (ID: ${classId})!`;
        } catch (error) {
            console.error("Error setting character class:", error);
            return "Error: " + error.message;
        }
        '''

    async def get_set_character_class_ui_autocomplete(self, query: str = ""):
        if hasattr(self, 'injector') and self.injector:
            try:
                if self.debug:
                    console.print(f"[class_unlock] Getting class autocomplete for query: {query}")
                result = self.run_js_export('get_all_class_names_js', self.injector, query=query)
                return result
            except Exception as e:
                if self.debug:
                    console.print(f"[class_unlock] Error getting class autocomplete: {e}")
                return []
        return []

    @js_export(params=["query"])
    def get_all_class_names_js(self, query=None):
        return '''
        try {
            const allClasses = [
                "Beginner", "Rocklyte", "Cactolyte", "Voidwalker", "Promotheus", "Beginner (Max)",
                "Warrior", "Barbarian", "Squire", "Blood Berserker", "Death Bringer", "Divine Knight", "Royal Guardian",
                "Archer", "Hunter", "Ranger", "Bowman", "Siege Breaker", "Beast Master", "Wind Walker",
                "Mage", "Wizard", "Shaman", "Bubonic Conjuror", "Arcane Cultist", "Elemental Sorcerer",
                "Journeyman", "Maestro", "Voidwalker"
            ];
            
            if (!query) return allClasses;
            
            const queryLower = query.toLowerCase();
            return allClasses.filter(name => 
                name.toLowerCase().includes(queryLower)
            );
        } catch (error) {
            console.error("Error getting all class names:", error);
            return [];
        }
        '''



plugin_class = ClassUnlockPlugin
