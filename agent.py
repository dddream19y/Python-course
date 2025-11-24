import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters, SseConnectionParams
import requests
import os
from dotenv import load_dotenv, dotenv_values

# Load environment variables from .env file
load_dotenv()

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.
    Args:
        city (str): The name of the city for which to retrieve the weather report.
        The city name must be in English.
    Returns:
        dict: status and result or error msg.
    """
    # if city.lower() == "new york":
    #     return {
    #         "status": "success",
    #         "report": (
    #             "The weather in New York is sunny with a temperature of 25 degrees"
    #             " Celsius (77 degrees Fahrenheit)."
    #         ),
    #     }
    # else:
    #     return {
    #         "status": "error",
    #         "error_message": f"Weather information for '{city}' is not available.",
    #     }
    api_key = os.getenv("OPEN_WEATHER_MAP_API_KEY")
    if not api_key:
        return {
            "status": "error",
            "error_message": "API key for OpenWeatherMap is not set.",
        }
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        print(data)
        if data["cod"] != 200:
            return {
                "status": "error",
                "error_message": f"Weather information for '{city}' is not available.",
            }
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        report = (
            f"The weather in {city} is {weather_description} with a temperature of "
            f"{temperature} degrees Celsius."
        )
        return {"status": "success", "report": report}
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"An error occurred while fetching the weather data: {str(e)}",
        }


def get_current_time(tz_identifier: str) -> dict:
    """Returns the current time in a specified time zone identifier.
    Args:
        tz_identifier (str): The time zone identifier for which to retrieve the current time.
        ex. "America/New_York", "Asia/Taipei", etc.
    Returns:
        dict: status and result or error msg.
    """

    # city_taiwan = ["taipei", "zhongli", "taoyuan", "kaohsiung", "taichung"]

    # if city.lower() == "new york":
    #     tz_identifier = "America/New_York"
    # elif city.lower() in city_taiwan:
    #     tz_identifier = "Asia/Taipei"
    # else:
    #     return {
    #         "status": "error",
    #         "error_message": (f"Sorry, I don't have timezone information for {city}."),
    #     }
    try:
        tz = ZoneInfo(tz_identifier)
        now = datetime.datetime.now(tz)
        report = f'The current time is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
        return {"status": "success", "report": report}
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"An error occurred while fetching the current time: {str(e)}",
        }
    
# def read_ncu_calendar() -> dict:
#     """
#     When a student from National Central University asks which days have classes, you should answer, for example: "No class on 9/29 due to Mid-Autumn Festival."
#     Reads the NCU academic calendar file and returns its content.
#     Returns:
#         dict: status and result or error msg.
#     """
#     # 直接回傳固定內容
#     return {"status": "success", "calendar": "中央大學行事曆9/29, 10/6不上課"}

#-------------老師提供的範例---------------------------
def get_ncu_calendar() -> dict:
    """Returns the NCU(中央大學) academic calendar 行事曆.
    Returns:
        dict: status and result or error msg.
    """
    try:
        # Fetch the NCU academic calendar from a reliable source
        return {"status": "success", "calendar": "9/29, 10/6 不上課"}
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"An error occurred while fetching the NCU calendar: {str(e)}",
        }
#----------------------------------------------------

root_agent = LlmAgent(
    name="weather_time_agent",
    model="gemini-2.0-flash-lite",
    description=("Agent to answer questions about the time and weather in a city."),
    instruction=(
        """
        You are a helpful agent who can answer user questions about the time and weather in a city.
        When you call a tool, you must use English for the city name.
        當使用者的需求跟檔案存取有關時，請先取得 list_allowed_directories 的結果。
        這個資料夾就是預設檔案存取的位置。
        請用繁體中文回答問題。
        """
    ),
    tools=[
        get_weather,
        get_current_time,
        #read_ncu_calendar,
        get_ncu_calendar, 
        MCPToolset(
            # Use StdioServerParameters for local process communication
            connection_params=StdioServerParameters(
                command="npx",  # Command to run the server
                args=[
                    "-y",  # Arguments for the command
                    "@modelcontextprotocol/server-filesystem",
                    "C:\\Users\\JINGYI\\Desktop\\AIshare",
                ],
            ),
            # tool_filter=[
            #     "read_file",
            #     "list_directory",
            # ],  # Optional: filter specific tools
            # For remote servers, you would use SseServerParams instead:
            # connection_params=SseServerParams(url="http://remote-server:port/path", headers={...})
        ),
        # 連接 UV MCP server
        MCPToolset(
            connection_params=StdioServerParameters(
                command="C:\\Users\\JINGYI\\.local\\bin\\uv.exe",
                args=[
                    "--directory",
                    "C:\\Users\\JINGYI\\Desktop\\1013Weather2mood",
                    "run",
                    "server.py",
                ],
            ),
        # Optional: Filter which tools from the MCP server are exposed
        ),
        # 連接 CoinGecko MCP server
        MCPToolset(
            # Use StdioServerParameters for local process communication
            connection_params=SseConnectionParams(
                url="https://mcp.api.coingecko.com/sse",  # URL for the SSE server
            ),
            # tool_filter=[
            #     "read_file",
            #     "list_directory",
            # ],  # Optional: filter specific tools
            # For remote servers, you would use SseServerParams instead:
            # connection_params=SseServerParams(url="http://remote-server:port/path", headers={...})
        ),
        # 連接 127.0.0.1 MCP server(someone_Saying)
        MCPToolset(
            # Use StdioServerParameters for local process communication
            connection_params=SseConnectionParams(
                url="http://127.0.0.1:5002/sse",  # URL for the SSE server
            ),
            # tool_filter=[
            #     "get_simple_price",
            # ],  # Optional: filter specific tools
            # For remote servers, you would use SseServerParams instead:
            # connection_params=SseServerParams(url="http://remote-server:port/path", headers={...})
        ),
    ],
)
