#!/bin/bash
#
# Environment Test Script for rcfiles
# Verifies that all components are properly installed and configured
#
# Usage: ./test-environment.sh
#

set +e  # Don't exit on error - we want to collect all test results

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test result counters
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_WARNING=0

# Helper functions
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_subheader() {
    echo -e "\n${BLUE}--- $1 ---${NC}"
}

test_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((TESTS_PASSED++))
}

test_fail() {
    echo -e "${RED}✗${NC} $1"
    ((TESTS_FAILED++))
}

test_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((TESTS_WARNING++))
}

print_info() {
    echo -e "  ${BLUE}ℹ${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Check if file/directory exists
path_exists() {
    [ -e "$1" ]
}

# Check if symlink points to correct target
check_symlink() {
    local link_path="$1"
    local expected_target="$2"
    
    if [ -L "$link_path" ]; then
        local actual_target=$(readlink -f "$link_path")
        local expected_full=$(readlink -f "$expected_target")
        
        if [ "$actual_target" = "$expected_full" ]; then
            return 0
        else
            return 1
        fi
    else
        return 2
    fi
}

# Test core tools installation
test_core_tools() {
    print_header "Testing Core Tools"
    
    # Check git
    if command_exists git; then
        test_pass "git is installed: $(git --version)"
    else
        test_fail "git is NOT installed"
    fi
    
    # Check curl
    if command_exists curl; then
        test_pass "curl is installed: $(curl --version 2>&1 | head -n1)"
    else
        test_fail "curl is NOT installed"
    fi
    
    # Check wget
    if command_exists wget; then
        test_pass "wget is installed: $(wget --version 2>&1 | head -n1)"
    else
        test_fail "wget is NOT installed"
    fi
    
    # Check zsh
    if command_exists zsh; then
        test_pass "zsh is installed: $(zsh --version)"
    else
        test_fail "zsh is NOT installed"
    fi
    
    # Check neovim (command is nvim)
    if command_exists nvim; then
        test_pass "neovim is installed: $(nvim --version 2>&1 | head -n1)"
    else
        test_fail "neovim is NOT installed"
    fi
    
    # Check tmux
    if command_exists tmux; then
        test_pass "tmux is installed: $(tmux -V)"
    else
        test_fail "tmux is NOT installed"
    fi
}

# Test Neovim dependencies
test_neovim_deps() {
    print_header "Testing Neovim Dependencies"
    
    # Check ripgrep (command is rg)
    if command_exists rg; then
        test_pass "ripgrep is installed: $(rg --version 2>&1 | head -n1)"
    else
        test_fail "ripgrep is NOT installed"
    fi
    
    # Check fd
    if command_exists fd; then
        test_pass "fd is installed: $(fd --version 2>&1 | head -n1)"
    else
        test_fail "fd is NOT installed"
    fi
    
    # Check make
    if command_exists make; then
        test_pass "make is installed: $(make --version 2>&1 | head -n1)"
    else
        test_fail "make is NOT installed"
    fi
    
    # Check gcc
    if command_exists gcc; then
        test_pass "gcc is installed: $(gcc --version 2>&1 | head -n1)"
    else
        test_fail "gcc is NOT installed"
    fi
    
    # Check node (might be nodejs)
    if command_exists node; then
        test_pass "node is installed: $(node --version)"
    elif command_exists nodejs; then
        test_pass "nodejs is installed: $(nodejs --version)"
    else
        test_fail "node/nodejs is NOT installed"
    fi
    
    # Check npm
    if command_exists npm; then
        test_pass "npm is installed: $(npm --version)"
    else
        test_fail "npm is NOT installed"
    fi
    
    # Check python (might be python3)
    if command_exists python; then
        test_pass "python is installed: $(python --version 2>&1)"
    elif command_exists python3; then
        test_pass "python3 is installed: $(python3 --version 2>&1)"
    else
        test_fail "python is NOT installed"
    fi
    
    # Check pip (might be pip3)
    if command_exists pip; then
        test_pass "pip is installed: $(pip --version 2>&1 | head -n1)"
    elif command_exists pip3; then
        test_pass "pip3 is installed: $(pip3 --version 2>&1 | head -n1)"
    else
        test_fail "pip is NOT installed"
    fi
    
    # Check go
    if command_exists go; then
        test_pass "go is installed: $(go version)"
    else
        test_fail "go is NOT installed"
    fi
    
    # Check jq
    if command_exists jq; then
        test_pass "jq is installed: $(jq --version 2>&1)"
    else
        test_fail "jq is NOT installed"
    fi
    
    # Check luarocks
    if command_exists luarocks; then
        test_pass "luarocks is installed: $(luarocks --version 2>&1 | head -n1)"
    else
        test_fail "luarocks is NOT installed"
    fi
}

# Test LSP servers and formatters
test_lsp_formatters() {
    print_header "Testing LSP Servers & Formatters"
    
    print_subheader "Formatters"
    
    # Check black (Python formatter)
    if command_exists black; then
        test_pass "black is installed: $(black --version 2>&1 | head -n1)"
    else
        test_warn "black is NOT installed (install: pip install black)"
    fi
    
    # Check stylua (Lua formatter)
    if command_exists stylua; then
        test_pass "stylua is installed: $(stylua --version 2>&1 | head -n1)"
    else
        test_warn "stylua is NOT installed (install: pacman -S stylua OR luarocks install stylua)"
    fi
    
    # Check rubocop (Ruby formatter)
    if command_exists rubocop; then
        test_pass "rubocop is installed: $(rubocop --version 2>&1 | head -n1)"
    else
        test_warn "rubocop is NOT installed (install: gem install rubocop)"
    fi
    
    # Check jq (JSON formatter)
    if command_exists jq; then
        test_pass "jq is installed: $(jq --version 2>&1)"
    else
        test_warn "jq is NOT installed (install: pacman -S jq)"
    fi
    
    # Check opentofu (Terraform alternative)
    if command_exists tofu; then
        test_pass "opentofu is installed: $(tofu --version 2>&1 | head -n1)"
    elif command_exists terraform; then
        test_warn "terraform found but opentofu preferred: $(terraform --version 2>&1 | head -n1)"
    else
        test_warn "opentofu is NOT installed (install: pacman -S opentofu)"
    fi
    
    # Ruby LSP
    print_subheader "Ruby LSP"
    if command_exists solargraph; then
        test_pass "solargraph is installed: $(solargraph version 2>&1)"
    else
        test_warn "solargraph is NOT installed (optional)"
    fi
    
    # Check if gofmt exists (comes with Go)
    if command_exists gofmt; then
        test_pass "gofmt is installed (Go formatter)"
    else
        test_warn "gofmt is NOT installed"
    fi
}

# Test Mason LSP servers (requires Neovim)
test_mason_lsp() {
    print_header "Testing Mason LSP Servers"
    
    if command_exists nvim; then
        print_info "Checking Mason LSP servers (this may take a moment)..."
        
        # Get list of installed Mason packages
        local mason_packages=$(nvim --headless -c "lua print(vim.inspect(require('mason-registry').get_installed_package_names()))" -c "qa" 2>&1 | grep -o '"[^"]*"' | tr -d '"' || echo "")
        
        if [ -n "$mason_packages" ]; then
            local expected_servers=(dockerls gopls jsonls marksman lua_ls ruff solargraph terraformls yamlls)
            
            for server in "${expected_servers[@]}"; do
                if echo "$mason_packages" | grep -q "$server"; then
                    test_pass "Mason LSP server installed: $server"
                else
                    test_warn "Mason LSP server NOT found: $server (may install on first use)"
                fi
            done
        else
            test_warn "Could not query Mason packages (Neovim may need to be opened first)"
        fi
    else
        test_fail "Neovim not installed - cannot check Mason"
    fi
}

# Test development tools
test_dev_tools() {
    print_header "Testing Development Tools"
    
    local tools=(kubectl kubectx gh docker)
    
    for tool in "${tools[@]}"; do
        if command_exists "$tool"; then
            local version=$($tool version 2>&1 | head -n1 || $tool --version 2>&1 | head -n1)
            test_pass "$tool is installed: $version"
        else
            test_warn "$tool is NOT installed (optional)"
        fi
    done
    
    # kubecolor (AUR package)
    if command_exists kubecolor; then
        test_pass "kubecolor is installed: $(kubecolor --version 2>&1 | head -n1)"
    else
        test_warn "kubecolor is NOT installed (optional AUR package)"
    fi
}

# Test Conky
test_conky() {
    print_header "Testing Conky (Linux-only)"
    
    if command_exists conky; then
        test_pass "conky is installed: $(conky --version 2>&1 | head -n1)"
    else
        test_warn "conky is NOT installed (optional)"
    fi
    
    # Check sensors
    if command_exists sensors; then
        test_pass "lm_sensors is installed"
        print_info "Run 'sensors' to see detected hardware sensors"
    else
        test_warn "lm_sensors is NOT installed (optional)"
    fi
}

# Test oh-my-zsh installation
test_oh_my_zsh() {
    print_header "Testing oh-my-zsh"
    
    if [ -d "$HOME/.oh-my-zsh" ]; then
        test_pass "oh-my-zsh is installed at $HOME/.oh-my-zsh"
        
        # Check theme
        if [ -f "$HOME/.oh-my-zsh/themes/bira.zsh-theme" ]; then
            test_pass "bira theme is available"
        else
            test_fail "bira theme NOT found"
        fi
        
        # Check plugins directory
        if [ -d "$HOME/.oh-my-zsh/plugins" ]; then
            test_pass "oh-my-zsh plugins directory exists"
        else
            test_fail "oh-my-zsh plugins directory NOT found"
        fi
    else
        test_fail "oh-my-zsh is NOT installed"
    fi
}

# Test version managers
test_version_managers() {
    print_header "Testing Version Managers"
    
    print_subheader "asdf"
    if [ -d "$HOME/.asdf" ]; then
        test_pass "asdf is installed at $HOME/.asdf"
        
        # Source asdf to check plugins
        if [ -f "$HOME/.asdf/asdf.sh" ]; then
            . "$HOME/.asdf/asdf.sh"
            
            local plugins=$(asdf plugin list 2>&1)
            if [ -n "$plugins" ]; then
                print_info "asdf plugins installed:"
                echo "$plugins" | while read -r plugin; do
                    print_info "  - $plugin"
                done
                test_pass "asdf plugins are configured"
            else
                test_warn "No asdf plugins found"
            fi
        fi
    else
        test_warn "asdf is NOT installed (optional)"
    fi
    
    print_subheader "NVM"
    if [ -d "$HOME/.nvm" ]; then
        test_pass "NVM is installed at $HOME/.nvm"
    else
        test_warn "NVM is NOT installed (optional)"
    fi
    
    print_subheader "RVM"
    if command_exists rvm; then
        test_pass "RVM is installed: $(rvm --version 2>&1 | head -n1)"
    else
        test_warn "RVM is NOT installed (optional)"
    fi
    
    print_subheader "Poetry"
    if command_exists poetry; then
        test_pass "Poetry is installed: $(poetry --version 2>&1)"
    else
        test_warn "Poetry is NOT installed (optional)"
    fi
}

# Test symlinks
test_symlinks() {
    print_header "Testing Configuration Symlinks"
    
    local rcfiles_dir="$HOME/.rcfiles"
    
    # ZSH
    if check_symlink "$HOME/.zshrc" "$rcfiles_dir/zshrc"; then
        test_pass ".zshrc symlink is correctly configured"
    elif [ -L "$HOME/.zshrc" ]; then
        test_fail ".zshrc symlink points to wrong location: $(readlink $HOME/.zshrc)"
    elif [ -f "$HOME/.zshrc" ]; then
        test_warn ".zshrc exists but is not a symlink"
    else
        test_fail ".zshrc does not exist"
    fi
    
    # tmux
    if check_symlink "$HOME/.tmux.conf" "$rcfiles_dir/tmux.conf"; then
        test_pass ".tmux.conf symlink is correctly configured"
    elif [ -L "$HOME/.tmux.conf" ]; then
        test_fail ".tmux.conf symlink points to wrong location: $(readlink $HOME/.tmux.conf)"
    elif [ -f "$HOME/.tmux.conf" ]; then
        test_warn ".tmux.conf exists but is not a symlink"
    else
        test_fail ".tmux.conf does not exist"
    fi
    
    # Neovim
    if check_symlink "$HOME/.config/nvim" "$rcfiles_dir/nvim/config/nvim"; then
        test_pass "Neovim config symlink is correctly configured"
    elif [ -L "$HOME/.config/nvim" ]; then
        test_fail "Neovim config symlink points to wrong location: $(readlink $HOME/.config/nvim)"
    elif [ -d "$HOME/.config/nvim" ]; then
        test_warn "Neovim config exists but is not a symlink"
    else
        test_fail "Neovim config does not exist"
    fi
    
    # tool-versions
    if check_symlink "$HOME/.tool-versions" "$rcfiles_dir/tool-versions"; then
        test_pass ".tool-versions symlink is correctly configured"
    elif [ -L "$HOME/.tool-versions" ]; then
        test_fail ".tool-versions symlink points to wrong location: $(readlink $HOME/.tool-versions)"
    elif [ -f "$HOME/.tool-versions" ]; then
        test_warn ".tool-versions exists but is not a symlink"
    else
        test_warn ".tool-versions does not exist (optional)"
    fi
    
    # Conky
    if check_symlink "$HOME/.config/conky" "$rcfiles_dir/conky"; then
        test_pass "Conky config symlink is correctly configured"
    elif [ -L "$HOME/.config/conky" ]; then
        test_fail "Conky config symlink points to wrong location: $(readlink $HOME/.config/conky)"
    elif [ -d "$HOME/.config/conky" ]; then
        test_warn "Conky config exists but is not a symlink"
    else
        test_warn "Conky config does not exist (optional)"
    fi
}

# Test Git submodules
test_git_submodules() {
    print_header "Testing Git Submodules"
    
    cd "$HOME/.rcfiles" || return
    
    if [ -f ".gitmodules" ]; then
        test_pass ".gitmodules file exists"
        
        # Check if submodule is initialized
        if [ -d "cheatsheets/.git" ] || [ -f "cheatsheets/.git" ]; then
            test_pass "cheatsheets submodule is initialized"
            
            # Check if submodule has content
            if [ "$(ls -A cheatsheets 2>/dev/null)" ]; then
                test_pass "cheatsheets submodule has content"
            else
                test_fail "cheatsheets submodule is empty"
            fi
        else
            test_fail "cheatsheets submodule is NOT initialized"
        fi
    else
        test_warn "No .gitmodules file found"
    fi
}

# Test ZSH configuration
test_zsh_config() {
    print_header "Testing ZSH Configuration"
    
    # Check if default shell is zsh
    if [ "$SHELL" = "$(which zsh)" ]; then
        test_pass "Default shell is zsh"
    else
        test_warn "Default shell is not zsh: $SHELL (change with: chsh -s \$(which zsh))"
    fi
    
    # Test if zshrc loads without errors
    if [ -f "$HOME/.zshrc" ]; then
        test_pass ".zshrc file exists"
        
        print_info "Testing if zshrc loads without errors..."
        if zsh -c "source $HOME/.zshrc" &>/dev/null; then
            test_pass "zshrc loads without errors"
        else
            test_fail "zshrc has errors when loading"
        fi
    else
        test_fail ".zshrc file does not exist"
    fi
    
    # Check custom functions directory
    if [ -d "$HOME/.rcfiles/zfunc" ]; then
        test_pass "zfunc directory exists"
        
        local func_count=$(ls -1 "$HOME/.rcfiles/zfunc" 2>/dev/null | wc -l)
        test_pass "Found $func_count custom ZSH functions"
    else
        test_fail "zfunc directory does not exist"
    fi
    
    # Check hostspecific directory
    if [ -d "$HOME/.rcfiles/hostspecific/zsh" ]; then
        test_pass "hostspecific/zsh directory exists"
    else
        test_warn "hostspecific/zsh directory does not exist"
    fi
}

# Test Neovim configuration
test_neovim_config() {
    print_header "Testing Neovim Configuration"
    
    if command_exists nvim; then
        # Check if lazy.nvim is installed
        if [ -d "$HOME/.local/share/nvim/lazy/lazy.nvim" ]; then
            test_pass "lazy.nvim plugin manager is installed"
        else
            test_warn "lazy.nvim not found (will bootstrap on first nvim launch)"
        fi
        
        # Check if plugins directory exists
        if [ -d "$HOME/.local/share/nvim/lazy" ]; then
            local plugin_count=$(ls -1 "$HOME/.local/share/nvim/lazy" 2>/dev/null | wc -l)
            test_pass "Neovim plugins directory exists with $plugin_count plugins"
        else
            test_warn "Neovim plugins not yet installed (open nvim to install)"
        fi
        
        # Check Mason directory
        if [ -d "$HOME/.local/share/nvim/mason" ]; then
            test_pass "Mason LSP directory exists"
        else
            test_warn "Mason directory not found (will be created on first use)"
        fi
        
        # Test if Neovim config loads without errors
        print_info "Testing if Neovim config loads (this may take a moment)..."
        if timeout 10 nvim --headless +qall 2>&1 | grep -qi "error"; then
            test_warn "Neovim config may have errors (check :checkhealth)"
        else
            test_pass "Neovim config loads without obvious errors"
        fi
    else
        test_fail "Neovim not installed - cannot test config"
    fi
}

# Test tmux configuration
test_tmux_config() {
    print_header "Testing tmux Configuration"
    
    if command_exists tmux; then
        test_pass "tmux is installed: $(tmux -V)"
        
        # Check if tmux.conf exists
        if [ -f "$HOME/.tmux.conf" ]; then
            test_pass ".tmux.conf exists"
            
            # Test if tmux config is valid
            if tmux -f "$HOME/.tmux.conf" source-file "$HOME/.tmux.conf" 2>&1 | grep -qi "error"; then
                test_fail "tmux configuration has errors"
            else
                test_pass "tmux configuration is valid"
            fi
        else
            test_fail ".tmux.conf does not exist"
        fi
    else
        test_fail "tmux not installed - cannot test config"
    fi
}

# Test file permissions
test_file_permissions() {
    print_header "Testing File Permissions"
    
    # Check if install script is executable
    if [ -x "$HOME/.rcfiles/install-arch.sh" ]; then
        test_pass "install-arch.sh is executable"
    else
        test_warn "install-arch.sh is not executable (run: chmod +x install-arch.sh)"
    fi
    
    # Check if test script is executable
    if [ -x "$HOME/.rcfiles/test-environment.sh" ]; then
        test_pass "test-environment.sh is executable"
    else
        test_warn "test-environment.sh is not executable"
    fi
    
    # Check conky scripts
    if [ -x "$HOME/.rcfiles/conky/conky-power-aware.sh" ]; then
        test_pass "conky-power-aware.sh is executable"
    else
        test_warn "conky-power-aware.sh is not executable (optional)"
    fi
}

# Test documentation
test_documentation() {
    print_header "Testing Documentation"
    
    local docs=(
        "README.md"
        "docs/neovim.md"
        "docs/zsh.md"
        "docs/tmux.md"
        "docs/conky.md"
    )
    
    cd "$HOME/.rcfiles" || return
    
    for doc in "${docs[@]}"; do
        if [ -f "$doc" ]; then
            test_pass "$doc exists"
        else
            test_fail "$doc is missing"
        fi
    done
}

# Print summary
print_summary() {
    print_header "Test Summary"
    
    local total_tests=$((TESTS_PASSED + TESTS_FAILED + TESTS_WARNING))
    
    echo -e "${GREEN}Passed:${NC}   $TESTS_PASSED"
    echo -e "${RED}Failed:${NC}   $TESTS_FAILED"
    echo -e "${YELLOW}Warnings:${NC} $TESTS_WARNING"
    echo -e "Total:    $total_tests"
    echo ""
    
    if [ $TESTS_FAILED -eq 0 ]; then
        if [ $TESTS_WARNING -eq 0 ]; then
            echo -e "${GREEN}🎉 All tests passed! Your environment is fully configured.${NC}\n"
            return 0
        else
            echo -e "${YELLOW}✓ Core tests passed, but some optional components have warnings.${NC}"
            echo -e "${YELLOW}  Review warnings above for optional improvements.${NC}\n"
            return 0
        fi
    else
        echo -e "${RED}✗ Some tests failed. Please review the failures above.${NC}"
        echo -e "${YELLOW}  Run the installation script or install missing components manually.${NC}\n"
        return 1
    fi
}

# Provide next steps
print_next_steps() {
    if [ $TESTS_FAILED -gt 0 ]; then
        echo -e "${YELLOW}Recommended Next Steps:${NC}"
        echo -e "  1. Run ${BLUE}./install-arch.sh${NC} to install missing components"
        echo -e "  2. Run ${BLUE}./test-environment.sh${NC} again to verify"
        echo -e "  3. Open Neovim and run ${BLUE}:checkhealth${NC} for detailed diagnostics"
        echo -e "  4. Check ${BLUE}:Mason${NC} in Neovim to install LSP servers\n"
    else
        echo -e "${GREEN}Your environment is ready to use!${NC}"
        echo -e "\n${YELLOW}Optional Next Steps:${NC}"
        echo -e "  • Open Neovim and run ${BLUE}:checkhealth${NC} for detailed diagnostics"
        echo -e "  • Run ${BLUE}:Mason${NC} in Neovim to manage LSP servers"
        echo -e "  • Configure GitHub Copilot: ${BLUE}:Copilot setup${NC} in Neovim"
        echo -e "  • Set up GitHub CLI auth: ${BLUE}gh auth login${NC}"
        echo -e "  • Configure AWS credentials for aws-vault if needed\n"
    fi
}

# Main test execution
main() {
    print_header "rcfiles - Environment Test Script"
    echo "Testing installation and configuration..."
    
    test_core_tools
    test_neovim_deps
    test_lsp_formatters
    test_mason_lsp
    test_dev_tools
    test_conky
    test_oh_my_zsh
    test_version_managers
    test_symlinks
    test_git_submodules
    test_zsh_config
    test_neovim_config
    test_tmux_config
    test_file_permissions
    test_documentation
    
    print_summary
    local exit_code=$?
    
    print_next_steps
    
    exit $exit_code
}

# Run tests
main
