window.setup_proxy_mob_respawn_rate = async function() {

                        try {
                            // Wait for game to be ready before executing plugin function
                            await window.__idleon_wait_for_game_ready();
                            
                            
        const ctx = window.__idleon_cheats__;
        const engine = ctx["com.stencyl.Engine"].engine;

        console.log("Setup proxy mob respawn rate");

        console.log(window.pluginConfigs['mob_spawn_rate']?.toggle);
        
        engine.setGameAttribute("MonsterRespawnTime", 
            new Proxy(engine.getGameAttribute("MonsterRespawnTime"), {
                set: function(target, prop, value) {
                    return (target[prop] = window.pluginConfigs['mob_spawn_rate']?.toggle ? 0 : value);
                },
            })
        );
        
                        } catch (e) {
                            console.error('[setup_proxy_mob_respawn_rate] Error:', e);
                            return `Error: ${e.message}`;
                        }
                        
}
