import pychrome
import time
from config_manager import config_manager

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