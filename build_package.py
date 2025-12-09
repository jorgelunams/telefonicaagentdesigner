"""
Package Builder for Telefonica MCP Orchestrator
Programmatically creates all required files for a complete Python package
"""

import os
import json
from datetime import datetime
from pathlib import Path

def create_package_structure():
    """Create complete package structure with all required files."""
    
    base_path = r"C:\TelefonicaProcessAgent\Data\SourceDesigned"
    package_name = "telefonica_mcp_orchestrator"
    
    print("=" * 80)
    print("TELEFONICA MCP PACKAGE BUILDER")
    print("=" * 80)
    print(f"\nTarget directory: {base_path}")
    print(f"Package name: {package_name}\n")
    
    # Step 1: Create .env file
    print("[1/6] Creating .env file...")
    env_content = """# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://workshopopenaisw.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_API_VERSION=2024-08-01-preview
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4

# Azure APIM Gateway Configuration
APIM_BASE_URL=https://telefonicaapimgt.azure-api.net
APIM_SUBSCRIPTION_KEY=8d7b89290b7b46a6b5ccd4cceff11993
APIM_TIMEOUT=15.0

# Direct API Configuration
BEARER_TOKEN=AgTiwiEoTSxdPTdic163evZQoLhvap1WUzd3unT87ypBBadRbmzf6N

# Test Data
TEST_CUSTOMER_ID=45829374
TEST_MSISIDN=56987654321
"""
    
    env_path = os.path.join(base_path, ".env")
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(env_content)
    print(f"   ✓ Created: {env_path}")
    
    # Step 2: Create requirements.txt
    print("\n[2/6] Creating requirements.txt...")
    requirements_content = """# Core dependencies
httpx>=0.27.0
python-dotenv>=1.0.0
asyncio

# MCP SDK
mcp>=1.0.0

# Agent Framework
agent-framework>=1.0.0
agent-framework-azure-ai>=1.0.0

# Azure OpenAI
openai>=1.0.0
azure-identity>=1.15.0

# Utilities
pydantic>=2.0.0
"""
    
    req_path = os.path.join(base_path, "requirements.txt")
    with open(req_path, 'w', encoding='utf-8') as f:
        f.write(requirements_content)
    print(f"   ✓ Created: {req_path}")
    
    # Step 3: Create README.md
    print("\n[3/6] Creating README.md...")
    readme_content = f"""# Telefonica MCP Orchestrator

Automated billing workflow orchestrator using Model Context Protocol (MCP) and Azure OpenAI.

## Overview

This package orchestrates a multi-step billing workflow:
1. **Payment Documents**: Retrieve customer payment documents
2. **Invoice List**: Get list of customer invoices via Azure APIM Gateway
3. **Invoice Links**: Retrieve download links for invoices

## Architecture

- **MCP Server**: `telefonica_mcp_server_*.py` - Exposes Telefonica APIs as MCP tools
- **MCP Clients**: `mcp_client_*.py` - Individual clients for each API endpoint
- **Orchestrator**: `process_orchestrator_main.py` - Coordinates workflow execution

## Installation

### 1. Create Virtual Environment

```bash
python -m venv venv
venv\\Scripts\\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Edit `.env` file with your credentials:
- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
- `APIM_SUBSCRIPTION_KEY`: Azure APIM subscription key
- `BEARER_TOKEN`: Bearer token for direct APIs

### 4. Verify Setup

```bash
python verify_setup.py
```

## Usage

### Run Complete Workflow

```bash
python process_orchestrator_main.py
```

### Run Individual MCP Client

```bash
python mcp_client_deuda_fija_*.py
python mcp_client_listado_de_boletas_fija_*.py
python mcp_client_retrieve_invoice_link_*.py
```

### Start MCP Server Standalone

```bash
python telefonica_mcp_server_*.py
```

## Configuration

All configuration is in `.env`:

| Variable | Description | Example |
|----------|-------------|---------|
| `APIM_BASE_URL` | Azure APIM Gateway base URL | `https://telefonicaapimgt.azure-api.net` |
| `APIM_SUBSCRIPTION_KEY` | APIM subscription key | `8d7b89290b7b46a6b5ccd4cceff11993` |
| `BEARER_TOKEN` | Bearer token for direct APIs | `AgTiwiEoTSxdPTdic163evZQoLhvap1WUzd3unT87ypBBadRbmzf6N` |
| `TEST_CUSTOMER_ID` | Customer ID for testing | `45829374` |
| `TEST_MSISIDN` | Phone number for testing | `56987654321` |

## Workflow Results

Results are saved to `../WorkflowResults/`:
- `workflow_results_<timestamp>.json` - Complete workflow output
- `execution_log_<timestamp>.json` - Execution timeline and logs

## Development

### Package Generated

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### File Structure

```
SourceDesigned/
├── .env                                    # Environment configuration
├── requirements.txt                        # Python dependencies
├── README.md                              # This file
├── setup_environment.py                   # Environment setup script
├── verify_setup.py                        # Setup verification
├── telefonica_mcp_server_*.py            # MCP server
├── mcp_client_deuda_fija_*.py            # Payment documents client
├── mcp_client_listado_de_boletas_*.py    # Invoice list client
├── mcp_client_retrieve_invoice_link_*.py # Invoice link client
├── process_orchestrator_main.py          # Workflow orchestrator
└── package_metadata_*.json               # Generation metadata
```

## Troubleshooting

### MCP Server Connection Issues

1. Verify MCP server starts: `python telefonica_mcp_server_*.py`
2. Check `.env` configuration is loaded
3. Ensure APIM_BASE_URL and APIM_SUBSCRIPTION_KEY are correct

### API Authentication Errors

- **401 Unauthorized**: Check APIM_SUBSCRIPTION_KEY
- **Illegal header value**: Check BEARER_TOKEN is not empty
- **Missing protocol**: Verify APIM_BASE_URL includes `https://`

### Agent Framework Issues

Ensure agent-framework is installed:
```bash
pip install agent-framework agent-framework-azure-ai
```

## Support

For issues or questions, review the execution logs in `../WorkflowResults/`.
"""
    
    readme_path = os.path.join(base_path, "README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"   ✓ Created: {readme_path}")
    
    # Step 4: Create setup_environment.py
    print("\n[4/6] Creating setup_environment.py...")
    setup_env_content = """\"\"\"
Environment Setup Script for Telefonica MCP Orchestrator
Automates creation and configuration of Python virtual environment
\"\"\"

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    \"\"\"Run shell command and handle errors.\"\"\"
    print(f"\\n→ {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"  ✓ {description} completed")
        if result.stdout:
            print(f"  {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Error: {e}")
        if e.stderr:
            print(f"  {e.stderr.strip()}")
        return False

def setup_environment():
    \"\"\"Setup complete Python environment for the package.\"\"\"
    
    print("=" * 80)
    print("TELEFONICA MCP ORCHESTRATOR - ENVIRONMENT SETUP")
    print("=" * 80)
    
    base_path = Path(__file__).parent
    venv_path = base_path / "venv"
    
    print(f"\\nWorking directory: {base_path}")
    print(f"Python version: {sys.version}")
    
    # Step 1: Create virtual environment
    if not venv_path.exists():
        if not run_command("python -m venv venv", "Creating virtual environment"):
            return False
    else:
        print("\\n→ Virtual environment already exists")
        print("  ✓ Skipping creation")
    
    # Step 2: Determine activation command
    if sys.platform == "win32":
        activate_cmd = "venv\\\\Scripts\\\\activate.bat"
        pip_cmd = "venv\\\\Scripts\\\\pip.exe"
        python_cmd = "venv\\\\Scripts\\\\python.exe"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    print(f"\\n→ Activation command: {activate_cmd}")
    
    # Step 3: Upgrade pip
    if not run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip"):
        print("  ⚠ Warning: pip upgrade failed, continuing...")
    
    # Step 4: Install requirements
    requirements_file = base_path / "requirements.txt"
    if requirements_file.exists():
        if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies"):
            return False
    else:
        print("\\n⚠ Warning: requirements.txt not found")
    
    # Step 5: Verify .env file exists
    env_file = base_path / ".env"
    if not env_file.exists():
        print("\\n⚠ Warning: .env file not found")
        print("  Please create .env with required configuration")
    else:
        print("\\n✓ Found .env file")
    
    # Success summary
    print("\\n" + "=" * 80)
    print("✓ ENVIRONMENT SETUP COMPLETE")
    print("=" * 80)
    print(f"\\nTo activate the environment, run:")
    print(f"  {activate_cmd}")
    print(f"\\nTo run the orchestrator:")
    print(f"  {python_cmd} process_orchestrator_main.py")
    print(f"\\nTo verify setup:")
    print(f"  {python_cmd} verify_setup.py")
    
    return True

if __name__ == "__main__":
    success = setup_environment()
    sys.exit(0 if success else 1)
"""
    
    setup_path = os.path.join(base_path, "setup_environment.py")
    with open(setup_path, 'w', encoding='utf-8') as f:
        f.write(setup_env_content)
    print(f"   ✓ Created: {setup_path}")
    
    # Step 5: Create verify_setup.py
    print("\n[5/6] Creating verify_setup.py...")
    verify_content = """\"\"\"
Setup Verification Script
Checks all dependencies and configuration before running orchestrator
\"\"\"

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    \"\"\"Check if file exists and report.\"\"\"
    if os.path.exists(filepath):
        print(f"  ✓ {description}")
        return True
    else:
        print(f"  ✗ {description} - NOT FOUND")
        return False

def check_env_variable(var_name):
    \"\"\"Check if environment variable is set.\"\"\"
    value = os.getenv(var_name)
    if value and value != "your-api-key-here":
        print(f"  ✓ {var_name} is set")
        return True
    else:
        print(f"  ✗ {var_name} is NOT set or using default")
        return False

def check_import(module_name):
    \"\"\"Check if Python module can be imported.\"\"\"
    try:
        __import__(module_name)
        print(f"  ✓ {module_name}")
        return True
    except ImportError:
        print(f"  ✗ {module_name} - NOT INSTALLED")
        return False

def verify_setup():
    \"\"\"Run complete verification of setup.\"\"\"
    
    print("=" * 80)
    print("TELEFONICA MCP ORCHESTRATOR - SETUP VERIFICATION")
    print("=" * 80)
    
    all_checks_passed = True
    
    # Load .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("\\n✓ Loaded .env file")
    except ImportError:
        print("\\n✗ python-dotenv not installed")
        all_checks_passed = False
    
    # Check 1: Required Files
    print("\\n[1] Checking Required Files...")
    base_path = Path(__file__).parent
    
    required_files = [
        (".env", "Environment configuration"),
        ("requirements.txt", "Python dependencies"),
        ("README.md", "Documentation"),
    ]
    
    for filename, description in required_files:
        filepath = base_path / filename
        if not check_file_exists(filepath, description):
            all_checks_passed = False
    
    # Check for generated files
    mcp_server_files = list(base_path.glob("telefonica_mcp_server_*.py"))
    if mcp_server_files:
        print(f"  ✓ Found MCP server: {mcp_server_files[0].name}")
    else:
        print(f"  ✗ MCP server not found")
        all_checks_passed = False
    
    # Check 2: Environment Variables
    print("\\n[2] Checking Environment Variables...")
    
    required_vars = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME",
        "APIM_BASE_URL",
        "APIM_SUBSCRIPTION_KEY",
        "BEARER_TOKEN"
    ]
    
    for var in required_vars:
        if not check_env_variable(var):
            all_checks_passed = False
    
    # Check 3: Python Dependencies
    print("\\n[3] Checking Python Dependencies...")
    
    required_modules = [
        "httpx",
        "dotenv",
        "asyncio",
        "openai"
    ]
    
    for module in required_modules:
        if not check_import(module):
            all_checks_passed = False
    
    # Check 4: Python Version
    print("\\n[4] Checking Python Version...")
    python_version = sys.version_info
    if python_version.major == 3 and python_version.minor >= 10:
        print(f"  ✓ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    else:
        print(f"  ✗ Python {python_version.major}.{python_version.minor} (3.10+ required)")
        all_checks_passed = False
    
    # Summary
    print("\\n" + "=" * 80)
    if all_checks_passed:
        print("✓ ALL CHECKS PASSED - Ready to run orchestrator")
        print("=" * 80)
        print("\\nRun the orchestrator with:")
        print("  python process_orchestrator_main.py")
    else:
        print("✗ SOME CHECKS FAILED - Please fix issues above")
        print("=" * 80)
        print("\\nTo fix:")
        print("  1. Run: python setup_environment.py")
        print("  2. Edit .env file with your credentials")
        print("  3. Run verification again")
    
    return all_checks_passed

if __name__ == "__main__":
    success = verify_setup()
    sys.exit(0 if success else 1)
"""
    
    verify_path = os.path.join(base_path, "verify_setup.py")
    with open(verify_path, 'w', encoding='utf-8') as f:
        f.write(verify_content)
    print(f"   ✓ Created: {verify_path}")
    
    # Step 6: Create build metadata
    print("\n[6/6] Creating build metadata...")
    
    # Find latest generated files
    mcp_server_files = list(Path(base_path).glob("telefonica_mcp_server_*.py"))
    client_files = list(Path(base_path).glob("mcp_client_*.py"))
    orchestrator_files = list(Path(base_path).glob("process_orchestrator_main.py"))
    
    build_metadata = {
        "package_name": package_name,
        "build_date": datetime.now().isoformat(),
        "base_path": base_path,
        "components": {
            "mcp_server": [f.name for f in mcp_server_files],
            "mcp_clients": [f.name for f in client_files],
            "orchestrator": [f.name for f in orchestrator_files]
        },
        "configuration_files": [".env", "requirements.txt", "README.md"],
        "setup_scripts": ["setup_environment.py", "verify_setup.py"]
    }
    
    metadata_path = os.path.join(base_path, "build_metadata.json")
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(build_metadata, f, indent=2)
    print(f"   ✓ Created: {metadata_path}")
    
    # Final Summary
    print("\n" + "=" * 80)
    print("✓ PACKAGE BUILD COMPLETE")
    print("=" * 80)
    print(f"\nPackage location: {base_path}")
    print(f"\nNext steps:")
    print(f"  1. cd {base_path}")
    print(f"  2. python setup_environment.py")
    print(f"  3. Edit .env with your credentials")
    print(f"  4. python verify_setup.py")
    print(f"  5. python process_orchestrator_main.py")
    print("\n" + "=" * 80)

if __name__ == "__main__":
    create_package_structure()
