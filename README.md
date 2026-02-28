# algo-practice

以 **AI Agent + Skills** 為核心的演算法面試練習系統。目標是透過客製化技能模組，讓 AI 扮演專業技術面試官與教練，幫助你從 LeetCode Rating 1500 提升至 2000。

---

## 🛠️ Skills 架構

```
.agent/skills/
├── leetcode-fetcher/       # Step 1：題目環境自動建立
├── algo-interview-prep/    # Step 2：解題引導與教學
└── algo-progress-tracker/  # Step 3：弱點記錄與進度追蹤
```

### 1. `leetcode-fetcher` — 自動化題目環境建立

| 功能         | 說明                                                            |
| ------------ | --------------------------------------------------------------- |
| **來源支援** | `leetcode.com`、`neetcode.io`、或純文字描述                     |
| **自動分類** | 依核心解題邏輯歸類至 18 種題型之一                              |
| **檔名規則** | `00215._Kth_Largest_Element_In_An_Array.py`                     |
| **輸出路徑** | `{cwd}/{Category}/{檔名}.py`                                    |
| **核心限制** | ⛔ **嚴禁在此階段撰寫任何解題邏輯**，`Solution` 方法維持 `pass` |

### 2. `algo-interview-prep` — 白板面試模擬教練

引導流程分為 5 個步驟：

1. **題目分類** — 判斷屬於哪種題型（18 種）並分析 Edge Cases
2. **蘇格拉底引導** — 不直接給答案，用問題引導你自己推導思路
3. **多層次解法比較** — 從暴力解 → 最佳解，附帶複雜度分析
4. **練習題推薦** — 推薦 2-3 題漸進難度的配套題目
5. **自動呼叫 Progress Tracker** — 將本次弱點記錄入 `algo_check_list.md`

### 3. `algo-progress-tracker` — 個人學習紀錄系統

- 維護 **`algo_check_list.md`**（個人學習檔案）於當前工作目錄
- 記錄每道題的具體錯誤原因（例如：「忘記 `k > array.length` 邊界情況」）
- 分析是否**重蹈覆轍**或有所進步
- 本身的 `references/check_list.md` 是唯讀模板，**不會被修改**

---

## 🔄 典型工作流程

```
使用者提供題目 URL 或名稱
        ↓
[leetcode-fetcher] 抓取題目 → 建立分類目錄與 .py 檔案
        ↓
[algo-interview-prep] 引導思考 → 探討解法 → 分析複雜度
        ↓
[algo-progress-tracker] 自動記錄弱點 → 更新 algo_check_list.md
```

---

## 📁 題目分類（18 種題型）

| 題型                    | 題型                    |
| ----------------------- | ----------------------- |
| Arrays & Hashing        | Two Pointers            |
| Sliding Window          | Stack                   |
| Binary Search           | Linked List             |
| Trees                   | Heap / Priority Queue   |
| Backtracking            | Tries                   |
| Graphs                  | Advanced Graphs         |
| 1-D Dynamic Programming | 2-D Dynamic Programming |
| Greedy                  | Intervals               |
| Math & Geometry         | Bit Manipulation        |
