"""
# [3. Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/)
**Difficulty:** 🟡 Medium
**Tags:** Hash Table, String, Sliding Window

## Problem Description

Given a string `s`, find the length of the **longest** **substring** without duplicate characters.



Example 1:**

```

**Input:** s = "abcabcbb"
**Output:** 3
**Explanation:** The answer is "abc", with the length of 3. Note that `"bca"` and `"cab"` are also correct answers.

```

Example 2:**

```

**Input:** s = "bbbbb"
**Output:** 1
**Explanation:** The answer is "b", with the length of 1.

```

Example 3:**

```

**Input:** s = "pwwkew"
**Output:** 3
**Explanation:** The answer is "wke", with the length of 3.
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.

```



**Constraints:**

        - `0 <= s.length <= 5 * 10^4`

        - `s` consists of English letters, digits, symbols and spaces.

## Hints
1. Generate all possible substrings & check for each substring if it's valid and keep updating maxLen accordingly.

## Similar Questions
- [Longest Substring with At Most Two Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-two-distinct-characters/) (Medium)
- [Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/) (Medium)
- [Subarrays with K Different Integers](https://leetcode.com/problems/subarrays-with-k-different-integers/) (Hard)
- [Maximum Erasure Value](https://leetcode.com/problems/maximum-erasure-value/) (Medium)
- [Number of Equal Count Substrings](https://leetcode.com/problems/number-of-equal-count-substrings/) (Medium)
- [Minimum Consecutive Cards to Pick Up](https://leetcode.com/problems/minimum-consecutive-cards-to-pick-up/) (Medium)
- [Longest Nice Subarray](https://leetcode.com/problems/longest-nice-subarray/) (Medium)
- [Optimal Partition of String](https://leetcode.com/problems/optimal-partition-of-string/) (Medium)
- [Count Complete Subarrays in an Array](https://leetcode.com/problems/count-complete-subarrays-in-an-array/) (Medium)
- [Find Longest Special Substring That Occurs Thrice II](https://leetcode.com/problems/find-longest-special-substring-that-occurs-thrice-ii/) (Medium)
- [Find Longest Special Substring That Occurs Thrice I](https://leetcode.com/problems/find-longest-special-substring-that-occurs-thrice-i/) (Medium)
"""


class Solution:
    def lengthOfLongestSubstring_brute(self, s: str) -> int:
        """
        暴力解：枚舉所有子字串
        - 雙迴圈枚舉起點 i 與終點 j
        - 用 Set 判斷 s[i..j] 是否有重複字元
        - 若無重複 → 更新最大長度

        Time:  O(n²) ~ O(n³)  — 雙迴圈 × Set 建立
        Space: O(min(n, m))   — Set 最多存字元集大小
        """
        result = 0
        n = len(s)

        for i in range(n):
            seen = set()
            for j in range(i, n):
                if s[j] in seen:
                    break  # 出現重複，此起點終止
                seen.add(s[j])
                result = max(result, j - i + 1)

        return result

    def lengthOfLongestSubstring_set(self, s: str) -> int:
        """
        Sliding Window + Set：
        - Set 記錄視窗內現有的字元
        - right 每次向右擴展，若 s[right] 已在 Set（重複），
          用 while 從 left 逐一移除，直到重複消除，再把 s[right] 加入
        - 更新 result = max(result, right - left + 1)

        與 v2 HashMap 的差異：
          Set 版需要 while 逐步縮左（left 最多走 n 步），
          HashMap 版直接跳到 last_seen[ch]+1（O(1) 定位）。
          Time 同為 O(n)，但 HashMap 版常數較小、更直觀。

        Time:  O(n)           — left / right 各最多走 n 步
        Space: O(min(n, m))   — Set 最多存字元集大小 m
        """
        left = 0
        seen = set()
        result = 0

        for right in range(len(s)):
            while s[right] in seen:  # 有重複就從左縮
                seen.remove(s[left])
                left += 1
            seen.add(s[right])
            result = max(result, right - left + 1)

        return result

    def lengthOfLongestSubstring_v1(self, s: str) -> int:
        """
        【原始思路】（第一直覺）
        用 r index 走訪字串，每次查看 map 此字元出現次數是否為 0：
          - 為 0（不重複）：更新 window 答案，map 次數 +1
          - 非 0（重複）  ：清空整個 map，以 l 為新起點，長度 = r - l + 1，更新最大值

        【缺失的要素 → 修正後的做法】
        1. ❌ map 存「出現次數」→ ✅ 應存「上次出現的 index」
           才能直接跳 left = last_seen[ch] + 1，不用重置整個 map。

        2. ❌ 清空 map、重設 l → ✅ left = max(left, last_seen[ch] + 1)
           取 max 是為了防止 left 倒退：若重複字元的舊 index 已在視窗外，
           不應讓 left 往左縮。反例："abba"，right=3 遇 'a'，
           last_seen['a']=0，但 left 已是 2，不取 max 會退回 left=1。

        3. ❌ result 只在不重複時更新 → ✅ 在 loop 末尾統一更新
           遇重複但舊 index 在視窗外時，left 不動、right 仍前進，
           視窗反而長大，此時也要更新 result。反例："tmmzuxt"。

        ⚠️ Bug 1（操作順序）：else 分支先寫入 last_seen[ch]=right 再讀，
            讀到的是新值，left 跳過頭 → 先讀舊值計算 left，再更新 map。
        ⚠️ Bug 2（漏算）：else 分支忘記更新 result → 移至 loop 末尾統一計算。
        """
        left = 0
        last_seen = {}
        result = 0

        for right in range(len(s)):
            ch = s[right]
            if last_seen.get(ch) is None:
                last_seen[ch] = right
            else:
                left = max(left, last_seen[ch] + 1)  # 先讀舊 index
                last_seen[ch] = right  # 再更新
            result = max(result, right - left + 1)  # 統一在最後更新

        return result

    def lengthOfLongestSubstring_v2(self, s: str) -> int:
        """
        算法描述（Sliding Window + HashMap）：
        1. 維護左指標 left 與右指標 right，形成一個不含重複字元的滑動視窗
        2. 右指標每次向右移動一格，讀取當前字元 ch
        3. 若 ch 已在 map 中（代表視窗內有重複）：
           - 將 left 跳至 max(left, last_seen[ch] + 1)，取 max 防止 left 倒退
        4. 更新 map：last_seen[ch] = right（記錄 ch 最後出現的位置）
        5. 更新答案：result = max(result, right - left + 1)
        6. 重複 2~5 直到 right 走完整個字串

        Time: O(n)  — right 只走一遍，left 最多也只走一遍
        Space: O(min(n, m))  — m 為字元集大小（ASCII 最多 128）
        """
        left = 0
        last_seen = {}
        result = 0

        for right in range(len(s)):
            ch = s[right]
            if ch in last_seen:
                left = max(left, last_seen[ch] + 1)
            last_seen[ch] = right
            result = max(result, right - left + 1)

        return result

    # 面試使用 v2
    def lengthOfLongestSubstring(self, s: str) -> int:
        return self.lengthOfLongestSubstring_v2(s)


def main():
    solution = Solution()

    # Case 1
    assert solution.lengthOfLongestSubstring("abcabcbb") == 3

    # Case 2
    assert solution.lengthOfLongestSubstring("bbbbb") == 1

    # Case 3
    assert solution.lengthOfLongestSubstring("pwwkew") == 3
    assert solution.lengthOfLongestSubstring("tmmzuxt") == 5

    print("All tests passed!")


if __name__ == "__main__":
    main()
