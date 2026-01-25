#!/bin/bash
#
# Security Check Script for AI Configuration Files
# Scans AI configuration files for potentially sensitive data before committing
#
# Usage: ./scripts/check-ai-configs.sh [file1 file2 ...]
#        If no files specified, scans all files in ai-configs/
#
# Exit codes:
#   0 - No issues found
#   1 - Potential security issues detected
#   2 - Script error
#

set -e

# Color codes for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
ISSUES_FOUND=0
FILES_SCANNED=0
WARNINGS_FOUND=0

# Helper functions
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_error() {
    echo -e "${RED}✗ ERROR:${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠ WARNING:${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check a single file for sensitive data
check_file() {
    local file="$1"
    local file_issues=0
    local file_warnings=0
    
    if [ ! -f "$file" ]; then
        return
    fi
    
    ((FILES_SCANNED++))
    echo -e "\n${BLUE}Scanning:${NC} $file"
    
    # Skip binary files
    if ! file "$file" | grep -q "text"; then
        print_info "Skipping binary file"
        return
    fi
    
    # 1. Check for API keys and tokens
    if grep -qE "(apiKey|api_key|API_KEY|access_?key|secret_?key|private_?key).*[:=].*['\"][a-zA-Z0-9_\-]{20,}['\"]" "$file" 2>/dev/null; then
        print_error "Potential API key or token found"
        grep -nE "(apiKey|api_key|API_KEY|access_?key|secret_?key|private_?key).*[:=]" "$file" | head -3
        ((file_issues++))
    fi
    
    # 2. Check for Bearer tokens
    if grep -qE "Bearer [a-zA-Z0-9_\-\.]{20,}" "$file" 2>/dev/null; then
        print_error "Bearer token found"
        grep -nE "Bearer [a-zA-Z0-9_\-\.]{20,}" "$file" | head -3
        ((file_issues++))
    fi
    
    # 3. Check for passwords
    if grep -qE "(password|passwd|pwd).*[:=].*['\"][^'\"]{1,}['\"]" "$file" 2>/dev/null; then
        # Exclude obvious placeholders
        if ! grep -qE "(password|passwd|pwd).*[:=].*['\"]?(YOUR_|EXAMPLE_|CHANGE_|xxx|123|test)" "$file" 2>/dev/null; then
            print_error "Potential password found"
            grep -nE "(password|passwd|pwd).*[:=]" "$file" | head -3
            ((file_issues++))
        fi
    fi
    
    # 4. Check for AWS credentials
    if grep -qE "AKIA[0-9A-Z]{16}" "$file" 2>/dev/null; then
        print_error "AWS Access Key ID found"
        grep -nE "AKIA[0-9A-Z]{16}" "$file" | head -3
        ((file_issues++))
    fi
    
    # 5. Check for AWS account IDs (12 digits)
    if grep -qE "(aws|account).*[0-9]{12}" "$file" 2>/dev/null; then
        print_warning "Potential AWS account ID found (12 consecutive digits)"
        grep -nE "[0-9]{12}" "$file" | head -3
        ((file_warnings++))
    fi
    
    # 6. Check for email addresses
    if grep -qE "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" "$file" 2>/dev/null; then
        # Exclude common example domains
        if ! grep -qE "@(example\.com|example\.org|test\.com|localhost)" "$file" 2>/dev/null; then
            print_warning "Email address found"
            grep -nE "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" "$file" | head -3
            ((file_warnings++))
        fi
    fi
    
    # 7. Check for internal/private URLs
    if grep -qE "(https?://)?(internal|private|vpn|corp|intranet)[\.\-]" "$file" 2>/dev/null; then
        print_warning "Internal/private URL found"
        grep -nE "(internal|private|vpn|corp|intranet)" "$file" | head -3
        ((file_warnings++))
    fi
    
    # 8. Check for .local domains
    if grep -qE "https?://[a-zA-Z0-9\-\.]+\.local" "$file" 2>/dev/null; then
        print_warning "Local domain (.local) found"
        grep -nE "\.local" "$file" | head -3
        ((file_warnings++))
    fi
    
    # 9. Check for private IP addresses
    if grep -qE "(192\.168\.|10\.|172\.(1[6-9]|2[0-9]|3[01])\.)" "$file" 2>/dev/null; then
        print_warning "Private IP address found"
        grep -nE "(192\.168\.|10\.|172\.(1[6-9]|2[0-9]|3[01])\.)" "$file" | head -3
        ((file_warnings++))
    fi
    
    # 10. Check for localhost references
    if grep -qE "(localhost|127\.0\.0\.1)" "$file" 2>/dev/null; then
        # Only warn if it's in a URL or connection string context
        if grep -qE "(http://|https://|://.*)(localhost|127\.0\.0\.1)" "$file" 2>/dev/null; then
            print_warning "Localhost URL found"
            grep -nE "(localhost|127\.0\.0\.1)" "$file" | head -3
            ((file_warnings++))
        fi
    fi
    
    # 11. Check for SSH keys
    if grep -qE "-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----" "$file" 2>/dev/null; then
        print_error "SSH private key found"
        echo "  Line: $(grep -n 'BEGIN.*PRIVATE KEY' "$file" | cut -d: -f1)"
        ((file_issues++))
    fi
    
    # 12. Check for JWT tokens
    if grep -qE "eyJ[a-zA-Z0-9_\-]*\.eyJ[a-zA-Z0-9_\-]*\.[a-zA-Z0-9_\-]*" "$file" 2>/dev/null; then
        print_error "JWT token found"
        grep -nE "eyJ[a-zA-Z0-9_\-]*\.eyJ" "$file" | head -3
        ((file_issues++))
    fi
    
    # 13. Check for database connection strings
    if grep -qE "(mongodb|mysql|postgresql|postgres)://[^@]+@" "$file" 2>/dev/null; then
        print_warning "Database connection string with credentials found"
        grep -nE "(mongodb|mysql|postgresql|postgres)://" "$file" | head -3
        ((file_warnings++))
    fi
    
    # 14. Check for certificate files
    if grep -qE "-----BEGIN CERTIFICATE-----" "$file" 2>/dev/null; then
        print_warning "Certificate found in file"
        ((file_warnings++))
    fi
    
    # Summary for this file
    if [ $file_issues -eq 0 ] && [ $file_warnings -eq 0 ]; then
        print_success "No issues found"
    else
        if [ $file_issues -gt 0 ]; then
            echo -e "${RED}  Found $file_issues critical issue(s)${NC}"
            ((ISSUES_FOUND += file_issues))
        fi
        if [ $file_warnings -gt 0 ]; then
            echo -e "${YELLOW}  Found $file_warnings warning(s)${NC}"
            ((WARNINGS_FOUND += file_warnings))
        fi
    fi
}

# Main execution
main() {
    print_header "AI Configuration Security Scanner"
    
    local files_to_scan=()
    
    # If arguments provided, scan those files
    if [ $# -gt 0 ]; then
        files_to_scan=("$@")
    # Otherwise, scan all files in ai-configs/
    elif [ -d "ai-configs" ]; then
        print_info "Scanning all files in ai-configs/"
        while IFS= read -r -d '' file; do
            files_to_scan+=("$file")
        done < <(find ai-configs -type f \( -name "*.md" -o -name "*.yml" -o -name "*.yaml" -o -name "*.json" -o -name "*.conf" -o -name "*.config" \) -print0)
    else
        print_error "No ai-configs/ directory found and no files specified"
        echo "Usage: $0 [file1 file2 ...]"
        exit 2
    fi
    
    if [ ${#files_to_scan[@]} -eq 0 ]; then
        print_warning "No files to scan"
        exit 0
    fi
    
    # Scan each file
    for file in "${files_to_scan[@]}"; do
        check_file "$file"
    done
    
    # Print summary
    print_header "Scan Summary"
    echo "Files scanned: $FILES_SCANNED"
    echo -e "${RED}Critical issues: $ISSUES_FOUND${NC}"
    echo -e "${YELLOW}Warnings: $WARNINGS_FOUND${NC}"
    
    # Provide recommendations
    if [ $ISSUES_FOUND -gt 0 ] || [ $WARNINGS_FOUND -gt 0 ]; then
        echo ""
        echo -e "${YELLOW}Recommendations:${NC}"
        if [ $ISSUES_FOUND -gt 0 ]; then
            echo "  • Review and remove all critical issues before committing"
            echo "  • Replace real credentials with placeholders (e.g., YOUR_API_KEY_HERE)"
            echo "  • Consider using .example files for configs with sensitive data"
        fi
        if [ $WARNINGS_FOUND -gt 0 ]; then
            echo "  • Review warnings to ensure no sensitive data is exposed"
            echo "  • Use generic examples instead of real URLs/IPs/emails"
            echo "  • Add entries to .gitignore for files with sensitive data"
        fi
    fi
    
    # Exit with appropriate code
    if [ $ISSUES_FOUND -gt 0 ]; then
        echo ""
        print_error "Critical security issues found. DO NOT COMMIT."
        exit 1
    elif [ $WARNINGS_FOUND -gt 0 ]; then
        echo ""
        print_warning "Warnings found. Review carefully before committing."
        # Still exit 0 for warnings (can be committed with caution)
        exit 0
    else
        echo ""
        print_success "All security checks passed!"
        exit 0
    fi
}

# Run main function
main "$@"
