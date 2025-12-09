# Telefonica Agent Designer

Sistema completo de generación y orquestación de agentes MCP (Model Context Protocol) para integración con APIs de Telefónica.

## 📋 Descripción

Este proyecto automatiza la generación de servidores MCP y clientes unificados desde un catálogo de APIs, permitiendo orquestar flujos de trabajo empresariales complejos de manera eficiente.

## 🎯 Características

- **Generación Automática de Servidores MCP**: Crea servidores MCP desde catálogos de APIs JSON
- **Clientes Unificados**: Genera métodos async tipados para cada API
- **Orquestación de Procesos**: Ejecuta flujos de trabajo con paso de datos entre APIs
- **Integración Azure OpenAI**: Usa GPT-4 para generación inteligente de código
- **Trazabilidad Completa**: Logging detallado y resultados en JSON

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.10+
- Azure OpenAI API key
- Acceso a APIs de Telefónica (APIM)

### Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/jorgelunams/telefonicaagentdesigner.git
cd telefonicaagentdesigner
```

2. Crear entorno virtual:
```bash
python -m venv agentdesignerenv
agentdesignerenv\Scripts\activate  # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
copy .env.sample .env
# Editar .env con tus credenciales reales
```

### Uso

#### Paso 1: Generar Servidor MCP
```bash
python mcp_servers_generator.py
```

#### Paso 2: Generar Cliente Unificado
```bash
python mcp_client_generator.py
```

#### Paso 3: Ejecutar Orquestación
```bash
python process_orchestrator_main.py
```

## 📂 Estructura del Proyecto

```
telefonicaagentdesigner/
├── mcp_servers_generator.py      # Generador de servidores MCP
├── mcp_client_generator.py       # Generador de clientes unificados
├── process_orchestrator_main.py  # Orquestador de procesos
├── build_package.py              # Script de empaquetado
├── requirements.txt              # Dependencias Python
├── .env.sample                   # Plantilla de configuración
├── .gitignore                    # Archivos ignorados por Git
└── GUIA_PROCESO_COMPLETO.md      # Documentación detallada
```

## 📖 Documentación

Consulta [GUIA_PROCESO_COMPLETO.md](GUIA_PROCESO_COMPLETO.md) para:
- Diagramas completos del flujo de trabajo
- Explicación detallada de cada componente
- Ejemplos de uso
- Solución de problemas

## 🔧 Configuración

### Variables de Entorno Requeridas

```bash
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4

# Telefónica APIM
APIM_BASE_URL=https://your-apim.azure-api.net
APIM_SUBSCRIPTION_KEY=your_subscription_key
```

## 🛠️ APIs Implementadas

- **deuda_fija**: Obtener detalles de deuda del cliente
- **listado_de_boletas_fija**: Listar facturas del cliente
- **retrieve_invoice_link**: Obtener enlace de descarga de factura

## 📊 Flujo de Trabajo

```
api_catalog.json
    ↓
mcp_servers_generator.py (Genera Servidor MCP)
    ↓
telefonica_mcp_server.py
    ↓
mcp_client_generator.py (Genera Cliente)
    ↓
telefonica_mcp_client.py
    ↓
process_orchestrator_main.py (Orquesta Proceso)
    ↓
orchestrator_results.json
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## ⚠️ Seguridad

- **NUNCA** commits archivos `.env` con credenciales reales
- Usa `.env.sample` como plantilla sin datos sensibles
- Revisa `.gitignore` antes de hacer commit
- Rota credenciales si fueron expuestas accidentalmente

## 📝 Licencia

Copyright (c) Microsoft. All rights reserved.

## 📧 Contacto

Jorge Luna - [@jorgelunams](https://github.com/jorgelunams)

Project Link: [https://github.com/jorgelunams/telefonicaagentdesigner](https://github.com/jorgelunams/telefonicaagentdesigner)
