# 演算法面試準備進度與弱點追蹤 (Algorithm Progress & Weakness Tracker)

這份文件用於追蹤使用者在不同演算法題型上的掌握度、常犯錯誤以及思考盲點。
目的是讓使用者有意識地成長，清楚知道自己的弱項在哪裡。

## 題型掌握度與錯誤紀錄

### Arrays & Hashing (陣列與雜湊)

- _熟練度評估：_ 普通 -> 熟練 (起手式掌握度極高)
- _常犯錯誤/思考盲點：_
  - **Cyclic Sort (循環排序) 的識別** (LC 41)：當題目要求「陣列內尋找連續缺失的正整數/數字」，且嚴格限制空間 O(1) 時，核心破題技巧就是「將陣列本身當成 Hash Map（蘿蔔坑）」。透過 `while` 迴圈把有效數值 `x` 換回 `index x-1` 的位置。
  - **時間複雜度攤還分析**：即使是雙迴圈 (`for` 包 `while`)，只要我們確保每個數字「最多只會被歸位（Swap）一次」，整體的交換次數總和依然不會超過 N，其時間複雜度仍為嚴格的 O(N)。
  - **Python 連鎖交換陷阱 (Tuple Swap)**：在實作交換時，如果寫成 `nums[i], nums[nums[i]-1] = nums[nums[i]-1], nums[i]`，因為 Python 會從等號左邊依序提取索引位置，若前面先被覆寫，後面讀取的 `nums[i]` 就會抓錯目標，導致不可預期的 Bug。永遠獨立抽出目標位置（`correct_idx = nums[i] - 1`）是最穩定的做法。
  - **方向 Index 技巧** (LC 906)：四個方向依順時針存入 List，用整數 index 管理當前方向。右轉 = `(idx+1) % 4`，左轉 = `(idx-1) % 4`。Python 的負數取模自動循環，無需 match/case。
  - **最大距離需走訪中途追蹤** (LC 906)：機器人可能在中途到達最遠點後被擋住或轉頭，只在最後一步計算距離會錯過中途的最大值。必須每走一格就即時更新 `max_dist_sq`。

### Two Pointers (雙指標)

- _熟練度評估：_
- _常犯錯誤/思考盲點：_

### Sliding Window (滑動窗口)

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
  - **「求最短」 vs 「求最長」的 Pattern 識別**：過去容易受到 LC 3 的優化寫法影響，以為 Sliding Window 沒有標準收縮框架。現已釐清核心口訣：「求最長是在不合法時掙扎（`while not is_valid`），求最短是在合法時壓榨（`while is_valid`）」。
  - **區間條件的審題盲點**：遇見「包含從 L 到 R 重的所有整數」時，容易看漏「所有」二字，誤以為只要包含頭尾端點。這決定了狀態設計必須用 `need = R - L + 1` 來追蹤收集進度。

### Stack (堆疊)

- _熟練度評估：_
- _常犯錯誤/思考盲點：_

### Binary Search (二分搜尋)

- _熟練度評估：_ 普通 -> 熟練
- _常犯錯誤/思考盲點：_
  - **二分搜邊界預設值 (Edge Case)**：當陣列所有元素都大於/小於 target 時，預設的 index 該落在哪裡？
    - 找 `>= target`（lower_bound）或 `> target`（upper_bound）時，若全部元素過小，合理的插入點在陣列最尾巴外側，預設 `ans = len(nums)`。
    - 找 `<= target` 或 `< target` 時，若全部元素過大，合理的分界點在陣列最前方外側，預設 `ans = -1`。
  - **利用對稱性簡化實作**：`last <= target` 完全等價於 `upper_bound(target) - 1`。在整數域中即是 `find_gte(nums, target+1) - 1`，這能讓我們只依靠一個正確處理過邊界的 `find_gte` 函數，無腦應付所有變形。

### Linked List (連結串列)

- _熟練度評估：_
- _常犯錯誤/思考盲點：_

### Trees (樹)

- _熟練度評估：_ 普通 -> 熟練 (BFS 掌握度高)
- _常犯錯誤/思考盲點：_
  - **定義正確的 DFS 回傳值（核心）**：DFS 函數回傳的不一定是答案，而是「對父節點有用的資訊」。思考方式：站在當前節點，我需要從子節點知道什麼，才能算出我的結果？這決定了回傳值的定義。
  - **DFS 回傳值 vs. 全域答案**：兩者不一定相同。若答案可以直接由 root 的回傳值得到（如樹高），不需要全域變數。若答案需要在遍歷過程中跨節點比較（如路徑最大和），則需要在 DFS 內部另外維護全域變數更新。
    - 範例 — 樹高，解法 A（後序）：`dfs` 回傳子樹高度，`root` 的回傳值直接就是答案，無需全域變數。
    - 範例 — 樹高，解法 B（前序）：`dfs` 帶著當前深度向下傳，在每個節點更新全域 `max_depth`，答案存在全域變數裡。
  - **後序遍歷識別**：需要先知道子節點的結果才能決定自身行為，因此是後序（左 → 右 → 根）。
  - **BFS 層序遍歷模板**：掌握良好。能清晰區分控制 BFS 終止的 `while`，與控制單層處理的內部 `for` 迴圈。對於二元樹，用明確的 `left`/`right` 條件判斷取代 Graph 結構中對鄰居節點的遍歷迴圈。

### Heap / Priority Queue (堆積 / 優先佇列)

- _熟練度評估：_ 普通
- _常犯錯誤/思考盲點：_
  - Insert 條件一開始未考慮 heap 未滿（`size < k`）時需無條件 push，只記得「比 heap[0] 大才 push」，需提示才修正。
  - 對 `heapq` API 不熟悉（`heappush` / `heappop` / 初始化），需要查閱。
  - 未能立即識別 stateful streaming 場景（LC 703）與 batch 解法的介面差異：batch 是一次呼叫回傳答案，streaming 需要 class 持久化 heap 狀態，並透過 `add()` 逐次回傳。
  - **QuickSelect**：pivot 的目的（分割，與 k 無關）需提示才理解；`>=` vs `>` 在重複元素時可能退化成 O(n²) 未主動意識到。
  - **QuickSelect Index 轉換**：未能立即意識道 k 是 1-indexed（第 1 大 = 最大值），而降序排序後對應的 0-indexed 位置是 `k-1`，導致在 `_quickselect` 中與 pivot index `p` 比較時，不確定應寫 `p == k` 還是 `p == k-1`。需銘記：**第 k 大 → index k-1**。

### Backtracking (回溯法)

- _熟練度評估：_ 普通（框架建立中）
- _常犯錯誤/思考盲點：_
  - **參數語意混淆**（LC 139）：過去在 Combination/Subset 類題目習慣用 `i` 表示 wordDict 的 index，for loop 從 `i` 開始（保證不重複挑選）。本題推進的是「字串 s 消耗到哪個位置」，參數應是 `start = s 的 index`，for loop 重頭掃整個 wordDict（允許重複使用）。兩者設計不同，核心差異在「推進維度」。
  - **Backtracking 兩種模式對比**：
    - **子集合/組合（Combination）模式**：`for j in range(i, n)`，每個元素最多選一次，保持順序。適用：Combination Sum（不可重複）、Subsets 等。
    - **可重複使用（with repetition）模式**：`for w in wordDict`（每層全掃），允許同一個字多次使用，推進的是目標序列的消耗位置。適用：Word Break、Combination Sum II（可重複）等。
  - **Dead code 陷阱**（LC 139）：在 `can_break(start)` 加 `if start > len(s): return False` 是 dead code。原因：Python slice 超出範圍會截短，長度不符則 `s[start:end] == w` 一定為 False，因此遞迴傳入的 `start` 永遠 `<= len(s)`，該條件永不觸發。

### Tries (字典樹)

- _熟練度評估：_
- _常犯錯誤/思考盲點：_

### Graphs (圖)

- _熟練度評估：_ 普通（Multi-Source BFS 掌握度高）
- _常犯錯誤/思考盲點：_
  - **圖的表示方式**：Adjacency List `graph[node] = [鄰居...]` 空間 O(V+E)，適合稀疏圖；Adjacency Matrix `matrix[u][v]` 空間 O(V²)，適合稠密圖，查詢單條邊 O(1)。競賽/面試預設用 Adjacency List。
  - **Multi-Source BFS 識別**：能主動識別「多個起點同時展開」的場景（腐爛橙子、牆與門等），直接將所有起點入隊，不需要逐一 BFS。
  - **`minute += 1` 時機**：正確識別步數計算應在整個 level traversal 結束後，不是每次 pop 後。
  - **邊界條件識別**：主動識別「一開始就沒有新鮮 orange」需回傳 0，並發現此情況其實被演算法本身隱性處理（`total == rotten` 在 BFS 前成立）。
  - **Invariant 推理**：理解 while 迴圈結束後 `total != rotten` 是不變量，最終可直接 `return -1`，原始的 ternary 寫法是等價但具防禦性的 self-documenting 風格。
  - **DFS 三色狀態機**（LC 207）：能正確提出 `unseen / path / seen` 三態設計；初版將 `state[course] = "path"` / `"seen"` 放在 for 迴圈內部，提示後自行理解「狀態改變是節點層級的事，不是邊層級的事」並修正至迴圈外。
  - **BFS vs DFS Graph 方向相反**（LC 207）：自行觀察到 DFS 建的是 `course ← pre`（追蹤依賴來源），BFS 建的是 `pre → course`（往下游擴散），兩者邊方向相反是解法結構決定的，非隨意選擇。
  - **BFS level-by-level 模式誤用**（LC 207）：在 Kahn's Algorithm 中使用了 `size = len(queue)` 的層序模板，實際上不需要逐層處理，提醒後簡化；自行觀察到 DFS/BFS 圖方向相反的現象並補充註解。兩種解法均獨立完成且測試通過。時間 O(V+E)，空間 O(V+E)。
  - **Degree-based BFS Peeling（葉節點剝除）**（Codility: Vertices Stop Disappearing）：「每秒移除 degree ≤ 1 的頂點」是此類問題的核心。暴力解需每輪掃全部存活頂點 O(N²)；優化解使用 BFS 分層（類 Topological Sort），以 `degree[]` 陣列追蹤度數、`removed[]` 防重複入隊，每個頂點與邊只被處理一次，達到 O(N+M)。對 `set.discard()` vs `set.remove()` 的差異（存在與否的安全性）以及 `set.clear()` 語意在引導後充分理解。
  - **Grid 方向座標盲點**（Codility: Cleaning Robot）：直覺將「往右」誤認為 `(1, 0)`，混淆了 Cartesian x/y 系統與 Matrix row/col 系統。牢記第一維度是 row（向下），往右應是 col+1 也就是 `(dr=0, dc=1)`。
  - **Grid 模擬的循環偵測**（Codility: Cleaning Robot）：對於永遠移動的模擬題，停止條件就是「狀態重複」。狀態必須同時包含「位置 + 面向方向」，缺一不可，這等同於在走訪過程中偵測 Cycle。

### Advanced Graphs (進階圖論)

- _熟練度評估：_
- _常犯錯誤/思考盲點：_

### 1-D Dynamic Programming (一維動態規劃)

- _熟練度評估：_ 普通（概念框架建立中）
- _常犯錯誤/思考盲點：_
  - **與 Sliding Window 的識別差異**：DP 適合「需要跳著選或非連續子問題」的場景（如 House Robber 的隔格選取）；若子問題只依賴「一段連續區區間」，通常能用 Sliding Window 取代且更直觀。判斷口訣：當 dp 陣列可以滾動壓縮成一兩個變數時，優先考慮是否為 Sliding Window 問題。
  - **DP 類型識別（LC 452 討論整理）**：
    - **线性 DP**（`f[i][j]`）：對兩個序列求解，例如 Edit Distance、LCS。
    - **划分型 DP**（`f[i]` = 前綴 `a[:i]` 的最優解）：把序列切割分組，枚舉最後這組的左端點 `j`，從 `f[j]` 轉移到 `f[i]`，**需要先排序才有意義的線性前綴狀態**。LC 452 的 DP 解法屬此類。
    - **狀態機 DP**（`f[i][j]`，j 代表小狀態集合）：例如買賣股票（持有/不持有）。
  - **「枚舉所有可能」vs「貪心固定唯一選擇」**（LC 452）：
    - DP 的本質是「不知道最佳選擇，所以枚舉所有合法選項取 min/max」。
    - Greedy 的本質是「數學上可證明局部最佳 = 全域最佳，所以直接選唯一最佳解」。
    - 若一個遞迴函數每個節點只有唯一一條路徑（無分支），它只是「遞迴版貪婪」，不是真正的 DP（加 `@cache` 也毫無意義）。
  - **「排序是否必要」判斷**（LC 452）：線性 DP 的狀態定義為「前綴」，需要排序才能讓 index 代表有意義的線性順序。不排序則只能用 Bitmask DP（O(2ⁿ)），不實用。
  - **時間複雜度分析框架**：`總時間 = 遞迴節點數量 × 每個節點的時間`。
    - 節點數 = 不同狀態的 `fn(i)` 數量（有 `@cache` 則每個狀態只算一次）。
    - 每個節點的時間 = 該狀態內枚舉的工作量。
    - Greedy 每節點 O(1)（找到第一個 return，各節點掃描範圍不重疊 → 均攤）；DP 每節點 O(n)（枚舉所有合法 j，掃描範圍大量重疊）。
  - **v1 vs v2 DP 內層枚舉方式的對比**（LC 139）：
    - **v1（枚舉 wordDict）**：內層 `for word in wordDict`（W 次），每次字串比對 O(L)，總時間 O(N×W×L)。不能在 `dp[i+w] = True` 後 break，因為不同 word 長度不同，會更新**不同位置**的 dp 格子。
    - **v2（枚舉子串長度）**：內層 `for length in possible_lengths`（L' 次，L' <= L），配合 Hash Set 查詢 O(L)，總時間 O(N×L²)。可以在 `dp[i+length] = True` 後立即 break，因為我們是針對「當前位置 i」枚舉長度，只要找到任何一個長度能讓 `dp[i]` 成立即可。
  - **狀態機進化 (LC 714)**: 成功從 O(N^2) 的「方法 b (以 i 結尾，枚舉 j)」進化到 O(N) 的「方法 a (前 i 天最優值) + 狀態機」。
    - **核心洞察**：Method B 容易讓人陷入「我今天要跟哪一天接」的迴圈思考；而 Method A 搭配狀態機（持有為真/假）則轉化為「我今天結束時要處於什麼狀態」，這使得狀態轉移只需依賴「昨天」的最優解，達成 O(1) 轉移。

### 2-D Dynamic Programming (二維動態規劃)

- _熟練度評估：_ 普通（框架建立中）
- _常犯錯誤/思考盲點：_
  - **狀態定義的兩種視角（方法 a vs 方法 b）**：初期困惑「選或不選」與「枚舉選哪個」的差異，經引導後理解：
    - 方法 a（前 i 個元素）：每個元素只需決定「要」或「不要」，如 LCS。
    - 方法 b（以 i 個元素結尾）：需要回溯前面「接在誰後面」，如 LIS。
  - **「結尾」是否有意義的判斷**：方法 b 適合需要「連接」的問題（如 LIS：必須知道結尾才能判斷遞增），LCS 不需要因為子序列的結尾是誰沒有特殊意義。
  - **判斷口溜**：「如果不知道結尾是誰，能不能繼續往下算？」能的話 → 方法 a；不能的話 → 方法 b。
  - **最佳子結構的信任 (Optimal Substructure)**：(LC 831) 疑惑「平均數相加」在整體切分中是否保證最佳。經釐清後理解：因為總目標是「加法（Sum of Averages）」，所以只要外部相加，單看剩下的元素切 k-1 刀必定需要其「絕對最大值」，不會因為前半段切法不同而有內部連動影響。
  - **DP 緩存 (@cache) 與 區間運算 (Prefix Sum) 的混淆**：(LC 831) 誤以為有了 `@cache` 就不需要顧慮「計算區間總和」的成本。需釐清：`@cache` 是用來省下「重複的 DFS 狀態遞迴」，而 Prefix Sum 是用來省下「狀態內部單次 O(N) 的區間加總」。兩者解決的效能瓶頸維度完全不同。
  - **維度擴張的原因：資訊欠債 (Information Deficiency)**：(集合分組總數) 當 1D 狀態 f(i) 不足以決定下一步（如：加入現有組需知道現有幾組）時，必須將缺少的資訊提升為新維度 k。
  - **第二類 Stirling 數的 * k 邏輯**：因為元素可區分，加入 k 個內容物不同的組會產生 k 種不同結果。這與「袋子無序」不衝突，因為內容物的差異打破了對稱性。

### Greedy (貪婪演算法)

- _熟練度評估：_ 普通
- _常犯錯誤/思考盲點：_
  - **為何按 `end` 而非 `start` 排序**（LC 452）：需要具體反例（短氣球 vs 長氣球）才能豁然開朗。核心直覺：按 `end` 排序後，每次決策只需考慮「當前最快消失的目標」，不需回頭修改；按 `start` 排序則需要不斷縮短射擊極限，邏輯複雜。
  - **EDF 思維（Earliest Deadline First）**：`end` = 死線，優先處理死線最早的目標，是 Greedy 區間問題的通用框架。
  - **交換論證（Exchange Argument）**：箭射在 `end` 永遠不比射在左邊差，是證明局部最佳解成立的核心論證，能獨立理解。

### Intervals (區間問題)

- _熟練度評估：_
- _常犯錯誤/思考盲點：_

### Math & Geometry (數學與幾何)

- _熟練度評估：_ 普通
- _常犯錯誤/思考盲點：_
  - **迴圈區間與計數對應**：在設計 O(N/K) 迴圈（如每次跳 1000）時，容易忽略中段完整區間內所包含的總數量，導致計數遺漏。
  - **區間邊界 (Off-by-one) 判定**：判斷大於等於 K 的數字總數時，會猶豫要減去 K 還是 K-1。透過「極端值代入法」（例如 `n=1000` 驗算總數是否為 1）可以有效破解盲點。

### Bit Manipulation (位元運算)

- _熟練度評估：_
- _常犯錯誤/思考盲點：_

---

## 最近練習紀錄

- [2026-04-09] Total Ways to Partition a Set (2-D Dynamic Programming / Math): 計算將 n 個可區分元素劃分為若干非空子集的總數（Bell Number）。
  - **核心挑戰**：經歷了 **「1D 到 2D 的維度擴張」** 推導。識別出當 1D 狀態 f(i) 因為「資訊欠債」（不知道目前有幾組，無法計算加入現有組的 k 倍可能性）而無法轉移時，必須提升維度至 f(i, k)。
  - **關鍵洞察**：
    - **維度 A：輸入視角 (Stirling Numbers)**：著重於逐一處理元素。
        - 遞迴公式：S(n, k) = S(n-1, k-1) + k * S(n-1, k)。
        - 理解 k 的乘數意義：內容物的差異打破了「袋無序」的對應關係。
        - 邊界條件：掌握 k=1, k=i, k>i 等關鍵終止條件。
    - **維度 B：結果視角 (Bell Recurrence)**：著重於直接拆解最終結構。
        - 透過固定「主角」進行二元劃分：先處理「其餘分組 (子問題 bell(j))」，再乘以「組隊成員挑選 (comb)」。
        - 乘法原理與對稱性：深刻理解 `bell(j) * math.comb(i-1, j)` 的轉移細節，並利用 C(n, k) = C(n, n-k) 的物理意義簡化實作。
  - **技術掌握**：成功實作兩種視角的 Top-down DP。掌握度評分：遞迴推導 ✅ | 維度設計 ✅ | 組合數學對稱性 ✅

- [2026-04-07] LC 906 Walking Robot Simulation (Arrays & Hashing / Simulation): 第一直覺即正確識別模擬法架構，並主動分析暴力解 O(n×m×k) 的瓶頸。優化探索上提出 Binary Search 方向（固定一維後搜尋另一維），邏輯正確但實作複雜度高；在引導後自行推導出 HashSet O(1) 查詢 + 逐格走訪的最優解。實作中發現思考盲點：
  - **`or` vs `and` guard clause**：`cmd != -1 or cmd != -2` 永遠為 True，需改為 `and`。
  - **方向應用 index 取代 match/case**：未能初始想到，引導後立即理解 `(idx ± 1) % 4` 技巧。
  - **最大距離計算時機**：誤以為「全部走完才計算」即可，反例（北走後轉頭回原點）後立即釐清須每步更新。
  - **`break` 後的距離是否遺漏**：誤以為 break 後有格子沒算到，澄清後理解 break 在「移動更新之前」執行，不會遺漏任何已到達位置。
  - 整體邏輯思維優秀，卡點集中在細節實作與 Python 語義，屬可快速修正的弱點。掌握度評分：HashSet 模擬 ✅ | 方向 index 技巧 🔶（需提示才想到）

- [2026-03-22] Codility Interview Q3: Shortest Fragment (Sliding Window): 尋找包含 [L, R] 區間內所有整數的最短連續子陣列。
  - **審題盲點**：一開始誤將「包含 L 到 R」解讀為只要包含邊界值即可，經舉例後釐清必須集齊區間內**所有**整數（需 `R - L + 1` 種數字）。
  - **狀態設計與雜訊過濾**：學習到如何利用 `need` (目標種類數)、`have` (已搜集種類數) 與 `window_count` (目前視窗內的有效目標頻率) 來進行 O(1) 的狀態即時追蹤，並直接放生非有效範圍內的雜訊數字。
  - **Sliding Window 模式釐清**：解題過程中對「求最長」與「求最短」的架構產生疑問。經過筆記梳理後，建立了穩固的 3 大模板（Shortest / Longest / Fixed Size），徹底解開了對 LC 3 優化寫法「為何沒有傳統 while 收縮」的長期困惑。

- [2026-03-22] Codility Interview Q2: Cleaning Robot (Graphs / Grid Simulation): 機器人格子走訪模擬題。
  - **方向座標盲點**：初始直覺將「往右」定義為 `(dr=1, dc=0)`，未意識到在 grid 陣列系統中，第一維度 (row) 是垂直向下，第二維度 (col) 才是水平向右，因此往右應為 `(dr=0, dc=+1)`，提醒後徹底釐清 x/y 座摽與 row/col 系統的 90° 差異。
  - **停止條件設計**：一開始無法想出何時該讓「永遠移動」的機器人停止。引導後理解到，只要將 `(位置, 面向方向)` 作為一個「狀態 (state)」，當相同狀態再次出現時，就代表進入了無限循環（未來軌跡將完全重複），此時即可安全終止。
  - **迴圈與方向切換優化**：初始單次 step 嘗試結合 `dr, dc` 與 state 檢查，邏輯交錯。優化後改為大迴圈負責狀態紀錄，內部透過 `for _ in range(4)` 配合 `% 4` 實現「站在原地轉找路」的獨立邏輯，大幅提升清晰度，並順勢處理了「四面被封死」的終止條件。

- [2026-03-22] Codility Interview Q1: Vertices Stop Disappearing (Graphs / BFS Peeling): 題目來自圖片截圖（非 LeetCode），初始完全沒有方向（0 提示起點）。
  - **卡點 1 - 建模**：對「degree」概念不陌生，但無法獨立連結到「每秒剝除葉節點」的模擬框架，需引導才進入暴力解思路。
  - **API 盲點**：不熟悉 `set.discard()` vs `set.remove()`（存在與否的安全性差異）以及 `set.clear()` 語意，提示後理解。
  - **優化解**：能理解「只有被移除頂點的鄰居 degree 才會下降 → 不需全掃」的核心觀察；BFS 分層模板（`current_wave = list(queue); queue.clear()`）屬新接觸，由 AI 展示後順利讀懂。與 Topological Sort 葉節點剝除的結構等價性本次未主動點出，建議下次複習時自行連結。
  - **掌握度評分**：暴力模擬 ✅ | BFS 分層優化 🔶（能讀懂，無法獨立寫出）

- [2026-03-22] LC 4245 Count Commas in Range (Math & Geometry): 成功從 O(N) 暴力迴圈解法推進到 O(1) 數學規律解。
  - 第一直覺採用 O(N/1000) 迴圈，但忽略了每次減去 1000 所跳過的數字也會貢獻逗號，經引導後修正為 O(N) 暴力迴圈並順利通過。
  - 觀察數學規律時，對區間差值邊界（減 999 還是 1000）產生疑惑。透過極端值 `n=1000` 代入驗算，成功建立「頭尾包含」的直覺，最終完成 max(0, n - 999) 的 O(1) 最優解。
- [2026-03-21] LC 831 Largest Sum of Averages (2-D Dynamic Programming): 練習過程中能迅速識別出暴力解的組合數學基礎（2^(N-1)）與 O(N * K) 的 DFS 狀態空間。盲點在於：
  1. 對最佳子結構產生質疑：擔心「平均數獨立切分」最後加起來不是全域最佳。
  2. 對 Memoization 與 Prefix Sum 的應用場景混淆：誤以為 `@cache` 已經解決了所有重複計算。
  3. 對 DFS `(i, k)` 的嚴格定義變得模糊，導致不知如何實作。
- [2026-03-21] First Missing Positive (Arrays & Hashing): 在面試演練中展現優秀的起手式，第一時間提出 bool 陣列紀錄（空間 O(N)、時間 O(N)）的 Baseline 解法。後續在空間 O(1) 優化挑戰中，成功在引導下聯想到「數值化為 Index」的概念，並理解了 Cyclic Sort (循環排序) 的實作核心。同時釐清了「時間複雜度的攤還分析」以及「Python Tuple Swap 語法陷阱」。整體邏輯思維與引導吸收力極佳。
- [2026-03-18] LC 714 Best Time to Buy and Sell Stock with Transaction Fee (1-D Dynamic Programming / State Machine DP): 成功從 O(N^2) 的「方法 b (以 i 結尾，枚舉 j)」進化到 O(N) 的「方法 a (前 i 天最優值) + 狀態機」。
  - **核心洞察**：Method B 容易讓人陷入「我今天要跟哪一天接」的迴圈思考；而 Method A 搭配狀態機（持有為真/假）則轉化為「我今天結束時要處於什麼狀態」，這使得狀態轉移只需依賴「昨天」的最優解，達成 O(1) 轉移。
  - **盲點紀錄**：
    - 初始直覺易受 Method B 誤導而寫出內層迴圈。
    - Base Case 的非法狀態處理：`i = -1` 且 `holding = True` 應回傳 `-inf` 以防止被選中。
    - 轉移函數初始化 `ans = 0` 可能會掩蓋負利潤（買入）的過程，應改為直接比較。
- [2026-03-16] LC 1143 Longest Common Subsequence (2-D DP): 正確使用「方法 a（前 i 個元素的最優值）」定義狀態 `dfs(i,j)`。遞迴公式：配對成功 → `dfs(i-1,j-1) + 1`，配對失敗 → `max(dfs(i-1,j), dfs(i,j-1))`。成功獨立實作 Top-down DP + @cache，時間 O(m×n)，空間 O(m×n)。理解過程：初期困惑「選或不選」v.s.「枚舉選哪個」，經引導後理解 LCS 適合方法 a（核心是「選或不選」而非「接在誰後面」），並補充了「判斷口溜」幫助未來識別。
- [2026-03-12] LC 34 Find First and Last Position of Element in Sorted Array (Binary Search): 首次針對 二分搜尋（Binary Search）的五種邊界條件（find_gte, find_gt, find_lte, find_lt, find_equal）進行獨立實作。成功運用「Record and Reduce」模式（用 `ans` 記錄最佳解並持續縮小範圍），乾淨俐落避開了死迴圈。關鍵洞察：若將 `find_gte` 視為通用的 `lower_bound` 函數，不應在內部寫死 `if nums[ans] == target else -1` 的判斷，而應直接回傳最接近的 index，交由 caller（如 `searchRange`）來決定是否符合目標。此一 decouple 的思維展現了良好的軟體工程直覺。
- [2026-03-12] LC 34 (尋找邊界優化): 深入探討 Binary Search 尋找不同邊界時的預設值設計（Edge Cases）。理解了當全陣列元素皆小於 target 時，找 `>= target` 應預設回傳 `len(nums)` 而非 `-1`，藉此吻合 STL 與 Python `bisect` 的標準行為。此外，成功體驗了整數域同構轉換 `last <= target == upper_bound(target) - 1` 所帶來的高可維護性，後續只靠單一底層函數（find_gte）就能實作出所有的邊界搜尋需求。
- [2026-03-12] LC 300 Longest Increasing Subsequence (1-D DP): 正確釐清 DP 狀態定義的兩種核心視角：「站在輸入 (考慮選或不選)」vs「站在答案 (強制結尾往前找枚舉)」。成功以「枚舉前輩」的視角實作 v2 版本的 Top-Down DP + Memoization。空間複雜度精準估算為 O(N)（遞迴深度 + cache 大小）。時間複雜度的分析，透過「狀態總數 × 計算單一狀態成本」的黃金公式，成功自行推導出 O(N²) 的正確結論。
- [2026-03-11] LC 139 Word Break — DP v2 解法 (1-D DP): 在 DP v1（枚舉 wordDict）基礎上進一步最佳化，改為「枚舉子串長度 + hash set 查詢」。能理解核心洞察：wordDict 最多 1000 個字，但長度種類最多 20 種，應枚舉長度（O(L²)）而非字典（O(W×L)）。能正確推導 `range(1, min(i, max_len)+1)` 的邊界（為何不能直接寫 `range(1, max_len)`：語義不同、off-by-one、需要 min(i,...) 防止 j < 0）。能理解 v2 可以 break 而 v1 不行的根本原因：v1 不同 word 更新不同 dp 位置，v2 不同 length 寫同一個 dp[i]。主動提出「枚舉長度比位置更直覺」並完成重構，可讀性提升。時間 O(WL + NL²)，空間 O(WL + N)。
- [2026-03-11] LC 139 Word Break — Backtracking 解法 (Backtracking / 1-D DP): 首次明確區分兩種 Backtracking 模式。初始直覺是暴力組合所有可能，在引導下正確重構為「推進字串消耗位置」的框架。能自行撰寫正確的 `can_break` 遞迴，并主動嘗試從後往前收斂（`can_break(len(s)) → 0`）的方向，與原始版和 DP 均等價正確。觀察到 dead code（`start > len(s)` 永不觸發），能理解 Python slice 截短原因。對「Combination 模式（from i）」vs「Word Break 模式（全掃 wordDict）」的差異在提示後清晰理解。時間 O(W^N)，空間 O(N)。
- [2026-03-11] LC 452 Minimum Number of Arrows to Burst Balloons (Intervals / Greedy): 熟練度：普通→熟練。概念澄清方面：初始誤解 Bounding Box（找 max(start)/min(end)），提示後正確理解題目是「最少點覆蓋」問題。核心貪心邏輯上對「為何按 end 排序（EDF 思維）」一開始理解有困難，引導後能以具體反例（A=[1,10]、B=[2,3]、C=[4,5]）對比 start 排序 vs end 排序的邏輯複雜度，豁然開朗。交換論證（Exchange Argument）獨立理解無困難。實作上一開始漏掉 sorted() 第一個位置參數（`sorted(key=...)` 少傳 iterable），自行發現並修正。最終實作乾淨簡潔：按 end 排序 + 初始化「先射第一支箭」（類 dummy node 設計）+ 單趟掃描。時間 O(n log n)，空間 O(n)（可改 in-place sort 優化為 O(1)）。
- [2026-03-11] LC 207 Course Schedule (Graphs / DFS + BFS): 正確識別「有向圖環形偵測」核心。自行推導出三色狀態機（unseen/path/seen）並完整說明語意。初版將 state 變更寫在 for 迴圈內，提示後立即理解並修正（狀態是節點層級，非邊層級）。完成 BFS Kahn's Algorithm 實作；誤用 level-by-level 模板，提示後簡化；自行觀察到 DFS/BFS 圖方向相反的現象並補充註解。兩種解法均獨立完成且測試通過。時間 O(V+E)，空間 O(V+E)。
- [2026-03-10] LC 994 Rotting Oranges (Graphs / Multi-Source BFS): 自行完整描述 Multi-Source BFS 解法並直接進入實作。立即識別將所有腐爛起點一次性入隊的策略，`minute += 1` 時機正確（level traversal 後）。主動識別「全是 rotten/empty」邊界條件，且能理解此邊界應被演算法本身隱性處理。能推論 while 結束後的不變量（`total != rotten`），理解最終 return 可簡化。整體概念清晰，屬首次解題成功。時間 O(m×n)，空間 O(m×n)。
- [2026-03-10] LC 102 Binary Tree Level Order Traversal (Trees / BFS): 成功且正確實作 BFS 模板。能清晰描述 BFS 的三個層次：(1) while queue > 0 控制總體結束；(2) for \_ in range(size) 控制單層邊界；(3) 處理內部子節點 (left/right) 加入 queue。觀念穩固，無明顯思考盲點。時間 O(N)，空間 O(N)。
- [2026-03-04] LC 124 Binary Tree Maximum Path Sum (Trees / DFS): 複習核心概念與思考過程。掌握了「轉彎點」直覺（路徑最高點 = 左+根+右），及後序遍歷 DFS 的雙重職責：回傳上層只能單側（`node.val + max(left, right)`）、更新全域可兩側（`node.val + left + right`）。關鍵洞察：負貢獻以 `max(0, gain)` 截斷。時間 O(N)，空間 O(H)。
- [2026-03-01] LC 3 Longest Substring Without Repeating Characters (Sliding Window): 第一直覺正確（雙指標 + map），但初版設計 map 存「出現次數」，提問後自行發現應改存「上次出現 index」，洞察力佳。犯了兩個操作順序 bug：(1) 先覆蓋 last_seen 再讀取舊值，導致 left 跳過頭；(2) else 分支漏更新 result，忽略「left 不動時視窗仍會變大」的情境（用 tmmzuxt 反例觸發）。max(left, ...) 的防倒退語意在提示反例 abba 後自行推導出。整體思路清晰，屬於「細節實作陷阱」類型的錯誤，非概念盲點。
- [2026-03-01] LC 121 Best Time to Buy and Sell Stock (Sliding Window / Arrays): 第一直覺「找全域最大最小相減」被自己識破（有時間線性要素）。暴力解描述清晰正確（O(n²) 雙迴圈）。Single Pass 解法獨立完成，邏輯清晰。Kadane's 變體：踩了差分方向 bug（prices[i-1] - prices[i] 順序搞反）；current_sum < 0 → 歸零的「換日」語意需引導後豁然開朗。整體表現良好，Kadane's intuition 建立完整。
- [2026-02-28] LC 215 QuickSelect 延伸 (Heap / Priority Queue): 成功獨立實作 QuickSelect。需提示才理解 pivot 是隨意選的值（與 k 無關）；`>=` vs `>` 在重複元素退化問題未主動發現，提醒後能立即理解並修正。在 `_quickselect` 判斷停止條件時，未能立即想到 k 是 1-indexed、要與 pivot index 比較需轉換為 `k-1`（0-indexed）。
- [2026-02-28] LC 215 Kth Largest Element in an Array (Heap / Priority Queue): 概念掌握紮實，直接推導出 Min-Heap + size-k 解法與 O(n log k) 正確複雜度。實作上需要查 heapq API；insert 邏輯起初漏掉 heap 未滿時無條件 push 的情境，提示後立即修正。對 streaming 場景（stateful class vs one-shot function）的設計模式尚未熟悉，建議下一步練習 LC 703。
