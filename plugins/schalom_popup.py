from plugin_system import PluginBase, plugin_command, js_export


class SchalomPopupPlugin(PluginBase):
    
    """Show a beautiful Schalom popup on screen!"""
    VERSION = "1.0.0"
    DESCRIPTION = "Show a beautiful Schalom popup on screen!"

    def __init__(self, config=None):
        super().__init__(config or {})
        self.injector = None
        self.debug = self.config.get('debug', True)
        self.name = self.__class__.__name__

    async def initialize(self, injector) -> bool:
        self.injector = injector
        self.counter = 0
        return True

    async def cleanup(self) -> None:
        pass

    async def update(self) -> None:
        self.debug = self.config.get('debug', True)
        self.counter += 1
        self.injector.evaluate(f"console.log('{self.name} counter: {self.counter}')")

    @js_export(params=["text"])
    def schalom_popup_js(self, text="Schalom! Popup from plugin!"):
        """JS: Show a popup with the given text."""
        return f'''
        console.log("[schalom_popup_js] text:", text);
        let div = document.createElement('div');
        div.innerHTML = '<div style="font-size:2em;padding:2em;background:#fff3;border:2px solid #aaf;border-radius:1em;box-shadow:0 0 1em #00f8;">' + text + '</div>';
        div.style.position = 'fixed';
        div.style.top = '30%';
        div.style.left = '30%';
        div.style.zIndex = 99999;
        document.body.appendChild(div);
        setTimeout(()=>div.remove(), 3000);
        return 'Popup shown!';
        '''

    @plugin_command(
        help="Show a beautiful Schalom popup in the game.",
        params=[
            {"name": "text", "type": str, "default": "Schalom! Popup from plugin!", "help": "Popup text to show."}
        ]
    )
    async def schalom_popup(self, text, injector=None, **kwargs):
        """Python: Show a popup in the game via JS injection."""
        return self.run_js_export('schalom_popup_js', injector, text=text)

    @js_export(params=["text", "count", "value"])
    def schalom_greet_js(self, text="Schalom! Greeting from plugin in browser console.", count=1, value=3.14):
        """JS: Print a greeting in the browser console with custom text, count, and value."""
        return f'''
        console.log("[schalom_greet_js] text:", text);
        console.log("[schalom_greet_js] count:", count);
        console.log("[schalom_greet_js] value:", value);
        return `Greeting: ${text} (x${count}, value=${value})`;
        '''

    @plugin_command(
        help="Print a custom Schalom greeting from the plugin.",
        params=[
            {"name": "text", "type": str, "default": "Schalom! This is a greeting from the SchalomPopup plugin.", "help": "Greeting text to print."},
            {"name": "count", "type": int, "default": 1, "help": "How many times to repeat the greeting."},
            {"name": "value", "type": float, "default": 3.14, "help": "A float value to show in the greeting."}
        ]
    )
    async def schalom_greet(self, text, count=1, value=3.14, injector=None, **kwargs):
        """Python: Print a custom greeting via JS injection."""
        return self.run_js_export('schalom_greet_js', injector, text=text, count=count, value=value)

plugin_class = SchalomPopupPlugin 