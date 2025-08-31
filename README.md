# Wolfram|Alpha MCP Server

A Model Context Protocol (MCP) server that provides access to the Wolfram|Alpha LLM API, allowing AI assistants to perform computational queries and get structured mathematical, scientific, and factual information.

## Features

- Query the Wolfram|Alpha LLM API with natural language
- **Unit conversion prompts** with intelligent unit suggestions
- **Smart completions** for 40+ physical quantity categories (769+ units)
- Support for abbreviations, plurals, and technical units
- Proper error handling for common API issues
- Support for optional parameters (character limits, units, location)
- Easy integration with Claude Desktop and other MCP clients

## Usage

### Configuration Example

Add to your Claude Desktop configuration file (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "wolframalpha": {
      "command": "uv",
      "args": [
        "--directory",
        "path/to/server",
        "run",
        "python",
        "-m",
        "wolframalpha_mcp_server.server"
      ],
      "env": {
        "WOLFRAM_APP_ID": "your_app_id_here"
      }
    }
  }
}
```

### Standalone
```bash
# Using uv
uv run python -m wolframalpha_mcp_server.server

# Or directly
python -m wolframalpha_mcp_server.server
```

## Development Setup

1. **Get a Wolfram|Alpha App ID**
   - Visit https://developer.wolframalpha.com/portal/myapps/
   - Sign up or log in with your Wolfram ID
   - Create a new app and copy the App ID

2. **Install dependencies**
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -e .
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your Wolfram|Alpha App ID
   ```


## Available Tools

### query_wolfram

Query the Wolfram|Alpha LLM API for computational results and knowledge across multiple domains.

**Supported Topics:**
- **Mathematics**: calculations, derivatives, integrals, equations, statistics
- **Physics**: constants, formulas, unit conversions, physical properties
- **Chemistry**: elements, compounds, reactions, molecular properties
- **Geography**: countries, cities, populations, geographic data
- **History**: dates, events, historical figures, timelines
- **Art**: artists, artworks, cultural information
- **Astronomy**: celestial objects, astronomical data, space facts
- **General knowledge**: facts, comparisons, data analysis

**Parameters:**
- `query` (required): Natural language query in English
- `maxchars` (optional): Maximum response characters (default: 6800)
- `units` (optional): Unit system preference ("metric", "imperial", etc.)
- `location` (optional): Geographic context for location-dependent queries

**Best Practices:**
- **Simplify queries**: "How many people live in France?" → "France population"
- **Use proper notation**: "6*10^14" (never "6e14")
- **Single-letter variables**: x, y, n, n1, n_1
- **Named constants**: "speed of light" (not numerical values)
- **Compound units**: "Ω m" (with spaces)
- **Multiple properties**: Make separate calls for each data property

**Examples:**
```
# Mathematical queries
query_wolfram("derivative of x^2")
query_wolfram("solve x^2 + 3x + 2 = 0")
query_wolfram("integral sin(x) from 0 to pi")

# Scientific queries  
query_wolfram("speed of light in km/s")
query_wolfram("molecular weight of caffeine")
query_wolfram("density of gold")

# Data queries
query_wolfram("France population", maxchars=1000)
query_wolfram("largest countries by area")
query_wolfram("weather in Paris", location="Paris, France")

# Unit conversions
query_wolfram("100 fahrenheit to celsius", units="metric")
query_wolfram("50 miles to kilometers")
```

## Error Handling

The server handles common API errors gracefully:
- **501**: Input could not be interpreted (may include suggestions)
- **400**: Bad request or missing parameters
- **403**: Authentication errors (invalid or missing App ID)
- Network timeouts and connection errors

## Development

Run tests:
```bash
uv run python test.py
```

## License

This project is open source. Please refer to the Wolfram|Alpha API terms of service for usage restrictions.