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
    
    if (setupDone && window.bEngine) {
      return true;
    }
    
    while (
      !context["com.stencyl.Engine"] ||
      !context["com.stencyl.Engine"].hasOwnProperty("engine") ||
      !context["com.stencyl.Engine"].engine.hasOwnProperty("scene") ||
      !context["com.stencyl.Engine"].engine.sceneInitialized ||
      context["com.stencyl.Engine"].engine.behaviors.behaviors[0].script._CloudLoadComplete !== 1
    ) {
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
  }

  async function setup() {
    if (setupDone && window.bEngine) return "Core setup already complete";
    
    try {
      const context = window.__idleon_cheats__;
      if (!context) {
        throw new Error("__idleon_cheats__ context not found");
      }

      await gameReady.call(context);
      
      setupDone = true;
      
      return "Core setup complete - game is ready";
    } catch (error) {
      console.error('[core.js] Setup failed:', error);
      setupDone = false;
      throw error;
    }
  }

  window.__idleon_core_setup = setup;

  function getGameContext() {
    if (window.__idleon_cheats__) return window.__idleon_cheats__;
    const iframes = Array.from(window.document.querySelectorAll('iframe'));
    for (const f of iframes) {
      try {
        if (f && f.contentWindow && f.contentWindow.__idleon_cheats__) return f.contentWindow.__idleon_cheats__;
      } catch (_) {}
    }
    return null;
  }

  window.__idleon_wait_for_game_ready = function() {
    if (gameReadyPromise) {
      return gameReadyPromise;
    }

    if (setupDone && window.bEngine) {
      return Promise.resolve();
    }

    gameReadyPromise = new Promise(async (resolve, reject) => {
      try {

        const context = getGameContext();
        if (!context) throw new Error("Could not find __idleon_cheats__ context");

        await gameReady.call(context);
        
        setupDone = true;
        gameReadyPromise = null;
        
        console.log('[core.js] Game is fully ready!');
        resolve();
      } catch (error) {

        gameReadyPromise = null;
        setupDone = false;
        
        reject(error);
      }
    });

    return gameReadyPromise;
  };

  window.__idleon_is_game_ready = function() {
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
      
      if (isReady && !setupDone) {
        console.log('[core.js] Game detected as ready via legacy check, but setup not complete');
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