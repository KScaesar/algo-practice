"""
# [4245. Count Commas in Range](https://leetcode.com/problems/count-commas-in-range/)
**Difficulty:** 🟢 Easy
**Tags:** Math

## Problem Description

You are given an integer `n`.

Return the **total** number of commas used when writing all integers from `[1, n]` (inclusive) in **standard** number formatting.

In **standard** formatting:

        - A comma is inserted after **every three** digits from the right.

        - Numbers with **fewer** than 4 digits contain no commas.



**Example 1:**

**Input:** n = 1002
**Output:** 3
**Explanation:**
The numbers `"1,000"`, `"1,001"`, and `"1,002"` each contain one comma, giving a total of 3.

**Example 2:**

**Input:** n = 998
**Output:** 0
**Explanation:**
All numbers from 1 to 998 have fewer than four digits. Therefore, no commas are used.



**Constraints:**

        - `1 <= n <= 10^5`

## Hints
1. Numbers in the range `[1000, 100000]` have one comma.
"""


class Solution:
    def countCommas_v1(self, n: int) -> int:
        """
        解法 1：暴力迴圈法 (Time Complexity: O(N))
        逐步遞減驗證直到無逗號為止。
        """
        ans = 0
        q = n // 1000
        while q != 0:
            ans += 1
            n -= 1
            q = n // 1000
        return ans

    def countCommas_v2(self, n: int) -> int:
        """
        解法 2：數學規律法 (Time Complexity: O(1))
        觀察 1 <= n <= 10^5，直接計算大於等於 1000 的數字數量。
        """
        # 📝 筆記：
        # 原本最直覺是想寫 `if n > 999: return n - 999 else: return 0`
        # 後來發現可以直接利用 `max(0, ...)` 這個技巧，
        # 把「小於 0 的情況自動夾在 (clamp) 0」，讓程式碼變得只有一行，更乾淨優雅！
        # 1e3    類型是 float（1000.0）直接 `-1` 運算結果會變成 float
        # 10**3  類型是 int（1000）
        #
        # ⚠️ 進階探討：為何此解法在 n >= 1,000,000 (大於六位數) 時會失效？
        # 因為 `n - 999` 這條公式的底層假設是：「每一個大於等於 1000 的數字都『恰好只貢獻 1 個逗號』」。
        # 但是當數字來到 1,000,000 (七位數) 及以上時，它身上會開始出現第 2 個逗號（例如 1,000,000）。
        # 此時如果只用 `n - 999`，我們就只算到了它們的第 1 個逗號，而「少算」了百萬級距帶來的第 2 個逗號。
        # (附帶一提，v1 的迴圈解法因為每次也只 +1，所以同樣會遇到少算的問題喔！)
        # 若要涵蓋更大範圍，通用版的 O(1) 寫法會變成疊加： max(0, n - 999) + max(0, n - 999999) + ...
        return max(0, n - (10**3 - 1))

    def countCommas_v3(self, n: int) -> int:
        """
        解法 3：通用數學疊加法 (Time Complexity: O(log_{1000} N))
        打破 n <= 10^5 的限制，可以處理任意大小的數字 (如 n >= 1,000,000)。
        從右往左，枚舉每個逗號的位置並加上該位置貢獻的逗號總數。
        """
        ans = 0
        low = 10**3
        while low <= n:
            ans += n - low + 1
            low *= 1000
        return ans


def main():
    solution = Solution()

    if solution.countCommas_v1(1002) is not None:
        assert solution.countCommas_v1(1002) == 3
        assert solution.countCommas_v1(998) == 0
        assert solution.countCommas_v1(2000) == 1001
        assert solution.countCommas_v1(1000) == 1
        print("v1 測試通過！")

    if solution.countCommas_v2(1002) is not None:
        assert solution.countCommas_v2(1002) == 3
        assert solution.countCommas_v2(998) == 0
        assert solution.countCommas_v2(2000) == 1001
        assert solution.countCommas_v2(1000) == 1
        print("v2 測試通過！")

    if solution.countCommas_v3(1002) is not None:
        assert solution.countCommas_v3(1002) == 3
        assert solution.countCommas_v3(998) == 0
        assert solution.countCommas_v3(2000) == 1001
        assert solution.countCommas_v3(1000) == 1
        assert solution.countCommas_v3(1004590) == 1008182
        print("v3 測試通過！")

    print("All tests passed!")


if __name__ == "__main__":
    main()
