// core.js - Ensures Idleon game is fully ready before plugins run
// Compatible with cheats.js initialization pattern

(function() {
  // Global variables similar to cheats.js
  let bEngine; // The Stencyl engine
  let itemDefs; // The item definitions
  let monsterDefs;
  let CList; // The custom list definitions
  let events; // function that returns actorEvent script by it's number
  let behavior; // Stencyl behavior object
  let setupDone = false;

  // Game readiness check similar to cheats.js
  async function gameReady() {
    // Use 'this' context like in cheats.js
    const context = this || window.__idleon_cheats__;
    
    while (
      !context["com.stencyl.Engine"] ||
      !context["com.stencyl.Engine"].hasOwnProperty("engine") ||
      !context["com.stencyl.Engine"].engine.hasOwnProperty("scene") ||
      !context["com.stencyl.Engine"].engine.sceneInitialized ||
      context["com.stencyl.Engine"].engine.behaviors.behaviors[0].script._CloudLoadComplete !== 1
    ) {
      console.log("[core.js] Waiting for game to be ready...", context);
      await new Promise((resolve) => setTimeout(resolve, 1000));
    }
    await new Promise((resolve) => setTimeout(resolve, 1000)); // Extra wait like cheats.js
    registerCommonVariables.call(context);
    return true;
  }

  // Register common variables like in cheats.js
  function registerCommonVariables() {
    const context = this || window.__idleon_cheats__;
    
    bEngine = context["com.stencyl.Engine"].engine;
    itemDefs = bEngine.getGameAttribute("ItemDefinitionsGET").h;
    monsterDefs = bEngine.getGameAttribute("MonsterDefinitionsGET").h;
    CList = bEngine.getGameAttribute("CustomLists").h;
    behavior = context["com.stencyl.behavior.Script"];
    events = function (num) {
      return context["scripts.ActorEvents_" + num];
    }.bind(context);

    // Make these available globally like in cheats.js
    if (typeof window !== 'undefined') {
      window.bEngine = bEngine;
      window.itemDefs = itemDefs;
      window.monsterDefs = monsterDefs;
      window.CList = CList;
      window.behavior = behavior;
      window.events = events;
    }

    console.log('[core.js] Common variables registered successfully');
  }

  // Main setup function similar to cheats.js setup()
  async function setup() {
    if (setupDone) return "Core setup already complete";
    
    console.log('[core.js] Starting setup...');
    setupDone = true;

    try {
      const context = window.__idleon_cheats__;
      if (!context) {
        throw new Error("__idleon_cheats__ context not found");
      }

      // Wait for game to be ready
      await gameReady.call(context);
      
      console.log('[core.js] Setup completed successfully');
      return "Core setup complete - game is ready";
    } catch (error) {
      console.error('[core.js] Setup failed:', error);
      setupDone = false;
      throw error;
    }
  }

  // Expose the main setup function globally
  window.__idleon_core_setup = setup;

  // Enhanced game ready check that returns a Promise
  window.__idleon_wait_for_game_ready = function() {
    return new Promise(async (resolve, reject) => {
      try {
        console.log('[core.js] Starting game readiness check...');
        
        let context = window.__idleon_cheats__;
        if (!context) {
          // Try to find context in iframe
          const iframe = window.document.querySelector('iframe');
          if (iframe && iframe.contentWindow && iframe.contentWindow.__idleon_cheats__) {
            context = iframe.contentWindow.__idleon_cheats__;
            console.log('[core.js] Found context in iframe');
          } else {
            throw new Error("Could not find __idleon_cheats__ context");
          }
        }

        // Wait for game to be fully ready
        await gameReady.call(context);
        
        console.log('[core.js] Game is fully ready!');
        resolve();
      } catch (error) {
        console.error('[core.js] Game readiness check failed:', error);
        reject(error);
      }
    });
  };

  // Legacy compatibility - simple game ready check
  window.__idleon_is_game_ready = function() {
    try {
      const context = window.__idleon_cheats__;
      return !!(
        context &&
        context['com.stencyl.Engine'] &&
        context['com.stencyl.Engine'].engine &&
        context['com.stencyl.Engine'].engine.scene &&
        context['com.stencyl.Engine'].engine.sceneInitialized &&
        context['com.stencyl.Engine'].engine.behaviors.behaviors[0].script._CloudLoadComplete === 1
      );
    } catch (e) {
      return false;
    }
  };

  // Initialize result collector for plugin communication
  if (!window.__plugin_results__) {
    window.__plugin_results__ = {};
  }

  // Add postMessage handler for plugin function calls
  window.addEventListener('message', async function(event) {
    if (!event.data || event.data.type !== 'plugin_call') return;
    
    try {
      const { func, args, callId } = event.data;
      let result;
      
      if (typeof window[func] === 'function') {
        result = await window[func](...(args || []));
      } else {
        result = `Function '${func}' not found`;
      }
      
      // Store result for polling
      window.__plugin_results__[callId] = { type: 'plugin_result', callId, result };
      
      // Also post back for in-browser listeners
      window.postMessage({ type: 'plugin_result', callId, result }, '*');
    } catch (e) {
      const errorMsg = e && e.stack ? e.stack : e;
      window.__plugin_results__[event.data.callId] = { 
        type: 'plugin_result', 
        callId: event.data.callId, 
        error: errorMsg 
      };
      window.postMessage({ 
        type: 'plugin_result', 
        callId: event.data.callId, 
        error: errorMsg 
      }, '*');
    }
  });

  // Auto-initialize when context becomes available
  function checkForContext() {
    if (window.__idleon_cheats__ && !setupDone) {
      console.log('[core.js] Context detected, running auto-setup...');
      setup().catch(error => {
        console.error('[core.js] Auto-setup failed:', error);
      });
    } else if (!window.__idleon_cheats__) {
      // Check again in 1 second
      setTimeout(checkForContext, 1000);
    }
  }

  // Start checking for context
  setTimeout(checkForContext, 100);

  console.log('[core.js] Core initialization script loaded');
})();