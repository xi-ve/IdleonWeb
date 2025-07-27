const { spawn, exec } = require('child_process');
const CDP = require('chrome-remote-interface');
const fs = require('fs');
const os = require('os');
const path = require('path');
const _ = require('lodash');

class ConfigManager {
    constructor() {
        this.confPath = path.join(__dirname, 'conf.json');
        this.config = this.loadConfig();
        this.injectorConfig = this.config.injector || {};
        this.cdpPort = this.injectorConfig.cdp_port || 32123;
        this.njsPattern = this.injectorConfig.njs_pattern || '*N.js';
        this.idleonUrl = this.injectorConfig.idleon_url || 'https://www.legendsofidleon.com/ytGl5oc/';
    }

    loadConfig() {
        if (fs.existsSync(this.confPath)) {
            const config = JSON.parse(fs.readFileSync(this.confPath, 'utf-8'));
            if (typeof config.interactive === 'undefined') config.interactive = false;
            console.log('[Injector] Loaded config from conf.json:', config);
            return config;
        } else {
            console.warn('[Injector] conf.json not found, using default config.');
            return { openDevTools: false, interactive: false };
        }
    }
}

class BrowserLauncher {
    constructor(config) {
        this.config = config;
        this.possibleChromiumPaths = [
            '/usr/bin/chromium',
            '/usr/bin/chromium-browser',
            '/usr/bin/google-chrome',
            '/usr/bin/google-chrome-stable',
            '/usr/bin/chrome',
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '/Applications/Chromium.app/Contents/MacOS/Chromium',
            'C:/Program Files/Google/Chrome/Application/chrome.exe',
            'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
            'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
            'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
            'C:/Program Files/Chromium/Application/chrome.exe',
            'C:/Program Files (x86)/Chromium/Application/chrome.exe',
            'C:/Users/' + process.env.USERNAME + '/AppData/Local/Google/Chrome/Application/chrome.exe',
            'C:/Users/' + process.env.USERNAME + '/AppData/Local/Microsoft/Edge/Application/msedge.exe',
        ];
    }

    findChromiumPath() {
        for (const p of this.possibleChromiumPaths) {
            if (fs.existsSync(p)) {
                return p;
            }
        }
        throw new Error("Could not find Chromium/Chrome executable. Please install Chromium or Google Chrome.");
    }

    launch() {
        const chromiumCmd = this.findChromiumPath();
        const userDataDir = path.join(process.cwd(), 'idleon-chromium-profile');
        const args = [
            `--remote-debugging-port=${this.config.cdpPort}`,
            `--user-data-dir=${userDataDir}`,
            '--no-first-run',
            '--no-default-browser-check',
            '--remote-allow-origins=*',
        ];
        
        if (process.platform === 'linux') {
            args.push('--disable-gpu');
        }
        
        args.push(this.config.idleonUrl);
        console.log(`[Injector] Launching Chromium with Idleon at ${this.config.idleonUrl} ...`);
        spawn(chromiumCmd, args, { detached: true, stdio: 'inherit' });
    }
}

class CDPManager {
    constructor(config) {
        this.config = config;
        this.client = null;
        this.tab = null;
    }

    async waitForCDP(timeout = 60_000) {
        return new Promise((resolve, reject) => {
            const start = Date.now();
            const check = () => {
                require('http').get(`http://localhost:${this.config.cdpPort}/json/version`, res => {
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
            };
            
            const retry = () => {
                if (Date.now() - start > timeout) {
                    reject(new Error('Timeout waiting for CDP endpoint'));
                } else {
                    setTimeout(check, 500);
                }
            };
            check();
        });
    }

    async connect() {
        const tabs = await CDP.List({ port: this.config.cdpPort });
        this.tab = tabs[0];
        this.client = await CDP({ target: this.tab, port: this.config.cdpPort });
        return this.client;
    }

    async setupNetworkInterception() {
        const { Network, Runtime, Page } = this.client;
        
        await Network.enable();
        await Runtime.enable();
        await Page.enable();
        await Page.setBypassCSP({ enabled: true });

        Runtime.consoleAPICalled((entry) => {
            console.log('[Game Console]', entry.args.map(arg => arg.value).join(" "));
        });

        Network.setRequestInterception({
            patterns: [{
                urlPattern: this.config.njsPattern,
                resourceType: 'Script',
                interceptionStage: 'HeadersReceived'
            }]
        });

        return { Network, Runtime, Page };
    }
}

class ScriptInjector {
    constructor(cdpManager) {
        this.cdpManager = cdpManager;
        this.intercepted = false;
    }

    async injectScripts(Network) {
        return new Promise((resolve) => {
            Network.requestIntercepted(async ({ interceptionId, request }) => {
                try {
                    console.log(`[Injector] Intercepted request: ${request.url}`);
                    if (!this.intercepted && request.url.endsWith('N.js')) {
                        this.intercepted = true;
                        console.log(`[Injector] Intercepting and modifying: ${request.url}`);
                        
                        const response = await Network.getResponseBodyForInterception({ interceptionId });
                        const originalBody = Buffer.from(response.body, 'base64').toString();
                        
                        const injreg = /\w+\.ApplicationMain\s*?=/;
                        const match = injreg.exec(originalBody);
                        if (!match) {
                            console.error("Injection regex did not match.");
                            await Network.continueInterceptedRequest({ interceptionId });
                            return;
                        }
                        
                        const varName = match[0].split('.')[0];
                        let injected = originalBody.replace(match[0], `window.__idleon_cheats__=${varName};${match[0]}`);

                        let pluginJsCode = '';
                        const pluginJsPath = path.join(__dirname, 'plugins_combined.js');
                        if (fs.existsSync(pluginJsPath)) {
                            pluginJsCode = fs.readFileSync(pluginJsPath, 'utf-8');
                            console.log(`[Injector] Prepending plugin JS from: ${pluginJsPath}`);
                        }
                        
                        const corePath = path.join(__dirname, 'core.js');
                        if (fs.existsSync(corePath)) {
                            const coreCode = fs.readFileSync(corePath, 'utf-8');
                            pluginJsCode = coreCode + '\n' + pluginJsCode;
                            console.log(`[Injector] Prepending core.js for game readiness`);
                        }
                        
                        injected = pluginJsCode + '\n' + injected;

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
                        resolve();
                    } else {
                        await Network.continueInterceptedRequest({ interceptionId });
                    }
                } catch (err) {
                    console.error("Error in requestIntercepted handler:", err);
                    await Network.continueInterceptedRequest({ interceptionId });
                }
            });
        });
    }
}

class GameContextManager {
    constructor(cdpManager) {
        this.cdpManager = cdpManager;
        this.pageLoaded = false;
    }

    async waitForPageLoad() {
        return new Promise((resolve) => {
            this.cdpManager.client.Page.loadEventFired(async () => {
                console.log("[Injector] Page load event fired. Waiting for game context...");
                
                let contextReady = false;
                let contextExpr = "window.__idleon_cheats__";
                
                for (let i = 0; i < 60; ++i) {
                    let res = await this.cdpManager.client.Runtime.evaluate({ 
                        expression: `typeof ${contextExpr} === 'object'`, 
                        returnByValue: true 
                    });
                    if (res.result && res.result.value) {
                        contextReady = true;
                        console.log("[Injector] Found context in main window");
                        break;
                    }
                    
                    res = await this.cdpManager.client.Runtime.evaluate({ 
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

                console.log("[Injector] Waiting for game to be fully ready...");
                try {
                    await this.cdpManager.client.Runtime.evaluate({ 
                        expression: `await window.__idleon_wait_for_game_ready()`, 
                        awaitPromise: true 
                    });
                    console.log("[Injector] Game is ready!");
                    
                    const pluginJsPath = path.join(__dirname, 'plugins_combined.js');
                    if (fs.existsSync(pluginJsPath)) {
                        const code = fs.readFileSync(pluginJsPath, 'utf-8');
                        console.log("[Injector] Injecting plugins into game context...");
                        
                        let injectExpression;
                        if (contextExpr.includes('iframe')) {
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
                            injectExpression = code;
                        }
                        
                        await this.cdpManager.client.Runtime.evaluate({ 
                            expression: injectExpression, 
                            allowUnsafeEvalBlockedByCSP: true 
                        });
                        console.log("[Injector] Plugins injected successfully.");
                    }
                    
                } catch (gameReadyError) {
                    console.error("[Injector] Error waiting for game ready:", gameReadyError);
                }
                
                this.pageLoaded = true;
                resolve();
            });
        });
    }
}

class IdleonInjector {
    constructor() {
        this.configManager = new ConfigManager();
        this.browserLauncher = new BrowserLauncher(this.configManager);
        this.cdpManager = new CDPManager(this.configManager);
        this.scriptInjector = new ScriptInjector(this.cdpManager);
        this.gameContextManager = new GameContextManager(this.cdpManager);
    }

    async run() {
        try {
            console.log('[Injector] Starting main logic...');
            
            this.browserLauncher.launch();
            await this.cdpManager.waitForCDP();
            
            const client = await this.cdpManager.connect();
            const { Network, Runtime, Page } = await this.cdpManager.setupNetworkInterception();

            if (this.configManager.config.openDevTools) {
                const devtoolsUrl = `http://localhost:${this.configManager.cdpPort}/devtools/inspector.html?ws=localhost:${this.configManager.cdpPort}/devtools/page/${this.cdpManager.tab.id}`;
                console.log(`[Injector] Opening DevTools: ${devtoolsUrl}`);
                this.openUrl(devtoolsUrl);
            }

            await Page.reload({ ignoreCache: true });
            await this.scriptInjector.injectScripts(Network);
            await this.gameContextManager.waitForPageLoad();

            console.log('[Injector] Injection complete. Keeping process alive for interaction...');
            
            setTimeout(() => {
                process.exit(0);
            }, 2000);
            
        } catch (err) {
            console.error('[Injector] Uncaught error:', err && err.stack ? err.stack : err);
            process.stderr.write('\n');
            process.exit(1);
        }
    }

    openUrl(url) {
        const platform = process.platform;
        if (platform === 'win32') {
            exec(`start "" "${url}"`);
        } else if (platform === 'darwin') {
            exec(`open "${url}"`);
        } else {
            exec(`xdg-open "${url}"`);
        }
    }
}

const injector = new IdleonInjector();
injector.run();