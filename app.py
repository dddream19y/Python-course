from flask import Flask, render_template, request, session
import requests
import time
import markdown  # 用來處理 **粗體** 等格式
import os
import secrets

app = Flask(__name__)

# 設定 Secret Key 才能使用 Flask 的 session 功能
# 在生產環境中應該設定為固定的亂數，但在這裡我們每次重啟隨機產生即可
app.secret_key = secrets.token_hex(16)

# Agent Server 的設定 (統一管理，方便以後修改)
AGENT_SERVER_URL = "http://localhost:8000"
APP_NAME = "my-first-ai-agent"
USER_ID = "somebody"  # 這裡未來可以改成真實的使用者 ID

@app.route("/")
def home():
    # 1. 初始化 Session (解決多使用者衝突問題)
    if "session_id" not in session:
        session["session_id"] = str(time.time())
    
    current_session = session["session_id"]
    
    # 2. 通知 Agent Server 建立新對話
    try:
        requests.post(
            f"{AGENT_SERVER_URL}/apps/{APP_NAME}/users/{USER_ID}/sessions/{current_session}",
            headers={"Content-Type": "application/json"},
            json={},
            timeout=5 # 設定 timeout 避免網頁卡死
        )
    except requests.exceptions.RequestException:
        print("Warning: Agent server might be down or unreachable.")

    return render_template("index.html")


@app.route("/call_llm", methods=["POST"])
def call_llm():
    if request.method == "POST":
        user_message = request.form.get("message", "") # 使用 .get 避免報錯
        print(f"User: {user_message}")

        # 取得當前使用者的 session_id
        current_session = session.get("session_id", str(time.time()))

        try:
            # 3. 發送請求給 Agent
            payload = {
                "app_name": APP_NAME,
                "user_id": USER_ID,
                "session_id": current_session,
                "new_message": {
                    "role": "user",
                    "parts": [{"text": user_message}],
                },
            }
            
            response = requests.post(
                f"{AGENT_SERVER_URL}/run", 
                headers={"Content-Type": "application/json"}, 
                json=payload
            )
            response.raise_for_status() # 如果 API 回傳 4xx/5xx 錯誤會直接跳到 except

            # 4. 解析 Agent 回傳的複雜 JSON (呼叫獨立函式處理)
            result_html = parse_agent_response(response.json())
            return result_html

        except Exception as e:
            print(f"Error calling LLM: {e}")
            return "<div style='color:red;'>⚠️ 發生錯誤：無法連接到 AI Agent，請確認 Server 是否已啟動。</div>"

    return ""

def parse_agent_response(response_json):
    """
    專門負責解析 Agent 回傳的 JSON，並轉成漂亮的 HTML。
    這樣主程式邏輯會比較乾淨。
    """
    result_text = ""
    
    for item in response_json:
        # 安全取值，避免 KeyError
        content = item.get("content", {})
        parts = content.get("parts", [])
        
        for part in parts:
            # === 情況 A: 工具呼叫 (Function Call) ===
            if "functionCall" in part:
                func_name = part["functionCall"].get("name", "Unknown Tool")
                args = part["functionCall"].get("args", {})
                
                # 美化顯示
                args_html = ", ".join([f"<b>{k}</b>: {v}" for k, v in args.items()])
                result_text += (
                    f"<div style='background-color: #f0f0f0; padding: 8px; border-radius: 5px; margin: 5px 0; color: #555; font-size: 0.9em;'>"
                    f"🔧 <b>正在呼叫工具：</b> {func_name}<br>"
                    f"<span style='margin-left: 20px;'>參數：{args_html}</span>"
                    f"</div>"
                )

            # === 情況 B: 工具回傳 (Function Response) ===
            elif "functionResponse" in part:
                resp_data = part["functionResponse"].get("response", {})
                resp_content = "工具執行完畢"

                # 嘗試抓取各種可能的回傳格式
                if "report" in resp_data:
                    resp_content = resp_data["report"]
                elif "result" in resp_data:
                    # 處理 FastMCP 標準回傳結構
                    inner_content = resp_data["result"].get("content", [])
                    if inner_content and "text" in inner_content[0]:
                        resp_content = inner_content[0]["text"]
                elif "content" in resp_data:
                    inner_content = resp_data["content"]
                    if inner_content and "text" in inner_content[0]:
                        resp_content = inner_content[0]["text"]

                result_text += (
                    f"<div style='background-color: #e8f5e9; padding: 8px; border-radius: 5px; margin: 5px 0; color: #2e7d32; font-size: 0.9em;'>"
                    f"✅ <b>工具回傳：</b> {resp_content}"
                    f"</div>"
                )

            # === 情況 C: 一般文字對話 (Markdown 轉 HTML) ===
            elif "text" in part:
                raw_text = part["text"]
                # 這裡就是解決 **符號問題的關鍵！
                html_text = markdown.markdown(raw_text)
                result_text += f"<div class='message-text'>{html_text}</div>"

    return result_text
