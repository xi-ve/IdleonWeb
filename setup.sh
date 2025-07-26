#!/bin/bash

# IdleonWeb Setup Script
# This script sets up the development environment for IdleonWeb

set -e  # Exit on any error

echo "🚀 Setting up IdleonWeb development environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3 is installed
check_python() {
    print_status "Checking Python installation..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1)
        print_success "Found Python: $PYTHON_VERSION"
    else
        print_error "Python 3 is not installed. Please install Python 3.8+ and try again."
        exit 1
    fi
}

# Check if Node.js is installed
check_node() {
    print_status "Checking Node.js installation..."
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version 2>&1)
        print_success "Found Node.js: $NODE_VERSION"
    else
        print_error "Node.js is not installed. Please install Node.js and try again."
        exit 1
    fi
    
    print_status "Checking npm installation..."
    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version 2>&1)
        print_success "Found npm: $NPM_VERSION"
    else
        print_error "npm is not installed. Please install npm and try again."
        exit 1
    fi
}

# Create virtual environment
setup_venv() {
    print_status "Setting up Python virtual environment..."
    
    if [ -d ".venv" ]; then
        print_warning "Virtual environment already exists. Removing old one..."
        rm -rf .venv
    fi
    
    python3 -m venv .venv
    print_success "Virtual environment created successfully"
}

# Activate virtual environment and install Python requirements
install_python_deps() {
    print_status "Installing Python dependencies..."
    
    # Activate virtual environment
    source .venv/bin/activate
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    # Install requirements
    if [ -f "requirements.txt" ]; then
        print_status "Installing requirements from requirements.txt..."
        pip install -r requirements.txt
        print_success "Python dependencies installed successfully"
    else
        print_warning "requirements.txt not found. Installing basic dependencies..."
        pip install prompt_toolkit rich pychrome
        print_success "Basic Python dependencies installed"
    fi
}

# Install Node.js dependencies
install_node_deps() {
    print_status "Installing Node.js dependencies..."
    
    if [ -d "core" ]; then
        cd core
        
        if [ -f "package.json" ]; then
            print_status "Installing npm dependencies from package.json..."
            npm install
            print_success "Node.js dependencies installed successfully"
        else
            print_warning "package.json not found in core directory"
        fi
        
        cd ..
    else
        print_warning "core directory not found"
    fi
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    # Create plugins directory if it doesn't exist
    if [ ! -d "plugins" ]; then
        mkdir -p plugins
        print_success "Created plugins directory"
    fi
    
    # Create core directory if it doesn't exist
    if [ ! -d "core" ]; then
        mkdir -p core
        print_success "Created core directory"
    fi
    
    # Create tmp_js directory (will be ignored by git)
    if [ ! -d "core/tmp_js" ]; then
        mkdir -p core/tmp_js
        print_success "Created core/tmp_js directory"
    fi
}

# Generate initial config if it doesn't exist
setup_config() {
    print_status "Setting up initial configuration..."
    
    if [ ! -f "core/conf.json" ]; then
        cat > core/conf.json << EOF
{
  "openDevTools": false,
  "interactive": true,
  "plugins": [
    "spawn_item",
    "mob_spawn_rate"
  ],
  "plugin_configs": {
    "spawn_item": {
      "debug": false
    },
    "mob_spawn_rate": {
      "debug": true,
      "toggle": false
    }
  },
  "debug": false,
  "injectFiles": [
    "plugins_combined.js"
  ]
}
EOF
        print_success "Created initial conf.json"
    else
        print_status "conf.json already exists"
    fi
}

# Main setup function
main() {
    echo "=========================================="
    echo "    IdleonWeb Development Setup"
    echo "=========================================="
    echo ""
    
    # Check prerequisites
    check_python
    check_node
    echo ""
    
    # Setup environment
    setup_venv
    install_python_deps
    echo ""
    
    # Setup Node.js dependencies
    install_node_deps
    echo ""
    
    # Create directories
    create_directories
    echo ""
    
    # Setup configuration
    setup_config
    echo ""
    
    print_success "Setup completed successfully! 🎉"
    echo ""
    echo "Next steps:"
    echo "1. Activate the virtual environment: source .venv/bin/activate"
    echo "2. Run the application: python main.py"
    echo "3. For development, use: python test_js_gen.py"
    echo ""
    echo "Happy coding! 🚀"
}

# Run main function
main "$@" 