"""Wolfram|Alpha MCP Server implementation."""

import os
import urllib.parse
from typing import Optional
import requests
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the FastMCP server
mcp = FastMCP(name="wolframalpha-llm")

WOLFRAM_BASE_URL = "https://www.wolframalpha.com/api/v1/llm-api"

def get_app_id() -> str:
    """Get Wolfram|Alpha App ID from environment variable."""
    app_id = os.getenv("WOLFRAM_APP_ID")
    if not app_id:
        raise ValueError("WOLFRAM_APP_ID environment variable is required")
    return app_id


@mcp.tool()
def query_wolfram(
    query: str, 
    maxchars: Optional[int] = None,
    units: Optional[str] = None,
    location: Optional[str] = None
) -> dict:
    """
    Query the Wolfram|Alpha LLM API for computational results and knowledge.
    
    IMPORTANT USAGE GUIDELINES:
    
    SUPPORTED TOPICS:
    - Mathematics: calculations, derivatives, integrals, equations, statistics
    - Physics: constants, formulas, unit conversions, physical properties  
    - Chemistry: elements, compounds, reactions, molecular properties
    - Geography: countries, cities, populations, geographic data
    - History: dates, events, historical figures, timelines
    - Art: artists, artworks, cultural information
    - Astronomy: celestial objects, astronomical data, space facts
    - General knowledge: facts, comparisons, data analysis
    
    QUERY OPTIMIZATION:
    - Convert complex questions to simple keyword queries when possible
      Example: "How many people live in France?" → "France population"
    - Use English only - translate non-English queries before sending
    - Keep queries concise and specific for best results
    - For multiple data properties, make separate calls for each property
    
    MATHEMATICAL NOTATION:
    - Always use proper exponent notation: "6*10^14" (NEVER "6e14")
    - Use single-letter variable names only (e.g., x, y, n, n1, n_1)
    - Use named physical constants without substitution (e.g., "speed of light")
    - Include spaces in compound units (e.g., "Ω m" for ohm*meter)
    - For equations with units, consider solving without units first
    
    OUTPUT HANDLING:
    - Results may include image URLs - display with Markdown: ![URL]
    - Mathematical formulas use proper Markdown formatting
    - Never mention knowledge cutoff dates (Wolfram may have recent data)
    - If results seem irrelevant, the API may suggest alternative assumptions
    
    TROUBLESHOOTING:
    - Invalid queries return suggestions for corrections
    - Authentication errors indicate App ID issues
    - Status 501 means query couldn't be interpreted (may include suggestions)
    
    Args:
        query: Natural language query in English (mathematical, scientific, factual)
        maxchars: Maximum response characters (default: 6800, can be reduced for shorter answers)
        units: Unit system preference ("metric", "imperial", etc.)
        location: Geographic context for location-dependent queries
        
    Returns:
        Dictionary with 'success' boolean and either 'result' (string) or 'error' details
        
    Examples:
        query_wolfram("derivative of x^2")
        query_wolfram("population of Tokyo", maxchars=1000)  
        query_wolfram("speed of light in km/s")
        query_wolfram("solve x^2 + 3x + 2 = 0")
        query_wolfram("weather in Paris", location="Paris, France")
        query_wolfram("10 largest countries by area")
    """
    try:
        app_id = get_app_id()
        
        # Build parameters
        params = {
            "input": query,
            "appid": app_id
        }
        
        if maxchars is not None:
            params["maxchars"] = str(maxchars)
        if units:
            params["units"] = units
        if location:
            params["location"] = location
            
        # Make the API request
        response = requests.get(WOLFRAM_BASE_URL, params=params, timeout=30)
        
        # Handle different HTTP status codes
        if response.status_code == 200:
            return {
                "success": True,
                "query": query,
                "result": response.text,
                "characters": len(response.text)
            }
        elif response.status_code == 501:
            return {
                "success": False,
                "error": "Input could not be interpreted",
                "status_code": 501,
                "query": query,
                "suggestion": response.text if response.text else None
            }
        elif response.status_code == 400:
            return {
                "success": False,
                "error": "Bad request - missing or invalid input parameter",
                "status_code": 400,
                "query": query
            }
        elif response.status_code in [401, 403]:
            error_text = response.text.lower()
            if "invalid appid" in error_text:
                error_msg = "Invalid App ID"
            elif "appid missing" in error_text:
                error_msg = "App ID missing"
            else:
                error_msg = "Authentication error"
                
            return {
                "success": False,
                "error": error_msg,
                "status_code": response.status_code,
                "query": query
            }
        else:
            return {
                "success": False,
                "error": f"Unexpected status code: {response.status_code}",
                "status_code": response.status_code,
                "query": query,
                "response_text": response.text
            }
            
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timed out after 30 seconds",
            "query": query
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Network error: {str(e)}",
            "query": query
        }
    except ValueError as e:
        return {
            "success": False,
            "error": str(e),
            "query": query
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "query": query
        }


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()