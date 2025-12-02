from fastmcp import FastMCP
from deep_translator import GoogleTranslator
import httpx

# 初始化 MCP Server
mcp = FastMCP("Frankfurter Currency Server")

BASE_URL = "https://api.frankfurter.dev/v1"

@mcp.tool()
async def get_exchange_rates(base: str = "EUR", symbols: str = None) -> str:
    """
    查詢最新的匯率。
    
    Args:
        base: 基準貨幣 (例如: USD, EUR, TWD)。預設為 EUR。
        symbols: (可選) 想要查詢的目標貨幣代碼，用逗號分隔 (例如: 'JPY,GBP')。若不填則回傳所有貨幣。
    """
    url = f"{BASE_URL}/latest"
    params = {"base": base.upper()}
    if symbols:
        params["symbols"] = symbols.upper()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # 格式化輸出讓 AI 更容易閱讀
            rates = data.get("rates", {})
            date = data.get("date")
            result = f"基準貨幣: {data.get('base')} (日期: {date})\n匯率列表:\n"
            for currency, rate in rates.items():
                result += f"- {currency}: {rate}\n"
            return result
            
        except httpx.HTTPStatusError as e:
            return f"API 請求錯誤: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"發生錯誤: {str(e)}"

@mcp.tool()
async def convert_currency(amount: float, from_curr: str, to_curr: str) -> str:
    """
    進行貨幣換算 (例如: 將 100 USD 換算成 TWD)。

    Args:
        amount: 金額數值 (例如: 100)
        from_curr: 持有貨幣代碼 (例如: USD)
        to_curr: 目標貨幣代碼 (例如: TWD)
    """
    url = f"{BASE_URL}/latest"
    # Frankfurter API 支援直接用 amount 參數做轉換
    params = {
        "amount": amount,
        "from": from_curr.upper(),
        "to": to_curr.upper()
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            rates = data.get("rates", {})
            # 取得目標貨幣的匯率數值
            converted_amount = rates.get(to_curr.upper())
            
            if converted_amount:
                return f"{amount} {from_curr.upper()} = {converted_amount} {to_curr.upper()} (日期: {data.get('date')})"
            else:
                return f"無法找到目標貨幣 {to_curr} 的匯率。"

        except httpx.HTTPStatusError as e:
            return f"API 請求錯誤: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"發生錯誤: {str(e)}"


@mcp.tool()
def get_translate(text: str, target_lang: str) -> str:
    """
    旅遊翻譯小幫手。可以將文字翻譯成指定語言。
    
    Args:
        text: 想翻譯的句子 (例如: "廁所在哪裡？", "這個多少錢？")
        target_lang: 目標語言代碼 (例如: "en" 是英文, "ja" 是日文, "ko" 是韓文, "th" 是泰文, "fr" 是法文)
    """
    try:
        # 自動偵測來源語言，翻譯成目標語言
        translator = GoogleTranslator(source='auto', target=target_lang)
        translated_text = translator.translate(text)
        
        return f"【翻譯結果】\n原文: {text}\n譯文 ({target_lang}): {translated_text}"
    except Exception as e:
        return f"翻譯失敗: {str(e)}"

    
if __name__ == "__main__":
    mcp.run(transport="stdio")
