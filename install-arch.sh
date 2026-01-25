#!/bin/bash
#
# Comprehensive Arch Linux Installation Script for rcfiles
# This script installs all tools, dependencies, and configurations
# for the rcfiles dotfiles repository.
#
# Usage: ./install-arch.sh
#

set -e  # Exit on error

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

# Check if running on Arch Linux
check_arch_linux() {
    if [ ! -f /etc/arch-release ]; then
        print_error "This script is designed for Arch Linux only"
        exit 1
    fi
    print_success "Running on Arch Linux"
}

# Update system packages
update_system() {
    print_header "Updating System Packages"
    sudo pacman -Syu --noconfirm
    print_success "System updated"
}

# Install core tools
install_core_tools() {
    print_header "Installing Core Tools"
    
    local core_packages=(
        git
        curl
        wget
        base-devel  # Required for building packages
        zsh
        neovim
        tmux
    )
    
    for package in "${core_packages[@]}"; do
        if pacman -Qi "$package" &> /dev/null; then
            print_info "$package already installed"
        else
            print_info "Installing $package..."
            sudo pacman -S --noconfirm "$package"
            print_success "$package installed"
        fi
    done
}

# Install Neovim dependencies
install_neovim_deps() {
    print_header "Installing Neovim Dependencies"
    
    local nvim_packages=(
        ripgrep           # Telescope grep
        fd                # Telescope file finder
        make              # telescope-fzf-native build
        gcc               # Treesitter compilation
        nodejs            # Mason LSP, Copilot
        npm               # Mason LSP
        python            # Python LSP, formatters
        python-pip        # Python package manager
        go                # Go LSP, formatters
        jq                # JSON formatter
        luarocks          # Lua package manager (for stylua)
    )
    
    for package in "${nvim_packages[@]}"; do
        if pacman -Qi "$package" &> /dev/null; then
            print_info "$package already installed"
        else
            print_info "Installing $package..."
            sudo pacman -S --noconfirm "$package"
            print_success "$package installed"
        fi
    done
}

# Install LSP and formatter dependencies
install_lsp_formatter_deps() {
    print_header "Installing LSP & Formatter Dependencies"
    
    local lsp_packages=(
        opentofu          # OpenTofu (Terraform alternative) LSP & formatter
        docker            # Docker support
        ruby              # Ruby LSP
        rubygems          # Ruby package manager
    )
    
    for package in "${lsp_packages[@]}"; do
        if pacman -Qi "$package" &> /dev/null; then
            print_info "$package already installed"
        else
            print_info "Installing $package..."
            sudo pacman -S --noconfirm "$package"
            print_success "$package installed"
        fi
    done
    
    # Install stylua (Lua formatter) via luarocks
    if command -v stylua &> /dev/null; then
        print_info "stylua already installed"
    else
        print_info "Installing stylua via luarocks..."
        sudo luarocks install --server=https://luarocks.org/dev stylua
        print_success "stylua installed"
    fi
    
    # Install black (Python formatter) via pip
    if command -v black &> /dev/null; then
        print_info "black already installed"
    else
        print_info "Installing black..."
        sudo pip install black --break-system-packages
        print_success "black installed"
    fi
    
    # Install rubocop (Ruby formatter) via gem
    if command -v rubocop &> /dev/null; then
        print_info "rubocop already installed"
    else
        print_info "Installing rubocop..."
        sudo gem install rubocop
        print_success "rubocop installed"
    fi
    
    # Install solargraph (Ruby LSP) via gem
    if command -v solargraph &> /dev/null; then
        print_info "solargraph already installed"
    else
        print_info "Installing solargraph..."
        sudo gem install solargraph
        print_success "solargraph installed"
    fi
}

# Install optional development tools
install_dev_tools() {
    print_header "Installing Development Tools"
    
    local dev_packages=(
        kubectl           # Kubernetes CLI
        kubectx           # Kubernetes context switcher
        github-cli        # GitHub CLI (gh command)
    )
    
    for package in "${dev_packages[@]}"; do
        if pacman -Qi "$package" &> /dev/null; then
            print_info "$package already installed"
        else
            print_info "Installing $package..."
            sudo pacman -S --noconfirm "$package"
            print_success "$package installed"
        fi
    done
    
    # Install kubecolor from AUR
    if command -v kubecolor &> /dev/null; then
        print_info "kubecolor already installed"
    else
        print_warning "kubecolor requires AUR - installing via yay/paru if available"
        if command -v yay &> /dev/null; then
            yay -S --noconfirm kubecolor
            print_success "kubecolor installed via yay"
        elif command -v paru &> /dev/null; then
            paru -S --noconfirm kubecolor
            print_success "kubecolor installed via paru"
        else
            print_warning "No AUR helper found. Install kubecolor manually or install yay/paru first"
        fi
    fi
}

# Install Conky (Linux system monitor)
install_conky() {
    print_header "Installing Conky"
    
    local conky_packages=(
        conky
        lm_sensors  # Hardware monitoring
    )
    
    for package in "${conky_packages[@]}"; do
        if pacman -Qi "$package" &> /dev/null; then
            print_info "$package already installed"
        else
            print_info "Installing $package..."
            sudo pacman -S --noconfirm "$package"
            print_success "$package installed"
        fi
    done
    
    # Detect sensors
    print_info "Detecting sensors (you may need to answer yes to some prompts)..."
    sudo sensors-detect --auto || print_warning "sensors-detect had issues, but continuing..."
    
    # Detect AC adapter path
    print_info "Detecting AC adapter path..."
    
    local AC_PATH=""
    local POSSIBLE_PATHS=(
        "/sys/class/power_supply/AC/online"
        "/sys/class/power_supply/AC0/online"
        "/sys/class/power_supply/ACAD/online"
        "/sys/class/power_supply/ADP0/online"
        "/sys/class/power_supply/ADP1/online"
    )
    
    for path in "${POSSIBLE_PATHS[@]}"; do
        if [ -f "$path" ]; then
            AC_PATH="$path"
            print_success "Found AC adapter at: $AC_PATH"
            break
        fi
    done
    
    if [ -z "$AC_PATH" ]; then
        print_warning "Could not detect AC adapter path automatically"
        AC_PATH="/sys/class/power_supply/AC/online"
        print_warning "Using default: $AC_PATH"
    fi
    
    # Create wrapper script
    print_info "Creating power-aware wrapper script..."
    
    mkdir -p "$HOME/.config/conky"
    
    cat > "$HOME/.config/conky/conky-power-aware.sh" << WRAPPER_EOF
#!/bin/bash

# Detect AC adapter path
AC_PATH="$AC_PATH"

# Function to check if on AC power
is_on_ac() {
    if [ -f "\$AC_PATH" ]; then
        [ "\$(cat "\$AC_PATH")" = "1" ]
    else
        # Default to AC if can't detect
        true
    fi
}

# Determine which config to use
if is_on_ac; then
    CONFIG="\$HOME/.config/conky/conky-ac.conf"
else
    CONFIG="\$HOME/.config/conky/conky-battery.conf"
fi

# Start conky with appropriate config
exec /usr/bin/conky -c "\$CONFIG"
WRAPPER_EOF
    
    chmod +x "$HOME/.config/conky/conky-power-aware.sh"
    print_success "Wrapper script created and made executable"
    
    # Create systemd service
    print_info "Creating systemd user service..."
    
    mkdir -p "$HOME/.config/systemd/user"
    
    cat > "$HOME/.config/systemd/user/conky.service" << 'SERVICE_EOF'
[Unit]
Description=Conky System Monitor (Power-Aware)
After=graphical-session.target

[Service]
Type=simple
ExecStart=%h/.config/conky/conky-power-aware.sh
Restart=on-failure
RestartSec=3

[Install]
WantedBy=default.target
SERVICE_EOF
    
    print_success "Systemd service created"
    
    # Create udev rule
    print_info "Creating udev rule for automatic power state switching..."
    
    sudo tee /etc/udev/rules.d/99-conky-power.rules > /dev/null << 'UDEV_EOF'
# Restart conky when AC power state changes
# This allows conky to switch between AC and battery configurations automatically
SUBSYSTEM=="power_supply", ATTR{online}=="0", RUN+="/usr/bin/systemctl --user --machine=$env{USER}@.host restart conky.service"
SUBSYSTEM=="power_supply", ATTR{online}=="1", RUN+="/usr/bin/systemctl --user --machine=$env{USER}@.host restart conky.service"
UDEV_EOF
    
    sudo udevadm control --reload-rules
    print_success "Udev rule created and reloaded"
    
    # Enable and start service
    print_info "Enabling and starting conky service..."
    
    systemctl --user daemon-reload
    systemctl --user enable conky.service
    systemctl --user start conky.service
    
    # Verify installation
    sleep 2
    
    if systemctl --user is-active --quiet conky.service; then
        print_success "Conky service is running"
    else
        print_warning "Conky service failed to start. Check logs: journalctl --user -u conky.service"
    fi
}

# Install oh-my-zsh
install_oh_my_zsh() {
    print_header "Installing oh-my-zsh"
    
    if [ -d "$HOME/.oh-my-zsh" ]; then
        print_info "oh-my-zsh already installed"
    else
        print_info "Installing oh-my-zsh..."
        sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
        print_success "oh-my-zsh installed"
    fi
}

# Install asdf version manager
install_asdf() {
    print_header "Installing asdf Version Manager"
    
    if [ -d "$HOME/.asdf" ]; then
        print_info "asdf already installed"
    else
        print_info "Installing asdf..."
        git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.14.0
        print_success "asdf installed"
    fi
    
    # Source asdf to make it available in this script
    . "$HOME/.asdf/asdf.sh"
    
    # Install asdf plugins for tools in tool-versions
    print_info "Adding asdf plugins..."
    
    local plugins=(ruby nodejs yarn python)
    for plugin in "${plugins[@]}"; do
        if asdf plugin list | grep -q "^${plugin}$"; then
            print_info "asdf plugin $plugin already added"
        else
            asdf plugin add "$plugin"
            print_success "asdf plugin $plugin added"
        fi
    done
    
    # Install asdf plugin for packer (might need to add from custom URL)
    if asdf plugin list | grep -q "^packer$"; then
        print_info "asdf plugin packer already added"
    else
        asdf plugin add packer https://github.com/asdf-community/asdf-hashicorp.git || \
            print_warning "Could not add packer plugin - may need manual installation"
    fi
    
    # Install asdf plugin for aws-vault
    if asdf plugin list | grep -q "^aws-vault$"; then
        print_info "asdf plugin aws-vault already added"
    else
        asdf plugin add aws-vault https://github.com/karancode/asdf-aws-vault.git || \
            print_warning "Could not add aws-vault plugin - may need manual installation"
    fi
}

# Install NVM (Node Version Manager)
install_nvm() {
    print_header "Installing NVM (Node Version Manager)"
    
    if [ -d "$HOME/.nvm" ]; then
        print_info "NVM already installed"
    else
        print_info "Installing NVM..."
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
        print_success "NVM installed"
    fi
}

# Install RVM (Ruby Version Manager)
install_rvm() {
    print_header "Installing RVM (Ruby Version Manager)"
    
    if command -v rvm &> /dev/null; then
        print_info "RVM already installed"
    else
        print_info "Installing RVM..."
        # Import GPG keys
        gpg --keyserver keyserver.ubuntu.com --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB || \
            print_warning "GPG key import failed, but continuing..."
        # Install RVM
        curl -sSL https://get.rvm.io | bash -s stable
        print_success "RVM installed"
    fi
}

# Install Poetry (Python package manager)
install_poetry() {
    print_header "Installing Poetry (Python Package Manager)"
    
    if command -v poetry &> /dev/null; then
        print_info "Poetry already installed"
    else
        print_info "Installing Poetry..."
        curl -sSL https://install.python-poetry.org | python3 -
        print_success "Poetry installed"
    fi
}

# Create symlinks
create_symlinks() {
    print_header "Creating Configuration Symlinks"
    
    local rcfiles_dir="$HOME/.rcfiles"
    
    # ZSH configuration
    if [ -L "$HOME/.zshrc" ]; then
        print_info ".zshrc symlink already exists"
    else
        if [ -f "$HOME/.zshrc" ]; then
            print_warning "Backing up existing .zshrc to .zshrc.backup"
            mv "$HOME/.zshrc" "$HOME/.zshrc.backup"
        fi
        ln -sf "$rcfiles_dir/zshrc" "$HOME/.zshrc"
        print_success "Created .zshrc symlink"
    fi
    
    # tmux configuration
    if [ -L "$HOME/.tmux.conf" ]; then
        print_info ".tmux.conf symlink already exists"
    else
        if [ -f "$HOME/.tmux.conf" ]; then
            print_warning "Backing up existing .tmux.conf to .tmux.conf.backup"
            mv "$HOME/.tmux.conf" "$HOME/.tmux.conf.backup"
        fi
        ln -sf "$rcfiles_dir/tmux.conf" "$HOME/.tmux.conf"
        print_success "Created .tmux.conf symlink"
    fi
    
    # Neovim configuration
    mkdir -p "$HOME/.config"
    if [ -L "$HOME/.config/nvim" ]; then
        print_info "Neovim config symlink already exists"
    else
        if [ -d "$HOME/.config/nvim" ]; then
            print_warning "Backing up existing nvim config to nvim.backup"
            mv "$HOME/.config/nvim" "$HOME/.config/nvim.backup"
        fi
        ln -sf "$rcfiles_dir/nvim/config/nvim" "$HOME/.config/nvim"
        print_success "Created Neovim config symlink"
    fi
    
    # asdf tool-versions
    if [ -L "$HOME/.tool-versions" ]; then
        print_info ".tool-versions symlink already exists"
    else
        if [ -f "$HOME/.tool-versions" ]; then
            print_warning "Backing up existing .tool-versions to .tool-versions.backup"
            mv "$HOME/.tool-versions" "$HOME/.tool-versions.backup"
        fi
        ln -sf "$rcfiles_dir/tool-versions" "$HOME/.tool-versions"
        print_success "Created .tool-versions symlink"
    fi
    
    # Conky configuration
    if [ -L "$HOME/.config/conky" ]; then
        print_info "Conky config symlink already exists"
    else
        if [ -d "$HOME/.config/conky" ]; then
            print_warning "Backing up existing conky config to conky.backup"
            mv "$HOME/.config/conky" "$HOME/.config/conky.backup"
        fi
        ln -sf "$rcfiles_dir/conky" "$HOME/.config/conky"
        print_success "Created Conky config symlink"
    fi
}

# Initialize git submodules
init_git_submodules() {
    print_header "Initializing Git Submodules"
    
    cd "$HOME/.rcfiles"
    
    if [ -f ".gitmodules" ]; then
        print_info "Initializing and updating submodules..."
        git submodule init
        git submodule update
        print_success "Git submodules initialized"
    else
        print_warning "No .gitmodules file found"
    fi
}

# Change default shell to zsh
change_default_shell() {
    print_header "Setting Default Shell to ZSH"
    
    if [ "$SHELL" = "$(which zsh)" ]; then
        print_info "Default shell is already zsh"
    else
        print_info "Changing default shell to zsh..."
        chsh -s "$(which zsh)"
        print_success "Default shell changed to zsh (will take effect on next login)"
    fi
}

# Install Neovim plugins
install_nvim_plugins() {
    print_header "Installing Neovim Plugins"
    
    print_info "Launching Neovim to install plugins (this may take a few minutes)..."
    print_warning "If you see errors, don't worry - plugins are still installing in the background"
    
    # Launch Neovim headless to trigger lazy.nvim bootstrap and plugin installation
    timeout 180 nvim --headless "+Lazy! sync" +qa || print_warning "Neovim plugin sync timed out or had issues, but basic setup is done"
    
    print_success "Neovim plugins installation triggered"
}

# Install asdf tool versions
install_asdf_tools() {
    print_header "Installing asdf Tool Versions"
    
    if [ -f "$HOME/.tool-versions" ]; then
        print_info "Installing tools from .tool-versions..."
        
        # Source asdf
        if [ -f "$HOME/.asdf/asdf.sh" ]; then
            . "$HOME/.asdf/asdf.sh"
        fi
        
        cd "$HOME"
        asdf install || print_warning "Some asdf tools failed to install - you may need to install them manually"
        print_success "asdf tools installation attempted"
    else
        print_warning ".tool-versions file not found"
    fi
}

# Create hostspecific directory
create_hostspecific_dir() {
    print_header "Creating Host-Specific Configuration Directory"
    
    local hostspecific_dir="$HOME/.rcfiles/hostspecific/zsh"
    
    if [ -d "$hostspecific_dir" ]; then
        print_info "Host-specific directory already exists"
    else
        mkdir -p "$hostspecific_dir"
        print_success "Created $hostspecific_dir"
        print_info "Add machine-specific ZSH configs here (*.sh files)"
    fi
}

# Final setup instructions
print_final_instructions() {
    print_header "Installation Complete!"
    
    echo -e "${GREEN}Your rcfiles have been installed successfully!${NC}\n"
    
    echo -e "${YELLOW}Next Steps:${NC}"
    echo -e "  1. Restart your shell or run: ${BLUE}source ~/.zshrc${NC}"
    echo -e "  2. Open Neovim and run ${BLUE}:checkhealth${NC} to verify everything works"
    echo -e "  3. In Neovim, run ${BLUE}:Mason${NC} to verify LSP servers are installed"
    echo -e "  4. Run ${BLUE}tmux${NC} to test tmux configuration"
    echo -e "  5. (Optional) Add machine-specific configs to ${BLUE}~/.rcfiles/hostspecific/zsh/${NC}\n"
    
    echo -e "${YELLOW}Manual Steps (if needed):${NC}"
    echo -e "  • If you installed kubecolor manually: configure kubectl alias"
    echo -e "  • Configure AWS credentials for aws-vault"
    echo -e "  • Set up GitHub authentication for gh CLI: ${BLUE}gh auth login${NC}"
    echo -e "  • Set up GitHub Copilot in Neovim: ${BLUE}:Copilot setup${NC}\n"
    
    echo -e "${GREEN}Enjoy your new development environment!${NC}\n"
}

# Main installation flow
main() {
    print_header "rcfiles - Arch Linux Installation Script"
    
    check_arch_linux
    update_system
    install_core_tools
    install_neovim_deps
    install_lsp_formatter_deps
    install_dev_tools
    install_conky
    install_oh_my_zsh
    install_asdf
    install_nvm
    install_rvm
    install_poetry
    create_symlinks
    init_git_submodules
    change_default_shell
    create_hostspecific_dir
    install_nvim_plugins
    install_asdf_tools
    print_final_instructions
}

# Run main installation
main
