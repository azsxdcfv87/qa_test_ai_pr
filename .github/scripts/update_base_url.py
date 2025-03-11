import os
import sys
import yaml
import re

# 讀取環境變數
pr_number = os.environ.get('GITHUB_EVENT_PULL_REQUEST_NUMBER', '')
pr_title = os.environ.get('PR_TITLE', '')
pr_body = os.environ.get('PR_BODY', '')

# 嘗試讀取測試數據 YAML 檔案
try:
    with open('.github/data/test_data.yaml', 'r') as file:
        test_data = yaml.safe_load(file)
    
    default_base_url = test_data.get('BASE_URL', [''])[0]
    print(f"預設 BASE_URL: {default_base_url}")
except Exception as e:
    print(f"讀取測試數據檔案時發生錯誤: {e}")
    default_base_url = 'https://swag.live/?lang=zh-tw'

# 檢查 PR 內容是否已有 BASE_URL
base_url_match = re.search(r'BASE_URL:\s*(.+)', pr_body)

if not base_url_match:
    # 如果沒有 BASE_URL，則添加預設值
    updated_pr_body = f"{pr_body}\n\nBASE_URL: {default_base_url}"
    
    # 使用 GitHub CLI 更新 PR 描述
    update_cmd = f"gh pr edit {pr_number} --body '{updated_pr_body}'"
    print(f"執行命令: {update_cmd}")
    os.system(update_cmd)
    
    print(f"已將預設 BASE_URL 添加到 PR 描述：{default_base_url}")
else:
    print("PR 描述中已存在 BASE_URL，無需修改")