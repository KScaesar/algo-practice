"""
# [139. Word Break](https://leetcode.com/problems/word-break/)
**Difficulty:** 🟡 Medium
**Tags:** Array, Hash Table, String, Dynamic Programming, Trie, Memoization

## Problem Description

Given a string `s` and a dictionary of strings `wordDict`, return `true` if `s` can be segmented into a space-separated sequence of one or more dictionary words.

**Note** that the same word in the dictionary may be reused multiple times in the segmentation.



Example 1:**

```

**Input:** s = "leetcode", wordDict = ["leet","code"]
**Output:** true
**Explanation:** Return true because "leetcode" can be segmented as "leet code".

```

Example 2:**

```

**Input:** s = "applepenapple", wordDict = ["apple","pen"]
**Output:** true
**Explanation:** Return true because "applepenapple" can be segmented as "apple pen apple".
Note that you are allowed to reuse a dictionary word.

```

Example 3:**

```

**Input:** s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
**Output:** false

```



**Constraints:**

        - `1 <= s.length <= 300`

        - `1 <= wordDict.length <= 1000`

        - `1 <= wordDict[i].length <= 20`

        - `s` and `wordDict[i]` consist of only lowercase English letters.

        - All the strings of `wordDict` are **unique**.

## Similar Questions
- [Word Break II](https://leetcode.com/problems/word-break-ii/) (Hard)
- [Extra Characters in a String](https://leetcode.com/problems/extra-characters-in-a-string/) (Medium)
"""

from typing import List


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        # return self._backtracking(s, wordDict)
        # return self._dp(s, wordDict)
        return self._dp_v2(s, wordDict)

    def _backtracking(self, s: str, wordDict: List[str]) -> bool:
        """
        解法一：Backtracking（暴力解）

        思路：
            從當前位置開始，嘗試 wordDict 裡每個字。
            若匹配成功，遞迴處理剩下的字串。
            只要有任何一條路徑走到底就回傳 True。

        決策樹：
            每層有 |wordDict| 個分支，最多 N 層。
            → 總節點數 ≈ |wordDict|^N

        時間複雜度：O(W^N × L)（無 cache，最壞情況）
            - W = len(wordDict)，每層遞迴嘗試 W 個字
            - N = len(s)，決策樹最多 N 層（每次至少消耗 1 個字元）
            - L = max(len(w))，每次字串比對 s[start:end] == w 需 O(L)
            - 實際上因 early return 通常遠小於 W^N，但最壞情況仍是指數
            - 若加上 @cache：每個 start（共 N+1 種）只算一次 → O(N × W × L)
        空間複雜度：O(N)
            - 遞迴深度最多 N 層（不含 cache 時）
        """

        # 【參數設計】start = 字串 s 的當前位置（不是 wordDict 的 index）
        # 每次遞迴推進的是「s 消耗了多少字元」，而非「用到第幾個字典字」。
        def can_break(start: int) -> bool:
            if start == 0:
                return True

            # 【for loop 設計】每次從整個 wordDict 重頭掃，而非從 i 開始
            # 這是「可重複使用元素 (with repetition)」的 backtracking 模式。
            #
            # 對比：若 for loop 從 i 開始（for j in range(i, len(wordDict))），
            # 那是「子集合 / 組合 (Combination)」模式：
            #   → 每個元素只挑一次，且保持順序，避免重複挑選
            #   → 適用於 Combination Sum、Subsets 等題型
            #
            # 本題允許同一個字重複使用，且順序固定（從左到右匹配 s），
            # 所以每層都要重頭掃 wordDict，找「當前位置能接上哪個字」。
            for word in wordDict:
                w = len(word)
                if s[start - w : start] == word:
                    if can_break(start - w):
                        return True
            return False

        return can_break(len(s))

    def _dp(self, s: str, wordDict: List[str]) -> bool:
        """
        解法二：1-D Dynamic Programming（枚舉字典中的每個字）

        思路：
            dp[i] = s[:i] 是否可以被拆解

            子問題？
            dp[i] = dp[i-w] and s[i-w:i] in wordDict

            等效子問題？
            dp[i+w] = dp[i] and s[i:i+w] in wordDict

            當前操作？
            無法知道選個 w 是比較好的，所以列舉每一個可能性

        時間複雜度：O(N × W × L)
            - N = len(s)，外層 for i 跑 N 次
            - W = len(wordDict)，內層 for word 跑 W 次
            - L = max(len(word))，s[i:i+w] == word 字串比對需 O(L)
            - 等同於 Backtracking + @cache 的複雜度（bottom-up vs top-down）
            - 由於 L ≤ 20（題目限制），面試中常簡化寫成 O(N × W)
        空間複雜度：O(N)
            - dp 陣列大小 N+1

        ⚠️ 與 v2 的差異（為何 v2 更優）：
            本版本內層枚舉 wordDict（W 個字），每次做字串比對 O(L)。
            題目允許 W=1000、但長度最多 20 種（L≤20），
            → 等效枚舉次數 = N × W，可能比 N × L 大很多。
            v2 改為「枚舉長度 j」，只需 O(L) 次迭代並用 hash set O(L) 查詢，
            → 時間降為 O(N × L²)，且完全不受 W 影響。
        """

        size = len(s)
        dp = [False] * (size + 1)
        dp[0] = True

        # 從每個「已確認可拆解的位置 i」出發，
        # 嘗試所有 word，若 s[i:i+w] 匹配，
        # 就把 dp[i+w] 標記為可達 —— 類比決策樹的「向前延伸一步」。
        for i in range(size):
            for word in wordDict:
                w = len(word)
                # dp[i] = True：前綴 s[:i] 可拆解，才值得繼續延伸
                # i + w <= size：不越界（此 check 略冗餘，但可減少無效 slice）
                # s[i:i+w] == word：從 i 開始的子串恰好匹配這個字
                if dp[i] and i + w <= size and s[i : i + w] == word:
                    dp[i + w] = True  # s[:i+w] 也可被拆解
                    # ❌ 不可 break：此 word 把 dp[i+w] 標記為 True，
                    #    但其他 word（不同長度）可能更新別的位置 dp[i+w']，
                    #    提早 break 會漏掉那些位置的標記。

        # print(dp)
        return dp[size]

    def _dp_v2(self, s: str, wordDict: List[str]) -> bool:
        """
        解法三：1-D Dynamic Programming（枚舉長度 + Hash Set 查詢）

        思路：
            與 v1 相同 —— dp[i] 表示 s[:i] 是否可拆解。
            差異在「內層枚舉方式」：
                v1：枚舉 wordDict 中每個字（W 次）再比對字串
                v2：枚舉可能的切割長度 j（最多 L 種），再用 hash set O(L) 查詢

            關鍵觀察：
                wordDict 有多達 1000 個字，但長度最多只有 20 種（L ≤ 20）。
                → 應枚舉長度，而非枚舉字典。

        子問題（top-down 視角，對應 dfs(i)）：
            dfs(i) = True  若存在 j 使得 s[j:i] in words 且 dfs(j) = True

        等效 bottom-up：
            dp[i] = True  若存在 j 使得 s[j:i] in words 且 dp[j] = True
            其中 j 的範圍：max(0, i - max_len) ≤ j < i

        時間複雜度：O(WL + NL²)
            - W = len(wordDict)，建 hash set 需 O(WL)
            - N = len(s)，外層 for i 跑 N 次
            - 內層 j 最多跑 L 次（L = max_len ≤ 20）
            - s[j:i] in words：字串 hash 需 O(L)
            - 總計：O(WL + N × L × L) = O(WL + NL²)
            - 由於 L ≤ 20，NL² ≤ 300 × 400 = 120_000，遠小於 v1 的 N×W = 300_000
        空間複雜度：O(WL + N)
            - hash set O(WL) + dp 陣列 O(N)
        """

        # max_len：限制內層 j 的枚舉範圍，超過此長度的子串不可能在 wordDict 中
        max_len = max(map(len, wordDict))
        words = set(wordDict)  # hash set，讓 s[j:i] in words 查詢達到 O(L)（hash 計算）

        N = len(s)
        dp = [False] * (N + 1)
        dp[0] = True

        for i in range(1, N + 1):
            for length in range(1, min(i, max_len) + 1):
                # length：當前嘗試的子串長度（1 ~ min(i, max_len)）
                #   j   ：子串的起始索引，由 length 推導得出
                j = i - length

                # dp[j]：s[:j] 可拆解（前半段成立）
                # s[j:i] in words：後半段恰好是字典中的字
                if dp[j] and s[j:i] in words:
                    dp[i] = True

                    # dp[i] 已確定為 True，
                    # 不同的 length 都只是在寫同一個 dp[i]，繼續找毫無意義。
                    break

        return dp[N]


def main():
    solution = Solution()

    # Case 1：可拆解 → True
    assert solution.wordBreak("leetcode", ["leet", "code"]) == True

    # Case 2：可重複使用單字 → True
    assert solution.wordBreak("applepenapple", ["apple", "pen"]) == True

    # Case 3：無法拆解 → False
    assert (
        solution.wordBreak("catsandog", ["cats", "dog", "sand", "and", "cat"]) == False
    )

    print("All tests passed!")


if __name__ == "__main__":
    main()
