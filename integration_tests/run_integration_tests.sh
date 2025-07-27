#!/bin/bash

# IdleonWeb Integration Tests Runner
# This script sets up and runs comprehensive integration tests with detailed reporting

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_header() {
    echo -e "${PURPLE}==================================================${NC}"
    echo -e "${PURPLE}$1${NC}"
    echo -e "${PURPLE}==================================================${NC}"
}

print_subheader() {
    echo -e "${CYAN}$1${NC}"
}

# Function to check if Docker is available
check_docker() {
    print_status "Checking Docker availability..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed or not in PATH"
        return 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker is not running or user doesn't have permissions"
        return 1
    fi
    
    print_success "Docker is available and running"
    return 0
}

# Function to check if Docker Compose is available
check_docker_compose() {
    print_status "Checking Docker Compose availability..."
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed or not in PATH"
        return 1
    fi
    
    print_success "Docker Compose is available"
    return 0
}

# Function to clean up Docker resources
cleanup_docker() {
    print_status "Cleaning up Docker resources..."
    
    # Stop and remove containers
    docker compose down --remove-orphans 2>/dev/null || true
    
    # Remove test images
    docker rmi integration_tests-test-arch integration_tests-test-ubuntu 2>/dev/null || true
    
    print_success "Docker cleanup completed"
}

# Function to run tests for a specific platform
run_platform_tests() {
    local platform=$1
    local profile_name="${platform}-test"
    
    print_subheader "Running tests for $platform..."
    
    # Build and run tests
    if docker compose --profile "$profile_name" up --build --exit-code-from "test-${platform}"; then
        print_success "$platform tests completed successfully"
        return 0
    else
        print_error "$platform tests failed"
        return 1
    fi
}

# Function to run all tests
run_all_tests() {
    print_subheader "Running tests for all platforms..."
    
    # Build and run all tests
    if docker compose --profile all-test up --build --exit-code-from test-all; then
        print_success "All platform tests completed successfully"
        return 0
    else
        print_error "Some platform tests failed"
        return 1
    fi
}

# Function to show test results summary
show_results_summary() {
    print_header "Test Results Summary"
    
    echo "Platform Tests:"
    echo "  - Arch Linux: $([ $arch_result -eq 0 ] && echo "PASS" || echo "FAIL")"
    echo "  - Ubuntu: $([ $ubuntu_result -eq 0 ] && echo "PASS" || echo "FAIL")"
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
        echo "  - Windows: $([ $windows_result -eq 0 ] && echo "PASS" || echo "FAIL")"
    else
        echo "  - Windows: UNAVAILABLE (requires Windows host)"
    fi
    echo ""
    
    local total_tests=3
    local passed_tests=0
    
    [ $arch_result -eq 0 ] && ((passed_tests++))
    [ $ubuntu_result -eq 0 ] && ((passed_tests++))
    [ $windows_result -eq 0 ] && ((passed_tests++))
    
    echo "Overall Results:"
    echo "  - Total Tests: $total_tests"
    echo "  - Passed: $passed_tests"
    echo "  - Failed: $((total_tests - passed_tests))"
    echo ""
    
    if [ $passed_tests -eq $total_tests ]; then
        print_success "All integration tests passed!"
        return 0
    else
        print_error "Some integration tests failed"
        return 1
    fi
}

# Function to show detailed error information
show_error_details() {
    print_header "Error Details"
    
    if [ $arch_result -ne 0 ]; then
        print_subheader "Arch Linux Test Errors:"
        echo "To see detailed Arch Linux test output, run:"
        echo "  docker compose --profile arch-test up --build"
        echo ""
    fi
    
    if [ $ubuntu_result -ne 0 ]; then
        print_subheader "Ubuntu Test Errors:"
        echo "To see detailed Ubuntu test output, run:"
        echo "  docker compose --profile ubuntu-test up --build"
        echo ""
    fi
    
    if [ $windows_result -ne 0 ]; then
        print_subheader "Windows Test Errors:"
        echo "To see detailed Windows test output, run:"
        echo "  docker compose --profile windows-test up --build"
        echo ""
    elif [[ "$OSTYPE" != "msys" && "$OSTYPE" != "cygwin" && "$OSTYPE" != "win32" ]]; then
        print_subheader "Windows Test Information:"
        echo "Windows tests are unavailable on Linux/macOS hosts."
        echo "To test Windows functionality:"
        echo "  - Run on a Windows machine: ./run_integration_tests.sh windows"
        echo "  - Use GitHub Actions for cross-platform testing"
        echo "  - Windows containers require Windows host with Docker Desktop"
        echo ""
    fi
    
    print_subheader "Troubleshooting Tips:"
    echo "1. Ensure Docker and Docker Compose are installed and running"
    echo "2. Check that you have sufficient disk space for Docker images"
    echo "3. Verify your internet connection for downloading base images"
    echo "4. Try running individual platform tests to isolate issues"
    echo "5. Check Docker logs for specific error messages"
    echo "6. Windows tests require Windows host - use GitHub Actions for cross-platform testing"
    echo ""
}

# Function to show usage information
show_usage() {
    echo "Usage: $0 [OPTIONS] [PLATFORMS]"
    echo ""
    echo "Options:"
    echo "  -h, --help          Show this help message"
    echo "  -c, --clean         Clean up Docker resources before running tests"
    echo "  -v, --verbose       Show verbose output"
    echo "  --no-cleanup        Don't clean up Docker resources after tests"
    echo ""
    echo "Platforms:"
echo "  arch                Run tests for Arch Linux only"
echo "  ubuntu              Run tests for Ubuntu only"
echo "  windows             Run tests for Windows only"
echo "  all                 Run tests for all platforms (default)"
    echo ""
    echo "Examples:"
echo "  $0                  # Run all platform tests"
echo "  $0 arch             # Run Arch Linux tests only"
echo "  $0 ubuntu           # Run Ubuntu tests only"
echo "  $0 windows          # Run Windows tests only"
echo "  $0 -c all           # Clean up and run all tests"
echo "  $0 --verbose arch   # Run Arch tests with verbose output"
}

# Main function
main() {
    local platforms="all"
    local clean_before=false
    local cleanup_after=true
    local verbose=false
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_usage
                exit 0
                ;;
            -c|--clean)
                clean_before=true
                shift
                ;;
            -v|--verbose)
                verbose=true
                shift
                ;;
            --no-cleanup)
                cleanup_after=false
                shift
                ;;
            arch|ubuntu|windows|all)
                platforms="$1"
                shift
                ;;
            *)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    print_header "IdleonWeb Integration Tests"
    echo "Platforms: $platforms"
    echo "Clean before: $clean_before"
    echo "Cleanup after: $cleanup_after"
    echo "Verbose: $verbose"
    echo ""
    
    # Check prerequisites
    print_header "Checking Prerequisites"
    
    if ! check_docker; then
        print_error "Docker check failed. Please install Docker and try again."
        exit 1
    fi
    
    if ! check_docker_compose; then
        print_error "Docker Compose check failed. Please install Docker Compose and try again."
        exit 1
    fi
    
    # Clean up before if requested
    if [ "$clean_before" = true ]; then
        print_header "Cleaning Up Before Tests"
        cleanup_docker
    fi
    
    # Run tests based on platform selection
    print_header "Running Integration Tests"
    
    local arch_result=0
    local ubuntu_result=0
    local windows_result=0
    
    case $platforms in
        arch)
            print_subheader "Running Arch Linux Tests Only"
            run_platform_tests "arch" || arch_result=1
            ;;
        ubuntu)
            print_subheader "Running Ubuntu Tests Only"
            run_platform_tests "ubuntu" || ubuntu_result=1
            ;;
        windows)
            print_subheader "Running Windows Tests Only"
            if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
                # On Windows, run tests directly
                print_subheader "Running Windows tests directly..."
                if python integration_tests/run_tests.py windows; then
                    print_success "Windows tests completed successfully"
                    windows_result=0
                else
                    print_error "Windows tests failed"
                    windows_result=1
                fi
            else
                print_warning "Windows containers require Windows host. Skipping Windows tests on Linux."
                print_warning "Use GitHub Actions or run on Windows machine for Windows testing."
                windows_result=0  # Skip, not fail
            fi
            ;;
        all)
            print_subheader "Running All Platform Tests"
            
            # Run Arch tests
            print_subheader "Testing Arch Linux..."
            run_platform_tests "arch" || arch_result=1
            
            # Run Ubuntu tests
            print_subheader "Testing Ubuntu..."
            run_platform_tests "ubuntu" || ubuntu_result=1
            
            # Run Windows tests (if on Windows)
            print_subheader "Testing Windows..."
            if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
                if python integration_tests/run_tests.py windows; then
                    print_success "Windows tests completed successfully"
                    windows_result=0
                else
                    print_error "Windows tests failed"
                    windows_result=1
                fi
            else
                print_warning "Windows containers require Windows host. Skipping Windows tests on Linux."
                print_warning "Use GitHub Actions or run on Windows machine for Windows testing."
                windows_result=0  # Skip, not fail
            fi
            ;;
    esac
    
    # Show results
    show_results_summary
    
    # Show error details if any tests failed
    if [ $arch_result -ne 0 ] || [ $ubuntu_result -ne 0 ]; then
        show_error_details
    fi
    
    # Clean up after if requested
    if [ "$cleanup_after" = true ]; then
        print_header "Cleaning Up After Tests"
        cleanup_docker
    fi
    
    # Exit with appropriate code
    if [ $arch_result -eq 0 ] && [ $ubuntu_result -eq 0 ] && [ $windows_result -eq 0 ]; then
        print_success "All tests completed successfully!"
        exit 0
    else
        print_error "Some tests failed. Check the output above for details."
        exit 1
    fi
}

# Run main function with all arguments
main "$@" 