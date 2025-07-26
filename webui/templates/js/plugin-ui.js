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
        
        // Safety check: ensure required elements exist
        if (!resultsContainer || !resultsList) {
            console.error('Required search result elements not found');
            this.showStatus(element, 'Error: Search results container not found', 'error');
            this.executingActions.delete(actionId);
            return;
        }
        
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
        if (!resultText || typeof resultText !== 'string') {
            return '<div class="result-item">No results found</div>';
        }
        
        // Handle error messages
        if (resultText.startsWith('ERROR:') || resultText.startsWith('Error:')) {
            return `<div class="result-item error">${resultText}</div>`;
        }
        
        // Handle "All Items" format
        if (resultText.includes('**All Items**')) {
            const lines = resultText.split('\n');
            let formattedHtml = '';
            let itemCount = 0;
            
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
                        itemCount++;
                    } else {
                        formattedHtml += `<div class="result-item">${line}</div>`;
                    }
                } else if (line.trim() && !line.startsWith('**All Items**') && !line.includes('items)')) {
                    formattedHtml += `<div class="result-item">${line}</div>`;
                }
            }
            
            if (itemCount === 0) {
                return '<div class="result-item">No items found</div>';
            }
            
            return formattedHtml;
        }
        
        // Handle regular search results (item_id : display_name format)
        if (resultText.includes(' : ')) {
            const lines = resultText.split('\n');
            let formattedHtml = '';
            
            for (const line of lines) {
                if (line.trim() && line.includes(' : ')) {
                    const parts = line.split(' : ', 2);
                    if (parts.length === 2) {
                        const itemId = parts[0].trim();
                        const itemName = parts[1].trim();
                        formattedHtml += `
                            <div class="result-item">
                                <span class="item-id">${itemId}</span>
                                <span class="item-name"> : ${itemName}</span>
                            </div>
                        `;
                    } else {
                        formattedHtml += `<div class="result-item">${line}</div>`;
                    }
                } else if (line.trim()) {
                    formattedHtml += `<div class="result-item">${line}</div>`;
                }
            }
            
            return formattedHtml;
        }
        
        // Handle single line results
        if (resultText.trim()) {
            return `<div class="result-item">${resultText}</div>`;
        }
        
        return '<div class="result-item">No results found</div>';
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
        const resultsList = element.querySelector('.results-list');
        
        if (resultsContainer) {
            resultsContainer.style.display = 'none';
        }
        
        // Only clear the results list content, not the entire container
        if (resultsList) {
            resultsList.innerHTML = '';
        }
    }
}

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
    new PluginUI();
    new TabManager();
}); 