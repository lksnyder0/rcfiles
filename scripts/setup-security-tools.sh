#!/bin/bash
#
# Setup Security Tools for rcfiles
# Installs and configures pre-commit hooks and secret detection tools
#
# Usage: ./scripts/setup-security-tools.sh
#

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Detect platform
detect_platform() {
    if [ -f /etc/arch-release ]; then
        echo "arch"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    else
        echo "unknown"
    fi
}

# Install pre-commit
install_precommit() {
    print_header "Installing pre-commit"
    
    if command_exists pre-commit; then
        print_info "pre-commit already installed: $(pre-commit --version)"
        return
    fi
    
    print_info "Installing pre-commit..."
    
    if command_exists pip; then
        pip install pre-commit --user
        print_success "pre-commit installed via pip"
    elif command_exists pip3; then
        pip3 install pre-commit --user
        print_success "pre-commit installed via pip3"
    else
        print_error "pip not found. Please install Python and pip first."
        exit 1
    fi
}

# Install detect-secrets
install_detect_secrets() {
    print_header "Installing detect-secrets"
    
    if command_exists detect-secrets; then
        print_info "detect-secrets already installed: $(detect-secrets --version)"
        return
    fi
    
    print_info "Installing detect-secrets..."
    
    if command_exists pip; then
        pip install detect-secrets --user
        print_success "detect-secrets installed via pip"
    elif command_exists pip3; then
        pip3 install detect-secrets --user
        print_success "detect-secrets installed via pip3"
    else
        print_warning "pip not found. detect-secrets will be managed by pre-commit"
    fi
}

# Install gitleaks (optional)
install_gitleaks() {
    print_header "Installing gitleaks (optional)"
    
    if command_exists gitleaks; then
        print_info "gitleaks already installed: $(gitleaks version)"
        return
    fi
    
    local platform=$(detect_platform)
    
    print_info "Installing gitleaks..."
    
    if [ "$platform" = "macos" ]; then
        if command_exists brew; then
            brew install gitleaks
            print_success "gitleaks installed via Homebrew"
        else
            print_warning "Homebrew not found. Skipping gitleaks installation."
            print_info "Install manually: brew install gitleaks"
        fi
    elif [ "$platform" = "arch" ]; then
        if command_exists yay; then
            yay -S --noconfirm gitleaks
            print_success "gitleaks installed via yay"
        elif command_exists paru; then
            paru -S --noconfirm gitleaks
            print_success "gitleaks installed via paru"
        else
            print_warning "No AUR helper found. Skipping gitleaks installation."
            print_info "Install manually: yay -S gitleaks or paru -S gitleaks"
        fi
    else
        print_warning "Unsupported platform for automatic gitleaks installation"
        print_info "See: https://github.com/gitleaks/gitleaks#installing"
    fi
}

# Install shellcheck (optional)
install_shellcheck() {
    print_header "Installing shellcheck (optional)"
    
    if command_exists shellcheck; then
        print_info "shellcheck already installed: $(shellcheck --version | head -2 | tail -1)"
        return
    fi
    
    local platform=$(detect_platform)
    
    print_info "Installing shellcheck..."
    
    if [ "$platform" = "macos" ]; then
        if command_exists brew; then
            brew install shellcheck
            print_success "shellcheck installed via Homebrew"
        else
            print_warning "Homebrew not found. Skipping shellcheck installation."
        fi
    elif [ "$platform" = "arch" ]; then
        sudo pacman -S --noconfirm shellcheck
        print_success "shellcheck installed via pacman"
    else
        print_warning "Unsupported platform for automatic shellcheck installation"
    fi
}

# Setup pre-commit hooks
setup_precommit_hooks() {
    print_header "Setting up pre-commit hooks"
    
    if [ ! -f ".pre-commit-config.yaml" ]; then
        print_error ".pre-commit-config.yaml not found"
        exit 1
    fi
    
    print_info "Installing pre-commit hooks..."
    pre-commit install
    print_success "Pre-commit hooks installed"
    
    print_info "Installing hook environments (this may take a minute)..."
    pre-commit install-hooks
    print_success "Hook environments installed"
}

# Initialize secrets baseline
initialize_secrets_baseline() {
    print_header "Initializing secrets baseline"
    
    if [ -f ".secrets.baseline" ]; then
        print_info ".secrets.baseline already exists"
        
        echo -n "Update baseline with current files? [y/N]: "
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            print_info "Updating secrets baseline..."
            detect-secrets scan --baseline .secrets.baseline
            print_success "Secrets baseline updated"
        fi
    else
        print_info "Creating initial secrets baseline..."
        detect-secrets scan > .secrets.baseline
        print_success "Secrets baseline created"
        
        print_info "You should audit the baseline to mark false positives:"
        echo "  detect-secrets audit .secrets.baseline"
    fi
}

# Verify installation
verify_installation() {
    print_header "Verifying Installation"
    
    local all_good=true
    
    # Check pre-commit
    if command_exists pre-commit; then
        print_success "pre-commit is installed"
    else
        print_error "pre-commit is NOT installed"
        all_good=false
    fi
    
    # Check detect-secrets
    if command_exists detect-secrets; then
        print_success "detect-secrets is installed"
    else
        print_warning "detect-secrets is NOT installed (will be managed by pre-commit)"
    fi
    
    # Check gitleaks
    if command_exists gitleaks; then
        print_success "gitleaks is installed"
    else
        print_warning "gitleaks is NOT installed (optional)"
    fi
    
    # Check shellcheck
    if command_exists shellcheck; then
        print_success "shellcheck is installed"
    else
        print_warning "shellcheck is NOT installed (optional)"
    fi
    
    # Check custom script
    if [ -x "scripts/check-ai-configs.sh" ]; then
        print_success "check-ai-configs.sh is executable"
    else
        print_error "check-ai-configs.sh is NOT executable"
        chmod +x scripts/check-ai-configs.sh
        print_success "Made check-ai-configs.sh executable"
    fi
    
    # Check pre-commit hooks installed
    if [ -f ".git/hooks/pre-commit" ]; then
        print_success "Git pre-commit hook is installed"
    else
        print_error "Git pre-commit hook is NOT installed"
        all_good=false
    fi
    
    echo ""
    if $all_good; then
        print_success "All required tools are installed and configured!"
    else
        print_warning "Some tools are missing, but you can still proceed"
    fi
}

# Test the setup
test_setup() {
    print_header "Testing Security Setup"
    
    print_info "Running pre-commit on all files (this may take a minute)..."
    
    if pre-commit run --all-files; then
        print_success "All pre-commit checks passed!"
    else
        print_warning "Some pre-commit checks failed. Review the output above."
        print_info "This is normal for a first run. Review and fix any issues."
    fi
}

# Print usage instructions
print_usage_instructions() {
    print_header "Setup Complete!"
    
    echo -e "${GREEN}Security tools are now configured!${NC}\n"
    
    echo -e "${YELLOW}Usage:${NC}"
    echo "  • Pre-commit hooks run automatically on git commit"
    echo "  • Run manually: pre-commit run --all-files"
    echo "  • Check AI configs: ./scripts/check-ai-configs.sh"
    echo "  • Update hooks: pre-commit autoupdate"
    echo ""
    
    echo -e "${YELLOW}Next Steps:${NC}"
    echo "  1. Review scripts/README.md for detailed documentation"
    echo "  2. Audit secrets baseline: detect-secrets audit .secrets.baseline"
    echo "  3. Test by adding a file: git add <file> && git commit"
    echo ""
    
    echo -e "${YELLOW}Bypassing hooks (use cautiously):${NC}"
    echo "  • Skip all hooks: git commit --no-verify"
    echo "  • Skip specific hook: SKIP=check-ai-configs git commit"
    echo ""
}

# Main installation flow
main() {
    print_header "Security Tools Setup for rcfiles"
    
    # Check we're in the right directory
    if [ ! -f ".pre-commit-config.yaml" ]; then
        print_error "Must be run from the rcfiles repository root"
        exit 1
    fi
    
    # Install tools
    install_precommit
    install_detect_secrets
    install_gitleaks
    install_shellcheck
    
    # Setup hooks
    setup_precommit_hooks
    
    # Initialize baseline
    if command_exists detect-secrets; then
        initialize_secrets_baseline
    else
        print_warning "Skipping secrets baseline (detect-secrets not installed)"
    fi
    
    # Verify everything
    verify_installation
    
    # Test the setup
    echo ""
    echo -n "Run a test of all pre-commit hooks? [y/N]: "
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        test_setup
    fi
    
    # Print usage instructions
    print_usage_instructions
}

# Run main installation
main
