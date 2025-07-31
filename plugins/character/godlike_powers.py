import time
from plugin_system import PluginBase, ui_toggle, ui_slider, plugin_command, js_export, console
from config_manager import config_manager

class GodlikePowersPlugin(PluginBase):
    VERSION = "1.0.0"
    DESCRIPTION = "Provides godlike powers and abilities for the game."
    PLUGIN_ORDER = 1
    CATEGORY = "Character"

    def __init__(self, config=None):
        super().__init__(config or {})
        self.injector = None
        self.name = 'godlike_powers'
        self.enabled = self.config.get('enabled', False)
        self.debug = config_manager.get_path('plugin_configs.godlike_powers.debug', False)
        self.last_update = 0

    async def cleanup(self):
        pass

    async def update(self):
        self.debug = config_manager.get_path('plugin_configs.godlike_powers.debug', False)
        if self.last_update < time.time() - 10:
            self.last_update = time.time()
            if hasattr(self, 'injector') and self.injector and config_manager.get_path('plugin_configs.godlike_powers.enabled', False):
                self.run_js_export('godlike_powers_js', self.injector, enabled=self.config.get('enabled', False))

    async def on_config_changed(self, config):
        self.enabled = config.get('enabled', False)
        self.debug = config_manager.get_path('plugin_configs.godlike_powers.debug', False)
        if self.debug:
            console.print(f"[godlike_powers] Config changed: {config}")
        if hasattr(self, 'injector') and self.injector:
            self.set_config(config)
            try:
                self.run_js_export('godlike_powers_js', self.injector, enabled=self.config.get('enabled', False))
            except Exception as e:
                if self.debug:
                    console.print(f"[godlike_powers] Config change error: {e}")

    async def on_game_ready(self):
        if self.injector:
            try:
                self.set_config(config_manager.get_plugin_config(self.name))
                self.run_js_export('godlike_powers_js', self.injector, enabled=self.config.get('enabled', False))
            except Exception as e:
                console.print(f"[godlike_powers] Error setting up godlike powers: {e}")

    @ui_toggle(
        label="Enable Godlike Powers",
        description="Enable all godlike power features",
        config_key="enabled",
        default_value=False,
        order=1
    )
    async def enable_godlike_powers_ui(self, value=None):
        if value is not None:        
            self.enabled = value
            config_manager.set_path('plugin_configs.godlike_powers.enabled', value)
            if hasattr(self, 'injector') and self.injector:
                self.run_js_export('godlike_powers_js', self.injector, enabled=value)
        return f"Godlike Powers are {'enabled' if self.config.get('enabled', False) else 'disabled'}"

    @ui_toggle(
        label="Debug Mode",
        description="Enable debug logging for godlike powers plugin",
        config_key="debug",
        default_value=False,
        category="Debug Settings",
        order=1
    )
    async def enable_debug(self, value=None):
        if value is not None:
            self.config['debug'] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                self.run_js_export('godlike_powers_js', self.injector, enabled=self.config.get('enabled', False))
        return f"Debug mode {'enabled' if self.config.get('debug', False) else 'disabled'}"

    @ui_toggle(
        label="Reach Power",
        description="Set player reach to 666",
        config_key="reach",
        default_value=False,
        order=2
    )
    async def reach_power_ui(self, value=None):
        if value is not None:
            self.config['reach'] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                self.run_js_export('godlike_powers_js', self.injector, enabled=self.config.get('enabled', False))
        return f"Reach power {'enabled' if self.config.get('reach', False) else 'disabled'}"

    @ui_toggle(
        label="Critical Hit Power",
        description="Set critical hit chance to 100%",
        config_key="crit",
        default_value=False,
        order=3
    )
    async def crit_power_ui(self, value=None):
        if value is not None:
            self.config['crit'] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                self.run_js_export('godlike_powers_js', self.injector, enabled=self.config.get('enabled', False))
        return f"Critical hit power {'enabled' if self.config.get('crit', False) else 'disabled'}"

    @ui_toggle(
        label="Ability Power",
        description="Zero ability cooldown, mana cost nullification and cast time 0.1s",
        config_key="ability",
        default_value=False,
        order=4
    )
    async def ability_power_ui(self, value=None):
        if value is not None:
            self.config['ability'] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                self.run_js_export('godlike_powers_js', self.injector, enabled=self.config.get('enabled', False))
        return f"Ability power {'enabled' if self.config.get('ability', False) else 'disabled'}"

    @ui_toggle(
        label="Food Power",
        description="Food deduction nullification",
        config_key="food",
        default_value=False,
        order=5
    )
    async def food_power_ui(self, value=None):
        if value is not None:
            self.config['food'] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                self.run_js_export('godlike_powers_js', self.injector, enabled=self.config.get('enabled', False))
        return f"Food power {'enabled' if self.config.get('food', False) else 'disabled'}"

    @ui_toggle(
        label="Hit Chance Power",
        description="Set hit chance to 100%",
        config_key="hitchance",
        default_value=False,
        order=6
    )
    async def hitchance_power_ui(self, value=None):
        if value is not None:
            self.config['hitchance'] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                self.run_js_export('godlike_powers_js', self.injector, enabled=self.config.get('enabled', False))
        return f"Hit chance power {'enabled' if self.config.get('hitchance', False) else 'disabled'}"

    @ui_toggle(
        label="Divine Intervention",
        description="Instant divine intervention",
        config_key="intervention",
        default_value=False,
        order=7
    )
    async def intervention_power_ui(self, value=None):
        if value is not None:
            self.config['intervention'] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                self.run_js_export('godlike_powers_js', self.injector, enabled=self.config.get('enabled', False))
        return f"Divine intervention {'enabled' if self.config.get('intervention', False) else 'disabled'}"

    @ui_slider(
        label="Weapon Speed",
        description="Set weapon super speed (max 14 to avoid non-attacking bug)",
        config_key="weapon_speed",
        default_value=9,
        min_value=1,
        max_value=14,
        step=1,
        order=8
    )
    async def weapon_speed_ui(self, value=None):
        if value is not None:
            self.config['weapon_speed'] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                self.run_js_export('godlike_powers_js', self.injector, enabled=self.config.get('enabled', False))
        return f"Weapon speed set to {self.config.get('weapon_speed', 9)}"

    @ui_toggle(
        label="Card Power",
        description="Alter Efaunt, Chaotic Efaunt, Dr Defecaus, Oak Tree and Copper with insane stats",
        config_key="card",
        default_value=False,
        order=9
    )
    async def card_power_ui(self, value=None):
        if value is not None:
            self.config['card'] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                self.run_js_export('godlike_powers_js', self.injector, enabled=self.config.get('enabled', False))
        return f"Card power {'enabled' if self.config.get('card', False) else 'disabled'}"

    @ui_toggle(
        label="Poison Power",
        description="Instant bubo poison",
        config_key="poison",
        default_value=False,
        order=10
    )
    async def poison_power_ui(self, value=None):
        if value is not None:
            self.config['poison'] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                self.run_js_export('godlike_powers_js', self.injector, enabled=self.config.get('enabled', False))
        return f"Poison power {'enabled' if self.config.get('poison', False) else 'disabled'}"

    @ui_toggle(
        label="Invincibility",
        description="Never lose HP, become invincible",
        config_key="hp",
        default_value=False,
        order=11
    )
    async def hp_power_ui(self, value=None):
        if value is not None:
            self.config['hp'] = value
            self.save_to_global_config()
            if hasattr(self, 'injector') and self.injector:
                self.run_js_export('godlike_powers_js', self.injector, enabled=self.config.get('enabled', False))
        return f"Invincibility {'enabled' if self.config.get('hp', False) else 'disabled'}"

    @plugin_command(help="Set godlike powers")
    async def set_powers(self, injector=None, **kwargs):
        if not injector:
            return "ERROR: No injector available - run 'inject' first"
        
        return self.run_js_export('godlike_powers_js', injector, enabled=self.config.get('enabled', False))

    @js_export(params=["enabled"])
    def godlike_powers_js(self, enabled=None):
        return '''
        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx) {
                return "Error: Game context not available";
            }

            const engine = ctx["com.stencyl.Engine"].engine;
            const behavior = ctx["com.stencyl.behavior.Script"];
            const events = function(num) { return ctx["scripts.ActorEvents_" + num]; };

            if (!engine || !behavior) {
                return "Error: Game engine not ready";
            }

            if (!window.__godlike_powers_originals__) {
                window.__godlike_powers_originals__ = {
                    CritChance: events(12)._customBlock_CritChance,
                    PlayerReach: events(12)._customBlock_PlayerReach,
                    ArbitraryCode: events(12)._customBlock_ArbitraryCode,
                    PlayerHP: engine.gameAttributes.h.PlayerHP,
                    atkMoveMap: ctx["scripts.CustomMaps"].atkMoveMap.h
                };
            }

            if (window.pluginConfigs && window.pluginConfigs['godlike_powers'] && window.pluginConfigs['godlike_powers'].enabled) {
                const pluginConfig = window.pluginConfigs['godlike_powers'];
                const originals = window.__godlike_powers_originals__;

                if (originals.CritChance) {
                    events(12)._customBlock_CritChance = function(...argumentsList) {
                        if (pluginConfig.crit) return 100;
                        return originals.CritChance(...argumentsList);
                    };
                }

                if (originals.PlayerReach) {
                    events(12)._customBlock_PlayerReach = function(...argumentsList) {
                        if (pluginConfig.reach) return 666;
                        return originals.PlayerReach(...argumentsList);
                    };
                }

                if (originals.ArbitraryCode) {
                    events(12)._customBlock_ArbitraryCode = function(...argumentsList) {
                        const t = argumentsList[0];
                        if (t == "FoodNOTconsume" && pluginConfig.food) return 100;
                        if (t == "HitChancePCT" && pluginConfig.hitchance) return 100;
                        return originals.ArbitraryCode(...argumentsList);
                    };
                }

                if (originals.PlayerHP) {
                    Object.defineProperty(engine.gameAttributes.h, "PlayerHP", {
                        get: function() {
                            return this._PlayerHP;
                        },
                        set: function(value) {
                            if (pluginConfig.hp) {
                                return (this._PlayerHP = events(12)._customBlock_PlayerHPmax());
                            } else {
                                return (this._PlayerHP = value);
                            }
                        }
                    });
                }

                if (originals.atkMoveMap) {
                    const CustomMaps = ctx["scripts.CustomMaps"];
                    if (pluginConfig.ability) {
                        const atkMoveMap = JSON.parse(JSON.stringify(CustomMaps.atkMoveMap.h));
                        for (const [key, value] of Object.entries(atkMoveMap)) {
                            value.h["cooldown"] = 0;
                            value.h["castTime"] = 0.1;
                            value.h["manaCost"] = 0;
                            atkMoveMap[key] = value;
                        }
                        const handler = {
                            get: function(obj, prop) {
                                return atkMoveMap[prop];
                            }
                        };
                        const proxy = new Proxy(CustomMaps.atkMoveMap.h, handler);
                        CustomMaps.atkMoveMap.h = proxy;
                    } else {
                        CustomMaps.atkMoveMap.h = originals.atkMoveMap;
                    }
                }

                if (pluginConfig.weapon_speed && pluginConfig.weapon_speed > 1) {
                    const itemDefs = engine.getGameAttribute("ItemDefinitionsGET").h;
                    for (const [index, element] of Object.entries(itemDefs)) {
                        if (element.h["typeGen"] === "aWeapon") {
                            itemDefs[index].h["Speed"] = pluginConfig.weapon_speed;
                        }
                    }
                }

                if (pluginConfig.card) {
                    const CList = engine.getGameAttribute("CustomLists").h;
                    const CardStuff = CList["CardStuff"];
                    const TargetCards = ["Boss2A", "Boss2B", "poopBig", "OakTree", "Copper"];
                    for (const [key1, value1] of Object.entries(CardStuff)) {
                        for (const [key2, value2] of Object.entries(value1)) {
                            if (TargetCards.includes(value2[0])) {
                                CardStuff[key1][key2][4] = "10000";
                            }
                        }
                    }
                }

                return `Godlike powers applied: Reach(${pluginConfig.reach ? 'ON' : 'OFF'}), Crit(${pluginConfig.crit ? 'ON' : 'OFF'}), Ability(${pluginConfig.ability ? 'ON' : 'OFF'}), Food(${pluginConfig.food ? 'ON' : 'OFF'}), HitChance(${pluginConfig.hitchance ? 'ON' : 'OFF'}), Intervention(${pluginConfig.intervention ? 'ON' : 'OFF'}), Speed(${pluginConfig.weapon_speed}), Card(${pluginConfig.card ? 'ON' : 'OFF'}), Poison(${pluginConfig.poison ? 'ON' : 'OFF'}), Respawn(${pluginConfig.respawn ? 'ON' : 'OFF'}), HP(${pluginConfig.hp ? 'ON' : 'OFF'})`;
            } else {
                const originals = window.__godlike_powers_originals__;
                if (originals) {
                    if (originals.CritChance) events(12)._customBlock_CritChance = originals.CritChance;
                    if (originals.PlayerReach) events(12)._customBlock_PlayerReach = originals.PlayerReach;
                    if (originals.ArbitraryCode) events(12)._customBlock_ArbitraryCode = originals.ArbitraryCode;
                    if (originals.PlayerHP) {
                        Object.defineProperty(engine.gameAttributes.h, "PlayerHP", {
                            get: function() {
                                return this._PlayerHP;
                            },
                            set: function(value) {
                                return (this._PlayerHP = value);
                            }
                        });
                    }
                    if (originals.MonsterRespawnTime) {
                        engine.setGameAttribute("MonsterRespawnTime", originals.MonsterRespawnTime);
                    }
                    if (originals.atkMoveMap) {
                        const CustomMaps = ctx["scripts.CustomMaps"];
                        CustomMaps.atkMoveMap.h = originals.atkMoveMap;
                    }
                }
                return "Godlike powers disabled and original functions restored.";
            }
        } catch (e) {
            return `Error: ${e.message}`;
        }
        '''

plugin_class = GodlikePowersPlugin 