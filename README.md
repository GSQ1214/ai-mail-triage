# AI 客服信件分類器（AI Mail Triage）

使用 **Python + uv + Ollama** 將客服信件分類、排序優先度，並產生摘要與回覆建議。採用 Ollama **JSON Schema 結構化輸出**，符合 LLM 功能要求。另有 GitHub Actions 自動測試和 GitHub Pages 四頁作品展示。

## 功能

- 分類：帳務／技術支援／物流配送／退換貨／其他
- 優先度：高／中／低
- 繁體中文摘要及建議回覆
- 用 JSON Schema 指定模型輸出結構，並在 Python 再驗證一次
- 使用 `.env` 設定模型，不提交敏感資料

## 環境與安裝

1. 安裝 [uv](https://docs.astral.sh/uv/) 和 [Ollama](https://ollama.com/)。
2. 於終端機執行 `ollama pull llama3.2`。
3. 確認 Ollama 服務正在運作，必要時執行 `ollama serve`。
4. 於專案根目錄執行 `uv sync`。
5. 選用：複製 `.env.example` 為 `.env`，可設定 `OLLAMA_HOST`、`OLLAMA_MODEL`。本範例僅接受 localhost Ollama。

## 操作指令

```bash
uv run mail-triage --file examples/email.txt
uv run mail-triage --text "商品有瑕疵，我想退貨。"
uv run mail-triage --file examples/email.txt --output result.json
```

執行後會輸出 `category`、`priority`、`summary`、`suggested_reply` 四個 JSON 欄位。`examples/sample-output.json` 是**示意結果**；本機實測觀察請參閱作品網站「執行結果」。

## 測試

```bash
uv run python -m unittest discover -s tests -v
```

這些單元測試不需要模型啟動，會測試 JSON 欄位、合法性、錯誤處理及模擬 Ollama HTTP 請求。已在 Windows 實際執行模型並發現分類誤判；調整後的實際推論尚待重新驗證。

## GitHub Pages（Actions 自動部署）

1. 建立 GitHub Repository，把本專案所有檔案（包含 `.github/workflows/pages.yml`）push 到 `main`。
2. 前往 Repository → **Settings → Pages → Build and deployment → Source**，選擇 **GitHub Actions**。
3. 開啟 **Actions** 頁面，確認 `Test and deploy Pages` workflow 成功（綠燈）。
4. 部署網址通常是 `https://<你的帳號>.github.io/<repo>/`。

此 workflow 會先安裝 uv、執行測試，再上傳 `docs/` 與部署 GitHub Pages。網站使用相對路徑，在 repo 子路徑也能運作。

## 作品頁四頁

- `docs/index.html`：做了什麼
- `docs/run.html`：怎麼執行
- `docs/results.html`：本機實測轉錄、誤判分析與改進
- `docs/ai.html`：AI 使用說明

## AI 使用紀錄

- 使用 ChatGPT 協助產生此專案原始草稿、文字敘述、樣式與單元測試設計。
- 運作中的 LLM：本機 Ollama 模型（預設 `llama3.2`）。
- 已實測：Windows PowerShell 使用 `uv sync` 成功安裝、Ollama `llama3.2` 成功推論，實測回傳 JSON 四欄；但物流詢問被誤判為退換貨。
- 改進：補強分類邊界的提示詞、將 temperature 設為 0、補充模擬 API 與錯誤型別單元測試；模型改進後的真實準確率仍需後續測試。
- 驗證來源：使用者提供的終端機截圖，以及 GitHub Actions 執行紀錄。
- 注意：AI 生成的答案可能有誤，所有客服回覆都應人工核對。

## 安全與限制

`.gitignore` 排除 `.env`、虛擬環境與建置產物；只提交不含金鑰的 `.env.example`。不要將真實客戶個資上傳 GitHub。部署的靜態作品頁不會執行本地 LLM。模型輸出不一定穩定，請人工驗證。
