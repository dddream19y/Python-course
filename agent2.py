import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters, SseConnectionParams
import requests
import os
from dotenv import load_dotenv, dotenv_values

# Load environment variables from .env file
load_dotenv()

# --- 1. 原有的工具函數 (保留) ---

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.
    Args:
        city (str): The name of the city for which to retrieve the weather report.
        The city name must be in English.
    Returns:
        dict: status and result or error msg.
    """
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
        print(data) # Debug用
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

# --- 2. 設定 Brave Search Tool (新增) ---
# 確保環境變數中有 BRAVE_API_KEY，這對 npx 啟動的 server 至關重要
if os.getenv("BRAVE_API_KEY"):
    brave_api_key = os.getenv("BRAVE_API_KEY")
else:
    print("Warning: BRAVE_API_KEY not found in environment variables.")
    brave_api_key = ""

# --- 3. 定義 Agent ---

root_agent = LlmAgent(
    name="travel_planner_agent", # 改個名字比較符合主題
    model="gemini-2.0-flash-lite",
    description=("一個專業的旅遊行程規劃 Agent，能查詢天氣、搜尋景點並產生行程表。"),
    instruction=(
        """
        你是一位專業且貼心的旅遊行程規劃師。
        
        你的主要任務是協助使用者規劃完美的旅遊行程。你可以使用以下工具：
        1. **get_weather**: 查詢目的地天氣。請務必先查天氣，晴天安排戶外，雨天安排室內。
        2. **brave_search**: 當你需要尋找具體的景點、餐廳評價、或最新的旅遊資訊時，請使用此工具搜尋。
        3. **filesystem**: 用於將最終的行程表寫入使用者的桌面 (請先 list_allowed_directories 確認路徑)。
        4. **travel_equipment_server** (本地): 根據天氣查詢必備物品 (這是你原本的 Weather2mood 改的)。
        5. **travel_luck_server** (遠端): 每天給使用者一個旅遊運勢 (這是你原本的 Saying 改的)。

        **回答準則：**
        * 請一律用**繁體中文**回答。
        * 呼叫工具時，城市名稱請使用英文 (例如 Taipei, Tainan)。
        * 規劃行程後，主動詢問使用者是否要將行程表存成檔案。
        """
    ),
    tools=[
        # 1. 基礎工具
        get_weather,
        get_current_time,
        
        # 2. 檔案系統 (Filesystem MCP)
        MCPToolset(
            connection_params=StdioServerParameters(
                command="npx",
                args=[
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    "C:\\Users\\JINGYI\\Desktop\\AIshare", # 你的桌面分享路徑
                ],
            ),
        ),

        # 3. [新增] Brave Search MCP (搜尋景點用)
        MCPToolset(
            connection_params=StdioServerParameters(
                command="npx",
                args=[
                    "-y",
                    "@modelcontextprotocol/server-brave-search",
                ],
                # 這裡非常重要！必須把 Key 傳進去給 npx 跑起來的 process
                env={
                    "BRAVE_API_KEY": brave_api_key,
                    **os.environ # 把其他的環境變數也一併傳進去比較保險
                }
            ),
        ),

        # 4. [自建本地] 旅遊裝備檢查 (原 Weather2mood)
        # 請確認你的 server.py 已經改成旅遊邏輯
        MCPToolset(
            connection_params=StdioServerParameters(
                command="C:\\Users\\JINGYI\\.local\\bin\\uv.exe",
                args=[
                    "--directory",
                    "C:\\Users\\JINGYI\\Desktop\\1013Weather2mood", # 確認路徑對不對
                    "run",
                    "server.py",
                ],
            ),
        ),

        # 5. [自建遠端] 旅遊運勢 (原 Saying Server)
        # 這是連線到你自己電腦開的 ngrok 或 localhost (sse)
        MCPToolset(
            connection_params=SseConnectionParams(
                url="http://127.0.0.1:5002/sse", 
            ),
        ),
        
        # CoinGecko 暫時註解掉，除非你要做「匯率換算」功能
        # MCPToolset(
        #     connection_params=SseConnectionParams(
        #         url="https://mcp.api.coingecko.com/sse",
        #     ),
        # ),
    ],
)
