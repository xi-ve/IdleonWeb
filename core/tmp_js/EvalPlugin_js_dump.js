window.context_info = function() {

        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx) return "Error: No game context found";
            
            const info = {
                hasEngine: !!ctx["com.stencyl.Engine"],
                hasEngineEngine: !!ctx["com.stencyl.Engine"]?.engine,
                engineKeys: ctx["com.stencyl.Engine"] ? Object.keys(ctx["com.stencyl.Engine"]) : [],
                globalKeys: Object.keys(window).filter(k => k.startsWith('__idleon')),
                availableGlobals: ['bEngine', 'itemDefs', 'monsterDefs', 'CList', 'behavior', 'events', 'pluginConfigs'].filter(k => window[k] !== undefined)
            };
            
            return JSON.stringify(info, null, 2);
        } catch (e) {
            return `Error: ${e.message}`;
        }
        
}
window.eval = function(code) {

        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            // Execute the provided code in the game context
            const result = eval(code);
            
            // Return the result, handling different types
            if (result === undefined) return "undefined";
            if (result === null) return "null";
            if (typeof result === 'function') return "[Function]";
            if (typeof result === 'object') {
                try {
                    return JSON.stringify(result, null, 2);
                } catch (e) {
                    return result.toString();
                }
            }
            return result.toString();
        } catch (e) {
            return `Error: ${e.message}\nStack: ${e.stack}`;
        }
        
}
window.eval_raw = function(code) {

        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            // Execute the provided code and return raw result
            return eval(code);
        } catch (e) {
            return `Error: ${e.message}\nStack: ${e.stack}`;
        }
        
}
window.context_info = function() {

        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx) return "Error: No game context found";
            
            const info = {
                hasEngine: !!ctx["com.stencyl.Engine"],
                hasEngineEngine: !!ctx["com.stencyl.Engine"]?.engine,
                engineKeys: ctx["com.stencyl.Engine"] ? Object.keys(ctx["com.stencyl.Engine"]) : [],
                globalKeys: Object.keys(window).filter(k => k.startsWith('__idleon')),
                availableGlobals: ['bEngine', 'itemDefs', 'monsterDefs', 'CList', 'behavior', 'events', 'pluginConfigs'].filter(k => window[k] !== undefined)
            };
            
            return JSON.stringify(info, null, 2);
        } catch (e) {
            return `Error: ${e.message}`;
        }
        
}
window.eval = function(code) {

        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            // Execute the provided code in the game context
            const result = eval(code);
            
            // Return the result, handling different types
            if (result === undefined) return "undefined";
            if (result === null) return "null";
            if (typeof result === 'function') return "[Function]";
            if (typeof result === 'object') {
                try {
                    return JSON.stringify(result, null, 2);
                } catch (e) {
                    return result.toString();
                }
            }
            return result.toString();
        } catch (e) {
            return `Error: ${e.message}\nStack: ${e.stack}`;
        }
        
}
window.eval_raw = function(code) {

        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            // Execute the provided code and return raw result
            return eval(code);
        } catch (e) {
            return `Error: ${e.message}\nStack: ${e.stack}`;
        }
        
}
window.context_info = function() {

        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx) return "Error: No game context found";
            
            const info = {
                hasEngine: !!ctx["com.stencyl.Engine"],
                hasEngineEngine: !!ctx["com.stencyl.Engine"]?.engine,
                engineKeys: ctx["com.stencyl.Engine"] ? Object.keys(ctx["com.stencyl.Engine"]) : [],
                globalKeys: Object.keys(window).filter(k => k.startsWith('__idleon')),
                availableGlobals: ['bEngine', 'itemDefs', 'monsterDefs', 'CList', 'behavior', 'events', 'pluginConfigs'].filter(k => window[k] !== undefined)
            };
            
            return JSON.stringify(info, null, 2);
        } catch (e) {
            return `Error: ${e.message}`;
        }
        
}
window.eval = function(code) {

        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            // Execute the provided code in the game context
            const result = eval(code);
            
            // Return the result, handling different types
            if (result === undefined) return "undefined";
            if (result === null) return "null";
            if (typeof result === 'function') return "[Function]";
            if (typeof result === 'object') {
                try {
                    return JSON.stringify(result, null, 2);
                } catch (e) {
                    return result.toString();
                }
            }
            return result.toString();
        } catch (e) {
            return `Error: ${e.message}\nStack: ${e.stack}`;
        }
        
}
window.eval_raw = function(code) {

        try {
            const ctx = window.__idleon_cheats__;
            if (!ctx?.["com.stencyl.Engine"]?.engine) throw new Error("Game engine not found");
            
            // Execute the provided code and return raw result
            return eval(code);
        } catch (e) {
            return `Error: ${e.message}\nStack: ${e.stack}`;
        }
        
}
