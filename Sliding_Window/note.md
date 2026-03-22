# Sliding Window (滑動視窗) 核心思路與模式解析

Sliding Window 是一個非常強大但在不同題目下常有「變形」的演算法。
**它確實有一個統一的核心 Pattern**，只要抓住「何時擴張、何時收縮」的邏輯，無論怎麼變形都能輕鬆拆解。

面對所有 Sliding Window 的題目，請先問自己一個核心問題：
**這題要我求的是「最長/最大」還是「最短/最小」？**

---

## 核心的三大標準模式

核心的差異完全取決於：**`while` 迴圈（收縮）的觸發時機與條件是什麼？**

### 模式一：求「最短」 (Shortest / Minimum)

> **設計哲學**：只要合法，就盡量壓榨（縮短）。

- **代表題**：Shortest Fragment (Codility)、Minimum Window Substring (LC 76)
- **模板 (Pseudo Code)**：

```python
def sliding_window_shortest(nums):
    left = 0
    min_len = float("inf")
    # 💡 狀態追蹤變數 (視題目而定)
    # [簡單題] 例如: current_sum = 0
    # [複雜題] 經典的 (need / have / window) 組合技：
    #   - need: 我們總共需要集齊幾種不同的目標？
    #   - have: 目前視窗內，我們已經集齊了幾種「有效目標」？
    #   - window: 字典，負責記錄視窗內各「有效目標」出現的次數

    for right in range(len(nums)):
        # 1. 擴張：將 nums[right] 納入視窗，更新狀態
        # update_state_by_adding(nums[right])

        # 2. 如果狀態「滿足條件(合法)」，就不斷嘗試壓榨（縮短）視窗
        while is_valid(狀態):
            # 2a. 因為現在保證是合法的，立刻更新最短紀錄！
            min_len = min(min_len, right - left + 1)

            # 2b. 嘗試將最左邊的 nums[left] 吐出視窗，並更新狀態
            # update_state_by_removing(nums[left])
            left += 1

            # 吐出後，如果狀態變得不合法了，while 就會結束，繼續給 right 去找

    return min_len
```

### 模式二：求「最長」 (Longest / Maximum)

> **設計哲學**：只要不合法，就必須掙扎（縮短）到合法為止。

- **代表題**：Longest Substring Without Repeating Characters (LC 3)、Max Consecutive Ones III (LC 1004)
- **模板 (Pseudo Code)**：

```python
def sliding_window_longest(nums):
    left = 0
    max_len = 0
    # 💡 狀態追蹤變數 (視題目而定)
    # [簡單題] 例如: current_sum = 0, zero_count = 0
    # [複雜題] 經典的 (need / have / window) 組合技：
    #   - need: 我們總共需要集齊幾種不同的目標？
    #   - have: 目前視窗內，我們已經集齊了幾種「有效目標」？
    #   - window: 字典，負責記錄視窗內各「有效目標」出現的次數

    for right in range(len(nums)):
        # 1. 擴張：將 nums[right] 納入視窗，更新狀態
        # update_state_by_adding(nums[right])

        # 2. 如果狀態因為剛剛的加入而變得「不合法」，就不斷吐出直到合法為止
        while not is_valid(狀態):
            # 2a. 將最左邊的 nums[left] 吐出視窗，並更新狀態
            # update_state_by_removing(nums[left])
            left += 1

        # 3. 經過上面的 while，執行到這裡代表狀態【保證是合法的】
        # 在這裡更新最長紀錄！
        max_len = max(max_len, right - left + 1)

    return max_len
```

### 模式三：固定長度 (Fixed Size)

> **設計哲學**：維持視窗大小等於 K。

- **代表題**：Maximum Average Subarray I (LC 643)、Find All Anagrams in a String (LC 438)
- **模板 (Pseudo Code)**：

```python
def sliding_window_fixed(nums, k):
    left = 0
    result = 初期值 # 例如 0, -float("inf") 等
    # 💡 狀態追蹤變數
    # 這裡的狀態通常比較單純，例如 current_sum = 0，
    # 或是維護一個 window 字典來計算字元頻率

    for right in range(len(nums)):
        # 1. 擴張：將 nums[right] 納入視窗，更新狀態
        # update_state_by_adding(nums[right])

        # 2. 如果視窗太大了，吐出一個元素 (用 if 即可，因為每次只會超標 1 格)
        if right - left + 1 > k:
            # update_state_by_removing(nums[left])
            left += 1

        # 3. 只要到達指定長度，就結算並更新答案
        if right - left + 1 == k:
            result = max(result, 根據當前狀態的計算)

    return result
```

---

## 進階探討：為什麼常見的 LC 3 解答看起來長得不一樣？

你在解答區看到的 LC 3 程式碼通常長這樣：

```python
if ch in last_seen:
    left = max(left, last_seen[ch] + 1)
```

這其實是**模式二**的 **「高度優化版」**，它把「收縮 (Shrink)」的過程給壓縮了。

在標準模式中，`while` 迴圈是一步一步 `left += 1` 把元素吐出來，這在最差情況下會讓 `left` 重走一次 `right` 走過的路。
但既然我們用了 Hash Map (`last_seen`) 記錄了每個字元上次出現的 index，我們就可以 **「直接讓 left 瞬移（跳躍）過去」**！

優化邏輯：
既然我們知道導致「不合法」的罪魁禍首上次出現在 `last_seen[ch]`，我們就不需要慢慢 `while left += 1`，直接把 `left` 設為 `last_seen[ch] + 1`，一秒就跳過了所有不合法的區間。這省略了 `while` 迴圈，使得整個操作變成嚴格的 $O(N)$。

這就是為什麼你覺得「看起來沒有收縮 pattern」的原因：它依然在收縮，只是它用 $O(1)$ 的瞬移取代了 $O(K)$ 的迴圈慢走。

### 補充探討二：為什麼經典 Set 版的寫法，是先「收縮」再「擴張」？

如果你仔細對比 LC 3 在不使用 HashMap 瞬移，而是使用 Python `set()` 的傳統寫法時，你會發現它的順序似乎與「模式二」標準模板剛好相反：

```python
# LC 3 使用 Set 的經典寫法
while s[right] in seen:  # 1. 發現不合法，先收縮 
    seen.remove(s[left])
    left += 1
seen.add(s[right])       # 2. 確定安全了，才加進去 (擴張)
```

**這背後的原因，完全是被資料結構（Set）逼出來的。**

如果我們堅持套用標準模板「先擴張，再判斷是否合法收縮」，來看看兩種資料結構會發生什麼事：

#### 寫法 A：使用 Dictionary 記數 🟢 完美套用標準模板
因為 Dict 會記錄出現次數。加進去發現如果次數 `> 1`，就能安穩地觸發 `while` 收縮，邏輯完美通順！
```python
def longest_using_dict(s):
    window = {}
    left, ans = 0, 0
    for right in range(len(s)):
        r_val = s[right]
        # 1. 先擴張 (把右邊新元素加入)
        window[r_val] = window.get(r_val, 0) + 1
        
        # 2. 判斷不合法？(有辦法判斷！)
        while window[r_val] > 1:
            l_val = s[left]
            window[l_val] -= 1
            left += 1
            
        # 3. 確定合法了，結算答案
        ans = max(ans, right - left + 1)
    return ans
```

#### 寫法 B：依然堅持用 Set (只紀有無) 🔴 會發生災難
因為 Set 把重複默默吞掉了，加進去後你根本不知道該不該收縮。
```python
def longest_using_set_wrong(s):
    seen = set()
    left, ans = 0, 0
    for right in range(len(s)):
        r_val = s[right]
        # 1. 先擴張 (把右邊新元素加入)
        seen.add(r_val) # ⚠️ 如果 r_val 已經在裡面，這行等於默默吃掉事實
        
        # 2. 判斷不合法？完了！
        # while ???: 
        #   因為 Set 剛剛吞掉了重複的證據，你永遠不知道何時該觸發 while 去收縮！
```

#### 寫法 C：因應 Set 的正確變形 🟢 (防禦性收縮)
既然不能等到「加進去才發現闖禍了」，那就只能**「先預判，確定安全了再加進去」**。這也是我們在解答區常看到的經典 Set 寫法：
```python
def longest_using_set_correct(s):
    seen = set()
    left, ans = 0, 0
    for right in range(len(s)):
        r_val = s[right]
        # 1. 先防禦性收縮（預先看看如果加進去會不會出事）
        while r_val in seen:
            l_val = s[left]
            seen.remove(l_val)
            left += 1
            
        # 2. 確定安全不衝突了，才真正加進去 (擴張)
        seen.add(r_val)
        ans = max(ans, right - left + 1)
    return ans
```

理解這一點非常關鍵！你以後就不會去死背各種莫名其妙的操作順序，也能洞察這些其實都只是同一個框架因應資料結構而做的微調。

---

## 總結心法

只要掌握以下兩句口訣，所有的 Sliding Window 都能用這套框架破解：

1. **求最長是在「不合法」時掙扎**：`while (不合法) { 左邊吐出 }` → **在 while 外更新 Max**。
2. **求最短是在「合法」時壓榨**：`while (合法) { 更新 Min; 左邊吐出 }`。

至於 LC 3 的 HashMap Leap（跳躍）寫法，只是在熟練標準框架後，為了追求極致效能而做的變形優化。
