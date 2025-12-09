# Copyright (c) Microsoft. All rights reserved.

import os
import json
import ast
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

"""
MCP Client Generator

This script:
1. Reads the telefonica_mcp_server.py Python code
2. Extracts all methods/tools from the MCP server
3. Generates ONE unified MCP client with methods for each server tool
4. Uses unique names (no timestamps)
"""


def extract_tools_from_mcp_server(server_code):
    """
    Parse the MCP server Python code and extract tool definitions.
    Returns a list of tool information dictionaries.
    """
    tools = []
    import re
    
    # Find all Tool(...) definitions using a pattern that captures complete Tool objects
    # Split by 'Tool(' but keep the delimiter
    parts = server_code.split('Tool(')
    
    for part in parts[1:]:  # Skip first part (before first Tool)
        try:
            # Find the closing parenthesis for this Tool
            # Count parentheses to find the matching closing one
            paren_count = 1
            end_idx = 0
            
            for i, char in enumerate(part):
                if char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1
                    if paren_count == 0:
                        end_idx = i
                        break
            
            if end_idx == 0:
                continue
                
            tool_content = part[:end_idx]
            
            # Extract name
            name_match = re.search(r"name=['\"]([^'\"]+)['\"]", tool_content)
            if not name_match:
                continue
            name = name_match.group(1)
            
            # Extract description
            desc_match = re.search(r"description=['\"]([^'\"]+)['\"]", tool_content)
            description = desc_match.group(1) if desc_match else ""
            
            # Extract inputSchema
            schema_start = tool_content.find('inputSchema=')
            if schema_start != -1:
                schema_content = tool_content[schema_start + len('inputSchema='):]
                
                # Count braces to get the complete dict
                brace_count = 0
                end_pos = 0
                
                for i, char in enumerate(schema_content):
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end_pos = i + 1
                            break
                
                schema_str = schema_content[:end_pos]
                
                try:
                    input_schema = ast.literal_eval(schema_str)
                except Exception as e:
                    print(f"⚠️  Warning: Could not parse schema for {name}: {e}")
                    input_schema = {}
            else:
                input_schema = {}
            
            tools.append({
                'name': name,
                'description': description,
                'inputSchema': input_schema
            })
            
        except Exception as e:
            print(f"⚠️  Warning: Error parsing tool section: {e}")
            continue
    
    return tools


def create_unified_client_prompt(server_code, server_filename):
    """Create prompt for generating a unified MCP client with all methods."""
    
    prompt = f"""You are an expert Python developer specializing in creating MCP clients using the agent_framework.

YOUR TASK: Read the complete MCP server code below and generate ONE unified MCP client file with methods for EACH tool defined in the server.

MCP SERVER FILE: {server_filename}
MCP SERVER LOCATION: C:\\TelefonicaProcessAgent\\Data\\SourceDesigned\\{server_filename}

MCP SERVER CODE:
```python
{server_code}
```

INSTRUCTIONS:
1. READ the MCP server code above carefully
2. IDENTIFY all Tool definitions in the @server.list_tools() decorator
3. For EACH tool found, extract:
   - Tool name
   - Tool description
   - Required input parameters from inputSchema
   - Parameter types
4. Generate ONE unified client with ONE async method per tool

REQUIREMENTS:
1. Create ONE unified client file with multiple async methods
2. Each method corresponds to ONE MCP server tool
3. Use agent_framework with MCPStdioTool to spawn the server as subprocess
4. Each method should:
   - Accept the required parameters for that specific tool
   - Create an agent with Azure OpenAI
   - Call the MCP server tool with the parameters
   - Return the parsed JSON response
5. Include a main() function that demonstrates calling each method
6. Use proper error handling and logging
7. Follow the EXACT structure provided in the example below

EXACT STRUCTURE TO FOLLOW:

import os
import json
from dotenv import load_dotenv
from agent_framework import ChatAgent, MCPStdioTool
from agent_framework.azure import AzureOpenAIChatClient

# Load environment variables
load_dotenv()

# Configuration
MCP_SERVER_PATH = r"C:\\TelefonicaProcessAgent\\Data\\SourceDesigned\\{server_filename}"
PYTHON_EXECUTABLE = os.getenv("PYTHON_PATH", "python")

async def create_mcp_tool():
    \"\"\"Create and return the MCP tool connected to the Telefonica MCP server.\"\"\"
    return MCPStdioTool(
        name="Telefonica API MCP Server",
        command=PYTHON_EXECUTABLE,
        args=[MCP_SERVER_PATH],
        env=os.environ.copy()
    )

async def create_agent(tool_name: str, instructions: str):
    \"\"\"Create an Azure OpenAI agent with the MCP tool.\"\"\"
    mcp_tool = await create_mcp_tool()
    
    return AzureOpenAIChatClient(
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview"),
        model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-4")
    ).create_agent(
        name=f"Telefonica_{{tool_name}}_Agent",
        instructions=instructions,
        tools=[mcp_tool]
    )

# ============================================================================
# API CLIENT METHODS - ONE PER MCP SERVER TOOL
# ============================================================================

# Generate one async method per tool following this pattern:
# async def call_TOOL_NAME(**kwargs) -> dict:
#     \"\"\"
#     Call the TOOL_NAME API via MCP server.
#     
#     Args:
#         param1: description
#         param2: description
#     
#     Returns:
#         dict: API response
#     \"\"\"
#     instructions = (
#         "You are an API assistant for [TOOL DESCRIPTION]. "
#         "Use the TOOL_NAME tool from the MCP server to call the API. "
#         "Pass all the provided parameters to the tool. "
#         "Return the raw response from the API."
#     )
#     
#     async with await create_agent("TOOL_NAME", instructions) as agent:
#         # Build the query with parameters
#         query = f"Call TOOL_NAME with parameters: {{json.dumps(kwargs)}}"
#         response = await agent.run(query)
#         
#         # Parse JSON response
#         try:
#             return json.loads(response.text)
#         except:
#             return {{"raw_response": response.text, "success": True}}

async def main():
    \"\"\"
    Main function demonstrating usage of all API methods.
    \"\"\"
    print("=" * 80)
    print("TELEFONICA MCP CLIENT - UNIFIED INTERFACE")
    print("=" * 80)
    
    # Example calls for each method (use sample data from tool schemas)
    # Add try/except blocks for each call
    
    print("\\n✅ All API calls completed!")
    print("=" * 80)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

CRITICAL INSTRUCTIONS:
1. Generate ONE method per tool from the tools list
2. Use exact tool names from the MCP server
3. Extract required parameters from inputSchema
4. Use proper type hints based on inputSchema types
5. Include docstrings with parameter descriptions
6. Handle responses as JSON when possible
7. Include example calls in main() with sample data
8. NO TIMESTAMPS in any names
9. Use descriptive method names based on tool names

Generate ONLY the complete Python code. No explanations, no markdown formatting - just pure Python code."""

    return prompt


def generate_unified_mcp_client():
    """Main function to generate unified MCP client."""
    
    print("=" * 80)
    print("UNIFIED MCP CLIENT GENERATOR")
    print("=" * 80)
    
    # Step 1: Locate the MCP server file
    print("\n[Step 1] Locating MCP server file...")
    output_dir = r"C:\TelefonicaProcessAgent\Data\SourceDesigned"
    mcp_server_filename = "telefonica_mcp_server.py"
    mcp_server_path = os.path.join(output_dir, mcp_server_filename)
    
    if not os.path.exists(mcp_server_path):
        print(f"✗ MCP server not found at: {mcp_server_path}")
        print("  Please run mcp_servers_generator.py first!")
        return
    
    print(f"✓ Found MCP server: {mcp_server_filename}")
    
    # Step 2: Read the complete MCP server code
    print("\n[Step 2] Reading MCP server code...")
    try:
        with open(mcp_server_path, 'r', encoding='utf-8') as f:
            server_code = f.read()
        print(f"✓ Read {len(server_code)} characters of server code")
    except Exception as e:
        print(f"✗ Error reading MCP server: {e}")
        return
    
    # Step 3: Set up Azure OpenAI
    print("\n[Step 3] Setting up Azure OpenAI client...")
    
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
    
    if not azure_endpoint or not api_key:
        print("✗ Azure OpenAI credentials not configured in .env")
        return
    
    print(f"✓ Using deployment: {deployment_name}")
    
    client = AzureOpenAI(
        azure_endpoint=azure_endpoint,
        api_key=api_key,
        api_version=api_version
    )
    
    # Step 4: Generate the unified client by passing the entire server code to OpenAI
    print("\n[Step 4] Generating unified MCP client code...")
    print("⏳ Azure OpenAI is reading the server code and creating the client...")
    
    prompt = create_unified_client_prompt(server_code, mcp_server_filename)
    
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert Python developer. Generate clean, production-ready code with proper error handling."
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
        
        # Clean markdown if present
        if "```python" in generated_code:
            generated_code = generated_code.split("```python")[1].split("```")[0].strip()
        elif "```" in generated_code:
            generated_code = generated_code.split("```")[1].split("```")[0].strip()
        
        print(f"✓ Generated {len(generated_code)} characters of code")
        print(f"✓ Tokens used: {response.usage.total_tokens}")
        
    except Exception as e:
        print(f"✗ Error calling Azure OpenAI: {e}")
        return
    
    # Step 5: Delete old client files from output directory (except server and metadata)
    print("\n[Step 5] Cleaning up old client files...")
    try:
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            # Delete old client files and orchestrator files, but keep server, metadata, and api_catalog
            if os.path.isfile(file_path) and (
                filename.startswith('mcp_client_') or 
                filename.startswith('master_orchestrator_') or
                filename.startswith('package_metadata_')
            ):
                os.remove(file_path)
                print(f"   Deleted: {filename}")
        print("✓ Cleanup complete")
    except Exception as e:
        print(f"⚠️  Warning: Could not delete some files: {e}")
    
    # Step 7: Save the unified client
    print("\n[Step 7] Saving unified MCP client...")
    
    client_filename = "telefonica_mcp_client.py"
    client_path = os.path.join(output_dir, client_filename)
    
    try:
        with open(client_path, 'w', encoding='utf-8') as f:
            f.write(generated_code)
        print(f"✓ Client saved to: {client_path}")
    except Exception as e:
        print(f"✗ Error saving client: {e}")
        return
    
    # Step 6: Save metadata
    print("\n[Step 6] Saving metadata...")
    
    from datetime import datetime
    metadata = {
        "generated_at": datetime.now().isoformat(),
        "mcp_server": mcp_server_filename,
        "mcp_client": client_filename,
        "server_code_length": len(server_code),
        "tokens_used": response.usage.total_tokens,
        "model": deployment_name
    }
    
    metadata_path = os.path.join(output_dir, "telefonica_mcp_metadata.json")
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    print(f"✓ Metadata saved to: {metadata_path}")
    
    # Final summary
    print("\n" + "=" * 80)
    print("✅ UNIFIED MCP CLIENT GENERATION COMPLETE!")
    print("=" * 80)
    print("\nGenerated Files:")
    print(f"  • MCP Server: {mcp_server_filename}")
    print(f"  • MCP Client: {client_filename}")
    print(f"  • Tokens used: {response.usage.total_tokens}")
    print(f"\nAll files in: {output_dir}")
    print("\nNext steps:")
    print("  1. Configure .env with Azure OpenAI credentials")
    print("  2. Set PYTHON_PATH environment variable")
    print(f"  3. Run: python {client_filename}")
    print("=" * 80)


if __name__ == "__main__":
    generate_unified_mcp_client()
