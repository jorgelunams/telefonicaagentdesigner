# Copyright (c) Microsoft. All rights reserved.

import os
import json
from datetime import datetime
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_mcp_generation_prompt(api_catalog):
    """Create a detailed prompt for Azure OpenAI to generate MCP server code."""
    
    api_catalog_json = json.dumps(api_catalog, indent=2)
    
    prompt = ("You are an expert Python developer specializing in creating MCP (Model Context Protocol) servers.\n\n"
              "OBJECTIVE: Generate ONE complete Python MCP server file that includes ALL active APIs from the catalog.\n"
              "Each API will have its own implementation function and tool definition in the SAME file.\n\n"
              "REQUIREMENTS:\n"
              "1. Include ONLY APIs where 'active' field is true\n"
              "2. Create ONE implementation function per active API (e.g., async def deuda_fija_impl(...))\n"
              "3. Create ONE Tool definition per active API in the @server.list_tools() decorator\n"
              "4. Handle each API in the @server.call_tool() if/elif chain\n"
              "5. Use httpx AsyncClient with proper base_url configuration\n"
              "6. Handle both direct APIs and APIM Gateway APIs correctly\n"
              "7. Return all responses as JSON strings from implementation functions\n\n"
              "API CATALOG:\n" + api_catalog_json + "\n\n"
              "CRITICAL - FOLLOW THIS EXACT STRUCTURE:\n\n"
              "import os\n"
              "import urllib.parse\n"
              "import json\n"
              "from typing import Any\n"
              "import asyncio\n"
              "import httpx\n"
              "from dotenv import load_dotenv\n"
              "from mcp.server import Server\n"
              "from mcp.server.stdio import stdio_server\n"
              "from mcp.types import Tool, TextContent\n\n"
              "load_dotenv()\n\n"
              "# Configuration - Load ALL required environment variables\n"
              "APIM_TIMEOUT = float(os.getenv('APIM_TIMEOUT', '15.0'))\n"
              "BEARER_TOKEN = os.getenv('BEARER_TOKEN', '').strip()\n"
              "APIM_BASE_URL = os.getenv('APIM_BASE_URL', '').strip()\n"
              "APIM_SUBSCRIPTION_KEY = os.getenv('APIM_SUBSCRIPTION_KEY', '').strip()\n\n"
              "# Global HTTP client (will be initialized with proper base_url)\n"
              "_http_client: httpx.AsyncClient | None = None\n"
              "_apim_client: httpx.AsyncClient | None = None\n\n"
              "async def initialize_http_client() -> None:\n"
              "    '''Initialize HTTP clients for direct and APIM APIs'''\n"
              "    global _http_client, _apim_client\n"
              "    if _http_client is None:\n"
              "        _http_client = httpx.AsyncClient(timeout=APIM_TIMEOUT)\n"
              "    if _apim_client is None and APIM_BASE_URL:\n"
              "        _apim_client = httpx.AsyncClient(base_url=APIM_BASE_URL, timeout=APIM_TIMEOUT)\n\n"
              "async def cleanup_http_client() -> None:\n"
              "    '''Cleanup all HTTP clients'''\n"
              "    global _http_client, _apim_client\n"
              "    if _http_client:\n"
              "        await _http_client.aclose()\n"
              "        _http_client = None\n"
              "    if _apim_client:\n"
              "        await _apim_client.aclose()\n"
              "        _apim_client = None\n\n"
              "# ============================================================================\n"
              "# API IMPLEMENTATION FUNCTIONS - ONE PER ACTIVE API\n"
              "# ============================================================================\n\n"
              "# Example for direct API with Bearer token:\n"
              "# async def deuda_fija_impl(customerIdentification: str, type: str, document: str) -> str:\n"
              "#     '''Retrieves documents to pay for a customer'''\n"
              "#     if not _http_client:\n"
              "#         return json.dumps({'error': 'HTTP client not initialized'})\n"
              "#     \n"
              "#     url = 'https://apix.movistar.cl/paymentManagement/V3/documentsToPay'\n"
              "#     headers = {\n"
              "#         'Accept': 'application/json',\n"
              "#         'Authorization': f'Bearer {BEARER_TOKEN}'\n"
              "#     }\n"
              "#     params = {\n"
              "#         'customerIdentification': customerIdentification,\n"
              "#         'type': type,\n"
              "#         'document': document\n"
              "#     }\n"
              "#     try:\n"
              "#         resp = await _http_client.get(url, headers=headers, params=params)\n"
              "#         resp.raise_for_status()\n"
              "#         return resp.text\n"
              "#     except Exception as e:\n"
              "#         return json.dumps({'error': str(e)})\n\n"
              "# Example for APIM Gateway API (when useApimGateway=true and pythonExample provided):\n"
              "# async def listado_de_boletas_fija_impl(customerId: int, msisidn: str) -> str:\n"
              "#     '''Retrieves a list of invoices for a customer via APIM Gateway'''\n"
              "#     if not _apim_client:\n"
              "#         return json.dumps({'error': 'APIM client not initialized'})\n"
              "#     \n"
              "#     # Use path from pythonExample pattern: f'/bill/V2/retriveInvoice/{customerId}'\n"
              "#     path = f'/bill/V2/retriveInvoice/{customerId}'\n"
              "#     headers = {\n"
              "#         'Accept': 'application/json',\n"
              "#         'Ocp-Apim-Subscription-Key': APIM_SUBSCRIPTION_KEY\n"
              "#     }\n"
              "#     params = {'msisidn': msisidn}\n"
              "#     try:\n"
              "#         resp = await _apim_client.get(path, headers=headers, params=params)\n"
              "#         resp.raise_for_status()\n"
              "#         return resp.text\n"
              "#     except Exception as e:\n"
              "#         return json.dumps({'error': str(e)})\n\n"
              "async def main():\n"
              "    '''Main entry point - creates server with ALL active API tools'''\n"
              "    server = Server('telefonica-api-mcp')\n"
              "    \n"
              "    @server.list_tools()\n"
              "    async def list_tools() -> list[Tool]:\n"
              "        '''Return list of ALL active API tools'''\n"
              "        return [\n"
              "            # Example Tool 1 - Direct API:\n"
              "            # Tool(\n"
              "            #     name='deuda_fija',\n"
              "            #     description='Retrieves documents to pay for a customer.',\n"
              "            #     inputSchema={\n"
              "            #         'type': 'object',\n"
              "            #         'properties': {\n"
              "            #             'customerIdentification': {'type': 'string', 'description': '...'},\n"
              "            #             'type': {'type': 'string', 'description': '...'},\n"
              "            #             'document': {'type': 'string', 'description': '...'}\n"
              "            #         },\n"
              "            #         'required': ['customerIdentification', 'type', 'document']\n"
              "            #     }\n"
              "            # ),\n"
              "            # Example Tool 2 - APIM Gateway API:\n"
              "            # Tool(\n"
              "            #     name='listado_de_boletas_fija',\n"
              "            #     description='Retrieves a list of invoices for a customer.',\n"
              "            #     inputSchema={\n"
              "            #         'type': 'object',\n"
              "            #         'properties': {\n"
              "            #             'customerId': {'type': 'integer', 'description': '...'},\n"
              "            #             'msisidn': {'type': 'string', 'description': '...'}\n"
              "            #         },\n"
              "            #         'required': ['customerId', 'msisidn']\n"
              "            #     }\n"
              "            # )\n"
              "            # ... ADD ALL OTHER ACTIVE APIS HERE\n"
              "        ]\n"
              "    \n"
              "    @server.call_tool()\n"
              "    async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:\n"
              "        '''Route tool calls to appropriate implementation functions'''\n"
              "        # Example routing:\n"
              "        # if name == 'deuda_fija':\n"
              "        #     result = await deuda_fija_impl(\n"
              "        #         customerIdentification=arguments.get('customerIdentification'),\n"
              "        #         type=arguments.get('type'),\n"
              "        #         document=arguments.get('document')\n"
              "        #     )\n"
              "        #     return [TextContent(type='text', text=result)]\n"
              "        # elif name == 'listado_de_boletas_fija':\n"
              "        #     result = await listado_de_boletas_fija_impl(\n"
              "        #         customerId=arguments.get('customerId'),\n"
              "        #         msisidn=arguments.get('msisidn')\n"
              "        #     )\n"
              "        #     return [TextContent(type='text', text=result)]\n"
              "        # elif name == 'another_api':\n"
              "        #     result = await another_api_impl(...)\n"
              "        #     return [TextContent(type='text', text=result)]\n"
              "        # else:\n"
              "        #     raise ValueError(f'Unknown tool: {name}')\n"
              "        pass\n"
              "    \n"
              "    await initialize_http_client()\n"
              "    \n"
              "    try:\n"
              "        async with stdio_server() as (read_stream, write_stream):\n"
              "            await server.run(read_stream, write_stream, server.create_initialization_options())\n"
              "    finally:\n"
              "        await cleanup_http_client()\n\n"
              "if __name__ == '__main__':\n"
              "    asyncio.run(main())\n\n"
              "CRITICAL INSTRUCTIONS:\n\n"
              "1. STRUCTURE:\n"
              "   - Generate ONE file with ALL active APIs\n"
              "   - Each active API gets its own async implementation function\n"
              "   - All tools listed in ONE @server.list_tools() return statement\n"
              "   - All tool routing in ONE @server.call_tool() if/elif/else chain\n\n"
              "2. API TYPES - Handle both correctly:\n\n"
              "   A) DIRECT APIs (no useApimGateway or useApimGateway=false):\n"
              "      - Use _http_client (not _apim_client)\n"
              "      - Use FULL URL from 'endpoint' field\n"
              "      - Parse sampleCurl for headers:\n"
              "        * If sampleCurl has 'Authorization: Bearer', add: 'Authorization': f'Bearer {BEARER_TOKEN}'\n"
              "        * If sampleCurl has other headers, include them\n"
              "      - For GET: use params dict\n"
              "      - For POST with form data: use data dict with Content-Type: application/x-www-form-urlencoded\n\n"
              "   B) APIM GATEWAY APIs (useApimGateway=true):\n"
              "      - Use _apim_client (already configured with base_url=APIM_BASE_URL)\n"
              "      - Use RELATIVE path (from pythonExample or sampleCurl path part)\n"
              "      - Example: f'/bill/V2/retriveInvoice/{customerId}'\n"
              "      - Headers: 'Accept': 'application/json', 'Ocp-Apim-Subscription-Key': APIM_SUBSCRIPTION_KEY\n"
              "      - Follow pythonExample pattern EXACTLY if provided\n"
              "      - Parse sampleCurl for path structure (IDs in path vs query params)\n\n"
              "3. URL PATH HANDLING:\n"
              "   - Parse sampleCurl to detect path parameters\n"
              "   - Example: 'curl .../retriveInvoice/181696144?msisidn=...' means:\n"
              "     * customerId goes in PATH: f'/bill/V2/retriveInvoice/{customerId}'\n"
              "     * msisidn goes in PARAMS: params={'msisidn': msisidn}\n"
              "   - Use urllib.parse.quote() for URL encoding path parameters if needed\n\n"
              "4. INPUT PARAMETER MAPPING:\n"
              "   - Map each 'inputs' field to function parameters\n"
              "   - Use exact names from 'inputs'[].name\n"
              "   - Use exact types: 'int' -> int, 'string' -> str, 'boolean' -> bool\n"
              "   - For parameters in path, don't add to params dict\n"
              "   - For parameters in query string, add to params dict\n\n"
              "5. ERROR HANDLING:\n"
              "   - Wrap all HTTP calls in try/except\n"
              "   - Return JSON error objects: json.dumps({'error': 'message', 'details': ...})\n"
              "   - Check if clients are initialized\n"
              "   - Handle httpx.TimeoutException, httpx.HTTPError, general Exception\n\n"
              "6. RESPONSE HANDLING:\n"
              "   - Return resp.text for successful responses (already JSON string)\n"
              "   - Return json.dumps(...) for error responses\n"
              "   - Do NOT parse JSON unless needed for error handling\n\n"
              "7. IMPORTANT - NO DECORATORS MISTAKES:\n"
              "   - NEVER use server.add_tool() - it doesn't exist\n"
              "   - MUST use @server.list_tools() decorator\n"
              "   - MUST use @server.call_tool() decorator\n\n"
              "Generate ONLY the complete Python code. No explanations, no markdown, no comments outside the code - just pure Python code.")

    
    return prompt


def generate_mcp_server_code():
    """Main function to generate MCP server code using Azure OpenAI."""
    
    print("Starting MCP Server Code Generation...")
    print("=" * 80)
    
    # Step 1: Read API catalog
    print("\n[Step 1] Reading API catalog...")
    api_catalog_path = r"C:\TelefonicaProcessAgent\Data\api_catalog_modified_1765230841788.json"
    
    try:
        with open(api_catalog_path, 'r', encoding='utf-8') as f:
            api_catalog = json.load(f)
        print(f"✓ Loaded {len(api_catalog.get('apis', []))} APIs from catalog")
        
        # Check for active APIs
        active_apis = [api for api in api_catalog.get('apis', []) if api.get('active', False)]
        print(f"✓ Found {len(active_apis)} active APIs:")
        for api in active_apis:
            print(f"  - {api['name']}: {api['description']}")
        
        if not active_apis:
            print("⚠ Warning: No active APIs found in catalog!")
            return
        
        # Create filtered catalog with only active APIs
        filtered_catalog = {
            "apis": active_apis,
            "lastModified": api_catalog.get("lastModified", ""),
            "modifiedBy": api_catalog.get("modifiedBy", "")
        }
            
    except FileNotFoundError:
        print(f"✗ Error: API catalog file not found at {api_catalog_path}")
        return
    except json.JSONDecodeError as e:
        print(f"✗ Error: Invalid JSON in API catalog: {e}")
        return
    
    # Step 2: Create prompt
    print("\n[Step 2] Creating Azure OpenAI prompt...")
    prompt = create_mcp_generation_prompt(filtered_catalog)
    print(f"✓ Prompt created ({len(prompt)} characters)")
    
    # Step 3: Set up Azure OpenAI client
    print("\n[Step 3] Setting up Azure OpenAI client...")
    
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    
    if not azure_endpoint or not api_key:
        print("✗ Error: Azure OpenAI credentials not found in environment variables")
        print("   Please set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY in .env file")
        print("\n   Example .env file:")
        print("   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/")
        print("   AZURE_OPENAI_API_KEY=your-api-key")
        print("   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4")
        return
    
    print(f"✓ Endpoint: {azure_endpoint}")
    print(f"✓ Deployment: {deployment_name}")
    print(f"✓ API Version: {api_version}")
    
    client = AzureOpenAI(
        azure_endpoint=azure_endpoint,
        api_key=api_key,
        api_version=api_version
    )
    
    # Step 4: Call Azure OpenAI
    print("\n[Step 4] Calling Azure OpenAI to generate MCP server code...")
    print("⏳ This may take a minute...")
    
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert Python developer specializing in MCP server development. Generate clean, production-ready code."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=4000
        )
        
        generated_code = response.choices[0].message.content
        
        # Clean up the code if it has markdown formatting
        if "```python" in generated_code:
            generated_code = generated_code.split("```python")[1].split("```")[0].strip()
        elif "```" in generated_code:
            generated_code = generated_code.split("```")[1].split("```")[0].strip()
        
        print(f"✓ Generated {len(generated_code)} characters of code")
        print(f"✓ Tokens used: {response.usage.total_tokens}")
        
    except Exception as e:
        print(f"✗ Error calling Azure OpenAI: {e}")
        return
    
    # Step 5: Save the generated code
    print("\n[Step 5] Saving generated MCP server code...")
    
    # Create output directory if it doesn't exist
    output_dir = r"C:\TelefonicaProcessAgent\Data\SourceDesigned"
    os.makedirs(output_dir, exist_ok=True)
    
    # Delete all existing files in the output directory (except the API catalog)
    print("🗑️  Deleting old files from output directory...")
    try:
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            # Skip the API catalog file
            if os.path.isfile(file_path) and not filename.startswith('api_catalog'):
                os.remove(file_path)
                print(f"   Deleted: {filename}")
        print("✓ Old files deleted successfully")
    except Exception as e:
        print(f"⚠️  Warning: Could not delete some files: {e}")
    
    # Use a unique name without timestamp numbers
    output_filename = "telefonica_mcp_server.py"
    output_path = os.path.join(output_dir, output_filename)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(generated_code)
        print(f"✓ Code saved to: {output_path}")
        
        # Also save a metadata file
        metadata = {
            "generated_at": datetime.now().isoformat(),
            "api_catalog_file": api_catalog_path,
            "active_apis_count": len(active_apis),
            "active_apis": [api['name'] for api in active_apis],
            "tokens_used": response.usage.total_tokens,
            "model": deployment_name
        }
        
        metadata_path = os.path.join(output_dir, "telefonica_mcp_metadata.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        print(f"✓ Metadata saved to: {metadata_path}")
        
    except Exception as e:
        print(f"✗ Error saving files: {e}")
        return
    
    print("\n" + "=" * 80)
    print("✓ MCP Server Generation Complete!")
    print("\nNext steps:")
    print(f"1. Review the generated code at: {output_path}")
    print("2. Create a .env file with required environment variables:")
    print("   BEARER_TOKEN=your-bearer-token")
    print("   APIM_TIMEOUT=15.0")
    print("3. Install dependencies: pip install httpx python-dotenv mcp")
    print("4. Test the MCP server")
    print("=" * 80)


if __name__ == "__main__":
    generate_mcp_server_code()
