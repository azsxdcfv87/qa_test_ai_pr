import os
import sys
from google import genai

# 讀取環境變數
api_key = os.getenv("GOOGLE_API_KEY")
pr_title = os.getenv("PR_TITLE", "")
pr_body = os.getenv("PR_BODY", "")

if not api_key:
    raise ValueError("API Key 未設定，請檢查 GitHub Secrets")

# 初始化 Google GenAI 客戶端
genai.configure(api_key=api_key)

# 生成 AI 分析內容
prompt = f"""
你是一位專業的軟體測試專家，請根據以下 PR 標題和描述，提供適合的自動化測試建議（例如：單元測試、整合測試、E2E 測試、效能測試或安全測試），並解釋推薦的原因：
---
PR 標題: {pr_title}
PR 內文: {pr_body}
"""

try:
    # 使用 gemini-2.0-flash 模型生成內容
    response = genai.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        generation_config={
            "temperature": 0.2,
            "top_p": 0.7,
            "max_output_tokens": 1024
        }
    )
    
    # 擷取 AI 建議
    suggestions = response.text
    
    # 儲存到檔案
    with open("ai_suggestions.txt", "w", encoding="utf-8") as f:
        f.write(f"🚀 **AI 測試建議**\n{suggestions}")
    
except Exception as e:
    print(f"生成內容時發生錯誤: {e}")
    sys.exit(1)