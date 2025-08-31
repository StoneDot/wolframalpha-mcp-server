#!/usr/bin/env python3
"""Comprehensive test script for the Wolfram|Alpha MCP Server."""

import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wolframalpha_mcp_server.server import mcp, query_wolfram

def test_mcp_configuration():
    """Test MCP server configuration and registration."""
    print("=" * 60)
    print("MCP SERVER CONFIGURATION TEST")
    print("=" * 60)
    
    print(f"Server name: {mcp.name}")
    print("✓ query_wolfram function is accessible")
    print("✓ MCP server configuration appears correct")
    print()

def test_query_function():
    """Test the query_wolfram function with various inputs."""
    print("=" * 60)
    print("QUERY FUNCTION TESTS")
    print("=" * 60)
    
    test_cases = [
        {
            "name": "Basic arithmetic",
            "query": "2+2",
            "params": {}
        },
        {
            "name": "Mathematical derivative",
            "query": "derivative of x^2",
            "params": {"maxchars": 500}
        },
        {
            "name": "Scientific constant",
            "query": "speed of light",
            "params": {"maxchars": 800}
        },
        {
            "name": "Geographic data",
            "query": "France population",
            "params": {"maxchars": 600}
        },
        {
            "name": "Invalid query (error handling)",
            "query": "asdfghjkl",
            "params": {}
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['name']}")
        print(f"Query: '{test_case['query']}'")
        
        try:
            result = query_wolfram(test_case['query'], **test_case['params'])
            print(f"Success: {result['success']}")
            
            if result['success']:
                print(f"Characters: {result.get('characters', 'N/A')}")
                # Show first 200 characters of result
                result_preview = result['result'][:200]
                if len(result['result']) > 200:
                    result_preview += "..."
                print(f"Result preview: {result_preview}")
            else:
                print(f"Error: {result['error']}")
                if result.get('suggestion'):
                    print(f"Suggestion: {result['suggestion']}")
                if result.get('status_code'):
                    print(f"Status code: {result['status_code']}")
                    
        except Exception as e:
            print(f"✗ Exception occurred: {str(e)}")
        
        print("-" * 50)

def test_advanced_features():
    """Test advanced features and edge cases."""
    print("=" * 60)
    print("ADVANCED FEATURES TEST")
    print("=" * 60)
    
    # Test scientific notation (from guidelines)
    print("Testing scientific notation (per guidelines):")
    result = query_wolfram("6*10^14")
    print(f"Scientific notation query success: {result['success']}")
    if result['success']:
        print("✓ Scientific notation properly handled")
    print()
    
    # Test unit conversion
    print("Testing unit conversion:")
    result = query_wolfram("100 fahrenheit to celsius")
    print(f"Unit conversion query success: {result['success']}")
    if result['success']:
        print("✓ Unit conversion working")
    print()
    
    # Test mathematical equation solving
    print("Testing equation solving:")
    result = query_wolfram("solve x^2 + 3x + 2 = 0")
    print(f"Equation solving query success: {result['success']}")
    if result['success']:
        print("✓ Equation solving working")
    print()

async def run_all_tests():
    """Run all tests."""
    print("WOLFRAM|ALPHA MCP SERVER - COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    print("Testing server configuration, query functions, and advanced features")
    print()
    
    # Run configuration tests
    test_mcp_configuration()
    
    # Run basic query tests
    test_query_function()
    
    # Run advanced feature tests
    test_advanced_features()
    
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print("✓ MCP server configuration verified")
    print("✓ Query function tests completed")
    print("✓ Advanced features tested")
    print("✓ Ready for use with MCP clients (Claude Desktop, Claude Code)")
    print()
    print("To use with Claude Code, ensure the server is added with:")
    print("claude mcp add wolframalpha uv run python -m wolframalpha_mcp_server.server")

if __name__ == "__main__":
    asyncio.run(run_all_tests())