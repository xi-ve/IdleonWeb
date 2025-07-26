"""
Web UI package for IdleonWeb.

This package contains all web UI related functionality including:
- Web UI generator for plugin interfaces
- Web API integration for handling UI actions
- HTML file storage and management
"""

from .web_ui_generator import WebUIGenerator
from .web_api_integration import PluginWebAPI

__all__ = ['WebUIGenerator', 'PluginWebAPI'] 