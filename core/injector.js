// Idleon Injector - streamlined and organized

const { spawn, exec } = require('child_process');
const CDP = require('chrome-remote-interface');
const fs = require('fs');
const os = require('os');
const path = require('path');
const _ = require('lodash');

// --- Load Configuration ---
const confPath = path.join(__dirname, 'conf.json');
let config = {};
if (fs.existsSync(confPath)) {
  config = JSON.parse(fs.readFileSync(confPath, 'utf-8'));
  if (typeof config.interactive === 'undefined') config.interactive = false;
  console.log('[Injector] Loaded config from conf.json:', config);
} else {
  console.warn('[Injector] conf.json not found, using default config.');
  config = { injectFiles: ['test.js'], openDevTools: false, interactive: false };
}

// --- Constants ---
const CDP_PORT = 32123;
const NJS_PATTERN = '*N.js';
const IDLEON_URL = 'https://www.legendsofidleon.com/ytGl5oc/';

// --- Helper Functions ---
function openUrl(url) {
  const platform = process.platform;
  if (platform === 'win32') {
    exec(`start "" "${url}"`);
  } else if (platform === 'darwin') {
    exec(`open "${url}"`);
  } else {
    exec(`xdg-open "${url}"`);
  }
}

function launchChromiumWithIdleon() {
  const possibleChromiumPaths = [
    '/usr/bin/chromium',
    '/usr/bin/chromium-browser',
    '/usr/bin/google-chrome',
    '/usr/bin/google-chrome-stable',
    '/usr/bin/chrome',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    'C:/Program Files/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  ];
  let chromiumCmd = null;
  for (const p of possibleChromiumPaths) {
    if (fs.existsSync(p)) {
      chromiumCmd = p;
      break;
    }
  }
  if (!chromiumCmd) {
    console.error("Could not find Chromium/Chrome executable. Please install Chromium or Google Chrome.");
    process.exit(1);
  }
  const userDataDir = path.join(os.tmpdir(), 'idleon-chromium-profile');
  const args = [
    `--remote-debugging-port=${CDP_PORT}`,
    `--user-data-dir=${userDataDir}`,
    '--no-first-run',
    '--no-default-browser-check',
    '--remote-allow-origins=*',
  ];
  if (process.platform === 'linux') {
    args.push('--disable-gpu');
  }
  args.push(IDLEON_URL);
  console.log(`[Injector] Launching Chromium with Idleon at ${IDLEON_URL} ...`);
  spawn(chromiumCmd, args, { detached: true, stdio: 'inherit' });
}

function waitForCDP(timeout = 60_000) {
  return new Promise((resolve, reject) => {
    const start = Date.now();
    function check() {
      require('http').get(`http://localhost:${CDP_PORT}/json/version`, res => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            const json = JSON.parse(data);
            if (json.webSocketDebuggerUrl) {
              resolve();
              return;
            }
          } catch {}
          retry();
        });
      }).on('error', retry);
    }
    function retry() {
      if (Date.now() - start > timeout) {
        reject(new Error('Timeout waiting for CDP endpoint'));
      } else {
        setTimeout(check, 500);
      }
    }
    check();
  });
}

// --- Main Injector Logic ---
(async () => {
  try {
    console.log('[Injector] Starting main logic...');
    launchChromiumWithIdleon();
    await waitForCDP();

    const tabs = await CDP.List({ port: CDP_PORT });
    const tab = tabs[0];
    const client = await CDP({ target: tab, port: CDP_PORT });
    const { Network, Runtime, Page } = client;

    // Open DevTools if requested
    if (config.openDevTools) {
      const devtoolsUrl = `http://localhost:${CDP_PORT}/devtools/inspector.html?ws=localhost:${CDP_PORT}/devtools/page/${tab.id}`;
      console.log(`[Injector] Opening DevTools: ${devtoolsUrl}`);
      openUrl(devtoolsUrl);
    }

    await Network.enable();
    await Runtime.enable();
    await Page.enable();
    await Page.setBypassCSP({ enabled: true });

    // Enable console logging like main.js does
    Runtime.consoleAPICalled((entry) => {
      console.log('[Game Console]', entry.args.map(arg => arg.value).join(" "));
    });

    Network.setRequestInterception({
      patterns: [{
        urlPattern: NJS_PATTERN,
        resourceType: 'Script',
        interceptionStage: 'HeadersReceived'
      }]
    });
 
    await Page.reload({ ignoreCache: true });
    let intercepted = false;
    Network.requestIntercepted(async ({ interceptionId, request }) => {
      try {
        console.log(`[Injector] Intercepted request: ${request.url}`);
        if (!intercepted && request.url.endsWith('N.js')) {
          intercepted = true;
          console.log(`[Injector] Intercepting and modifying: ${request.url}`);
          const response = await Network.getResponseBodyForInterception({ interceptionId });
          const originalBody = Buffer.from(response.body, 'base64').toString();
          
          // Inject global object using the same pattern as main.js
          const injreg = /\w+\.ApplicationMain\s*?=/;
          const match = injreg.exec(originalBody);
          if (!match) {
            console.error("Injection regex did not match.");
            await Network.continueInterceptedRequest({ interceptionId });
            return;
          }
          const varName = match[0].split('.')[0];
          let injected = originalBody.replace(match[0], `window.__idleon_cheats__=${varName};${match[0]}`);

          // Prepend plugin JS code directly into N.js
          let pluginJsCode = '';
          const pluginJsPath = path.join(__dirname, 'plugins_combined.js');
          if (fs.existsSync(pluginJsPath)) {
            pluginJsCode = fs.readFileSync(pluginJsPath, 'utf-8');
            console.log(`[Injector] Prepending plugin JS from: ${pluginJsPath}`);
          }
          
          // Also prepend core.js for game readiness detection
          const corePath = path.join(__dirname, 'core.js');
          if (fs.existsSync(corePath)) {
            const coreCode = fs.readFileSync(corePath, 'utf-8');
            pluginJsCode = coreCode + '\n' + pluginJsCode;
            console.log(`[Injector] Prepending core.js for game readiness`);
          }
          
          injected = pluginJsCode + '\n' + injected;

          // Serve modified JS
          const headers = [
            `Date: ${(new Date()).toUTCString()}`,
            "Connection: closed",
            `Content-Length: ${injected.length}`,
            "Content-Type: text/javascript",
          ];
          const rawResponse = Buffer.from(
            "HTTP/1.1 200 OK\r\n" +
            headers.join('\r\n') +
            "\r\n\r\n" +
            injected
          ).toString('base64');
          await Network.continueInterceptedRequest({
            interceptionId,
            rawResponse
          });
          console.log("[Injector] Served modified JS to game (with plugin JS prepended).");
        } else {
          // Always continue all other requests
          await Network.continueInterceptedRequest({ interceptionId });
        }
      } catch (err) {
        console.error("Error in requestIntercepted handler:", err);
        await Network.continueInterceptedRequest({ interceptionId });
      }
    });

    // Wait for interception to complete
    while (!intercepted) {
      await new Promise(r => setTimeout(r, 500));
    }

    // Wait for the page to be fully loaded - CRITICAL FIX
    let pageLoaded = false;
    Page.loadEventFired(async () => {
      console.log("[Injector] Page load event fired. Waiting for game context...");
      
      let contextReady = false;
      let contextExpr = "window.__idleon_cheats__";
      
      // Wait for context in main window first
      for (let i = 0; i < 60; ++i) {
        let res = await client.Runtime.evaluate({ expression: `typeof ${contextExpr} === 'object'`, returnByValue: true });
        if (res.result && res.result.value) {
          contextReady = true;
          console.log("[Injector] Found context in main window");
          break;
        }
        
        // CRITICAL: Check iframe context like main.js does
        res = await client.Runtime.evaluate({ 
          expression: "typeof window.document.querySelector('iframe')?.contentWindow?.__idleon_cheats__ === 'object'", 
          returnByValue: true 
        });
        if (res.result && res.result.value) {
          contextExpr = "window.document.querySelector('iframe').contentWindow.__idleon_cheats__";
          contextReady = true;
          console.log("[Injector] Found context in iframe");
          break;
        }
        await new Promise(r => setTimeout(r, 1000));
      }
      
      if (!contextReady) {
        console.error("[Injector] ERROR: Could not find __idleon_cheats__ context after page load.");
        process.exit(1);
      }

      // CRITICAL FIX: Wait for game to be ready using the same approach as main.js
      console.log("[Injector] Waiting for game to be fully ready...");
      try {
        // Use the __idleon_wait_for_game_ready function from core.js
        await client.Runtime.evaluate({ 
          expression: `await window.__idleon_wait_for_game_ready()`, 
          awaitPromise: true 
        });
        console.log("[Injector] Game is ready!");
        
        // Now inject plugins into the correct context
        const pluginJsPath = path.join(__dirname, 'plugins_combined.js');
        if (fs.existsSync(pluginJsPath)) {
          const code = fs.readFileSync(pluginJsPath, 'utf-8');
          console.log("[Injector] Injecting plugins into game context...");
          
          // CRITICAL: Inject into the correct context (iframe if needed)
          let injectExpression;
          if (contextExpr.includes('iframe')) {
            // Inject into iframe context
            injectExpression = `
              (function() {
                const iframe = window.document.querySelector('iframe');
                if (iframe && iframe.contentWindow) {
                  iframe.contentWindow.eval(\`${code.replace(/`/g, '\\`').replace(/\$/g, '\\$')}\`);
                  return 'Injected into iframe context';
                } else {
                  return 'Error: iframe not found';
                }
              })()
            `;
          } else {
            // Inject into main window context
            injectExpression = code;
          }
          
          await client.Runtime.evaluate({ 
            expression: injectExpression, 
            allowUnsafeEvalBlockedByCSP: true 
          });
          console.log("[Injector] Plugins injected successfully.");
        }
        
      } catch (gameReadyError) {
        console.error("[Injector] Error waiting for game ready:", gameReadyError);
      }
      
      pageLoaded = true;
    });
    
    // Wait for page load event
    while (!pageLoaded) {
      await new Promise(r => setTimeout(r, 500));
    }

    console.log('[Injector] Injection complete. Keeping process alive for interaction...');
    
    // Keep process alive instead of exiting immediately
       
    // Give a moment for any final logging, then exit cleanly
    setTimeout(() => {
      process.exit(0);
    }, 2000);
    
  } catch (err) {
    console.error('[Injector] Uncaught error:', err && err.stack ? err.stack : err);
    process.stderr.write('\n');
    process.exit(1);
  }
})();