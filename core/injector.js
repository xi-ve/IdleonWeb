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
    args.push('--no-sandbox', '--disable-gpu');
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

    Network.setRequestInterception({
      patterns: [{
        urlPattern: NJS_PATTERN,
        resourceType: 'Script',
        interceptionStage: 'HeadersReceived'
      }]
    });

    await new Promise(r => setTimeout(r, 1000));

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
          // Inject global object
          const injreg = /\w+\.ApplicationMain\s*?=/;
          const match = injreg.exec(originalBody);
          if (!match) {
            console.error("Injection regex did not match.");
            await Network.continueInterceptedRequest({ interceptionId });
            return;
          }
          const varName = match[0].split('.')[0];
          let injected = originalBody.replace(match[0], `window.__idleon_cheats__=${varName};${match[0]}`);

          // --- NEW: Prepend plugin JS code directly into N.js ---
          let pluginJsCode = '';
          const pluginJsPath = path.join(__dirname, 'plugins_combined.js');
          if (fs.existsSync(pluginJsPath)) {
            pluginJsCode = fs.readFileSync(pluginJsPath, 'utf-8');
            console.log(`[Injector] Prepending plugin JS from: ${pluginJsPath}`);
            console.log(`[Injector] Plugin JS code (first 300 chars):\n${pluginJsCode.substring(0, 300)}...`);
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

          // --- Inject JS Files IMMEDIATELY after N.js is served ---
          let injectedCode = '';
          if (fs.existsSync(pluginJsPath)) {
            const code = fs.readFileSync(pluginJsPath, 'utf-8');
            injectedCode += code + '\n';
            console.log(`[Injector] Will inject: plugins_combined.js`);
            console.log(`[Injector] Injecting code from plugins_combined.js:\n${code.substring(0, 200)}...`);
          } else {
            console.warn(`[Injector] Warning: JS file not found: plugins_combined.js`);
          }
          console.log("[Injector] Injecting JS files into game context (after N.js)...");
          await Runtime.evaluate({ expression: injectedCode });
          console.log("[Injector] JS injected successfully (after N.js).");
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

    // Wait for the page to be fully loaded
    let pageLoaded = false;
    Page.loadEventFired(async () => {
      let contextReady = false;
      let contextExpr = "window.__idleon_cheats__";
      for (let i = 0; i < 60; ++i) {
        let res = await client.Runtime.evaluate({ expression: `typeof ${contextExpr} === 'object'`, returnByValue: true });
        if (res.result && res.result.value) {
          contextReady = true;
          break;
        }
        // Try iframe context if not found in main
        res = await client.Runtime.evaluate({ expression: "typeof window.document.querySelector('iframe')?.contentWindow?.__idleon_cheats__ === 'object'", returnByValue: true });
        if (res.result && res.result.value) {
          contextExpr = "window.document.querySelector('iframe').contentWindow.__idleon_cheats__";
          contextReady = true;
          break;
        }
        await new Promise(r => setTimeout(r, 1000));
      }
      if (contextReady) {
        global.gameContext = contextExpr;
        global.cdpClient = client;
        console.log("[Injector] Game context detected and verified.");
      } else {
        console.error("[Injector] ERROR: Could not find __idleon_cheats__ context after page load.");
        process.exit(1);
      }
      pageLoaded = true;
      console.log("[Injector] Page load event fired.");
    });
    while (!pageLoaded) {
      await new Promise(r => setTimeout(r, 500));
    }

    // --- Inject JS Files ---
    let injectedCode = '';
    const pluginJsPath = path.join(__dirname, 'plugins_combined.js');
    if (fs.existsSync(pluginJsPath)) {
      const code = fs.readFileSync(pluginJsPath, 'utf-8');
      injectedCode += code + '\n';
      console.log(`[Injector] Will inject: plugins_combined.js`);
      console.log(`[Injector] Injecting code from plugins_combined.js:\n${code.substring(0, 200)}...`);
    } else {
      console.warn(`[Injector] Warning: JS file not found: plugins_combined.js`);
    }
    console.log("[Injector] Injecting JS files into game context...");
    await Runtime.evaluate({ expression: injectedCode });
    console.log("[Injector] JS injected successfully.");

    // --- Call setup() if present ---
    console.log("[Injector] Calling setup() in game context...");
    await Runtime.evaluate({ expression: `if (typeof setup === 'function') setup.call(${global.gameContext});` });
    console.log("[Injector] setup() called.");

    // --- Exit after injection ---
    console.log('[Injector] Injection complete. Exiting.');
    process.exit(0);
  } catch (err) {
    console.error('[Injector] Uncaught error:', err && err.stack ? err.stack : err);
    process.stderr.write('\n');
    process.exit(1);
  }
})(); 