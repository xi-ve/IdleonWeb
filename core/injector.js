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
        this.timeout = this.injectorConfig.timeout || 120_000;
        this.profileInitTimeout = this.injectorConfig.profile_init_timeout || 5000;
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
            // Support brave
            'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe',
            'C:/Program Files (x86)/BraveSoftware/Brave-Browser/Application/brave.exe',
            'C:/Users/' + process.env.USERNAME + '/AppData/Local/BraveSoftware/Brave-Browser/Application/brave.exe',
            // Brave on linux
            '/usr/bin/brave',
            // Support OperaGX
            'C:/Users/' + process.env.USERNAME + '/AppData/Local/Programs/Opera GX/opera.exe',
            'C:/Program Files/Opera GX/opera.exe',
            'C:/Program Files (x86)/Opera GX/opera.exe',
            // OperaGX on linux
            '/usr/bin/opera-gx',
            '/usr/bin/opera',
            '/snap/bin/opera',
            // OperaGX on macOS
            '/Applications/Opera GX.app/Contents/MacOS/Opera GX'
        ];
        this.userDataDir = path.join(process.cwd(), 'idleon-chromium-profile');
    }

    findChromiumPath() {
        // Check if a specific browser path is configured
        if (this.config.browser && this.config.browser.path && fs.existsSync(this.config.browser.path)) {
            console.log(`[Injector] Using configured browser path: ${this.config.browser.path}`);
            return this.config.browser.path;
        }
        
        // Check if a specific browser name is configured
        if (this.config.browser && this.config.browser.name && this.config.browser.name !== 'auto') {
            const browserName = this.config.browser.name.toLowerCase();
            const filteredPaths = this.possibleChromiumPaths.filter(p => {
                const pathLower = p.toLowerCase();
                return pathLower.includes(browserName);
            });
            
            for (const p of filteredPaths) {
                if (fs.existsSync(p)) {
                    console.log(`[Injector] Using configured browser: ${browserName} at ${p}`);
                    return p;
                }
            }
        }
        
        // Fall back to auto-detection
        for (const p of this.possibleChromiumPaths) {
            if (fs.existsSync(p)) {
                console.log(`[Injector] Auto-detected browser: ${p}`);
                return p;
            }
        }
        throw new Error("Could not find Chromium/Chrome executable. Please install Chromium or Google Chrome.");
    }

    isProfileNew() {
        if (!fs.existsSync(this.userDataDir)) {
            return true;
        }
        
        const profileIndicators = [
            path.join(this.userDataDir, 'Default', 'Preferences'),
            path.join(this.userDataDir, 'Default', 'Cookies'),
            path.join(this.userDataDir, 'Default', 'Login Data')
        ];
        
        return !profileIndicators.some(file => fs.existsSync(file));
    }

    async initializeProfile() {
        if (!this.isProfileNew()) {
            console.log('[Injector] Chrome profile already exists and initialized.');
            return;
        }

        console.log('[Injector] Fresh Chrome profile detected. Initializing profile for login...');
        
        const chromiumCmd = this.findChromiumPath();
        const args = [
            `--remote-debugging-port=${this.config.cdpPort}`,
            `--user-data-dir=${this.userDataDir}`,
            '--no-first-run',
            '--no-default-browser-check',
            '--remote-allow-origins=*',
        ];
        
        if (process.platform === 'linux') {
            args.push('--disable-gpu');
        }
        
        args.push(this.config.idleonUrl);
        
        console.log('[Injector] Opening browser for profile initialization...');
        const initProcess = spawn(chromiumCmd, args, { detached: true, stdio: 'ignore' });
        
        console.log(`[Injector] Waiting ${this.config.profileInitTimeout/1000} seconds for profile initialization...`);
        await new Promise(resolve => setTimeout(resolve, this.config.profileInitTimeout));
        
        console.log('[Injector] Closing initialization browser via CDP...');
        try {
            await new Promise((resolve, reject) => {
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
                    if (Date.now() - start > 10000) {
                        reject(new Error('CDP not available for browser close'));
                    } else {
                        setTimeout(check, 200);
                    }
                };
                check();
            });
            
            const CDP = require('chrome-remote-interface');
            const targets = await CDP.List({ port: this.config.cdpPort });
            
            for (const target of targets) {
                if (target.type === 'page') {
                    try {
                        const client = await CDP({ target, port: this.config.cdpPort });
                        await client.Browser.close();
                        await client.close();
                        console.log('[Injector] Browser closed via CDP');
                        break;
                    } catch (e) {
                    }
                }
            }
            
            try {
                const browserTarget = targets.find(t => t.type === 'browser');
                if (browserTarget) {
                    const client = await CDP({ target: browserTarget, port: this.config.cdpPort });
                    await client.Browser.close();
                    await client.close();
                    console.log('[Injector] Browser closed via CDP (browser target)');
                }
            } catch (e) {
                console.log('[Injector] CDP browser close failed, trying fallback...');
                if (process.platform === 'win32') {
                    exec('taskkill /F /IM chrome.exe /T', () => {});
                    exec('taskkill /F /IM chromium.exe /T', () => {});
                } else {
                    exec('pkill -f "chrome.*--remote-debugging-port=' + this.config.cdpPort + '"', () => {});
                }
            }
            
        } catch (error) {
            console.log('[Injector] Error during CDP browser close:', error.message);
            if (process.platform === 'win32') {
                exec('taskkill /F /IM chrome.exe /T', () => {});
                exec('taskkill /F /IM chromium.exe /T', () => {});
            } else {
                exec('pkill -f "chrome.*--remote-debugging-port=' + this.config.cdpPort + '"', () => {});
            }
        }
        
        console.log('[Injector] Profile initialization complete. Starting actual injection...');
        
        await new Promise(resolve => setTimeout(resolve, 2000));
    }

    launch() {
        const chromiumCmd = this.findChromiumPath();
        const args = [
            `--remote-debugging-port=${this.config.cdpPort}`,
            `--user-data-dir=${this.userDataDir}`,
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

    async waitForCDP(timeout = null) {
        const actualTimeout = timeout || this.config.timeout || 120_000;
        console.log('[Injector] Waiting for Chrome to initialize...');
        
        return new Promise((resolve, reject) => {
            const start = Date.now();
            let attempt = 0;
            const maxAttempts = 50;
            
            const check = () => {
                attempt++;
                const elapsed = Date.now() - start;
                
                require('http').get(`http://localhost:${this.config.cdpPort}/json/version`, res => {
                    let data = '';
                    res.on('data', chunk => data += chunk);
                    res.on('end', () => {
                        try {
                            const json = JSON.parse(data);
                            if (json.webSocketDebuggerUrl) {
                                console.log(`[Injector] Chrome ready after ${elapsed}ms (${attempt} attempts)`);
                                resolve();
                                return;
                            }
                        } catch (e) {
                        }
                        retry();
                    });
                }).on('error', retry);
            };
            
            const retry = () => {
                if (Date.now() - start > actualTimeout) {
                    reject(new Error(`Timeout waiting for CDP endpoint after ${actualTimeout/1000} seconds`));
                } else if (attempt >= maxAttempts) {
                    reject(new Error(`Maximum attempts (${maxAttempts}) reached waiting for Chrome initialization`));
                } else {
                    // Exponential backoff: start with 100ms, max 2000ms
                    const baseDelay = 350;
                    const maxDelay = 2000;
                    const delay = Math.min(baseDelay * Math.pow(1.5, attempt), maxDelay);
                    
                    setTimeout(check, delay);
                }
            };
            check();
        });
    }

    async connect() {
        const connectionTimeout = this.config.timeout || 120_000;
        
        const tabs = await Promise.race([
            CDP.List({ port: this.config.cdpPort }),
            new Promise((_, reject) => 
                setTimeout(() => reject(new Error(`CDP connection timeout after ${connectionTimeout/1000} seconds`)), connectionTimeout)
            )
        ]);
        
        this.tab = tabs[0];
        this.client = await Promise.race([
            CDP({ target: this.tab, port: this.config.cdpPort }),
            new Promise((_, reject) => 
                setTimeout(() => reject(new Error(`CDP client connection timeout after ${connectionTimeout/1000} seconds`)), connectionTimeout)
            )
        ]);
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

                        const contentLength = Buffer.byteLength(injected, 'utf-8');
                        const headers = [
                            `Date: ${(new Date()).toUTCString()}`,
                            "Connection: close",
                            `Content-Length: ${contentLength}`,
                            "Content-Type: application/javascript; charset=utf-8",
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
                
                const contextTimeout = this.cdpManager.config.timeout || 120_000;
                const maxIterations = Math.ceil(contextTimeout / 1000);
                const startTime = Date.now();
                
                for (let i = 0; i < maxIterations; ++i) {
                    if (Date.now() - startTime > contextTimeout) {
                        console.error(`[Injector] ERROR: Could not find __idleon_cheats__ context after ${contextTimeout/1000} seconds.`);
                        process.exit(1);
                    }
                    
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
                    console.error(`[Injector] ERROR: Could not find __idleon_cheats__ context after ${contextTimeout/1000} seconds.`);
                    process.exit(1);
                }

                console.log("[Injector] Waiting for game to be fully ready...");
                try {
                    const gameReadyTimeout = this.cdpManager.config.timeout || 120_000;
                    await Promise.race([
                        this.cdpManager.client.Runtime.evaluate({ 
                            expression: `await window.__idleon_wait_for_game_ready()`, 
                            awaitPromise: true 
                        }),
                        new Promise((_, reject) => 
                            setTimeout(() => reject(new Error(`Game ready timeout after ${gameReadyTimeout/1000} seconds`)), gameReadyTimeout)
                        )
                    ]);
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
            
            await this.browserLauncher.initializeProfile();
            
            this.browserLauncher.launch();
            await this.cdpManager.waitForCDP(this.configManager.timeout);
            
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