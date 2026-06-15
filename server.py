from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

mcp = FastMCP("Calculator")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers and return their sum."""
    return a + b

"""
Tool: add

Description:
Add two numbers and return their sum.

Parameters:
- a (int)
- b (int)

Returns:
- int

"""


@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract the second number from the first and return the result."""
    return a - b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers and return the product."""
    return a * b

@mcp.tool()
def divide(a: int, b: int) -> float:
    """Divide the first number by the second and return the quotient."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

if __name__ == "__main__":
    mcp.run()