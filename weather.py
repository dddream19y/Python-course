from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("travel_equipment")


@mcp.tool()
def get_travel_equipment(weather_status: str) -> str:
    """
    根據天氣狀況，回傳旅遊必備的裝備建議清單。
    Args:
        weather_status: 天氣狀況 (例如 "Clear", "Rain", "Clouds" 等，通常來自 get_weather 工具)
    回答時，請完全依據以下對應關係回答，不要有任何額外補充
    """
    status = weather_status.lower()


    keyword_map = {
        "rain": "請攜帶輕便雨衣, 雨傘",
        "drizzle": "請攜帶輕便雨衣, 雨傘",
        "thunderstorm": "請攜帶避雷裝備, 防水鞋",
        "snow": "請攜帶保暖衣物、手套、暖暖包",
        "fog": "反光衣物, 手電筒，視線不佳請小心行駛",  
        "mist": "反光衣物, 手電筒，視線不佳請小心行駛",
        "haze": "反光衣物, 手電筒，視線不佳請小心行駛",
        "clear": "請攜帶太陽眼鏡, 防曬乳，並記得多補充水分",
        "sun": "請攜帶太陽眼鏡, 防曬乳，並記得多補充水分",
        "cloud": "建議採【洋蔥式穿搭】，隨身帶件薄外套", 
        "overcast": "請攜帶輕便雨衣, 雨傘", 
    }

    matched_advice = []
    for key, advice in keyword_map.items():
        if key in status:
            matched_advice.append(advice)
            # 找到一個就停，避免太多建議 (可選)
            break
    
    # 4. 決定回傳內容
    if matched_advice:
        equipment = matched_advice[0]
    else:
        # 如果真的都沒對到，把原本的 status 顯示出來方便除錯
        equipment = f"無特別建議 (因為我沒辨識出 '{weather_status}' 對應的裝備)"

    return f"The weather is {weather_status}, recommended travel equipment: {equipment}."


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
