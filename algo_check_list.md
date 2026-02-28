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
  - _熟練度評估：_
  - _常犯錯誤/思考盲點：_
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
