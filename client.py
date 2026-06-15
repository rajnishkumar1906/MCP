import asyncio
import json
import os
import re
from dotenv import load_dotenv
from google import genai
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

class GeminiClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)

    def generate_response(self, prompt):
        prompt = (
            f"Given the following user input, determine which tool to call and with what parameters. "
            f"User input: {prompt} "
            f"Available tools: add, subtract, multiply, divide. "
            f"Output ONLY a JSON object like this example: "
            f'{{"tool_name": "multiply", "parameters": {{"a": 6, "b": 7}}}} '
            f"For input 'add 5 and 3' output: "
            f'{{"tool_name": "add", "parameters": {{"a": 5, "b": 3}}}} '
            f"Return only the JSON, no explanation or markdown."
        )
        response = self.client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        raw = response.text
        clean = re.sub(r"```(?:json)?\s*|\s*```", "", raw).strip()
        return json.loads(clean)


        
async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"- {tool.name} :: {tool.description}") 

            ai = GeminiClient(api_key)

            while True:
                user_input = input("Enter a command: ")
                if user_input.lower() == "exit":
                    break

                response = ai.generate_response(user_input)
                print("Gemini response:", response)

                result = await session.call_tool(
                    name=response["tool_name"],  
                    arguments=response["parameters"]
                )

                print(f"{response['tool_name']}({response['parameters']}) = {result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())