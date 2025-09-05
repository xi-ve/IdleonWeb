import sys
import warnings
import logging

logging.getLogger('websocket').setLevel(logging.CRITICAL)
logging.getLogger('pychrome').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*JSONDecodeError.*")
warnings.filterwarnings("ignore", message=".*Expecting value.*")

def suppress_websocket_errors():
    original_stderr = sys.stderr
    
    class WebsocketErrorFilter:
        def __init__(self, original):
            self.original = original
            
        def write(self, message):
            if "JSONDecodeError" in message and "Expecting value" in message:
                return
            if "Exception in thread" in message and "_recv_loop" in message:
                return
            if "json.decoder.JSONDecodeError" in message:
                return
            if "Traceback" in message and "_recv_loop" in message:
                return
            self.original.write(message)
            
        def flush(self):
            self.original.flush()
            
        def __getattr__(self, name):
            return getattr(self.original, name)
    
    sys.stderr = WebsocketErrorFilter(original_stderr)

suppress_websocket_errors()

import threading
original_excepthook = threading.excepthook

def custom_excepthook(args):
    if hasattr(args, 'exc_value') and args.exc_value:
        exc_type = type(args.exc_value).__name__
        exc_msg = str(args.exc_value)
        
        if exc_type == 'JSONDecodeError' and 'Expecting value' in exc_msg:
            return
        if '_recv_loop' in str(args.thread):
            return
    
    original_excepthook(args)

threading.excepthook = custom_excepthook

import customtkinter as ctk
from tkinter import messagebox, scrolledtext, font, filedialog
import threading
import webbrowser
import subprocess
import os
import time
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any

sys.path.append(str(Path(__file__).parent))

from config_manager import config_manager
from plugin_system import PluginManager
from core.py_injector import PyInjector
from webui.web_api_integration import PluginWebAPI

class IdleonWebGUI:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("IdleonWeb")
        self.root.geometry("900x600")
        self.root.minsize(700, 500)
        
        self.root.attributes('-type', 'dialog')
        self.root.attributes('-topmost', False)
        
        self.plugin_manager: Optional[PluginManager] = None
        self.injector: Optional[PyInjector] = None
        self.web_server_task: Optional[threading.Thread] = None
        self.update_loop_task: Optional[threading.Thread] = None
        self.update_loop_stop = threading.Event()
        
        self.injection_status = "disconnected"
        self.browser_status = "not_detected"
        self.webui_status = "stopped"
        self.plugin_count = 0
        self.disconnect_popup_shown = False
        
        self.injection_in_progress = False
        
        self.create_widgets()
        
        self.load_plugins()
        
        self.start_status_monitor()
        
        self.update_button_states()
        
        if config_manager.get_auto_inject():
            self.root.after(2000, self.auto_inject)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=8, pady=8)
        
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", pady=(0, 8))
        
        title_label = ctk.CTkLabel(header_frame, text="IdleonWeb", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(side="left", padx=12, pady=8)
        
        status_frame = ctk.CTkFrame(header_frame)
        status_frame.pack(side="right", padx=12, pady=8)
        
        self.browser_status_indicator = self.create_compact_status_indicator(status_frame, "Browser", "not_detected")
        self.injection_status_indicator = self.create_compact_status_indicator(status_frame, "Injection", "disconnected")
        self.webui_status_indicator = self.create_compact_status_indicator(status_frame, "Web UI", "stopped")
        
        self.notebook = ctk.CTkTabview(main_frame)
        self.notebook.pack(fill="both", expand=True)
        
        self.create_control_tab()
        self.create_config_tab()
        self.create_plugins_tab()
        self.create_logs_tab()
    
    def create_compact_status_indicator(self, parent, label, status):
        frame = ctk.CTkFrame(parent)
        frame.pack(side="right", padx=4)
        
        dot = ctk.CTkCanvas(frame, width=8, height=8, highlightthickness=0)
        dot.pack(side="left", padx=(4, 2), pady=4)
        
        status_label = ctk.CTkLabel(frame, text=f"{label}: {status.title()}", font=ctk.CTkFont(size=10))
        status_label.pack(side="left", padx=(0, 4), pady=4)
        
        colors = {
            "running": "#4CAF50",
            "connected": "#4CAF50", 
            "detected": "#4CAF50",
            "stopped": "#F44336",
            "disconnected": "#F44336",
            "not_detected": "#F44336",
            "loading": "#FF9800",
            "reloading": "#FF9800",
            "error": "#F44336"
        }
        
        color = colors.get(status, "#9E9E9E")
        dot.create_oval(1, 1, 7, 7, fill=color, outline="")
        
        return {"frame": frame, "dot": dot, "label": status_label}
    
    def update_status_indicator(self, indicator, new_status):
        current_text = indicator["label"].cget("text")
        label_name = current_text.split(":")[0]
        indicator["label"].configure(text=f"{label_name}: {new_status.title()}")
        
        dot = indicator["dot"]
        dot.delete("all")
        
        colors = {
            "running": "#4CAF50",
            "connected": "#4CAF50", 
            "detected": "#4CAF50",
            "stopped": "#F44336",
            "disconnected": "#F44336",
            "not_detected": "#F44336",
            "loading": "#FF9800",
            "reloading": "#FF9800",
            "error": "#F44336"
        }
        
        color = colors.get(new_status, "#9E9E9E")
        dot.create_oval(1, 1, 7, 7, fill=color, outline="")
    
    def create_control_tab(self):
        control_frame = self.notebook.add("Control")
        
        injection_frame = ctk.CTkFrame(control_frame)
        injection_frame.pack(side="left", fill="both", expand=True, padx=(0, 6))
        
        self.injection_status_label = ctk.CTkLabel(injection_frame, text="Status: Disconnected", font=ctk.CTkFont(size=12, weight="bold"))
        self.injection_status_label.pack(pady=(12, 8), padx=12, anchor="w")
        
        self.inject_button = ctk.CTkButton(injection_frame, text="Start Injection", command=self.start_injection)
        self.inject_button.pack(fill="x", pady=(0, 4), padx=12)
        
        self.stop_injection_button = ctk.CTkButton(injection_frame, text="Stop Injection", command=self.stop_injection)
        self.stop_injection_button.pack(fill="x", pady=(0, 4), padx=12)
        
        self.reload_injection_button = ctk.CTkButton(injection_frame, text="Reload Injection", command=self.reload_injection)
        self.reload_injection_button.pack(fill="x", pady=(0, 8), padx=12)
        
        browser_info_frame = ctk.CTkFrame(injection_frame)
        browser_info_frame.pack(fill="x", pady=(8, 0), padx=12)
        
        browser_title = ctk.CTkLabel(browser_info_frame, text="Browser", font=ctk.CTkFont(size=11, weight="bold"))
        browser_title.pack(pady=(8, 4), padx=8, anchor="w")
        
        browser_name_frame = ctk.CTkFrame(browser_info_frame)
        browser_name_frame.pack(fill="x", pady=(0, 2), padx=8)
        
        ctk.CTkLabel(browser_name_frame, text="Name:").pack(side="left", padx=(0, 8))
        self.browser_name_label = ctk.CTkLabel(browser_name_frame, text="Auto")
        self.browser_name_label.pack(side="left")
        
        browser_path_frame = ctk.CTkFrame(browser_info_frame)
        browser_path_frame.pack(fill="x", pady=(0, 8), padx=8)
        
        ctk.CTkLabel(browser_path_frame, text="Path:").pack(side="left", padx=(0, 8))
        self.browser_path_label = ctk.CTkLabel(browser_path_frame, text="Not configured")
        self.browser_path_label.pack(side="left")
        
        plugins_info_frame = ctk.CTkFrame(injection_frame)
        plugins_info_frame.pack(fill="x", pady=(8, 12), padx=12)
        
        plugins_title = ctk.CTkLabel(plugins_info_frame, text="Plugins", font=ctk.CTkFont(size=11, weight="bold"))
        plugins_title.pack(pady=(8, 4), padx=8, anchor="w")
        
        plugins_count_frame = ctk.CTkFrame(plugins_info_frame)
        plugins_count_frame.pack(fill="x", pady=(0, 8), padx=8)
        
        ctk.CTkLabel(plugins_count_frame, text="Loaded:").pack(side="left", padx=(0, 8))
        self.plugin_count_label = ctk.CTkLabel(plugins_count_frame, text="0")
        self.plugin_count_label.pack(side="left")
        
        reload_plugins_button = ctk.CTkButton(plugins_info_frame, text="Reload All", command=self.reload_plugins)
        reload_plugins_button.pack(pady=(0, 8), padx=8)
        
        webui_frame = ctk.CTkFrame(control_frame)
        webui_frame.pack(side="right", fill="both", expand=True)
        
        self.webui_status_label = ctk.CTkLabel(webui_frame, text="Status: Stopped", font=ctk.CTkFont(size=12, weight="bold"))
        self.webui_status_label.pack(pady=(12, 8), padx=12, anchor="w")
        
        
        self.open_webui_button = ctk.CTkButton(webui_frame, text="Open in Target Browser", command=self.open_webui)
        self.open_webui_button.pack(fill="x", pady=(0, 8), padx=12)
        
        webui_info_frame = ctk.CTkFrame(webui_frame)
        webui_info_frame.pack(fill="x", pady=(8, 12), padx=12)
        
        webui_title = ctk.CTkLabel(webui_info_frame, text="Info", font=ctk.CTkFont(size=11, weight="bold"))
        webui_title.pack(pady=(8, 4), padx=8, anchor="w")
        
        webui_url_frame = ctk.CTkFrame(webui_info_frame)
        webui_url_frame.pack(fill="x", pady=(0, 2), padx=8)
        
        ctk.CTkLabel(webui_url_frame, text="URL:").pack(side="left", padx=(0, 8))
        self.webui_url_label = ctk.CTkLabel(webui_url_frame, text="http://localhost:8080")
        self.webui_url_label.pack(side="left")
        
        webui_port_frame = ctk.CTkFrame(webui_info_frame)
        webui_port_frame.pack(fill="x", pady=(0, 8), padx=8)
        
        ctk.CTkLabel(webui_port_frame, text="Port:").pack(side="left", padx=(0, 8))
        self.webui_port_label = ctk.CTkLabel(webui_port_frame, text="8080")
        self.webui_port_label.pack(side="left")
    
    def bind_mousewheel_to_scrollable(self, scrollable_widget, parent_frame=None):
        def _on_mousewheel(event):
            try:
                canvas = scrollable_widget._parent_canvas
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass
        
        def _on_mousewheel_linux(event):
            try:
                canvas = scrollable_widget._parent_canvas
                if event.num == 4:
                    canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    canvas.yview_scroll(1, "units")
            except:
                pass
        
        def bind_mousewheel_to_widget(widget):
            widget.bind("<MouseWheel>", _on_mousewheel)
            widget.bind("<Button-4>", _on_mousewheel_linux)
            widget.bind("<Button-5>", _on_mousewheel_linux)
        
        def bind_mousewheel_recursive(widget):
            bind_mousewheel_to_widget(widget)
            for child in widget.winfo_children():
                bind_mousewheel_recursive(child)
        
        bind_mousewheel_to_widget(scrollable_widget)
        if parent_frame:
            bind_mousewheel_to_widget(parent_frame)
            bind_mousewheel_recursive(parent_frame)
    
    def create_config_tab(self):
        config_frame = self.notebook.add("Config")
        
        scrollable_frame = ctk.CTkScrollableFrame(config_frame)
        scrollable_frame.pack(fill="both", expand=True, padx=8, pady=8)
        
        system_frame = ctk.CTkFrame(scrollable_frame)
        system_frame.pack(fill="x", pady=(0, 6))
        
        system_title = ctk.CTkLabel(system_frame, text="System Settings", font=ctk.CTkFont(size=14, weight="bold"))
        system_title.pack(pady=(12, 8), padx=12, anchor="w")
        
        self.auto_inject_var = ctk.BooleanVar(value=config_manager.get_auto_inject())
        auto_inject_checkbox = ctk.CTkCheckBox(system_frame, text="Auto-inject on startup", variable=self.auto_inject_var, command=self.update_auto_inject)
        auto_inject_checkbox.pack(pady=(0, 4), padx=12, anchor="w")
        
        self.gui_enabled_var = ctk.BooleanVar(value=config_manager.get_gui_enabled())
        gui_enabled_checkbox = ctk.CTkCheckBox(system_frame, text="Enable GUI mode", variable=self.gui_enabled_var, command=self.update_gui_enabled)
        gui_enabled_checkbox.pack(pady=(0, 4), padx=12, anchor="w")
        
        self.debug_var = ctk.BooleanVar(value=config_manager.get_path('debug', False))
        debug_checkbox = ctk.CTkCheckBox(system_frame, text="Debug mode", variable=self.debug_var, command=self.update_debug)
        debug_checkbox.pack(pady=(0, 12), padx=12, anchor="w")
        
        webui_frame = ctk.CTkFrame(scrollable_frame)
        webui_frame.pack(fill="x", pady=6)
        
        webui_title = ctk.CTkLabel(webui_frame, text="Web UI Settings", font=ctk.CTkFont(size=14, weight="bold"))
        webui_title.pack(pady=(12, 8), padx=12, anchor="w")
        
        port_frame = ctk.CTkFrame(webui_frame)
        port_frame.pack(fill="x", pady=(0, 4), padx=12)
        
        ctk.CTkLabel(port_frame, text="Port:").pack(side="left", padx=(0, 8))
        self.webui_port_entry = ctk.CTkEntry(port_frame, width=100)
        self.webui_port_entry.pack(side="left", padx=(0, 8))
        self.webui_port_entry.insert(0, str(config_manager.get_webui_port()))
        
        port_button = ctk.CTkButton(port_frame, text="Update", command=self.update_webui_port, width=80)
        port_button.pack(side="left")
        
        self.webui_auto_open_var = ctk.BooleanVar(value=config_manager.get_webui_auto_open())
        webui_auto_open_checkbox = ctk.CTkCheckBox(webui_frame, text="Auto-open Web UI after injection", variable=self.webui_auto_open_var, command=self.update_webui_auto_open)
        webui_auto_open_checkbox.pack(pady=(0, 12), padx=12, anchor="w")
        
        browser_frame = ctk.CTkFrame(scrollable_frame)
        browser_frame.pack(fill="x", pady=6)
        
        browser_title = ctk.CTkLabel(browser_frame, text="Browser Settings", font=ctk.CTkFont(size=14, weight="bold"))
        browser_title.pack(pady=(12, 8), padx=12, anchor="w")
        
        browser_name_frame = ctk.CTkFrame(browser_frame)
        browser_name_frame.pack(fill="x", pady=(0, 4), padx=12)
        
        ctk.CTkLabel(browser_name_frame, text="Browser:").pack(side="left", padx=(0, 8))
        self.browser_name_combo = ctk.CTkComboBox(browser_name_frame, values=["auto", "chrome", "chromium", "edge", "brave", "operagx"], width=120)
        self.browser_name_combo.pack(side="left", padx=(0, 8))
        self.browser_name_combo.set(config_manager.get_browser_name())
        
        browser_name_button = ctk.CTkButton(browser_name_frame, text="Update", command=self.update_browser_name, width=80)
        browser_name_button.pack(side="left")
        
        browser_path_frame = ctk.CTkFrame(browser_frame)
        browser_path_frame.pack(fill="x", pady=(0, 4), padx=12)
        
        ctk.CTkLabel(browser_path_frame, text="Path:").pack(side="left", padx=(0, 8))
        self.browser_path_entry = ctk.CTkEntry(browser_path_frame, width=300)
        self.browser_path_entry.pack(side="left", padx=(0, 8), fill="x", expand=True)
        self.browser_path_entry.insert(0, config_manager.get_browser_path() or "")
        
        browser_path_button = ctk.CTkButton(browser_path_frame, text="Browse", command=self.browse_browser_path, width=80)
        browser_path_button.pack(side="left", padx=(0, 4))
        
        auto_detect_button = ctk.CTkButton(browser_path_frame, text="Auto-detect", command=self.auto_detect_browser, width=80)
        auto_detect_button.pack(side="left")
        
        browser_path_button.pack(pady=(0, 12), padx=12)
        
        injector_frame = ctk.CTkFrame(scrollable_frame)
        injector_frame.pack(fill="x", pady=6)
        
        injector_title = ctk.CTkLabel(injector_frame, text="Injector Settings", font=ctk.CTkFont(size=14, weight="bold"))
        injector_title.pack(pady=(12, 8), padx=12, anchor="w")
        
        timeout_frame = ctk.CTkFrame(injector_frame)
        timeout_frame.pack(fill="x", pady=(0, 4), padx=12)
        
        ctk.CTkLabel(timeout_frame, text="Timeout (ms):").pack(side="left", padx=(0, 8))
        self.injector_timeout_entry = ctk.CTkEntry(timeout_frame, width=120)
        self.injector_timeout_entry.pack(side="left", padx=(0, 8))
        self.injector_timeout_entry.insert(0, str(config_manager.get_timeout()))
        
        timeout_button = ctk.CTkButton(timeout_frame, text="Update", command=self.update_injector_timeout, width=80)
        timeout_button.pack(side="left")
        
        timeout_button.pack(pady=(0, 12), padx=12)
        
        self.bind_mousewheel_to_scrollable(scrollable_frame, config_frame)
    
    def create_plugins_tab(self):
        plugins_frame = self.notebook.add("Plugins")
        
        plugins_list_frame = ctk.CTkFrame(plugins_frame)
        plugins_list_frame.pack(fill="both", expand=True, padx=12, pady=12)
        
        plugins_title = ctk.CTkLabel(plugins_list_frame, text="Loaded Plugins Overview", font=ctk.CTkFont(size=14, weight="bold"))
        plugins_title.pack(pady=(12, 8), padx=12, anchor="w")
        
        self.plugin_tree = ctk.CTkScrollableFrame(plugins_list_frame)
        self.plugin_tree.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        
        self.bind_mousewheel_to_scrollable(self.plugin_tree, plugins_frame)
    
    def create_logs_tab(self):
        logs_frame = self.notebook.add("Logs")
        
        self.log_text = scrolledtext.ScrolledText(logs_frame, height=20, bg='#1e1e1e', fg='#ffffff', insertbackground='#ffffff')
        self.log_text.pack(fill="both", expand=True, padx=12, pady=12)
        
        self.log_text.tag_configure("success", foreground="#4CAF50")
        self.log_text.tag_configure("error", foreground="#F44336")
        self.log_text.tag_configure("warning", foreground="#FF9800")
        self.log_text.tag_configure("info", foreground="#2196F3")
        
        def _on_mousewheel_logs(event):
            try:
                self.log_text.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass
        
        def _on_mousewheel_logs_linux(event):
            try:
                if event.num == 4:
                    self.log_text.yview_scroll(-1, "units")
                elif event.num == 5:
                    self.log_text.yview_scroll(1, "units")
            except:
                pass
        
        def bind_mousewheel_to_widget(widget):
            widget.bind("<MouseWheel>", _on_mousewheel_logs)
            widget.bind("<Button-4>", _on_mousewheel_logs_linux)
            widget.bind("<Button-5>", _on_mousewheel_logs_linux)
        
        def bind_mousewheel_recursive(widget):
            bind_mousewheel_to_widget(widget)
            for child in widget.winfo_children():
                bind_mousewheel_recursive(child)
        
        bind_mousewheel_to_widget(self.log_text)
        bind_mousewheel_to_widget(logs_frame)
        bind_mousewheel_recursive(logs_frame)
    
    def log_message(self, message: str, level: str = "info"):
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert("end", log_entry)
        self.log_text.see("end")
        
        start_index = f"end-{len(log_entry)}c"
        self.log_text.tag_add(level, start_index, "end-1c")
    
    def show_disconnect_popup(self, reason: str = "unknown"):
        popup = ctk.CTkToplevel(self.root)
        popup.title("Tab Disconnected")
        popup.geometry("400x200")
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()
        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 400) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 200) // 2
        popup.geometry(f"400x200+{x}+{y}")
        try: popup.attributes("-type", "dialog")
        except Exception: pass
        popup.attributes("-topmost", True)

        main = ctk.CTkFrame(popup)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(main, text="Tab Disconnected",
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 10))

        if reason == "reloaded":
            msg = "The Idleon tab was reloaded and needs full re-injection to restore functionality."
        elif reason == "closed":
            msg = "The Idleon tab was closed and needs full re-injection to restore functionality."
        else:
            msg = "The Idleon tab was disconnected and needs full re-injection to restore functionality."

        ctk.CTkLabel(main, text=msg, font=ctk.CTkFont(size=12), wraplength=350).pack(pady=(0, 20))

        btns = ctk.CTkFrame(main)
        btns.pack(fill="x")
        btns.grid_columnconfigure((0, 1), weight=1, uniform="b")

        inject = ctk.CTkButton(btns, text="Start Injection",
                            command=lambda: self.start_injection_from_popup(popup),
                            height=36, corner_radius=8)
        close = ctk.CTkButton(btns, text="Close", command=popup.destroy,
                            height=36, corner_radius=8)

        inject.grid(row=0, column=0, sticky="ew", padx=(10, 5), pady=10)
        close.grid(row=0, column=1, sticky="ew", padx=(5, 10), pady=10)

    def start_injection_from_popup(self, popup):
        popup.destroy()
        self.start_injection()
    
    def start_status_monitor(self):
        def monitor():
            while True:
                try:
                    browser_name = config_manager.get_browser_name()
                    browser_path = config_manager.get_browser_path()
                    
                    if browser_path and os.path.exists(browser_path):
                        if self.browser_status != "detected":
                            self.update_status_indicator(self.browser_status_indicator, "detected")
                            self.browser_status = "detected"
                    else:
                        if self.browser_status != "not_detected":
                            self.update_status_indicator(self.browser_status_indicator, "not_detected")
                            self.browser_status = "not_detected"
                    
                    if self.injection_status not in ["loading", "reloading"]:
                        import main
                        global_injector = getattr(main, 'injector', None)
                        
                        if self.injector and global_injector:
                            try:
                                self.injector.evaluate("1+1")
                                if self.injection_status != "connected":
                                    self.update_status_indicator(self.injection_status_indicator, "connected")
                                    self.injection_status = "connected"
                            except Exception:
                                if self.injection_status != "disconnected":
                                    tab_reload_detected = getattr(main, '_tab_reload_disconnected', False)
                                    reason = "reloaded" if tab_reload_detected else "closed"
                                    
                                    self.log_message("Tab disconnected", "warning")
                                    self.update_status_indicator(self.injection_status_indicator, "disconnected")
                                    self.injection_status = "disconnected"
                                    
                                    if not self.disconnect_popup_shown:
                                        self.disconnect_popup_shown = True
                                        self.root.after(100, lambda: self.show_disconnect_popup(reason))
                                    
                                    try:
                                        if self.injector:
                                            self.injector.close_browser()
                                    except Exception as e:
                                        self.log_message(f"Error closing browser: {e}", "error")
                                    self.injector = None
                                    main.injector = None
                        else:
                            if self.injection_status != "disconnected":
                                tab_reload_detected = getattr(main, '_tab_reload_disconnected', False)
                                reason = "reloaded" if tab_reload_detected else "closed"
                                
                                self.log_message("Tab disconnected", "warning")
                                self.update_status_indicator(self.injection_status_indicator, "disconnected")
                                self.injection_status = "disconnected"
                                
                                if not self.disconnect_popup_shown:
                                    self.disconnect_popup_shown = True
                                    self.root.after(100, lambda: self.show_disconnect_popup(reason))
                                
                                try:
                                    if self.injector:
                                        self.injector.close_browser()
                                except Exception as e:
                                    self.log_message(f"Error closing browser: {e}", "error")
                                self.injector = None
                                main.injector = None
                    
                    try:
                        import urllib.request
                        webui_port = config_manager.get_webui_port()
                        webui_url = f"http://localhost:{webui_port}"
                        urllib.request.urlopen(webui_url, timeout=1)
                        if self.webui_status != "running":
                            self.update_status_indicator(self.webui_status_indicator, "running")
                            self.webui_status = "running"
                    except:
                        if self.webui_status != "stopped":
                            self.update_status_indicator(self.webui_status_indicator, "stopped")
                            self.webui_status = "stopped"
                    
                    self.update_ui_labels()
                    self.update_button_states()
                    
                except Exception as e:
                    self.log_message(f"Status monitor error: {e}", "error")
                
                time.sleep(2)
        
        threading.Thread(target=monitor, daemon=True).start()
    
    def update_ui_labels(self):
        try:
            browser_name = config_manager.get_browser_name()
            browser_path = config_manager.get_browser_path()
            self.browser_name_label.configure(text=browser_name.title())
            self.browser_path_label.configure(text=browser_path or "Not configured")
            
            webui_port = config_manager.get_webui_port()
            webui_url = f"http://localhost:{webui_port}"
            self.webui_url_label.configure(text=webui_url)
            self.webui_port_label.configure(text=str(webui_port))
            
            if self.plugin_manager:
                plugin_count = len(self.plugin_manager.plugins)
                self.plugin_count_label.configure(text=str(plugin_count))
                self.plugin_count = plugin_count
            
            self.injection_status_label.configure(text=f"Status: {self.injection_status.title()}")
            self.webui_status_label.configure(text=f"Status: {self.webui_status.title()}")
            
        except Exception as e:
            self.log_message(f"UI update error: {e}", "error")
    
    def update_button_states(self):
        try:
            if self.injection_in_progress:
                self.inject_button.configure(state='disabled')
                self.stop_injection_button.configure(state='disabled')
                self.reload_injection_button.configure(state='disabled')
                self.open_webui_button.configure(state='disabled')
            else:
                self.inject_button.configure(state='disabled' if self.injector else 'normal')
                self.stop_injection_button.configure(state='normal' if self.injector else 'disabled')
                self.reload_injection_button.configure(state='normal' if self.injector else 'disabled')
                self.open_webui_button.configure(state='normal' if self.injector else 'disabled')
        except Exception as e:
            self.log_message(f"Button state update error: {e}", "error")
    
    def start_injection(self):
        def inject():
            try:
                if not self.plugin_manager:
                    self.log_message("No plugin manager available", "error")
                    return
                    
                self.injection_in_progress = True
                self.update_button_states()
                
                self.log_message("Starting game injection...")
                self.update_status_indicator(self.injection_status_indicator, "loading")
                
                from main import cmd_inject
                cmd_inject(plugin_manager=self.plugin_manager)
                
                import main
                self.injector = main.injector
                self.web_server_task = main.web_server_task
                
                if self.injector:
                    self.log_message("Game injection successful!", "success")
                    self.injection_status = "connected"
                    self.update_status_indicator(self.injection_status_indicator, "connected")
                    self.disconnect_popup_shown = False
                    
                    if config_manager.get_webui_auto_open():
                        webui_url = config_manager.get_webui_url_from_port()
                        self.log_message(f"Auto-opening Web UI at {webui_url}")
                        try:
                            time.sleep(1)
                            self.injector.open_url_in_new_tab(webui_url)
                            self.log_message("Web UI opened in target browser", "success")
                        except Exception as e:
                            self.log_message(f"Could not open Web UI automatically: {e}", "warning")
                            self.log_message(f"You can open it manually at {webui_url}")
                else:
                    self.log_message("Game injection failed - could not connect to browser", "error")
                    self.injection_status = "error"
                    self.update_status_indicator(self.injection_status_indicator, "error")
                
            except Exception as e:
                self.log_message(f"Injection failed: {e}", "error")
                self.injection_status = "error"
                self.update_status_indicator(self.injection_status_indicator, "error")
            finally:
                self.injection_in_progress = False
                self.update_button_states()
        
        threading.Thread(target=inject, daemon=True).start()
    
    def stop_injection(self):
        try:
            if self.injector:
                from main import cmd_stop_injection
                cmd_stop_injection(plugin_manager=self.plugin_manager)
                
                self.injector = None
                import main
                main.injector = None
                main.injector_process = None
                
                self.log_message("Injection stopped and browser closed")
                self.update_status_indicator(self.injection_status_indicator, "disconnected")
                self.injection_status = "disconnected"
                self.update_button_states()
            else:
                self.log_message("No active injection to stop", "warning")
        except Exception as e:
            self.log_message(f"Error stopping injection: {e}", "error")
    
    def reload_injection(self):
        def reload():
            try:
                if not self.plugin_manager:
                    self.log_message("No plugin manager available", "error")
                    return
                    
                self.injection_in_progress = True
                self.update_button_states()
                
                self.log_message("Reloading injection...")
                self.update_status_indicator(self.injection_status_indicator, "reloading")
                self.injection_status = "reloading"
                
                from main import cmd_reload
                cmd_reload(plugin_manager=self.plugin_manager)
                
                import main
                self.injector = main.injector
                self.web_server_task = main.web_server_task
                
                self.log_message("Injection reloaded successfully!", "success")
                self.update_status_indicator(self.injection_status_indicator, "connected")
                self.injection_status = "connected"
                
            except Exception as e:
                self.log_message(f"Reload failed: {e}", "error")
                self.update_status_indicator(self.injection_status_indicator, "error")
                self.injection_status = "error"
            finally:
                self.injection_in_progress = False
                self.update_button_states()
        
        threading.Thread(target=reload, daemon=True).start()
    
    
    def open_webui(self):
        try:
            if not self.injector:
                self.log_message("No active injection - cannot open Web UI in target browser", "error")
                return
                
            webui_url = config_manager.get_webui_url_from_port()
            self.log_message(f"Opening Web UI at {webui_url} in target browser...")
            
            self.injector.open_url_in_new_tab(webui_url)
            self.log_message("Web UI opened in target browser", "success")
        except Exception as e:
            self.log_message(f"Failed to open Web UI in target browser: {e}", "error")
            try:
                webui_url = config_manager.get_webui_url_from_port()
                webbrowser.open(webui_url)
                self.log_message(f"Opened Web UI in system browser at {webui_url}", "warning")
            except Exception as e2:
                self.log_message(f"Failed to open Web UI in system browser: {e2}", "error")
    
    def load_plugins(self):
        try:
            self.log_message("Loading plugins...")
            plugin_names = config_manager.get_path('plugins', [])
            plugin_configs = config_manager.get_path('plugin_configs', {})
            plugins_dir = Path(__file__).parent / 'plugins'
            
            self.plugin_manager = PluginManager(plugin_names, plugin_dir=str(plugins_dir))
            asyncio.run(self.plugin_manager.load_plugins(
                None, 
                plugin_configs=plugin_configs, 
                global_debug=config_manager.get_path('debug', False)
            ))
            self.log_message(f"Loaded {len(self.plugin_manager.plugins)} plugins", "success")
            self.refresh_plugin_list()
            
            self.start_webui_automatically()
        except Exception as e:
            self.log_message(f"Failed to load plugins: {e}", "error")
    
    def start_webui_automatically(self):
        def start():
            try:
                self.log_message("Starting Web UI server automatically...")
                self.update_status_indicator(self.webui_status_indicator, "loading")
                
                from main import cmd_web_ui
                cmd_web_ui(plugin_manager=self.plugin_manager)
                
                import main
                self.web_server_task = main.web_server_task
                
                webui_port = config_manager.get_webui_port()
                webui_url = f"http://localhost:{webui_port}"
                self.log_message(f"Web UI started automatically at {webui_url}", "success")
                self.webui_status = "running"
                self.update_status_indicator(self.webui_status_indicator, "running")
                
            except Exception as e:
                self.log_message(f"Failed to start Web UI automatically: {e}", "error")
                self.update_status_indicator(self.webui_status_indicator, "error")
        
        threading.Thread(target=start, daemon=True).start()
    
    def reload_plugins(self):
        try:
            if not self.plugin_manager:
                self.log_message("No plugin manager available", "error")
                return
                
            self.log_message("Reloading plugins...")
            asyncio.run(self.plugin_manager.reload_plugins())
            
            if self.injector:
                from main import cmd_reload
                cmd_reload(plugin_manager=self.plugin_manager)
            
            self.log_message("Plugins reloaded successfully!", "success")
        except Exception as e:
            self.log_message(f"Failed to reload plugins: {e}", "error")
    
    def refresh_plugin_list(self):
        try:
            for widget in self.plugin_tree.winfo_children():
                widget.destroy()
            
            if self.plugin_manager:
                for plugin_name, plugin in self.plugin_manager.plugins.items():
                    plugin_frame = ctk.CTkFrame(self.plugin_tree)
                    plugin_frame.pack(fill="x", pady=2, padx=4)
                    
                    plugin_label = ctk.CTkLabel(plugin_frame, text=plugin_name, font=ctk.CTkFont(size=12, weight="bold"))
                    plugin_label.pack(side="left", padx=8, pady=4)
                    
                    version = getattr(plugin, 'version', '1.0.0')
                    version_label = ctk.CTkLabel(plugin_frame, text=f"v{version}", font=ctk.CTkFont(size=10))
                    version_label.pack(side="right", padx=8, pady=4)
        except Exception as e:
            self.log_message(f"Failed to refresh plugin list: {e}", "error")
    
    
    def auto_inject(self):
        if config_manager.get_auto_inject():
            self.log_message("Auto-inject enabled, starting injection...")
            self.injection_status = "loading"
            self.update_status_indicator(self.injection_status_indicator, "loading")
            self.start_injection()
    
    def update_auto_inject(self):
        config_manager.set_auto_inject(self.auto_inject_var.get())
        self.log_message(f"Auto-inject {'enabled' if self.auto_inject_var.get() else 'disabled'}")
    
    def update_gui_enabled(self):
        config_manager.set_gui_enabled(self.gui_enabled_var.get())
        self.log_message(f"GUI mode {'enabled' if self.gui_enabled_var.get() else 'disabled'}")
    
    def update_debug(self):
        config_manager.set_path('debug', self.debug_var.get())
        self.log_message(f"Debug mode {'enabled' if self.debug_var.get() else 'disabled'}")
    
    def update_webui_port(self):
        try:
            port = int(self.webui_port_entry.get())
            if 1 <= port <= 65535:
                config_manager.set_webui_port(port)
                self.log_message(f"Web UI port updated to {port}")
            else:
                self.log_message("Port must be between 1 and 65535", "error")
        except ValueError:
            self.log_message("Invalid port number", "error")
    
    def update_webui_auto_open(self):
        config_manager.set_webui_auto_open(self.webui_auto_open_var.get())
        self.log_message(f"Web UI auto-open {'enabled' if self.webui_auto_open_var.get() else 'disabled'}")
    
    def update_browser_name(self):
        browser_name = self.browser_name_combo.get()
        config_manager.set_browser_name(browser_name)
        self.log_message(f"Browser name updated to {browser_name}")
    
    def update_browser_path(self):
        browser_path = self.browser_path_entry.get()
        config_manager.set_browser_path(browser_path)
        self.log_message(f"Browser path updated to {browser_path}")
    
    def update_injector_timeout(self):
        try:
            timeout = int(self.injector_timeout_entry.get())
            if timeout < 1000:
                self.log_message("Timeout must be at least 1000ms", "error")
                return
            config_manager.set_injector_config(timeout=timeout)
            self.log_message(f"Injector timeout updated to {timeout}ms")
        except ValueError:
            self.log_message("Invalid timeout value. Please enter a number.", "error")
    
    def browse_browser_path(self):
        file_path = filedialog.askopenfilename(
            title="Select Browser Executable",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        if file_path:
            self.browser_path_entry.delete(0, "end")
            self.browser_path_entry.insert(0, file_path)
            self.update_browser_path()
    
    def auto_detect_browser(self):
        try:
            from main import cmd_browser_detect
            cmd_browser_detect()
            browser_path = config_manager.get_browser_path()
            browser_name = config_manager.get_browser_name()
            
            self.browser_path_entry.delete(0, "end")
            self.browser_path_entry.insert(0, browser_path or "")
            self.browser_name_combo.set(browser_name)
            
            self.log_message(f"Auto-detected browser: {browser_name} at {browser_path}")
        except Exception as e:
            self.log_message(f"Failed to auto-detect browser: {e}", "error")
    
    def on_closing(self):
        try:
            if self.injection_status == "connected" and self.injector:
                self.log_message("Closing browser via CDP before shutdown...")
                try:
                    self.injector.close_browser()
                    self.log_message("Browser closed successfully", "success")
                except Exception as e:
                    self.log_message(f"Error closing browser: {e}", "error")
            
            if self.update_loop_task and self.update_loop_task.is_alive():
                self.update_loop_stop.set()
                self.update_loop_task.join(timeout=2)
            
            if self.plugin_manager:
                asyncio.run(self.plugin_manager.cleanup_all())
            
            self.log_message("Shutting down...")
            
        except Exception as e:
            self.log_message(f"Error during shutdown: {e}", "error")
        
        self.root.destroy()
    
    def run(self):
        self.log_message("IdleonWeb GUI System Manager started", "success")
        self.root.mainloop()

def main():
    try:
        app = IdleonWebGUI()
        app.run()
    except Exception as e:
        print(f"GUI Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":

    main()
