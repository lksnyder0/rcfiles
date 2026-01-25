# Personal Preferences

## Professional Background
- Python programmer with focus on performance optimization
- DevSecOps engineer specializing in Infrastructure as Code (IaC)

## Programming Preferences

### Python Development
- Prioritize low memory usage in code implementations
- Optimize for CPU performance
- Provide performance considerations and memory-efficient alternatives when relevant
- Include profiling suggestions when discussing optimization

### Infrastructure as Code
- **Default IaC tool**: OpenTofu (NOT Terraform)
- All infrastructure code examples should use OpenTofu syntax and best practices
- Focus on secure IaC practices aligned with DevSecOps principles

## Security Focus
- Emphasize security best practices in all code examples
- Highlight potential security vulnerabilities and mitigation strategies
- Include security scanning and compliance considerations for infrastructure code

### Secrets Management
- **Never commit secrets to version control**
- Use environment variables or secrets management tools (e.g., HashiCorp Vault, AWS Secrets Manager, Azure Key Vault)
- Include `.env.example` or `secrets.example` files with dummy values as templates
- Implement pre-commit hooks to prevent secret leaks (e.g., `git-secrets`, `detect-secrets`, `gitleaks`)
- Use `.gitignore` to exclude sensitive files (`.env`, `*.pem`, `*.key`, `credentials.*`, `secrets.*`, `*.tfvars` with real values)
- For OpenTofu/IaC: Use variable files with references to secrets managers, not hardcoded values
- Rotate secrets regularly and document rotation procedures
- Use least-privilege access for secrets retrieval

## Code Quality Expectations

### Performance Analysis
- Explain time and space complexity (Big O notation) for algorithms
- Provide performance implications and trade-offs of suggested approaches
- Include memory profiling recommendations (e.g., memory_profiler, tracemalloc)
- Suggest CPU profiling tools when relevant (e.g., cProfile, line_profiler)
- Compare performance characteristics of different implementation options

### Resource Usage
- Estimate memory footprint for data structures and operations
- Identify memory-intensive operations and suggest optimizations
- Recommend generator expressions over list comprehensions where appropriate
- Highlight opportunities for lazy evaluation and streaming processing
- Consider multiprocessing vs multithreading trade-offs for CPU-bound vs I/O-bound tasks

### Code Efficiency
- Prefer built-in Python functions and standard library over custom implementations
- Suggest appropriate data structures for performance (e.g., sets for membership testing, deque for queues)
- Recommend vectorized operations (NumPy, Pandas) for numerical computations
- Identify opportunities to reduce loop overhead and unnecessary iterations

### Security & DevSecOps
- Include security rationale for infrastructure and code recommendations
- Highlight common security pitfalls (injection vulnerabilities, secrets management, etc.)
- Recommend security scanning tools appropriate for the context
- Suggest least-privilege principles for IAM and access control
- Include input validation and sanitization in code examples

### Best Practices
- Follow PEP 8 style guidelines for Python code
- Use type hints for better code clarity and IDE support
- Include docstrings for functions and classes
- Suggest appropriate error handling and logging strategies
- Recommend testing approaches (unit tests, integration tests, performance tests)

### Infrastructure Code Quality
- Use OpenTofu modules for reusability and maintainability
- Include state management best practices
- Implement proper resource tagging and naming conventions
- Use variables and outputs effectively
- Include comments explaining security decisions and constraints
- Validate configurations before deployment
- Use remote state with appropriate locking mechanisms

## Project Structure & Documentation

### Required Files
- **`.gitignore`**: Include entries for all tools/languages used in the project
  - Python: `__pycache__/`, `*.py[cod]`, `.venv/`, `venv/`, `.pytest_cache/`, `.coverage`, `*.egg-info/`
  - OpenTofu/Terraform: `*.tfstate`, `*.tfstate.backup`, `.terraform/`, `.terraform.lock.hcl`, `*.tfvars` (for sensitive data)
  - IDE/Editors: `.vscode/`, `.idea/`, `*.swp`, `.DS_Store`
  - Secrets: `.env`, `*.pem`, `*.key`, `credentials.json`, `secrets.*`
  
- **`README.md`**: Comprehensive project documentation including:
  - Project name and description (scope and purpose)
  - Tools and technologies used (with version requirements)
  - Project outputs, deliverables, or interfaces
  - Setup/installation instructions
  - Usage examples
  - Configuration requirements
  - Contributing guidelines (if applicable)
  - License information

### Additional Recommended Files

#### Python Projects
- **`requirements.txt`** or **`pyproject.toml`**: Dependency management with pinned versions
- **`requirements-dev.txt`**: Development dependencies (testing, linting, profiling tools)
- **`.python-version`** or **`runtime.txt`**: Specify Python version
- **`setup.py`** or **`pyproject.toml`**: For installable packages
- **`pytest.ini`** or **`pyproject.toml`**: Test configuration
- **`.pre-commit-config.yaml`**: Git hooks for code quality checks (include secrets detection)
- **`Makefile`** or **`justfile`**: Common development tasks

#### Infrastructure Projects
- **`versions.tf`**: OpenTofu version constraints and required providers
- **`variables.tf`**: Input variable definitions with descriptions and validation
- **`outputs.tf`**: Output value definitions
- **`terraform.tfvars.example`**: Example configuration (without secrets)
- **`backend.tf`**: Remote state configuration
- **`locals.tf`**: Local values for common expressions
- **`.tflint.hcl`**: OpenTofu linting configuration
- **`SECURITY.md`**: Security policies and vulnerability reporting

#### DevSecOps/CI-CD
- **`.github/workflows/`** or **`.gitlab-ci.yml`**: CI/CD pipeline definitions
- **`Dockerfile`** and **`.dockerignore`**: Container definitions (if applicable)
- **`docker-compose.yml`**: Local development environment (if applicable)
- **`.editorconfig`**: Consistent coding styles across editors
- **`CHANGELOG.md`**: Version history and changes
- **`CONTRIBUTING.md`**: Contribution guidelines and development workflow

### Project Layout Standards

#### Python Project Structure
```
project-name/
├── .github/workflows/          # CI/CD pipelines
├── docs/                       # Additional documentation
├── src/project_name/          # Source code (or just project_name/)
│   ├── __init__.py
│   ├── main.py
│   └── modules/
├── tests/                      # Test files
│   ├── __init__.py
│   ├── unit/
│   └── integration/
├── .gitignore
├── .pre-commit-config.yaml
├── README.md
├── requirements.txt
├── requirements-dev.txt
└── pyproject.toml
```

#### OpenTofu/IaC Project Structure
```
infrastructure/
├── .github/workflows/          # CI/CD for infrastructure
├── modules/                    # Reusable OpenTofu modules
│   ├── networking/
│   ├── compute/
│   └── security/
├── environments/               # Environment-specific configs
│   ├── dev/
│   ├── staging/
│   └── prod/
├── .gitignore
├── .tflint.hcl
├── README.md
├── versions.tf
└── SECURITY.md
```

### Documentation Standards
- Use clear, concise language in all documentation
- Include code examples where applicable
- Document security considerations and compliance requirements
- Keep documentation up-to-date with code changes
- Include diagrams for complex architectures (infrastructure projects)
- Document performance characteristics and resource requirements
- Provide troubleshooting sections for common issues
