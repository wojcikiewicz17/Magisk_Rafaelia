#!/bin/bash
################################################################################
# GOVERNANCE VALIDATOR SCRIPT
# Version: 1.0.0
# Authority: ativar.txt v999
# Purpose: Validate compliance with global governance standards
################################################################################

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ATIVAR_FILE="$REPO_ROOT/ativar.txt"

# Counters
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNING_CHECKS=0

################################################################################
# Helper Functions
################################################################################

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
    ((PASSED_CHECKS++))
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
    ((WARNING_CHECKS++))
}

log_error() {
    echo -e "${RED}[FAIL]${NC} $1"
    ((FAILED_CHECKS++))
}

check_file_exists() {
    local file="$1"
    local description="$2"
    ((TOTAL_CHECKS++))
    
    if [ -f "$file" ]; then
        log_success "$description: Found"
        return 0
    else
        log_error "$description: Not found at $file"
        return 1
    fi
}

check_directory_exists() {
    local dir="$1"
    local description="$2"
    ((TOTAL_CHECKS++))
    
    if [ -d "$dir" ]; then
        log_success "$description: Found"
        return 0
    else
        log_warning "$description: Not found at $dir"
        return 1
    fi
}

################################################################################
# Governance Framework Checks
################################################################################

check_governance_framework() {
    log_info "===================================================================="
    log_info "1. GOVERNANCE FRAMEWORK VALIDATION"
    log_info "===================================================================="
    
    # Check ativar.txt v999 exists
    check_file_exists "$ATIVAR_FILE" "ativar.txt v999 governance configuration"
    
    # Verify ativar.txt content
    ((TOTAL_CHECKS++))
    if grep -q "v999" "$ATIVAR_FILE" 2>/dev/null; then
        log_success "ativar.txt version v999 confirmed"
    else
        log_error "ativar.txt does not contain v999 version marker"
    fi
    
    # Check governance implementation document
    check_file_exists "$REPO_ROOT/GOVERNANCE_IMPLEMENTATION.md" "Governance implementation guide"
    
    # Check for governance documentation directory
    check_directory_exists "$REPO_ROOT/docs/governance" "Governance documentation directory"
}

################################################################################
# ISO Standards Compliance Checks
################################################################################

check_iso_standards() {
    log_info ""
    log_info "===================================================================="
    log_info "2. ISO STANDARDS COMPLIANCE"
    log_info "===================================================================="
    
    # ISO 9001 - Quality Management
    ((TOTAL_CHECKS++))
    if [ -d "$REPO_ROOT/docs/governance/quality" ] || [ -f "$REPO_ROOT/docs/governance/quality-manual.md" ]; then
        log_success "ISO 9001: Quality management documentation present"
    else
        log_warning "ISO 9001: Quality management documentation recommended"
    fi
    
    # ISO 27001 - Information Security Management
    ((TOTAL_CHECKS++))
    if [ -d "$REPO_ROOT/docs/governance/security" ] || [ -f "$REPO_ROOT/docs/governance/security/isms-policy.md" ]; then
        log_success "ISO 27001: Security management documentation present"
    else
        log_warning "ISO 27001: Security management documentation recommended"
    fi
    
    # ISO 25010 - Software Quality Model
    ((TOTAL_CHECKS++))
    if [ -f "$REPO_ROOT/tests/test_quality.py" ] || [ -d "$REPO_ROOT/tests/quality" ]; then
        log_success "ISO 25010: Quality testing framework present"
    else
        log_warning "ISO 25010: Quality testing framework recommended"
    fi
}

################################################################################
# IEEE Standards Compliance Checks
################################################################################

check_ieee_standards() {
    log_info ""
    log_info "===================================================================="
    log_info "3. IEEE STANDARDS COMPLIANCE"
    log_info "===================================================================="
    
    # IEEE 830 - Software Requirements
    ((TOTAL_CHECKS++))
    if [ -d "$REPO_ROOT/docs/requirements" ] || [ -f "$REPO_ROOT/README.MD" ]; then
        log_success "IEEE 830: Requirements documentation present"
    else
        log_warning "IEEE 830: Formal requirements documentation recommended"
    fi
    
    # IEEE 1012 - Verification and Validation
    ((TOTAL_CHECKS++))
    if [ -d "$REPO_ROOT/tests" ] && [ -f "$REPO_ROOT/.github/workflows/ci.yml" ]; then
        log_success "IEEE 1012: V&V framework present (tests + CI)"
    else
        log_warning "IEEE 1012: Complete V&V framework recommended"
    fi
    
    # IEEE 12207 - Lifecycle Processes
    ((TOTAL_CHECKS++))
    if [ -f "$REPO_ROOT/CONTRIBUTING.md" ] || [ -d "$REPO_ROOT/docs/processes" ]; then
        log_success "IEEE 12207: Lifecycle process documentation present"
    else
        log_warning "IEEE 12207: Formal process documentation recommended"
    fi
}

################################################################################
# NIST Standards Compliance Checks
################################################################################

check_nist_standards() {
    log_info ""
    log_info "===================================================================="
    log_info "4. NIST STANDARDS COMPLIANCE"
    log_info "===================================================================="
    
    # NIST Cybersecurity Framework
    ((TOTAL_CHECKS++))
    if [ -f "$REPO_ROOT/.github/workflows/codeql.yml" ] || [ -f "$REPO_ROOT/SECURITY_SUMMARY.md" ]; then
        log_success "NIST CSF: Security controls implemented"
    else
        log_warning "NIST CSF: Security framework implementation recommended"
    fi
    
    # NIST 800-53 - Security Controls
    ((TOTAL_CHECKS++))
    if [ -f "$REPO_ROOT/docs/governance/security/controls-matrix.md" ]; then
        log_success "NIST 800-53: Security controls matrix present"
    else
        log_warning "NIST 800-53: Security controls documentation recommended"
    fi
    
    # NIST 800-207 - Zero Trust Architecture
    ((TOTAL_CHECKS++))
    if grep -q "zero.trust\|Zero Trust" "$REPO_ROOT"/*.md 2>/dev/null || \
       [ -f "$REPO_ROOT/docs/governance/security/zero-trust-architecture.md" ]; then
        log_success "NIST 800-207: Zero Trust principles documented"
    else
        log_warning "NIST 800-207: Zero Trust architecture documentation recommended"
    fi
}

################################################################################
# W3C Standards Compliance Checks
################################################################################

check_w3c_standards() {
    log_info ""
    log_info "===================================================================="
    log_info "5. W3C STANDARDS COMPLIANCE"
    log_info "===================================================================="
    
    # JSON format validation
    ((TOTAL_CHECKS++))
    if command -v jq &> /dev/null; then
        JSON_FILES=$(find "$REPO_ROOT" -name "*.json" -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null || true)
        JSON_VALID=true
        for json_file in $JSON_FILES; do
            if ! jq empty "$json_file" 2>/dev/null; then
                log_error "W3C JSON: Invalid JSON in $json_file"
                JSON_VALID=false
            fi
        done
        if [ "$JSON_VALID" = true ]; then
            log_success "W3C JSON: All JSON files are valid"
        fi
    else
        log_warning "W3C JSON: jq not installed, cannot validate JSON files"
    fi
    
    # YAML format validation
    ((TOTAL_CHECKS++))
    if command -v yamllint &> /dev/null; then
        YAML_FILES=$(find "$REPO_ROOT/.github/workflows" -name "*.yml" 2>/dev/null || true)
        YAML_VALID=true
        for yaml_file in $YAML_FILES; do
            if ! yamllint -d relaxed "$yaml_file" 2>/dev/null; then
                log_warning "W3C YAML: Issues in $yaml_file"
                YAML_VALID=false
            fi
        done
        if [ "$YAML_VALID" = true ] && [ -n "$YAML_FILES" ]; then
            log_success "W3C YAML: All YAML files pass basic validation"
        fi
    else
        log_warning "W3C YAML: yamllint not installed, cannot validate YAML files"
    fi
}

################################################################################
# Build System Compliance Checks
################################################################################

check_build_system() {
    log_info ""
    log_info "===================================================================="
    log_info "6. BUILD SYSTEM COMPLIANCE"
    log_info "===================================================================="
    
    # Check build.py exists
    check_file_exists "$REPO_ROOT/build.py" "Main build script"
    
    # Check build.py is executable
    ((TOTAL_CHECKS++))
    if [ -x "$REPO_ROOT/build.py" ]; then
        log_success "build.py is executable"
    else
        log_warning "build.py should be executable (chmod +x build.py)"
    fi
    
    # Check for governance integration in build system
    ((TOTAL_CHECKS++))
    if grep -q "governance\|compliance\|standards" "$REPO_ROOT/build.py" 2>/dev/null; then
        log_success "Build system includes governance references"
    else
        log_warning "Build system governance integration recommended"
    fi
}

################################################################################
# CI/CD Workflow Compliance Checks
################################################################################

check_cicd_workflows() {
    log_info ""
    log_info "===================================================================="
    log_info "7. CI/CD WORKFLOW COMPLIANCE"
    log_info "===================================================================="
    
    # Check main workflows exist
    check_file_exists "$REPO_ROOT/.github/workflows/build.yml" "Build workflow"
    check_file_exists "$REPO_ROOT/.github/workflows/ci.yml" "CI workflow"
    check_file_exists "$REPO_ROOT/.github/workflows/codeql.yml" "Security scanning workflow"
    
    # Check for governance workflow
    ((TOTAL_CHECKS++))
    if [ -f "$REPO_ROOT/.github/workflows/governance-check.yml" ]; then
        log_success "Dedicated governance check workflow present"
    else
        log_warning "Dedicated governance check workflow recommended"
    fi
    
    # Check for governance hooks in existing workflows
    ((TOTAL_CHECKS++))
    WORKFLOW_COUNT=0
    for workflow in "$REPO_ROOT/.github/workflows"/*.yml; do
        if grep -q "governance\|compliance\|ativar" "$workflow" 2>/dev/null; then
            ((WORKFLOW_COUNT++))
        fi
    done
    if [ $WORKFLOW_COUNT -gt 0 ]; then
        log_success "Governance integration found in $WORKFLOW_COUNT workflow(s)"
    else
        log_warning "Governance integration in workflows recommended"
    fi
}

################################################################################
# Security Compliance Checks
################################################################################

check_security_compliance() {
    log_info ""
    log_info "===================================================================="
    log_info "8. SECURITY COMPLIANCE"
    log_info "===================================================================="
    
    # Check for security documentation
    check_file_exists "$REPO_ROOT/SECURITY_SUMMARY.md" "Security summary documentation"
    
    # Check for CodeQL configuration
    ((TOTAL_CHECKS++))
    if [ -f "$REPO_ROOT/.github/workflows/codeql.yml" ]; then
        log_success "CodeQL security scanning configured"
    else
        log_warning "CodeQL security scanning recommended"
    fi
    
    # Check for secrets management
    ((TOTAL_CHECKS++))
    if grep -q "secrets\.\|GITHUB_TOKEN" "$REPO_ROOT/.github/workflows"/*.yml 2>/dev/null; then
        log_success "Secrets management present in workflows"
    else
        log_warning "Secrets management review recommended"
    fi
    
    # Check for security-sensitive files not in git
    ((TOTAL_CHECKS++))
    SECURITY_FILES=(".env" "secrets.txt" "private.key" "*.pem")
    INSECURE_FILES=false
    for pattern in "${SECURITY_FILES[@]}"; do
        if find "$REPO_ROOT" -name "$pattern" -not -path "*/.git/*" 2>/dev/null | grep -q .; then
            log_error "Security: Found potentially sensitive file matching $pattern"
            INSECURE_FILES=true
        fi
    done
    if [ "$INSECURE_FILES" = false ]; then
        log_success "Security: No obvious sensitive files in repository"
    fi
}

################################################################################
# Documentation Compliance Checks
################################################################################

check_documentation() {
    log_info ""
    log_info "===================================================================="
    log_info "9. DOCUMENTATION COMPLIANCE"
    log_info "===================================================================="
    
    # Check core documentation files
    check_file_exists "$REPO_ROOT/README.MD" "README documentation"
    check_file_exists "$REPO_ROOT/CONTRIBUTING.md" "Contributing guidelines"
    check_file_exists "$REPO_ROOT/LICENSE" "License file"
    
    # Check for governance documentation
    ((TOTAL_CHECKS++))
    if [ -d "$REPO_ROOT/docs/governance" ] || \
       [ -f "$REPO_ROOT/GOVERNANCE_IMPLEMENTATION.md" ] || \
       [ -f "$REPO_ROOT/ativar.txt" ]; then
        log_success "Governance documentation present"
    else
        log_warning "Comprehensive governance documentation recommended"
    fi
    
    # Check for API documentation
    ((TOTAL_CHECKS++))
    if [ -d "$REPO_ROOT/docs" ] && find "$REPO_ROOT/docs" -name "*.md" | grep -q .; then
        log_success "Documentation directory with content present"
    else
        log_warning "Comprehensive documentation recommended"
    fi
}

################################################################################
# Ethics Framework Checks
################################################################################

check_ethics_framework() {
    log_info ""
    log_info "===================================================================="
    log_info "10. ETHICS FRAMEWORK (Ethica[8])"
    log_info "===================================================================="
    
    # Check for ethics documentation
    ((TOTAL_CHECKS++))
    if grep -rq "Ethica\[8\]\|ethical\|ethics" "$REPO_ROOT"/*.md 2>/dev/null || \
       [ -f "$REPO_ROOT/docs/governance/ethics/ethica-8-framework.md" ]; then
        log_success "Ethica[8]: Ethics framework referenced"
    else
        log_warning "Ethica[8]: Ethics framework documentation recommended"
    fi
    
    # Check for privacy considerations
    ((TOTAL_CHECKS++))
    if grep -rq "privacy\|PII\|personal.data" "$REPO_ROOT"/*.md 2>/dev/null; then
        log_success "Ethics: Privacy considerations documented"
    else
        log_warning "Ethics: Privacy considerations documentation recommended"
    fi
}

################################################################################
# Test Coverage Checks
################################################################################

check_test_coverage() {
    log_info ""
    log_info "===================================================================="
    log_info "11. TEST COVERAGE"
    log_info "===================================================================="
    
    # Check for test directory
    check_directory_exists "$REPO_ROOT/tests" "Test directory"
    
    # Check for test files
    ((TOTAL_CHECKS++))
    TEST_COUNT=$(find "$REPO_ROOT/tests" -name "test_*.py" -o -name "*_test.py" 2>/dev/null | wc -l)
    if [ "$TEST_COUNT" -gt 0 ]; then
        log_success "Test coverage: Found $TEST_COUNT test file(s)"
    else
        log_warning "Test coverage: No Python test files found"
    fi
    
    # Check for CI test execution
    ((TOTAL_CHECKS++))
    if grep -q "test\|pytest\|unittest" "$REPO_ROOT/.github/workflows"/*.yml 2>/dev/null; then
        log_success "Test execution configured in CI/CD"
    else
        log_warning "Automated test execution in CI/CD recommended"
    fi
}

################################################################################
# Quality Metrics Checks
################################################################################

check_quality_metrics() {
    log_info ""
    log_info "===================================================================="
    log_info "12. QUALITY METRICS"
    log_info "===================================================================="
    
    # Check for quality gates workflow
    check_file_exists "$REPO_ROOT/.github/workflows/quality-gates.yml" "Quality gates workflow"
    
    # Check for linting configuration
    ((TOTAL_CHECKS++))
    LINTER_CONFIGS=(".pylintrc" ".flake8" "pyproject.toml" ".editorconfig")
    LINTER_FOUND=false
    for config in "${LINTER_CONFIGS[@]}"; do
        if [ -f "$REPO_ROOT/$config" ]; then
            LINTER_FOUND=true
            break
        fi
    done
    if [ "$LINTER_FOUND" = true ]; then
        log_success "Code quality: Linter configuration found"
    else
        log_warning "Code quality: Linter configuration recommended"
    fi
}

################################################################################
# Continuous Improvement Checks
################################################################################

check_continuous_improvement() {
    log_info ""
    log_info "===================================================================="
    log_info "13. CONTINUOUS IMPROVEMENT (INFINITE FEEDBACK LOOP)"
    log_info "===================================================================="
    
    # Check for monitoring and logging
    ((TOTAL_CHECKS++))
    if grep -rq "logging\|logger\|log_" "$REPO_ROOT/build.py" "$REPO_ROOT/scripts"/*.sh 2>/dev/null; then
        log_success "Logging framework present"
    else
        log_warning "Comprehensive logging recommended"
    fi
    
    # Check for metrics collection
    ((TOTAL_CHECKS++))
    if grep -rq "metrics\|statistics\|analytics" "$REPO_ROOT/.github/workflows"/*.yml 2>/dev/null; then
        log_success "Metrics collection references found"
    else
        log_warning "Metrics collection framework recommended"
    fi
    
    # Check for feedback mechanisms
    ((TOTAL_CHECKS++))
    if [ -f "$REPO_ROOT/.github/ISSUE_TEMPLATE" ] || \
       [ -d "$REPO_ROOT/.github/ISSUE_TEMPLATE" ] || \
       [ -f "$REPO_ROOT/.github/workflows/greetings.yml" ]; then
        log_success "User feedback mechanisms present"
    else
        log_warning "User feedback mechanisms recommended"
    fi
}

################################################################################
# Summary Report
################################################################################

generate_summary() {
    log_info ""
    log_info "===================================================================="
    log_info "GOVERNANCE VALIDATION SUMMARY"
    log_info "===================================================================="
    log_info "Total Checks:    $TOTAL_CHECKS"
    log_success "Passed:         $PASSED_CHECKS"
    log_warning "Warnings:       $WARNING_CHECKS"
    log_error "Failed:         $FAILED_CHECKS"
    
    COMPLIANCE_RATE=0
    if [ $TOTAL_CHECKS -gt 0 ]; then
        COMPLIANCE_RATE=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))
    fi
    
    log_info "Compliance Rate: ${COMPLIANCE_RATE}%"
    
    if [ $FAILED_CHECKS -eq 0 ]; then
        log_info ""
        log_success "✓ GOVERNANCE VALIDATION PASSED"
        log_info "All critical governance requirements are met."
        log_info "Warnings indicate recommendations for improvement."
        return 0
    else
        log_info ""
        log_error "✗ GOVERNANCE VALIDATION FAILED"
        log_info "Please address the failed checks above."
        return 1
    fi
}

################################################################################
# Main Execution
################################################################################

main() {
    log_info "===================================================================="
    log_info "GOVERNANCE VALIDATOR - ativar.txt v999"
    log_info "===================================================================="
    log_info "Repository: $REPO_ROOT"
    log_info "Started: $(date)"
    log_info ""
    
    # Run all checks
    check_governance_framework
    check_iso_standards
    check_ieee_standards
    check_nist_standards
    check_w3c_standards
    check_build_system
    check_cicd_workflows
    check_security_compliance
    check_documentation
    check_ethics_framework
    check_test_coverage
    check_quality_metrics
    check_continuous_improvement
    
    # Generate summary
    generate_summary
    RESULT=$?
    
    log_info ""
    log_info "Completed: $(date)"
    log_info "===================================================================="
    
    exit $RESULT
}

# Run main function
main "$@"
