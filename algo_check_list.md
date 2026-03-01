# 演算法面試準備進度與弱點追蹤 (Algorithm Progress & Weakness Tracker)

這份文件用於追蹤使用者在不同演算法題型上的掌握度、常犯錯誤以及思考盲點。
目的是讓使用者有意識地成長，清楚知道自己的弱項在哪裡。

## 題型掌握度與錯誤紀錄

- **Arrays & Hashing (陣列與雜湊)**
  - _熟練度評估：_ (例如：待加強 / 普通 / 熟練)
  - _常犯錯誤/思考盲點：_ (例如：常常忘記考慮陣列為空的邊界條件、不知道什麼時候該用 Hash Map 降低時間複雜度)
- **Two Pointers (雙指標)**
  - _熟練度評估：_
  - _常犯錯誤/思考盲點：_
- **Sliding Window (滑動窗口)**
  - _熟練度評估：_ 普通
  - _常犯錯誤/思考盲點：_
    - 初始直覺是「找全域最大最小相減」，未立即意識到時間線性要素（最小值可能出現在最大值之後）。
    - **Kadane's 差分方向踩坑**：實作時寫成 `prices[i-1] - prices[i]`（跌幅），應為 `prices[i] - prices[i-1]`（漲幅），需提醒才修正。
    - **Kadane's 換日機制**：未能立即想到 `current_sum < 0 → 歸零` 就是「放棄舊買入點、以今天為新起點」的語意，需引導才理解。
    - **與 1-D DP 的識別差異**：Sliding Window 的核心是「一段連續窗口的最佳值」，R 固定往右、L 按條件移動；1-D DP 則是「當前狀態依賴多個過去子問題」，且子問題範圍不一定連續（如 House Robber 不能選相鄰）。LC 121 雖然也可用 DP 解，但 dp[i] 只看 i-1，可壓縮成 Sliding Window，分類以最直觀解法為準。
    - **map 應存 index 而非次數**（LC 3）：初始直覺記錄出現次數，無法精確跳視窗；應改存「上次出現 index」才能一步定位 left 新起點。
    - **操作順序陷阱**（LC 3）：else 分支若先 `last_seen[ch] = right` 再讀 `last_seen[ch]`，讀到的是剛覆蓋的新值，導致 left 跳過頭；必須先用舊 index 計算 left，再更新 map。
    - **left 更新需取 max**（LC 3）：當重複字元的舊 index 已在視窗外（last_seen[ch] < left），若直接設 left = last_seen[ch]+1，left 會倒退。需 `left = max(left, last_seen[ch]+1)` 防止退縮。反例："abba"。
    - **else 分支不一定縮視窗**（LC 3）：若重複字元在視窗外，max 讓 left 不動，right 繼續前進，視窗反而長大；result 必須在 loop 末尾統一更新，不能只在 if 分支更新。
- **Stack (堆疊)**
  - _熟練度評估：_
  - _常犯錯誤/思考盲點：_
- **Binary Search (二分搜尋)**
  - _熟練度評估：_
  - _常犯錯誤/思考盲點：_
- **Linked List (連結串列)**
  - _熟練度評估：_
  - _常犯錯誤/思考盲點：_
- **Trees (樹)**
  - _熟練度評估：_
  - _常犯錯誤/思考盲點：_
- **Heap / Priority Queue (堆積 / 優先佇列)**
  - _熟練度評估：_ 普通
  - _常犯錯誤/思考盲點：_
    - Insert 條件一開始未考慮 heap 未滿（`size < k`）時需無條件 push，只記得「比 heap[0] 大才 push」，需提示才修正。
    - 對 `heapq` API 不熟悉（`heappush` / `heappop` / 初始化），需要查閱。
    - 未能立即識別 stateful streaming 場景（LC 703）與 batch 解法的介面差異：batch 是一次呼叫回傳答案，streaming 需要 class 持久化 heap 狀態，並透過 `add()` 逐次回傳。
    - **QuickSelect**：pivot 的目的（分割，與 k 無關）需提示才理解；`>=` vs `>` 在重複元素時可能退化成 O(n²) 未主動意識到。
    - **QuickSelect Index 轉換**：未能立即意識到 k 是 1-indexed（第 1 大 = 最大值），而降序排序後對應的 0-indexed 位置是 `k-1`，導致在 `_quickselect` 中與 pivot index `p` 比較時，不確定應寫 `p == k` 還是 `p == k-1`。需銘記：**第 k 大 → index k-1**。
- **Backtracking (回溯法)**
  - _熟練度評估：_
  - _常犯錯誤/思考盲點：_
- **Tries (字典樹)**
  - _熟練度評估：_
  - _常犯錯誤/思考盲點：_
- **Graphs (圖)**
  - _熟練度評估：_
  - _常犯錯誤/思考盲點：_
- **Advanced Graphs (進階圖論)**
  - _熟練度評估：_
  - _常犯錯誤/思考盲點：_
- **1-D Dynamic Programming (一維動態規劃)**
  - _熟練度評估：_
  - _常犯錯誤/思考盲點：_
    - **與 Sliding Window 的識別差異**：DP 適合「需要跳著選或非連續子問題」的場景（如 House Robber 的隔格選取）；若子問題只依賴「一段連續區間」，通常能用 Sliding Window 取代且更直觀。判斷口訣：當 dp 陣列可以滾動壓縮成一兩個變數時，優先考慮是否為 Sliding Window 問題。
- **2-D Dynamic Programming (二維動態規劃)**
  - _熟練度評估：_
  - _常犯錯誤/思考盲點：_
- **Greedy (貪婪演算法)**
  - _熟練度評估：_
  - _常犯錯誤/思考盲點：_
- **Intervals (區間問題)**
  - _熟練度評估：_
  - _常犯錯誤/思考盲點：_
- **Math & Geometry (數學與幾何)**
  - _熟練度評估：_
  - _常犯錯誤/思考盲點：_
- **Bit Manipulation (位元運算)**
  - _熟練度評估：_
  - _常犯錯誤/思考盲點：_

## 最近練習紀錄

- [2026-02-28] LC 215 Kth Largest Element in an Array (Heap / Priority Queue): 概念掌握紮實，直接推導出 Min-Heap + size-k 解法與 O(n log k) 正確複雜度。實作上需要查 heapq API；insert 邏輯起初漏掉 heap 未滿時無條件 push 的情境，提示後立即修正。對 streaming 場景（stateful class vs one-shot function）的設計模式尚未熟悉，建議下一步練習 LC 703。
- [2026-02-28] LC 215 QuickSelect 延伸 (Heap / Priority Queue): 成功獨立實作 QuickSelect。需提示才理解 pivot 是隨意選的值（與 k 無關）；`>=` vs `>` 在重複元素退化問題未主動發現，提醒後能立即理解並修正。在 `_quickselect` 判斷停止條件時，未能立即想到 k 是 1-indexed、要與 pivot index 比較需轉換為 `k-1`（0-indexed）。
- [2026-03-01] LC 121 Best Time to Buy and Sell Stock (Sliding Window / Arrays): 第一直覺「找全域最大最小相減」被自己識破（有時間線性要素）。暴力解描述清晰正確（O(n²) 雙迴圈）。Single Pass 解法獨立完成，邏輯清晰。Kadane's 變體：踩了差分方向 bug（prices[i-1] - prices[i] 順序搞反）；current_sum < 0 → 歸零的「換日」語意需引導後豁然開朗。整體表現良好，Kadane's intuition 建立完整。
- [2026-03-01] LC 3 Longest Substring Without Repeating Characters (Sliding Window): 第一直覺正確（雙指標 + map），但初版設計 map 存「出現次數」，提問後自行發現應改存「上次出現 index」，洞察力佳。犯了兩個操作順序 bug：(1) 先覆蓋 last_seen 再讀取舊值，導致 left 跳過頭；(2) else 分支漏更新 result，忽略「left 不動時視窗仍會變大」的情境（用 tmmzuxt 反例觸發）。max(left, ...) 的防倒退語意在提示反例 abba 後自行推導出。整體思路清晰，屬於「細節實作陷阱」類型的錯誤，非概念盲點。
