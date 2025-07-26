import json
from typing import Dict, List, Any
from pathlib import Path

class WebUIGenerator:
    def __init__(self):
        self.css_styles = self._get_css_styles()
        self.js_scripts = self._get_js_scripts()
    
    def _get_css_styles(self) -> str:
        return """
        <style>
        :root {
            --primary-color: #6366f1;
            --primary-hover: #5855eb;
            --secondary-color: #64748b;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --error-color: #ef4444;
            --background: #ffffff;
            --surface: #f8fafc;
            --border: #e2e8f0;
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
            --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--surface);
            color: var(--text-primary);
            line-height: 1.6;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }

        .header {
            background: var(--background);
            border-bottom: 1px solid var(--border);
            padding: 1rem 0;
            margin-bottom: 2rem;
        }

        .header h1 {
            color: var(--text-primary);
            font-size: 1.875rem;
            font-weight: 700;
        }

        .plugin-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 2rem;
        }

        .plugin-card {
            background: var(--background);
            border-radius: 0.75rem;
            border: 1px solid var(--border);
            box-shadow: var(--shadow);
            overflow: hidden;
            transition: all 0.2s ease;
        }

        .plugin-card:hover {
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
        }

        .plugin-header {
            background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
            color: white;
            padding: 1.5rem;
        }

        .plugin-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }

        .plugin-description {
            opacity: 0.9;
            font-size: 0.875rem;
        }

        .plugin-version {
            background: rgba(255, 255, 255, 0.2);
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 500;
            display: inline-block;
            margin-top: 0.5rem;
        }

        .category-section {
            padding: 1.5rem;
            border-bottom: 1px solid var(--border);
        }

        .category-section:last-child {
            border-bottom: none;
        }

        .category-title {
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .ui-element {
            margin-bottom: 1.5rem;
        }

        .ui-element:last-child {
            margin-bottom: 0;
        }

        .element-label {
            display: block;
            font-weight: 500;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
        }

        .element-description {
            font-size: 0.875rem;
            color: var(--text-secondary);
            margin-bottom: 0.75rem;
        }

        .toggle-container {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .toggle-switch {
            position: relative;
            width: 3rem;
            height: 1.5rem;
            background: var(--secondary-color);
            border-radius: 9999px;
            cursor: pointer;
            transition: background 0.2s ease;
        }

        .toggle-switch.active {
            background: var(--success-color);
        }

        .toggle-slider {
            position: absolute;
            top: 0.125rem;
            left: 0.125rem;
            width: 1.25rem;
            height: 1.25rem;
            background: white;
            border-radius: 50%;
            transition: transform 0.2s ease;
        }

        .toggle-switch.active .toggle-slider {
            transform: translateX(1.5rem);
        }

        .slider-container {
            width: 100%;
        }

        .slider {
            width: 100%;
            height: 0.5rem;
            background: var(--border);
            border-radius: 9999px;
            outline: none;
            -webkit-appearance: none;
        }

        .slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 1.25rem;
            height: 1.25rem;
            background: var(--primary-color);
            border-radius: 50%;
            cursor: pointer;
            box-shadow: var(--shadow);
        }

        .slider::-moz-range-thumb {
            width: 1.25rem;
            height: 1.25rem;
            background: var(--primary-color);
            border-radius: 50%;
            cursor: pointer;
            border: none;
            box-shadow: var(--shadow);
        }

        .slider-value {
            font-size: 0.875rem;
            color: var(--text-secondary);
            margin-top: 0.5rem;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.75rem 1.5rem;
            background: var(--primary-color);
            color: white;
            border: none;
            border-radius: 0.5rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            text-decoration: none;
            font-size: 0.875rem;
        }

        .btn:hover {
            background: var(--primary-hover);
            transform: translateY(-1px);
        }

        .btn:active {
            transform: translateY(0);
        }

        .btn-secondary {
            background: var(--secondary-color);
        }

        .btn-secondary:hover {
            background: #475569;
        }

        .input {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid var(--border);
            border-radius: 0.5rem;
            font-size: 0.875rem;
            transition: border-color 0.2s ease;
            background: var(--background);
        }

        .input:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }

        .select {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid var(--border);
            border-radius: 0.5rem;
            font-size: 0.875rem;
            background: var(--background);
            cursor: pointer;
        }

        .select:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }

        .status {
            padding: 0.75rem;
            border-radius: 0.5rem;
            margin-top: 0.75rem;
            font-size: 0.875rem;
        }

        .status.success {
            background: #dcfce7;
            color: #166534;
            border: 1px solid #bbf7d0;
        }

        .status.error {
            background: #fef2f2;
            color: #991b1b;
            border: 1px solid #fecaca;
        }

        .loading {
            display: inline-block;
            width: 1rem;
            height: 1rem;
            border: 2px solid var(--border);
            border-top: 2px solid var(--primary-color);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .input-with-button {
            display: flex;
            gap: 0.5rem;
            align-items: center;
        }

        .input-with-button .input {
            flex: 1;
        }

        .input-with-button .btn {
            flex-shrink: 0;
        }

        .search-with-results {
            width: 100%;
        }

        .search-input {
            display: flex;
            gap: 0.5rem;
            align-items: center;
            margin-bottom: 0.5rem;
        }

        .search-input .input {
            flex: 1;
        }

        .search-input .btn {
            flex-shrink: 0;
        }

        .search-results {
            border: 1px solid var(--border);
            border-radius: 0.5rem;
            background: var(--background);
            max-height: 400px;
            overflow: hidden;
            margin-top: 0.5rem;
        }

        .results-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border);
            background: var(--surface);
            border-radius: 0.5rem 0.5rem 0 0;
        }

        .results-title {
            font-weight: 600;
            color: var(--text);
        }

        .close-btn {
            background: none;
            border: none;
            color: var(--text-muted);
            font-size: 1.5rem;
            cursor: pointer;
            padding: 0;
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            transition: all 0.2s ease;
        }

        .close-btn:hover {
            background: var(--border);
            color: var(--text);
        }

        .results-content {
            max-height: 300px;
            overflow-y: auto;
        }

        .results-list {
            padding: 0.5rem;
        }

        .result-item {
            padding: 0.75rem;
            border-bottom: 1px solid var(--border);
            cursor: pointer;
            transition: background 0.2s ease;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            line-height: 1.4;
        }

        .result-item:hover {
            background: var(--surface);
        }

        .result-item:last-child {
            border-bottom: none;
        }

        .result-item .item-id {
            font-weight: bold;
            color: var(--primary-color);
        }

        .result-item .item-name {
            color: var(--text);
        }

        .autocomplete-input {
            display: flex;
            gap: 0.5rem;
            align-items: center;
        }

        .autocomplete-input .input {
            flex: 1;
        }

        .autocomplete-input .btn {
            flex-shrink: 0;
        }

        .autocomplete-field {
            position: relative;
        }

        .autocomplete-suggestions {
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: var(--background);
            border: 1px solid var(--border);
            border-radius: 0.5rem;
            box-shadow: var(--shadow-lg);
            max-height: 200px;
            overflow-y: auto;
            z-index: 1000;
            display: none;
        }

        .autocomplete-suggestion {
            padding: 0.75rem;
            cursor: pointer;
            border-bottom: 1px solid var(--border);
            transition: background 0.2s ease;
        }

        .autocomplete-suggestion:hover {
            background: var(--surface);
        }

        .autocomplete-suggestion:last-child {
            border-bottom: none;
        }

        .autocomplete-suggestion.highlighted {
            background: var(--primary-color);
            color: white;
        }

        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }
            
            .plugin-grid {
                grid-template-columns: 1fr;
            }

            .input-with-button,
            .search-input {
                flex-direction: column;
                align-items: stretch;
            }

            .input-with-button .btn,
            .search-input .btn {
                width: 100%;
            }
        }
        </style>
        """
    
    def _get_js_scripts(self) -> str:
        return """
        <script>
        class PluginUI {
            constructor() {
                this.executingActions = new Set();
                this.initializeEventListeners();
            }

            initializeEventListeners() {
                document.querySelectorAll('.toggle-switch').forEach(toggle => {
                    toggle.addEventListener('click', (e) => {
                        e.stopPropagation();
                        this.handleToggle(e.target.closest('.ui-element'));
                    });
                });

                document.querySelectorAll('.slider').forEach(slider => {
                    slider.addEventListener('input', (e) => {
                        this.handleSlider(e.target);
                    });
                    slider.addEventListener('change', (e) => {
                        e.stopPropagation();
                        this.handleSliderChange(e.target);
                    });
                });

                document.querySelectorAll('.btn:not(.autocomplete-input .btn):not(.search-input .btn)').forEach(btn => {
                    btn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        this.handleButton(e.target);
                    });
                });

                document.querySelectorAll('.input:not(.autocomplete-field):not(.search-input .input)').forEach(input => {
                    input.addEventListener('change', (e) => {
                        e.stopPropagation();
                        this.handleInput(e.target);
                    });
                });

                document.querySelectorAll('.select').forEach(select => {
                    select.addEventListener('change', (e) => {
                        e.stopPropagation();
                        this.handleSelect(e.target);
                    });
                });

                document.querySelectorAll('.input-with-button .btn').forEach(btn => {
                    btn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        this.handleInputWithButton(e.target);
                    });
                });

                document.querySelectorAll('.search-with-results .btn').forEach(btn => {
                    btn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        this.handleSearchWithResults(e.target);
                    });
                });

                document.querySelectorAll('.close-btn').forEach(btn => {
                    btn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        this.closeSearchResults(e.target);
                    });
                });

                document.querySelectorAll('.autocomplete-input .btn').forEach(btn => {
                    btn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        this.handleAutocompleteInput(e.target);
                    });
                });

                document.querySelectorAll('.autocomplete-field').forEach(input => {
                    input.addEventListener('input', (e) => {
                        this.handleAutocompleteFieldInput(e.target);
                    });
                });
            }

            async handleToggle(element) {
                const actionId = `${element.dataset.pluginName}-${element.dataset.elementName}`;
                if (this.executingActions.has(actionId)) return;
                
                this.executingActions.add(actionId);
                const toggle = element.querySelector('.toggle-switch');
                const elementName = element.dataset.elementName;
                const pluginName = element.dataset.pluginName;
                const value = !toggle.classList.contains('active');
                
                toggle.classList.toggle('active', value);
                this.showStatus(element, 'Updating...', 'loading');
                
                try {
                    const response = await this.executeUIAction(pluginName, elementName, value);
                    this.showStatus(element, response.result || 'Updated successfully', 'success');
                } catch (error) {
                    this.showStatus(element, 'Error: ' + error.message, 'error');
                    toggle.classList.toggle('active', !value);
                } finally {
                    this.executingActions.delete(actionId);
                }
            }

            async handleSlider(slider) {
                const element = slider.closest('.ui-element');
                const valueDisplay = element.querySelector('.slider-value');
                if (valueDisplay) {
                    valueDisplay.textContent = slider.value;
                }
            }

            async handleSliderChange(slider) {
                const element = slider.closest('.ui-element');
                const actionId = `${element.dataset.pluginName}-${element.dataset.elementName}`;
                if (this.executingActions.has(actionId)) return;
                
                this.executingActions.add(actionId);
                const elementName = element.dataset.elementName;
                const pluginName = element.dataset.pluginName;
                const value = parseFloat(slider.value);
                
                this.showStatus(element, 'Updating...', 'loading');
                
                try {
                    const response = await this.executeUIAction(pluginName, elementName, value);
                    this.showStatus(element, response.result || 'Updated successfully', 'success');
                } catch (error) {
                    this.showStatus(element, 'Error: ' + error.message, 'error');
                } finally {
                    this.executingActions.delete(actionId);
                }
            }

            async handleButton(btn) {
                const element = btn.closest('.ui-element');
                const actionId = `${element.dataset.pluginName}-${element.dataset.elementName}`;
                if (this.executingActions.has(actionId)) return;
                
                this.executingActions.add(actionId);
                const elementName = element.dataset.elementName;
                const pluginName = element.dataset.pluginName;
                
                btn.disabled = true;
                btn.innerHTML = '<span class="loading"></span> Executing...';
                
                try {
                    const response = await this.executeUIAction(pluginName, elementName);
                    this.showStatus(element, response.result || 'Action completed', 'success');
                } catch (error) {
                    this.showStatus(element, 'Error: ' + error.message, 'error');
                } finally {
                    btn.disabled = false;
                    btn.textContent = btn.dataset.originalText || 'Execute';
                    this.executingActions.delete(actionId);
                }
            }

            async handleInput(input) {
                const element = input.closest('.ui-element');
                const actionId = `${element.dataset.pluginName}-${element.dataset.elementName}`;
                if (this.executingActions.has(actionId)) return;
                
                this.executingActions.add(actionId);
                const elementName = element.dataset.elementName;
                const pluginName = element.dataset.pluginName;
                const value = input.value;
                
                this.showStatus(element, 'Updating...', 'loading');
                
                try {
                    const response = await this.executeUIAction(pluginName, elementName, value);
                    this.showStatus(element, response.result || 'Updated successfully', 'success');
                } catch (error) {
                    this.showStatus(element, 'Error: ' + error.message, 'error');
                } finally {
                    this.executingActions.delete(actionId);
                }
            }

            async handleSelect(select) {
                const element = select.closest('.ui-element');
                const actionId = `${element.dataset.pluginName}-${element.dataset.elementName}`;
                if (this.executingActions.has(actionId)) return;
                
                this.executingActions.add(actionId);
                const elementName = element.dataset.elementName;
                const pluginName = element.dataset.pluginName;
                const value = select.value;
                
                this.showStatus(element, 'Updating...', 'loading');
                
                try {
                    const response = await this.executeUIAction(pluginName, elementName, value);
                    this.showStatus(element, response.result || 'Updated successfully', 'success');
                } catch (error) {
                    this.showStatus(element, 'Error: ' + error.message, 'error');
                } finally {
                    this.executingActions.delete(actionId);
                }
            }

            async handleInputWithButton(btn) {
                const element = btn.closest('.ui-element');
                const actionId = `${element.dataset.pluginName}-${element.dataset.elementName}`;
                if (this.executingActions.has(actionId)) return;
                
                this.executingActions.add(actionId);
                const elementName = element.dataset.elementName;
                const pluginName = element.dataset.pluginName;
                const input = element.querySelector('.input');
                const value = input.value;
                
                btn.disabled = true;
                btn.innerHTML = '<span class="loading"></span> Executing...';
                
                try {
                    const response = await this.executeUIAction(pluginName, elementName, value);
                    this.showStatus(element, response.result || 'Action completed', 'success');
                } catch (error) {
                    this.showStatus(element, 'Error: ' + error.message, 'error');
                } finally {
                    btn.disabled = false;
                    btn.textContent = btn.dataset.originalText || 'Execute';
                    this.executingActions.delete(actionId);
                }
            }

            async handleSearchWithResults(btn) {
                const element = btn.closest('.ui-element');
                const actionId = `${element.dataset.pluginName}-${element.dataset.elementName}`;
                if (this.executingActions.has(actionId)) return;
                
                this.executingActions.add(actionId);
                const elementName = element.dataset.elementName;
                const pluginName = element.dataset.pluginName;
                const input = element.querySelector('.input');
                const value = input.value;
                const resultsContainer = element.querySelector('.search-results');
                const resultsList = element.querySelector('.results-list');
                
                btn.disabled = true;
                btn.innerHTML = '<span class="loading"></span> Searching...';
                
                try {
                    const response = await this.executeUIAction(pluginName, elementName, value);
                    
                    resultsContainer.style.display = 'block';
                    
                    if (response.result && typeof response.result === 'string') {
                        const formattedResults = this.formatSearchResults(response.result);
                        resultsList.innerHTML = formattedResults;
                    } else {
                        resultsList.innerHTML = '<div class="result-item">No results found</div>';
                    }
                    
                    this.showStatus(element, 'Search completed', 'success');
                } catch (error) {
                    this.showStatus(element, 'Error: ' + error.message, 'error');
                } finally {
                    btn.disabled = false;
                    btn.textContent = btn.dataset.originalText || 'Search';
                    this.executingActions.delete(actionId);
                }
            }

            formatSearchResults(resultText) {
                if (resultText.includes('**All Items**')) {
                    const lines = resultText.split('\n');
                    let formattedHtml = '';
                    
                    for (const line of lines) {
                        if (line.trim() && line.includes('• **') && line.includes('** : ')) {
                            const match = line.match(/• \*\*([^*]+)\*\* : (.+)/);
                            if (match) {
                                const itemId = match[1];
                                const itemName = match[2];
                                formattedHtml += `
                                    <div class="result-item">
                                        <span class="item-id">${itemId}</span>
                                        <span class="item-name"> : ${itemName}</span>
                                    </div>
                                `;
                            } else {
                                formattedHtml += `<div class="result-item">${line}</div>`;
                            }
                        } else if (line.trim() && !line.startsWith('**All Items**')) {
                            formattedHtml += `<div class="result-item">${line}</div>`;
                        }
                    }
                    
                    return formattedHtml;
                } else if (resultText.includes('No items found')) {
                    return `<div class="result-item">${resultText}</div>`;
                } else {
                    return `<div class="result-item">${resultText}</div>`;
                }
            }

            async handleAutocompleteInput(btn) {
                const element = btn.closest('.ui-element');
                const actionId = `${element.dataset.pluginName}-${element.dataset.elementName}`;
                if (this.executingActions.has(actionId)) return;
                
                this.executingActions.add(actionId);
                const elementName = element.dataset.elementName;
                const pluginName = element.dataset.pluginName;
                const input = element.querySelector('.input');
                const value = input.value;
                
                btn.disabled = true;
                btn.innerHTML = '<span class="loading"></span> Executing...';
                
                try {
                    const response = await this.executeUIAction(pluginName, elementName, value);
                    this.showStatus(element, response.result || 'Action completed', 'success');
                } catch (error) {
                    this.showStatus(element, 'Error: ' + error.message, 'error');
                } finally {
                    btn.disabled = false;
                    btn.textContent = btn.dataset.originalText || 'Execute';
                    this.executingActions.delete(actionId);
                }
            }

            async handleAutocompleteFieldInput(input) {
                const element = input.closest('.ui-element');
                const pluginName = element.dataset.pluginName;
                const value = input.value;
                
                clearTimeout(this.autocompleteTimeout);
                this.autocompleteTimeout = setTimeout(async () => {
                    if (value.length < 2) return;
                    
                    try {
                        const response = await fetch('/api/autocomplete', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                plugin_name: pluginName,
                                element_name: element.dataset.elementName,
                                query: value
                            })
                        });
                        
                        if (response.ok) {
                            const suggestions = await response.json();
                            this.updateAutocompleteSuggestions(element, suggestions);
                        }
                    } catch (error) {
                        console.error('Autocomplete error:', error);
                    }
                }, 300);
            }

            updateAutocompleteSuggestions(element, suggestions) {
                const input = element.querySelector('.autocomplete-field');
                const datalist = element.querySelector('datalist');
                
                datalist.innerHTML = '';
                
                suggestions.forEach(suggestion => {
                    const option = document.createElement('option');
                    option.value = suggestion;
                    datalist.appendChild(option);
                });
            }

            async executeUIAction(pluginName, elementName, value = null) {
                const response = await fetch('/api/plugin-ui-action', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        plugin_name: pluginName,
                        element_name: elementName,
                        value: value
                    })
                });
                
                if (!response.ok) {
                    throw new Error('Network error');
                }
                
                return await response.json();
            }

            showStatus(element, message, type) {
                let status = element.querySelector('.status');
                if (!status) {
                    status = document.createElement('div');
                    status.className = 'status';
                    element.appendChild(status);
                }
                
                status.className = `status ${type}`;
                status.innerHTML = type === 'loading' ? 
                    '<span class="loading"></span> ' + message : message;
                
                if (type !== 'loading') {
                    setTimeout(() => {
                        status.remove();
                    }, 3000);
                }
            }

            closeSearchResults(btn) {
                const element = btn.closest('.ui-element');
                const resultsContainer = element.querySelector('.search-results');
                resultsContainer.style.display = 'none';
                resultsContainer.innerHTML = '';
            }
        }

        document.addEventListener('DOMContentLoaded', () => {
            new PluginUI();
        });
        </script>
        """
    
    def generate_ui_html(self, plugin_schemas: Dict[str, Dict[str, Any]]) -> str:
        use_tabs = len(plugin_schemas) > 1
        
        if use_tabs:
            html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Plugin Configuration</title>
                {self.css_styles}
                {self._get_tabbed_css()}
            </head>
            <body>
                <div class="header">
                    <div class="container">
                        <h1>Plugin Configuration</h1>
                    </div>
                </div>
                
                <div class="container">
                    {self._generate_tabbed_interface(plugin_schemas)}
                </div>
                
                {self.js_scripts}
                {self._get_tabbed_js()}
            </body>
            </html>
            """
        else:
            html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Plugin Configuration</title>
                {self.css_styles}
            </head>
            <body>
                <div class="header">
                    <div class="container">
                        <h1>Plugin Configuration</h1>
                    </div>
                </div>
                
                <div class="container">
                    <div class="plugin-grid">
                        {self._generate_plugin_cards(plugin_schemas)}
                    </div>
                </div>
                
                {self.js_scripts}
            </body>
            </html>
            """
        
        return html
    
    def _get_tabbed_css(self) -> str:
        return """
        <style>
        .tab-container {
            background: var(--background);
            border-radius: 0.75rem;
            border: 1px solid var(--border);
            box-shadow: var(--shadow);
            overflow: hidden;
        }

        .tab-header {
            display: flex;
            background: var(--surface);
            border-bottom: 1px solid var(--border);
            overflow-x: auto;
        }

        .tab-button {
            padding: 1rem 1.5rem;
            background: transparent;
            border: none;
            color: var(--text-secondary);
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            white-space: nowrap;
            border-bottom: 2px solid transparent;
        }

        .tab-button:hover {
            color: var(--text-primary);
            background: rgba(99, 102, 241, 0.05);
        }

        .tab-button.active {
            color: var(--primary-color);
            border-bottom-color: var(--primary-color);
            background: var(--background);
        }

        .tab-content {
            display: none;
            padding: 0;
        }

        .tab-content.active {
            display: block;
        }

        .tab-content .plugin-card {
            border: none;
            box-shadow: none;
            border-radius: 0;
        }

        .tab-content .plugin-header {
            border-radius: 0;
        }

        .plugin-info {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
        }

        .plugin-badge {
            background: var(--primary-color);
            color: white;
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
            font-size: 0.75rem;
            font-weight: 500;
        }

        .plugin-count {
            background: var(--secondary-color);
            color: white;
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
            font-size: 0.75rem;
            font-weight: 500;
        }

        @media (max-width: 768px) {
            .tab-header {
                flex-direction: column;
            }
            
            .tab-button {
                text-align: left;
                border-bottom: 1px solid var(--border);
                border-right: none;
            }
            
            .tab-button.active {
                border-bottom-color: var(--primary-color);
                border-right-color: transparent;
            }
        }
        </style>
        """
    
    def _get_tabbed_js(self) -> str:
        return """
        <script>
        class TabManager {
            constructor() {
                this.initializeTabs();
            }

            initializeTabs() {
                const tabButtons = document.querySelectorAll('.tab-button');
                const tabContents = document.querySelectorAll('.tab-content');

                tabButtons.forEach(button => {
                    button.addEventListener('click', () => {
                        const targetTab = button.getAttribute('data-tab');
                        this.switchTab(targetTab);
                    });
                });

                if (tabButtons.length > 0) {
                    this.switchTab(tabButtons[0].getAttribute('data-tab'));
                }
            }

            switchTab(tabName) {
                document.querySelectorAll('.tab-content').forEach(content => {
                    content.classList.remove('active');
                });

                document.querySelectorAll('.tab-button').forEach(button => {
                    button.classList.remove('active');
                });

                const targetContent = document.querySelector(`[data-tab-content="${tabName}"]`);
                if (targetContent) {
                    targetContent.classList.add('active');
                }

                const targetButton = document.querySelector(`[data-tab="${tabName}"]`);
                if (targetButton) {
                    targetButton.classList.add('active');
                }
            }
        }

        document.addEventListener('DOMContentLoaded', () => {
            new TabManager();
        });
        </script>
        """
    
    def _generate_tabbed_interface(self, plugin_schemas: Dict[str, Dict[str, Any]]) -> str:
        tab_headers = ""
        tab_contents = ""
        
        for i, (plugin_name, schema) in enumerate(plugin_schemas.items()):
            plugin_info = schema.get("plugin_info", {})
            categories = schema.get("categories", {})
            
            total_elements = sum(len(elements) for elements in categories.values())
            
            tab_headers += f"""
            <button class="tab-button" data-tab="{plugin_name}">
                <div class="plugin-info">
                    <span class="plugin-badge">{plugin_info.get('name', plugin_name)}</span>
                    <span class="plugin-count">{total_elements} elements</span>
                </div>
            </button>
            """
            
            tab_content = f"""
            <div class="tab-content" data-tab-content="{plugin_name}">
                <div class="plugin-card">
                    <div class="plugin-header">
                        <div class="plugin-title">{plugin_info.get('name', plugin_name)}</div>
                        <div class="plugin-description">{plugin_info.get('description', 'No description')}</div>
                        <div class="plugin-version">v{plugin_info.get('version', '1.0.0')}</div>
                    </div>
                    
                    {self._generate_category_sections(plugin_name, categories)}
                </div>
            </div>
            """
            tab_contents += tab_content
        
        return f"""
        <div class="tab-container">
            <div class="tab-header">
                {tab_headers}
            </div>
            <div class="tab-contents">
                {tab_contents}
            </div>
        </div>
        """
    
    def _generate_plugin_cards(self, plugin_schemas: Dict[str, Dict[str, Any]]) -> str:
        cards_html = ""
        
        for plugin_name, schema in plugin_schemas.items():
            plugin_info = schema.get("plugin_info", {})
            categories = schema.get("categories", {})
            
            card_html = f"""
            <div class="plugin-card">
                <div class="plugin-header">
                    <div class="plugin-title">{plugin_info.get('name', plugin_name)}</div>
                    <div class="plugin-description">{plugin_info.get('description', 'No description')}</div>
                    <div class="plugin-version">v{plugin_info.get('version', '1.0.0')}</div>
                </div>
                
                {self._generate_category_sections(plugin_name, categories)}
            </div>
            """
            cards_html += card_html
        
        return cards_html
    
    def _generate_category_sections(self, plugin_name: str, categories: Dict[str, List[Dict[str, Any]]]) -> str:
        sections_html = ""
        
        for category_name, elements in categories.items():
            section_html = f"""
            <div class="category-section">
                <div class="category-title">
                    {category_name}
                </div>
                
                {self._generate_ui_elements(plugin_name, elements)}
            </div>
            """
            sections_html += section_html
        
        return sections_html
    
    def _generate_ui_elements(self, plugin_name: str, elements: List[Dict[str, Any]]) -> str:
        elements_html = ""
        
        from config_manager import config_manager
        config_manager.reload()
        plugin_config = config_manager.get_plugin_config(plugin_name)
        
        for element in elements:
            element_type = element.get("type", "button")
            element_html = ""
            
            if element_type == "toggle":
                element_html = self._generate_toggle_element(plugin_name, element, plugin_config)
            elif element_type == "slider":
                element_html = self._generate_slider_element(plugin_name, element, plugin_config)
            elif element_type == "button":
                element_html = self._generate_button_element(plugin_name, element)
            elif element_type == "select":
                element_html = self._generate_select_element(plugin_name, element, plugin_config)
            elif element_type == "text_input":
                element_html = self._generate_text_input_element(plugin_name, element, plugin_config)
            elif element_type == "number_input":
                element_html = self._generate_number_input_element(plugin_name, element, plugin_config)
            elif element_type == "input_with_button":
                element_html = self._generate_input_with_button_element(plugin_name, element)
            elif element_type == "search_with_results":
                element_html = self._generate_search_with_results_element(plugin_name, element)
            elif element_type == "autocomplete_input":
                element_html = self._generate_autocomplete_input_element(plugin_name, element)
            else:
                element_html = self._generate_button_element(plugin_name, element)
            
            elements_html += element_html
        
        return elements_html
    
    def _generate_toggle_element(self, plugin_name: str, element: Dict[str, Any], plugin_config: Dict[str, Any]) -> str:
        name = element.get("name", "")
        label = element.get("label", name)
        description = element.get("description", "")
        config_key = element.get("config_key", name)
        default_value = element.get("default_value", False)
        
        current_value = plugin_config.get(config_key, default_value)
        
        return f"""
        <div class="ui-element" data-plugin-name="{plugin_name}" data-config-key="{config_key}" data-element-name="{name}">
            <div class="element-label">{label}</div>
            {f'<div class="element-description">{description}</div>' if description else ''}
            <div class="toggle-container">
                <div class="toggle-switch{' active' if current_value else ''}">
                    <div class="toggle-slider"></div>
                </div>
                <span>{'Enabled' if current_value else 'Disabled'}</span>
            </div>
        </div>
        """
    
    def _generate_slider_element(self, plugin_name: str, element: Dict[str, Any], plugin_config: Dict[str, Any]) -> str:
        name = element.get("name", "")
        label = element.get("label", name)
        description = element.get("description", "")
        config_key = element.get("config_key", name)
        default_value = element.get("default_value", 0)
        min_value = element.get("min_value", 0)
        max_value = element.get("max_value", 100)
        step = element.get("step", 1)
        
        current_value = plugin_config.get(config_key, default_value)
        
        return f"""
        <div class="ui-element" data-plugin-name="{plugin_name}" data-config-key="{config_key}" data-element-name="{name}">
            <div class="element-label">{label}</div>
            {f'<div class="element-description">{description}</div>' if description else ''}
            <div class="slider-container">
                <input type="range" class="slider" 
                       min="{min_value}" max="{max_value}" step="{step}" 
                       value="{current_value}">
                <div class="slider-value">{current_value}</div>
            </div>
        </div>
        """
    
    def _generate_button_element(self, plugin_name: str, element: Dict[str, Any]) -> str:
        name = element.get("name", "")
        label = element.get("label", name)
        description = element.get("description", "")
        
        return f"""
        <div class="ui-element" data-plugin-name="{plugin_name}" data-element-name="{name}">
            <div class="element-label">{label}</div>
            {f'<div class="element-description">{description}</div>' if description else ''}
            <button class="btn" data-original-text="{label}">{label}</button>
        </div>
        """
    
    def _generate_select_element(self, plugin_name: str, element: Dict[str, Any], plugin_config: Dict[str, Any]) -> str:
        name = element.get("name", "")
        label = element.get("label", name)
        description = element.get("description", "")
        config_key = element.get("config_key", name)
        default_value = element.get("default_value", "")
        options = element.get("options", [])
        
        current_value = plugin_config.get(config_key, default_value)
        
        options_html = ""
        for option in options:
            option_label = option.get("label", option.get("value", ""))
            option_value = option.get("value", "")
            selected = "selected" if option_value == current_value else ""
            options_html += f'<option value="{option_value}" {selected}>{option_label}</option>'
        
        return f"""
        <div class="ui-element" data-plugin-name="{plugin_name}" data-config-key="{config_key}" data-element-name="{name}">
            <div class="element-label">{label}</div>
            {f'<div class="element-description">{description}</div>' if description else ''}
            <select class="select">
                {options_html}
            </select>
        </div>
        """
    
    def _generate_text_input_element(self, plugin_name: str, element: Dict[str, Any], plugin_config: Dict[str, Any]) -> str:
        name = element.get("name", "")
        label = element.get("label", name)
        description = element.get("description", "")
        config_key = element.get("config_key", name)
        default_value = element.get("default_value", "")
        placeholder = element.get("placeholder", "")
        required = element.get("required", False)
        
        current_value = plugin_config.get(config_key, default_value)
        
        return f"""
        <div class="ui-element" data-plugin-name="{plugin_name}" data-config-key="{config_key}" data-element-name="{name}">
            <div class="element-label">{label}</div>
            {f'<div class="element-description">{description}</div>' if description else ''}
            <input type="text" class="input" 
                   value="{current_value}" 
                   placeholder="{placeholder}"
                   {'required' if required else ''}>
        </div>
        """
    
    def _generate_number_input_element(self, plugin_name: str, element: Dict[str, Any], plugin_config: Dict[str, Any]) -> str:
        name = element.get("name", "")
        label = element.get("label", name)
        description = element.get("description", "")
        config_key = element.get("config_key", name)
        default_value = element.get("default_value", 0)
        min_value = element.get("min_value")
        max_value = element.get("max_value")
        step = element.get("step", 1)
        
        current_value = plugin_config.get(config_key, default_value)
        
        min_attr = f'min="{min_value}"' if min_value is not None else ""
        max_attr = f'max="{max_value}"' if max_value is not None else ""
        
        return f"""
        <div class="ui-element" data-plugin-name="{plugin_name}" data-config-key="{config_key}" data-element-name="{name}">
            <div class="element-label">{label}</div>
            {f'<div class="element-description">{description}</div>' if description else ''}
            <input type="number" class="input" 
                   value="{current_value}" 
                   step="{step}"
                   {min_attr}
                   {max_attr}>
        </div>
        """

    def _generate_input_with_button_element(self, plugin_name: str, element: Dict[str, Any]) -> str:
        name = element.get("name", "")
        label = element.get("label", name)
        description = element.get("description", "")
        placeholder = element.get("placeholder", "")
        button_text = element.get("button_text", "Execute")
        
        return f"""
        <div class="ui-element" data-plugin-name="{plugin_name}" data-element-name="{name}">
            <div class="element-label">{label}</div>
            {f'<div class="element-description">{description}</div>' if description else ''}
            <div class="input-with-button">
                <input type="text" class="input" placeholder="{placeholder}">
                <button class="btn" data-original-text="{button_text}">{button_text}</button>
            </div>
        </div>
        """

    def _generate_search_with_results_element(self, plugin_name: str, element: Dict[str, Any]) -> str:
        name = element.get("name", "")
        label = element.get("label", name)
        description = element.get("description", "")
        placeholder = element.get("placeholder", "")
        button_text = element.get("button_text", "Search")
        
        return f"""
        <div class="ui-element" data-plugin-name="{plugin_name}" data-element-name="{name}">
            <div class="element-label">{label}</div>
            {f'<div class="element-description">{description}</div>' if description else ''}
            <div class="search-with-results">
                <div class="search-input">
                    <input type="text" class="input" placeholder="{placeholder}">
                    <button class="btn" data-original-text="{button_text}">{button_text}</button>
                </div>
                <div class="search-results" style="display: none;">
                    <div class="results-header">
                        <span class="results-title">Search Results</span>
                        <button class="close-btn" title="Close results">×</button>
                    </div>
                    <div class="results-content">
                        <div class="results-list"></div>
                    </div>
                </div>
            </div>
        </div>
        """

    def _generate_autocomplete_input_element(self, plugin_name: str, element: Dict[str, Any]) -> str:
        name = element.get("name", "")
        label = element.get("label", name)
        description = element.get("description", "")
        placeholder = element.get("placeholder", "")
        button_text = element.get("button_text", "Execute")
        
        return f"""
        <div class="ui-element" data-plugin-name="{plugin_name}" data-element-name="{name}">
            <div class="element-label">{label}</div>
            {f'<div class="element-description">{description}</div>' if description else ''}
            <div class="autocomplete-input">
                <input type="text" class="input autocomplete-field" placeholder="{placeholder}" list="autocomplete-{name}">
                <datalist id="autocomplete-{name}"></datalist>
                <button class="btn" data-original-text="{button_text}">{button_text}</button>
            </div>
        </div>
        """
    
    def save_ui_file(self, plugin_schemas: Dict[str, Dict[str, Any]], output_path: str = "webui/html/plugin_ui.html") -> None:
        html_content = self.generate_ui_html(plugin_schemas)
        
        import os
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Plugin UI saved to: {output_path}")

# Example usage
if __name__ == "__main__":
    # This would be used with actual plugin schemas from the plugin manager
    generator = WebUIGenerator()
    
    # Example schema structure
    example_schemas = {
        "ui_example_plugin": {
            "plugin_info": {
                "name": "UI Example Plugin",
                "description": "Example plugin demonstrating UI element decorators",
                "version": "1.0.0"
            },
            "categories": {
                "General Settings": [
                    {
                        "name": "enable_debug",
                        "type": "toggle",
                        "label": "Enable Debug Mode",
                        "description": "Enable debug logging for this plugin",
                        "config_key": "debug",
                        "default_value": False,
                        "order": 1
                    }
                ]
            }
        }
    }
    
    generator.save_ui_file(example_schemas) 