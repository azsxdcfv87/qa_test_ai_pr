import os
import sys
import re
import yaml
import google.generativeai as genai

# 打印所有環境變數
print("環境變數:")
for key, value in os.environ.items():
    print(f"{key}: {value}")

# 讀取環境變數
api_key = os.getenv("GOOGLE_API_KEY")
pr_title = os.getenv("PR_TITLE", "")
pr_body = os.getenv("PR_BODY", "")

print(f"PR_TITLE: {pr_title}")
print(f"PR_BODY: {pr_body}")

if not api_key:
    raise ValueError("API Key 未設定，請檢查 GitHub Secrets")

# 讀取測試標籤 YAML 檔案
try:
    with open('.github/data/test_data.yaml', 'r') as file:
        tags_data = yaml.safe_load(file)
    # 將標籤列表轉換為逗號分隔的字符串
    available_tags = ", ".join(tags_data.get('TEST_RANGE', []))
    print(f"成功讀取標籤: {available_tags}")
except Exception as e:
    print(f"讀取標籤檔案時發生錯誤: {e}")
    available_tags = "livestream, settings, following, login, register"  # 預設標籤，以防檔案讀取失敗

# 初始化 Google GenAI 客戶端
genai.configure(api_key=api_key)

# 生成 AI 分析內容
prompt = f"""
你是一位專業的軟體測試專家，請根據以下 PR 標題和描述，以及測試提供的現有 Tags，提供符合內容的自動化測試Tags。

重要規則：
1. 直接輸出 TEST_RANGE: login, register, following
2. 不要使用代碼塊（```）標記
3. 只輸出 TEST_RANGE 的內容，不需要其他解釋

PR 標題: {pr_title}
PR 內文: {pr_body}

可用的測試 Tags: {available_tags}
"""

try:
    # 使用 gemini-2.0-flash 模型生成內容
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            temperature=0.2,
            top_p=0.7,
            max_output_tokens=1024
        )
    )
    
    # 擷取 AI 建議
    suggestions = response.text
    print("AI 建議內容:")
    print(suggestions)
    
    # 儲存到檔案
    with open("ai_suggestions.txt", "w", encoding="utf-8") as f:
        f.write(f"🚀 **AI 自動化測試標籤建議**\n{suggestions}")
    
    # 嘗試匹配多種可能的 TEST_RANGE 格式
    test_range_match = re.search(r'TEST_RANGE:(.*?)(?:\n|$)', suggestions, re.DOTALL)
    if not test_range_match:
        # 如果上面的模式不匹配，嘗試其他模式
        test_range_match = re.search(r'TEST_RANGE[:=]\s*(.*?)(?:\n|$)', suggestions, re.DOTALL)

    if test_range_match:
      test_range = test_range_match.group(1).strip()
      
      # 移除可能的引號和代碼塊標記
      test_range = test_range.strip('`" ')
      
      # 保存乾淨的 TEST_RANGE 到檔案
      with open("test_range.txt", "w", encoding="utf-8") as f:
          f.write(test_range)
      print(f"成功提取並保存 TEST_RANGE: {test_range}")
        
except Exception as e:
    print(f"生成內容時發生錯誤: {e}")
    sys.exit(1)