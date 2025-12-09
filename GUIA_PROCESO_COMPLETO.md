# Guía Completa del Proceso de Generación y Orquestación de Agentes MCP

## 📋 Descripción General

Este documento describe el proceso completo para generar servidores MCP (Model Context Protocol) desde un catálogo de APIs y orquestar su ejecución en flujos de trabajo empresariales para Telefónica.

---

## 🎯 Diagrama del Flujo de Trabajo Completo

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PROCESO COMPLETO DE GENERACIÓN                       │
│                        Y ORQUESTACIÓN DE AGENTES MCP                         │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ PASO 0: ENTRADA - CATÁLOGO DE APIs                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  📄 api_catalog_modified_1765230841788.json                                 │
│  ┌────────────────────────────────────────────────────────────┐            │
│  │ {                                                           │            │
│  │   "apis": [                                                 │            │
│  │     {                                                       │            │
│  │       "name": "deuda_fija",                                 │            │
│  │       "description": "Obtener deuda del cliente",           │            │
│  │       "httpMethod": "POST",                                 │            │
│  │       "endpoint": "/api/debt/fixed",                        │            │
│  │       "active": true,                                       │            │
│  │       "inputs": [...],                                      │            │
│  │       "outputs": [...]                                      │            │
│  │     },                                                      │            │
│  │     {...más APIs...}                                        │            │
│  │   ]                                                         │            │
│  │ }                                                           │            │
│  └────────────────────────────────────────────────────────────┘            │
│                                                                              │
│  Ubicación: C:\TelefonicaProcessAgent\Data\                                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PASO 1: GENERACIÓN DEL SERVIDOR MCP                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  🔧 mcp_servers_generator.py                                                │
│  ┌────────────────────────────────────────────────────────────┐            │
│  │                                                             │            │
│  │  1. Lee api_catalog.json                                   │            │
│  │  2. Limpia archivos antiguos (excepto api_catalog*)        │            │
│  │  3. Envía catálogo completo a Azure OpenAI (GPT-4)         │            │
│  │  4. Genera código Python del servidor MCP                  │            │
│  │  5. Implementa herramientas para cada API activa           │            │
│  │  6. Configura clientes HTTP (httpx)                        │            │
│  │  7. Maneja autenticación (Bearer Token, APIM)              │            │
│  │                                                             │            │
│  └────────────────────────────────────────────────────────────┘            │
│                                                                              │
│  Comando: python mcp_servers_generator.py                                   │
│  Ubicación: C:\TelefonicaProcessAgent\source\Agents\AgentDesigner\          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ SALIDA PASO 1: SERVIDOR MCP GENERADO                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  📄 telefonica_mcp_server.py (7,622 caracteres)                             │
│  ┌────────────────────────────────────────────────────────────┐            │
│  │ import asyncio                                              │            │
│  │ import httpx                                                │            │
│  │ from mcp.server import Server                               │            │
│  │ from mcp.types import Tool, TextContent                     │            │
│  │                                                             │            │
│  │ server = Server("telefonica-mcp-server")                    │            │
│  │                                                             │            │
│  │ @server.list_tools()                                        │            │
│  │ async def list_tools() -> list[Tool]:                       │            │
│  │     return [                                                │            │
│  │         Tool(name="deuda_fija", ...),                       │            │
│  │         Tool(name="listado_de_boletas_fija", ...),          │            │
│  │         Tool(name="retrieve_invoice_link", ...)             │            │
│  │     ]                                                       │            │
│  │                                                             │            │
│  │ @server.call_tool()                                         │            │
│  │ async def call_tool(name: str, arguments: dict):            │            │
│  │     # Implementación de cada API                            │            │
│  └────────────────────────────────────────────────────────────┘            │
│                                                                              │
│  ✅ 3 Herramientas implementadas:                                           │
│     • deuda_fija                                                            │
│     • listado_de_boletas_fija                                               │
│     • retrieve_invoice_link                                                 │
│                                                                              │
│  Ubicación: C:\TelefonicaProcessAgent\Data\SourceDesigned\                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PASO 2: GENERACIÓN DEL CLIENTE UNIFICADO                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  🔧 mcp_client_generator.py                                                 │
│  ┌────────────────────────────────────────────────────────────┐            │
│  │                                                             │            │
│  │  1. Lee telefonica_mcp_server.py completo                  │            │
│  │  2. Pasa código completo a Azure OpenAI (GPT-4)            │            │
│  │  3. OpenAI analiza las herramientas del servidor           │            │
│  │  4. Genera un método async por cada herramienta            │            │
│  │  5. Implementa comunicación MCP con agent_framework        │            │
│  │  6. Configura spawn de servidor como subproceso            │            │
│  │  7. Limpia archivos antiguos de clientes                   │            │
│  │                                                             │            │
│  └────────────────────────────────────────────────────────────┘            │
│                                                                              │
│  Comando: python mcp_client_generator.py                                    │
│  Ubicación: C:\TelefonicaProcessAgent\source\Agents\AgentDesigner\          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ SALIDA PASO 2: CLIENTE MCP UNIFICADO                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  📄 telefonica_mcp_client.py (6,194 caracteres)                             │
│  ┌────────────────────────────────────────────────────────────┐            │
│  │ from agent_framework import MCPStdioTool                    │            │
│  │ from agent_framework.azure import AzureOpenAIChatClient     │            │
│  │                                                             │            │
│  │ async def create_mcp_tool():                                │            │
│  │     """Inicia telefonica_mcp_server.py como subproceso"""  │            │
│  │     return MCPStdioTool(                                    │            │
│  │         command="python",                                   │            │
│  │         args=["telefonica_mcp_server.py"]                   │            │
│  │     )                                                       │            │
│  │                                                             │            │
│  │ async def call_deuda_fija(...):                             │            │
│  │     """Método para API deuda_fija"""                        │            │
│  │     # Crea agente con Azure OpenAI                          │            │
│  │     # Llama herramienta del servidor MCP                    │            │
│  │     # Retorna respuesta JSON                                │            │
│  │                                                             │            │
│  │ async def call_listado_de_boletas_fija(...):                │            │
│  │     """Método para API listado_de_boletas_fija"""           │            │
│  │                                                             │            │
│  │ async def call_retrieve_invoice_link(...):                  │            │
│  │     """Método para API retrieve_invoice_link"""             │            │
│  └────────────────────────────────────────────────────────────┘            │
│                                                                              │
│  ✅ 3 Métodos async implementados (uno por API)                             │
│                                                                              │
│  Ubicación: C:\TelefonicaProcessAgent\Data\SourceDesigned\                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PASO 3: ORQUESTACIÓN DEL PROCESO DE NEGOCIO                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  🔧 process_orchestrator_main.py                                            │
│  ┌────────────────────────────────────────────────────────────┐            │
│  │                                                             │            │
│  │  class TelefonicaProcessOrchestrator:                       │            │
│  │                                                             │            │
│  │    async def step_1_get_customer_invoices():               │            │
│  │        ┌─────────────────────────────────────┐             │            │
│  │        │ • Llama call_listado_de_boletas_fija│             │            │
│  │        │ • Obtiene lista completa de facturas│             │            │
│  │        │ • Extrae datos del cliente          │             │            │
│  │        │ • Cuenta facturas abiertas/pagadas  │             │            │
│  │        │ • Almacena en self.results          │             │            │
│  │        └─────────────────────────────────────┘             │            │
│  │                      ▼                                      │            │
│  │    async def step_2_get_first_unpaid_invoice_link():       │            │
│  │        ┌─────────────────────────────────────┐             │            │
│  │        │ • Lee facturas del Paso 1           │             │            │
│  │        │ • Busca primera factura impaga      │             │            │
│  │        │ • Extrae billingInvoiceNumber       │             │            │
│  │        │ • Llama call_retrieve_invoice_link  │             │            │
│  │        │ • Obtiene enlace de descarga        │             │            │
│  │        └─────────────────────────────────────┘             │            │
│  │                      ▼                                      │            │
│  │    async def step_3_get_payment_details():                 │            │
│  │        ┌─────────────────────────────────────┐             │            │
│  │        │ • Usa RUT del cliente del Paso 1    │             │            │
│  │        │ • Llama call_deuda_fija             │             │            │
│  │        │ • Obtiene detalles de pago          │             │            │
│  │        │ • Maneja errores sin detener flujo  │             │            │
│  │        └─────────────────────────────────────┘             │            │
│  │                      ▼                                      │            │
│  │    def print_summary():                                    │            │
│  │        • Imprime resumen ejecutivo                         │            │
│  │        • Guarda orchestrator_results.json                  │            │
│  │                                                             │            │
│  └────────────────────────────────────────────────────────────┘            │
│                                                                              │
│  Comando: python process_orchestrator_main.py                               │
│  Ubicación: C:\TelefonicaProcessAgent\source\Agents\AgentDesigner\          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ SALIDA PASO 3: RESULTADOS DEL PROCESO                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  📊 Consola - Resumen Ejecutivo:                                            │
│  ┌────────────────────────────────────────────────────────────┐            │
│  │ ════════════════════════════════════════════════════════    │            │
│  │ PROCESS ORCHESTRATION SUMMARY                               │            │
│  │ ════════════════════════════════════════════════════════    │            │
│  │                                                             │            │
│  │ Customer Information:                                       │            │
│  │   Name: LOPEZ TORRES MIGUEL ALEJANDRO                       │            │
│  │   RUT: 198765432                                            │            │
│  │   Account ID: 45829374                                      │            │
│  │   Phone: 56987654321                                        │            │
│  │                                                             │            │
│  │ Invoice Summary:                                            │            │
│  │   Total invoices: 3                                         │            │
│  │     - 523_47_682957384: $9539 CLP (OPEN)                    │            │
│  │     - 523_47_682957383: $8756 CLP (PAID)                    │            │
│  │     - 523_47_682957382: $10484 CLP (PAID)                   │            │
│  │                                                             │            │
│  │ Execution Log:                                              │            │
│  │   [✓] Step 1: Get Customer Invoices                        │            │
│  │   [✓] Step 2: Get Unpaid Invoice Link                      │            │
│  │   [✓] Step 3: Get Payment Details                          │            │
│  │                                                             │            │
│  │ ✓ Results saved to: orchestrator_results.json              │            │
│  │ ════════════════════════════════════════════════════════    │            │
│  └────────────────────────────────────────────────────────────┘            │
│                                                                              │
│  📄 orchestrator_results.json                                               │
│  ┌────────────────────────────────────────────────────────────┐            │
│  │ {                                                           │            │
│  │   "customer_data": {                                        │            │
│  │     "customer_id": 45829374,                                │            │
│  │     "customer_name": "LOPEZ TORRES MIGUEL ALEJANDRO",       │            │
│  │     "customer_rut": "198765432"                             │            │
│  │   },                                                        │            │
│  │   "results": {                                              │            │
│  │     "invoices": { /* Datos completos */ },                 │            │
│  │     "invoice_link": { /* Enlace descarga */ },             │            │
│  │     "payment_details": { /* Detalles pago */ }             │            │
│  │   },                                                        │            │
│  │   "execution_log": [ /* Log completo */ ]                  │            │
│  │ }                                                           │            │
│  └────────────────────────────────────────────────────────────┘            │
│                                                                              │
│  Ubicación: C:\TelefonicaProcessAgent\Data\SourceDesigned\                  │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                      ARQUITECTURA DE EJECUCIÓN                               │
└─────────────────────────────────────────────────────────────────────────────┘

    process_orchestrator_main.py (AgentDesigner)
            │
            │ import telefonica_mcp_client
            ▼
    telefonica_mcp_client.py (SourceDesigned)
            │
            │ async def call_listado_de_boletas_fija(...)
            │     ├─ create_mcp_tool()
            │     │   └─ MCPStdioTool spawns subprocess
            │     │           │
            │     │           ▼
            │     └─ telefonica_mcp_server.py (SourceDesigned)
            │             │
            │             │ @server.call_tool()
            │             ▼
            │         httpx.AsyncClient
            │             │
            │             ▼
            │     ┌───────────────────────────────────────┐
            │     │  APIs Telefónica (APIM Gateway)       │
            │     │  https://telefonicaapimgt.azure-api.net│
            │     └───────────────────────────────────────┘
            │             │
            │             ▼ Response JSON
            │         telefonica_mcp_server.py
            │             │
            │             ▼ MCP Protocol (stdio)
            │         telefonica_mcp_client.py
            │             │
            │             ▼ Parsed Response
            │     process_orchestrator_main.py
            │             │
            │             ▼
            │     orchestrator_results.json

┌─────────────────────────────────────────────────────────────────────────────┐
│                          FLUJO DE DATOS                                      │
└─────────────────────────────────────────────────────────────────────────────┘

  PASO 1                    PASO 2                    PASO 3
  ───────                   ───────                   ───────
                                                      
  INPUT:                    INPUT:                    INPUT:
  • customerId              • billingInvoiceNumber    • customerRut
  • msisidn                 • isCyclicInvoice         • document
                                                      
     │                          │                         │
     ▼                          │                         │
  call_listado_de_            │                         │
  boletas_fija()              │                         │
     │                          │                         │
     ▼                          │                         │
  OUTPUT:                     │                         │
  ┌──────────────────┐        │                         │
  │ • customer_name  │────┐   │                         │
  │ • customer_rut   │    │   │                         │
  │ • invoices[]     │    │   │                         │
  │   - billing#     │────┼───┘                         │
  │   - status (O/P) │    │                             │
  │   - amount       │    │                             │
  └──────────────────┘    │                             │
                          │                             │
                          ▼                             │
                    Extrae primera                      │
                    factura impaga                      │
                          │                             │
                          ▼                             │
                  call_retrieve_invoice_link()          │
                          │                             │
                          ▼                             │
                    OUTPUT:                             │
                    ┌──────────────┐                    │
                    │ • invoice#   │                    │
                    │ • link       │                    │
                    │ • amount     │                    │
                    └──────────────┘                    │
                                                        │
                    Usa RUT extraído ───────────────────┘
                    del Paso 1                          │
                                                        ▼
                                                call_deuda_fija()
                                                        │
                                                        ▼
                                                  OUTPUT:
                                                  ┌──────────────┐
                                                  │ • debt_info  │
                                                  │ • payment    │
                                                  └──────────────┘
```

---

## 📂 Paso 1: Generación del Servidor MCP

### Archivo: `mcp_servers_generator.py`

**Propósito:** Genera un servidor MCP desde un catálogo de APIs JSON.

### Proceso:

1. **Lee el catálogo de APIs** desde:
   ```
   C:\TelefonicaProcessAgent\Data\api_catalog_modified_1765230841788.json
   ```

2. **Limpia archivos antiguos** en el directorio de salida:
   ```
   C:\TelefonicaProcessAgent\Data\SourceDesigned\
   ```
   - ⚠️ **Protección**: No elimina archivos que comienzan con `api_catalog`

3. **Envía el catálogo a Azure OpenAI** (GPT-4) con el siguiente prompt:
   - Analiza el catálogo JSON con las definiciones de APIs
   - Genera código Python para un servidor MCP
   - Implementa herramientas (tools) para cada API activa
   - Incluye manejo de autenticación (Bearer Token, APIM)
   - Configura clientes HTTP (httpx) con timeouts apropiados

4. **Genera dos archivos**:
   - `telefonica_mcp_server.py` - Código del servidor MCP
   - `telefonica_mcp_metadata.json` - Metadatos de las APIs implementadas

### Comando de Ejecución:

```bash
python mcp_servers_generator.py
```

### Salida Esperada:

```
✓ Archivos antiguos limpiados (excepto api_catalog*)
✓ Servidor MCP generado: telefonica_mcp_server.py
✓ Total de herramientas implementadas: 3
  - deuda_fija
  - listado_de_boletas_fija
  - retrieve_invoice_link
```

### Estructura del Servidor Generado:

```python
# telefonica_mcp_server.py

import asyncio
import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent

# Clientes HTTP
_http_client = httpx.AsyncClient(timeout=30.0)
_apim_client = httpx.AsyncClient(
    base_url="https://telefonicaapimgt.azure-api.net",
    timeout=30.0
)

# Definición de herramientas
@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(name="deuda_fija", ...),
        Tool(name="listado_de_boletas_fija", ...),
        Tool(name="retrieve_invoice_link", ...)
    ]

# Implementación de cada herramienta
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "deuda_fija":
        # Lógica de la API
    elif name == "listado_de_boletas_fija":
        # Lógica de la API
    # ...
```

---

## 📂 Paso 2: Generación del Cliente Unificado

### Archivo: `mcp_client_generator.py`

**Propósito:** Lee el código del servidor MCP y genera un cliente unificado con métodos async para cada herramienta.

### Proceso:

1. **Lee el servidor MCP generado**:
   ```python
   telefonica_mcp_server.py (7622 caracteres)
   ```

2. **Envía el código completo a Azure OpenAI** con instrucciones para:
   - Analizar todas las herramientas definidas en el servidor
   - Crear un método async por cada herramienta
   - Implementar la comunicación MCP usando `agent_framework`
   - Generar interfaz limpia para llamadas a las APIs

3. **Genera el cliente unificado**:
   ```
   telefonica_mcp_client.py
   ```

### Comando de Ejecución:

```bash
python mcp_client_generator.py
```

### Salida Esperada:

```
✓ Servidor MCP leído: telefonica_mcp_server.py (7622 chars)
✓ Cliente unificado generado: telefonica_mcp_client.py
✓ Métodos implementados:
  - call_deuda_fija(customerIdentification, type, document)
  - call_listado_de_boletas_fija(customerId, msisidn)
  - call_retrieve_invoice_link(billingInvoiceNumber, isCyclicInvoice)
```

### Estructura del Cliente Generado:

```python
# telefonica_mcp_client.py

from agent_framework import MCPStdioTool, AzureOpenAIChatClient

def create_mcp_tool() -> MCPStdioTool:
    """Crea la herramienta MCP que inicia el servidor."""
    return MCPStdioTool(
        name="telefonica_mcp_tool",
        description="Herramientas para APIs de Telefónica",
        server_script_path="telefonica_mcp_server.py"
    )

async def call_deuda_fija(
    customerIdentification: str,
    type: str,
    document: str
) -> dict:
    """Obtiene detalles de deuda del cliente."""
    mcp_tool = create_mcp_tool()
    agent = create_agent(mcp_tool)
    
    prompt = f"Call deuda_fija with parameters..."
    response = await agent.generate_response(prompt)
    
    return response

# Similar para call_listado_de_boletas_fija y call_retrieve_invoice_link
```

### Configuración Requerida (.env):

```bash
# C:\TelefonicaProcessAgent\Data\SourceDesigned\.env

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://workshopopenaisw.openai.azure.com
AZURE_OPENAI_API_KEY=<tu_api_key>
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-08-01-preview

# APIs Telefónica
BEARER_TOKEN=<tu_bearer_token>
APIM_BASE_URL=https://telefonicaapimgt.azure-api.net
APIM_SUBSCRIPTION_KEY=8d7b89290b7b46a6b5ccd4cceff11993
```

---

## 📂 Paso 3: Orquestación del Proceso de Negocio

### Archivo: `process_orchestrator_main.py`

**Propósito:** Ejecuta los métodos del cliente MCP en secuencia, pasando datos entre pasos para crear un flujo de trabajo completo.

### Arquitectura del Orquestador:

```python
class TelefonicaProcessOrchestrator:
    
    async def step_1_get_customer_invoices(customer_id, msisidn):
        """Paso 1: Obtener facturas del cliente"""
        
    async def step_2_get_first_unpaid_invoice_link():
        """Paso 2: Obtener enlace de factura impaga"""
        
    async def step_3_get_payment_details(document_id):
        """Paso 3: Obtener detalles de pago"""
        
    def print_summary():
        """Imprime resumen de ejecución"""
```

### Flujo de Datos entre Pasos:

#### **Paso 1: Obtener Facturas del Cliente**

**API:** `listado_de_boletas_fija`

**Entrada:**
- `customerId`: 45829374
- `msisidn`: "56987654321"

**Proceso:**
1. Llama a `call_listado_de_boletas_fija()`
2. Extrae información del cliente (nombre, RUT)
3. Cuenta facturas abiertas vs pagadas
4. Almacena resultados en `self.results['invoices']`

**Salida:**
```json
{
  "implInvoiceLists": [
    {
      "billingInvoiceNumber": "523_47_682957384",
      "totalAmount": 9539,
      "invoiceStatusInd": "O",  // O=Open, P=Paid
      "dueDate": "2025-12-01",
      "name": "LOPEZ TORRES MIGUEL ALEJANDRO",
      "customerRut": "198765432"
    },
    {
      "billingInvoiceNumber": "523_47_682957383",
      "totalAmount": 8756,
      "invoiceStatusInd": "P"
    },
    {
      "billingInvoiceNumber": "523_47_682957382",
      "totalAmount": 10484,
      "invoiceStatusInd": "P"
    }
  ]
}
```

**Logs:**
```
[✓] Step 1: Get Customer Invoices - success
    total_invoices: 3
    open_invoices: 1
    paid_invoices: 2
    customer_name: LOPEZ TORRES MIGUEL ALEJANDRO
```

---

#### **Paso 2: Obtener Enlace de Factura Impaga**

**API:** `retrieve_invoice_link`

**Entrada:**
- `billingInvoiceNumber`: Extraído del Paso 1 (primera factura con status 'O')
- `isCyclicInvoice`: true/false según el tipo de documento

**Proceso:**
1. Busca primera factura impaga en resultados del Paso 1
2. Extrae `billingInvoiceNumber` (ej: "523_47_682957384")
3. Llama a `call_retrieve_invoice_link()`
4. Si no hay facturas impagas, continúa sin error

**Salida:**
```json
{
  "invoice_number": "523_47_682957384",
  "amount": 9539,
  "due_date": "2025-12-01",
  "download_link": "https://..."
}
```

**Logs:**
```
[✓] Step 2: Get Unpaid Invoice Link - success
    invoice_number: 523_47_682957384
    amount: 9539
    due_date: 2025-12-01
```

---

#### **Paso 3: Obtener Detalles de Pago**

**API:** `deuda_fija`

**Entrada:**
- `customerIdentification`: RUT extraído del Paso 1
- `type`: "RUT"
- `document`: ID del cliente

**Proceso:**
1. Usa el RUT del cliente obtenido en Paso 1
2. Llama a `call_deuda_fija()`
3. Si falla (WAF blocking), continúa sin detener el proceso

**Logs:**
```
[✓] Step 3: Get Payment Details - success
    document_id: 45829374
```

---

### Comando de Ejecución:

```bash
python process_orchestrator_main.py
```

### Salida Completa del Proceso:

```
================================================================================
TELEFONICA PROCESS ORCHESTRATOR
================================================================================

This orchestrator will execute a complete business process:
1. Retrieve customer invoices
2. Get download link for unpaid invoice
3. Get payment details (if available)

Processing customer: 45829374 (Phone: 56987654321)
================================================================================

[⏳] Step 1: Get Customer Invoices - running
[✓] Step 1: Get Customer Invoices - success

[⏳] Step 2: Get Unpaid Invoice Link - running
[✓] Step 2: Get Unpaid Invoice Link - success

[⏳] Step 3: Get Payment Details - running
[✓] Step 3: Get Payment Details - success

================================================================================
PROCESS ORCHESTRATION SUMMARY
================================================================================

Customer Information:
  Name: LOPEZ TORRES MIGUEL ALEJANDRO
  RUT: 198765432
  Account ID: 45829374
  Phone: 56987654321

Invoice Summary:
  Total invoices: 3
    - 523_47_682957384: $9539 CLP (OPEN)
    - 523_47_682957383: $8756 CLP (PAID)
    - 523_47_682957382: $10484 CLP (PAID)

Execution Log:
  [✓] Step 1: Get Customer Invoices
  [✓] Step 2: Get Unpaid Invoice Link
  [✓] Step 3: Get Payment Details

✓ Results saved to: C:\TelefonicaProcessAgent\Data\SourceDesigned\orchestrator_results.json
================================================================================
```

### Archivo de Resultados Generado:

**Ubicación:** `C:\TelefonicaProcessAgent\Data\SourceDesigned\orchestrator_results.json`

**Contenido:**
```json
{
  "customer_data": {
    "customer_id": 45829374,
    "msisidn": "56987654321",
    "customer_name": "LOPEZ TORRES MIGUEL ALEJANDRO",
    "customer_rut": "198765432"
  },
  "results": {
    "invoices": { /* Datos completos de facturas */ },
    "invoice_link": { /* Enlace de descarga */ },
    "payment_details": { /* Detalles de pago */ }
  },
  "execution_log": [
    {
      "timestamp": "2025-12-08T15:30:00",
      "step": "Step 1: Get Customer Invoices",
      "status": "success",
      "data": { /* Datos del paso */ }
    }
    // ... más logs
  ]
}
```

---

## 🔧 Configuración del Entorno

### Requisitos Previos:

1. **Python 3.10+** instalado
2. **Paquetes requeridos**:
   ```bash
   pip install agent-framework
   pip install httpx
   pip install python-dotenv
   pip install openai
   ```

3. **Archivo .env** configurado en:
   ```
   C:\TelefonicaProcessAgent\Data\SourceDesigned\.env
   ```

### Variables de Entorno Críticas:

```bash
# Azure OpenAI (obligatorio)
AZURE_OPENAI_ENDPOINT=https://workshopopenaisw.openai.azure.com
AZURE_OPENAI_API_KEY=<tu_key>
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-08-01-preview

# Autenticación Telefónica (obligatorio)
APIM_SUBSCRIPTION_KEY=8d7b89290b7b46a6b5ccd4cceff11993
APIM_BASE_URL=https://telefonicaapimgt.azure-api.net

# Token Bearer (opcional - algunas APIs requieren)
BEARER_TOKEN=<tu_bearer_token>
```

---

## 📊 Resumen de APIs Implementadas

### 1. **deuda_fija**
- **Propósito:** Obtener detalles de deuda del cliente
- **Método:** POST
- **Endpoint:** `/api/debt/fixed`
- **Autenticación:** Bearer Token
- **Estado:** ⚠️ Puede estar bloqueado por WAF

### 2. **listado_de_boletas_fija**
- **Propósito:** Listar facturas del cliente
- **Método:** POST
- **Endpoint:** `/obp/pdd/ods/mobile/v1/api/clients/GetListInvoices`
- **Autenticación:** APIM Subscription Key
- **Estado:** ✅ Funcionando correctamente

### 3. **retrieve_invoice_link**
- **Propósito:** Obtener enlace de descarga de factura
- **Método:** GET
- **Endpoint:** `/obp/pdd/ods/mobile/v1/api/clients/RetrieveInvoiceLink`
- **Autenticación:** APIM Subscription Key
- **Estado:** ⚠️ Requiere formato correcto de número de factura

---

## 🎯 Casos de Uso

### Caso 1: Consulta de Facturas Pendientes

```python
# Ejecutar proceso completo
python process_orchestrator_main.py

# Resultado:
# - Lista de todas las facturas
# - Identifica facturas impagas
# - Obtiene enlace de descarga para pagar
```

### Caso 2: Análisis de Cuenta del Cliente

```python
# El orquestador obtiene:
# - Información del cliente (nombre, RUT)
# - Estado de todas las facturas
# - Montos adeudados y pagados
# - Enlaces de descarga disponibles
```

### Caso 3: Proceso de Cobro Automatizado

```python
# Flujo completo:
# 1. Identificar clientes con facturas impagas
# 2. Obtener detalles de cada factura
# 3. Generar enlaces de pago
# 4. Registrar resultados en JSON
```

---

## 🚀 Próximos Pasos y Mejoras

### Mejoras Recomendadas:

1. **Manejo de Errores Avanzado**
   - Reintentos automáticos con backoff exponencial
   - Logging detallado de errores de API
   - Notificaciones de fallos críticos

2. **Procesamiento en Lote**
   - Procesar múltiples clientes en paralelo
   - Cola de trabajos con prioridades
   - Generación de reportes consolidados

3. **Integración con Base de Datos**
   - Almacenar resultados en SQL/NoSQL
   - Historial de ejecuciones
   - Métricas de rendimiento

4. **API REST del Orquestador**
   - Exponer endpoints HTTP
   - Autenticación y autorización
   - Webhooks para notificaciones

5. **Monitoreo y Observabilidad**
   - Integración con Azure Monitor
   - Dashboards de métricas en tiempo real
   - Alertas automáticas

---

## 🛠️ Solución de Problemas

### Problema: Error 401 - Authentication Failed

**Causa:** Credenciales de Azure OpenAI incorrectas

**Solución:**
```bash
# Verificar .env
cat C:\TelefonicaProcessAgent\Data\SourceDesigned\.env

# Asegurar formato correcto del endpoint
AZURE_OPENAI_ENDPOINT=https://<nombre>.openai.azure.com
# NO usar: https://<nombre>.services.ai.azure.com
```

### Problema: WAF Blocking en deuda_fija

**Causa:** Web Application Firewall bloqueando la solicitud

**Solución:**
- Usar APIM Gateway en lugar de API directa
- Solicitar whitelist de IP
- Verificar Bearer Token válido

### Problema: 404 en retrieve_invoice_link

**Causa:** Formato incorrecto del número de factura

**Solución:**
```python
# Usar formato correcto desde listado_de_boletas_fija
billing_number = "523_47_682957384"  # ✅ Correcto
billing_number = "45829374-001"      # ❌ Incorrecto
```

### Problema: Timeout en MCP Client

**Causa:** Servidor MCP tarda en responder

**Solución:**
```python
# Aumentar timeout en httpx
_client = httpx.AsyncClient(timeout=60.0)  # Era 30.0
```

---

## 📝 Conclusión

Este sistema proporciona un framework completo para:

✅ **Generación automática** de servidores MCP desde catálogos de APIs  
✅ **Creación de clientes unificados** con métodos tipados  
✅ **Orquestación de procesos** con flujo de datos entre pasos  
✅ **Logging y trazabilidad** completa de ejecuciones  
✅ **Manejo robusto de errores** con continuación del proceso  

**Resultado:** Un sistema escalable y mantenible para integrar múltiples APIs de Telefónica en flujos de trabajo empresariales automatizados.

---

## 📧 Contacto y Soporte

Para preguntas o problemas con el sistema:
- Revisar logs de ejecución en `orchestrator_results.json`
- Verificar configuración en archivos `.env`
- Consultar documentación de Azure OpenAI y agent_framework

---

**Última actualización:** 8 de diciembre, 2025  
**Versión:** 1.0  
**Autor:** Sistema de Generación Automática de Agentes MCP
