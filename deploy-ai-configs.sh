#!/bin/bash
#
# Deploy AI Tool Configurations
# Deploys AI configurations (Claude, Serena, Context7) to global locations
#
# Usage: ./deploy-ai-configs.sh [personal|work]
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

# Usage function
usage() {
    echo "Usage: $0 [personal|work]"
    echo ""
    echo "Deploy AI tool configurations to global locations."
    echo ""
    echo "Contexts:"
    echo "  personal    Deploy personal machine configurations"
    echo "  work        Deploy work machine configurations"
    echo ""
    echo "Example:"
    echo "  $0 personal"
    exit 1
}

# Check arguments
if [ $# -eq 0 ]; then
    usage
fi

CONTEXT="$1"

if [ "$CONTEXT" != "personal" ] && [ "$CONTEXT" != "work" ]; then
    print_error "Invalid context: $CONTEXT"
    usage
fi

# Paths
RCFILES_DIR="$HOME/.rcfiles"
AI_CONFIGS_DIR="$RCFILES_DIR/ai-configs"

CLAUDE_GLOBAL="$HOME/.claude/CLAUDE.md"
SERENA_GLOBAL="$HOME/.serena/serena_config.yml"

# Backup existing configs
backup_existing_configs() {
    print_header "Backing Up Existing Configurations"
    
    local backup_dir="$HOME/.ai-configs-backup-$(date +%Y%m%d-%H%M%S)"
    mkdir -p "$backup_dir"
    
    # Backup Claude config
    if [ -f "$CLAUDE_GLOBAL" ]; then
        cp "$CLAUDE_GLOBAL" "$backup_dir/CLAUDE.md"
        print_success "Backed up Claude config to $backup_dir/CLAUDE.md"
    else
        print_info "No existing Claude config to backup"
    fi
    
    # Backup Serena config
    if [ -f "$SERENA_GLOBAL" ]; then
        cp "$SERENA_GLOBAL" "$backup_dir/serena_config.yml"
        print_success "Backed up Serena config to $backup_dir/serena_config.yml"
    else
        print_info "No existing Serena config to backup"
    fi
    
    echo ""
    print_info "Backups saved to: $backup_dir"
}

# Deploy Claude configuration
deploy_claude() {
    print_header "Deploying Claude Configuration"
    
    local source_file=""
    
    if [ "$CONTEXT" = "personal" ]; then
        source_file="$AI_CONFIGS_DIR/claude/CLAUDE-personal.md"
    else
        source_file="$AI_CONFIGS_DIR/claude/CLAUDE-work.md"
    fi
    
    if [ ! -f "$source_file" ]; then
        print_error "Source file not found: $source_file"
        return 1
    fi
    
    # Create directory if it doesn't exist
    mkdir -p "$(dirname "$CLAUDE_GLOBAL")"
    
    # Remove existing file/symlink
    if [ -e "$CLAUDE_GLOBAL" ] || [ -L "$CLAUDE_GLOBAL" ]; then
        rm "$CLAUDE_GLOBAL"
    fi
    
    # Create symlink
    ln -sf "$source_file" "$CLAUDE_GLOBAL"
    
    if [ -L "$CLAUDE_GLOBAL" ]; then
        print_success "Claude config deployed (symlink created)"
        print_info "  Source: $source_file"
        print_info "  Target: $CLAUDE_GLOBAL"
    else
        print_error "Failed to create symlink for Claude config"
        return 1
    fi
}

# Deploy Serena configuration
deploy_serena() {
    print_header "Deploying Serena Configuration"
    
    local source_file="$AI_CONFIGS_DIR/serena/serena_config.yml.example"
    
    if [ ! -f "$source_file" ]; then
        print_warning "Source file not found: $source_file"
        print_info "Skipping Serena deployment"
        return 0
    fi
    
    # Create directory if it doesn't exist
    mkdir -p "$(dirname "$SERENA_GLOBAL")"
    
    # Check if target already exists
    if [ -f "$SERENA_GLOBAL" ]; then
        print_warning "Serena config already exists at $SERENA_GLOBAL"
        echo -n "Overwrite? [y/N]: "
        read -r response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            print_info "Keeping existing Serena config"
            return 0
        fi
    fi
    
    # Copy file (not symlink) so user can customize
    cp "$source_file" "$SERENA_GLOBAL"
    
    if [ -f "$SERENA_GLOBAL" ]; then
        print_success "Serena config deployed (copied)"
        print_info "  Source: $source_file"
        print_info "  Target: $SERENA_GLOBAL"
        print_warning "  Note: File copied (not symlinked) - customize as needed"
    else
        print_error "Failed to copy Serena config"
        return 1
    fi
}

# Deploy Context7 (informational only)
deploy_context7() {
    print_header "Context7 Configuration"
    
    print_info "Context7 is managed as a Claude Code MCP plugin"
    print_info "No configuration file to deploy"
    print_info ""
    print_info "To enable Context7:"
    print_info "  1. Open Claude Code"
    print_info "  2. Use /plugins command"
    print_info "  3. Enable context7@claude-plugins-official"
    print_info ""
    print_info "Context7 will be automatically configured"
}

# Verify deployment
verify_deployment() {
    print_header "Verifying Deployment"
    
    local all_good=true
    
    # Check Claude
    if [ -L "$CLAUDE_GLOBAL" ]; then
        local target=$(readlink -f "$CLAUDE_GLOBAL")
        if [ -f "$target" ]; then
            print_success "Claude config symlink is valid"
            print_info "  Points to: $target"
        else
            print_error "Claude config symlink is broken"
            all_good=false
        fi
    elif [ -f "$CLAUDE_GLOBAL" ]; then
        print_warning "Claude config exists but is not a symlink"
    else
        print_error "Claude config not found"
        all_good=false
    fi
    
    # Check Serena
    if [ -f "$SERENA_GLOBAL" ]; then
        print_success "Serena config exists"
        
        # Verify YAML syntax
        if command -v python3 &> /dev/null; then
            if python3 -c "import yaml; yaml.safe_load(open('$SERENA_GLOBAL'))" &> /dev/null; then
                print_success "Serena config YAML syntax is valid"
            else
                print_error "Serena config has YAML syntax errors"
                all_good=false
            fi
        fi
    else
        print_warning "Serena config not found (optional)"
    fi
    
    # Check Context7 (plugin status)
    if [ -f "$HOME/.claude/settings.json" ]; then
        if grep -q "context7.*true" "$HOME/.claude/settings.json" 2>/dev/null; then
            print_success "Context7 plugin is enabled"
        else
            print_info "Context7 plugin may not be enabled (check Claude Code)"
        fi
    fi
    
    echo ""
    if $all_good; then
        print_success "All deployments verified successfully!"
    else
        print_warning "Some issues were found. Review output above."
    fi
}

# Print next steps
print_next_steps() {
    print_header "Deployment Complete!"
    
    echo -e "${GREEN}AI configurations deployed successfully!${NC}\n"
    
    echo -e "${YELLOW}Next Steps:${NC}"
    echo "  1. Restart Claude Code (if running) to load new configs"
    echo "  2. Test Claude with a simple prompt to verify global instructions"
    echo "  3. Ask Claude to 'open the Serena dashboard' to verify Serena config"
    echo "  4. Check Context7 with a documentation query"
    echo ""
    
    echo -e "${YELLOW}Customization:${NC}"
    echo "  • Claude: Edit $CLAUDE_GLOBAL"
    echo "  • Serena: Edit $SERENA_GLOBAL"
    echo "  • Context7: Managed through Claude Code plugins"
    echo ""
    
    echo -e "${YELLOW}Troubleshooting:${NC}"
    echo "  • Claude not using instructions: Start new conversation"
    echo "  • Serena errors: Check dashboard at http://127.0.0.1:8765"
    echo "  • Context7 not working: Use /plugins to enable"
    echo ""
}

# Main deployment flow
main() {
    print_header "AI Configurations Deployment"
    echo "Context: ${YELLOW}${CONTEXT}${NC}"
    echo "Deploy to: ${BLUE}global user directories${NC}"
    echo ""
    
    # Confirm deployment
    echo -n "Proceed with deployment? [y/N]: "
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        print_info "Deployment cancelled"
        exit 0
    fi
    
    # Check we're in the right directory
    if [ ! -d "$AI_CONFIGS_DIR" ]; then
        print_error "ai-configs directory not found"
        print_error "Run this script from the rcfiles repository root"
        exit 1
    fi
    
    # Backup existing configs
    backup_existing_configs
    
    # Deploy each component
    deploy_claude || print_error "Claude deployment failed"
    deploy_serena || print_error "Serena deployment had issues"
    deploy_context7
    
    # Verify everything
    verify_deployment
    
    # Print next steps
    print_next_steps
}

# Run main deployment
main
