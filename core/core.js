(function() {
  let bEngine;
  let itemDefs;
  let monsterDefs;
  let CList;
  let events;
  let behavior;
  let setupDone = false;
  let gameReadyPromise = null;

  async function gameReady() {
    const context = this || window.__idleon_cheats__;
    
    // Early return if already setup and variables are registered
    if (setupDone && window.bEngine) {
      console.log('[core.js] Game already ready, skipping wait');
      return true;
    }
    
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
    await new Promise((resolve) => setTimeout(resolve, 1000));
    registerCommonVariables.call(context);
    return true;
  }

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

  async function setup() {
    if (setupDone && window.bEngine) return "Core setup already complete";
    
    console.log('[core.js] Starting setup...');

    try {
      const context = window.__idleon_cheats__;
      if (!context) {
        throw new Error("__idleon_cheats__ context not found");
      }

      await gameReady.call(context);
      
      // Only set setupDone after gameReady completes successfully
      setupDone = true;
      
      console.log('[core.js] Setup completed successfully');
      return "Core setup complete - game is ready";
    } catch (error) {
      console.error('[core.js] Setup failed:', error);
      setupDone = false;
      throw error;
    }
  }

  window.__idleon_core_setup = setup;

  // Fixed version with proper caching and early returns
  window.__idleon_wait_for_game_ready = function() {
    // Return cached promise if it exists
    if (gameReadyPromise) {
      console.log('[core.js] Returning cached game ready promise');
      return gameReadyPromise;
    }

    // Early return if already setup AND variables are properly initialized
    if (setupDone && window.bEngine) {
      console.log('[core.js] Game already ready, returning resolved promise');
      return Promise.resolve();
    }

    gameReadyPromise = new Promise(async (resolve, reject) => {
      try {
        console.log('[core.js] Starting game readiness check...');
        
        let context = window.__idleon_cheats__;
        if (!context) {
          const iframe = window.document.querySelector('iframe');
          if (iframe && iframe.contentWindow && iframe.contentWindow.__idleon_cheats__) {
            context = iframe.contentWindow.__idleon_cheats__;
            console.log('[core.js] Found context in iframe');
          } else {
            throw new Error("Could not find __idleon_cheats__ context");
          }
        }

        await gameReady.call(context);
        
        // Mark as done and clear the promise cache
        setupDone = true;
        gameReadyPromise = null;
        
        console.log('[core.js] Game is fully ready!');
        resolve();
      } catch (error) {
        console.error('[core.js] Game readiness check failed:', error);
        
        // Clear the promise cache on error so it can be retried
        gameReadyPromise = null;
        setupDone = false;
        
        reject(error);
      }
    });

    return gameReadyPromise;
  };

  window.__idleon_is_game_ready = function() {
    // Fast path - if setup is done AND variables are initialized, return true immediately
    if (setupDone && window.bEngine) return true;

    try {
      const context = window.__idleon_cheats__;
      const isReady = !!(
        context &&
        context['com.stencyl.Engine'] &&
        context['com.stencyl.Engine'].engine &&
        context['com.stencyl.Engine'].engine.scene &&
        context['com.stencyl.Engine'].engine.sceneInitialized &&
        context['com.stencyl.Engine'].engine.behaviors.behaviors[0].script._CloudLoadComplete === 1
      );
      
      // If game is ready but setup isn't done, we need to register variables first
      if (isReady && !setupDone) {
        console.log('[core.js] Game detected as ready via legacy check, but setup not complete');
        // Don't auto-mark as done here since variables might not be registered
      }
      
      return isReady && setupDone && window.bEngine;
    } catch (e) {
      return false;
    }
  };

  if (!window.__plugin_results__) {
    window.__plugin_results__ = {};
  }

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
      
      window.__plugin_results__[callId] = { type: 'plugin_result', callId, result };
      
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

  function checkForContext() {
    if (window.__idleon_cheats__ && !setupDone) {
      console.log('[core.js] Context detected, running auto-setup...');
      setup().catch(error => {
        console.error('[core.js] Auto-setup failed:', error);
      });
    } else if (!window.__idleon_cheats__) {
      setTimeout(checkForContext, 1000);
    }
  }

  setTimeout(checkForContext, 100);

  console.log('[core.js] Core initialization script loaded');
})();