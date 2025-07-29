import pychrome
import time
from config_manager import config_manager
from pathlib import Path

class PyInjector:
    def __init__(self, port=None):
        # Get port from config or use default
        if port is None:
            port = config_manager.get_path('injector.cdp_port', 32123)
        self.browser = pychrome.Browser(url=f"http://127.0.0.1:{port}")
        self.tab = None

    def connect(self, wait_timeout=10):
        start = time.time()
        while True:
            tabs = self.browser.list_tab()
            if tabs:
                self.tab = tabs[0]
                self.tab.start()
                self.tab.call_method("Page.enable")
                self.tab.call_method("Runtime.enable")
                return
            if time.time() - start > wait_timeout:
                raise RuntimeError("No tabs found in browser after waiting.")
            time.sleep(0.5)

    def evaluate(self, expression, awaitPromise=False):
        if not self.tab:
            raise RuntimeError("No tab connected")
        return self.tab.call_method("Runtime.evaluate", expression=expression, awaitPromise=awaitPromise)

    def reload_js(self):
        """Re-inject the combined plugin JS into the browser."""
        if not self.tab:
            raise RuntimeError("No tab connected")
        
        try:
            # Read the combined JS file
            js_path = Path(__file__).parent / "plugins_combined.js"
            if not js_path.exists():
                raise RuntimeError("plugins_combined.js not found")
            
            with open(js_path, 'r', encoding='utf-8') as f:
                js_code = f.read()
            
            from config_manager import config_manager
            debug_enabled = config_manager.get_path('debug', False)
            
            if debug_enabled:
                print(f"[DEBUG] Injecting {len(js_code)} characters of JS code...")
            
            # Check if we need to inject into iframe or main window
            check_iframe = self.evaluate("typeof window.document.querySelector('iframe')?.contentWindow?.__idleon_cheats__ === 'object'")
            if check_iframe.get('result', {}).get('value', False):
                # Inject into iframe context
                if debug_enabled:
                    print(f"[DEBUG] Injecting into iframe context...")
                # Escape the JS code for iframe injection
                escaped_js = js_code.replace('`', '\\`').replace('$', '\\$')
                inject_expression = f"""
                (function() {{
                    const iframe = window.document.querySelector('iframe');
                    if (iframe && iframe.contentWindow) {{
                        iframe.contentWindow.eval(`{escaped_js}`);
                        return 'Injected into iframe context';
                    }} else {{
                        return 'Error: iframe not found';
                    }}
                }})()
                """
            else:
                # Inject into main window context
                if debug_enabled:
                    print(f"[DEBUG] Injecting into main window context...")
                inject_expression = js_code
            
            # Evaluate the JS code in the browser
            result = self.evaluate(inject_expression, awaitPromise=False)
            
            if result.get('exceptionDetails'):
                raise RuntimeError(f"JS injection failed: {result['exceptionDetails']}")
            
            if debug_enabled:
                print(f"[DEBUG] JS injection successful")
            return True
        except Exception as e:
            if debug_enabled:
                print(f"[DEBUG] JS injection failed: {e}")
            raise RuntimeError(f"Failed to reload JS: {e}") 