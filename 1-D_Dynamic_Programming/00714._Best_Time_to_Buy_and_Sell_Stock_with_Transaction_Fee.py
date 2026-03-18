"""
# [714. Best Time to Buy and Sell Stock with Transaction Fee](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/)
**Difficulty:** 🟡 Medium
**Tags:** Array, Dynamic Programming, Greedy

## Problem Description

You are given an array `prices` where `prices[i]` is the price of a given stock on the `i^th` day, and an integer `fee` representing a transaction fee.

Find the maximum profit you can achieve. You may complete as many transactions as you like, but you need to pay the transaction fee for each transaction.

**Note:**

        - You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).

        - The transaction fee is only charged once for each stock purchase and sale.



Example 1:

```
**Input:** prices = [1,3,2,8,4,9], fee = 2
**Output:** 8
**Explanation:** The maximum profit can be achieved by:
- Buying at prices[0] = 1
- Selling at prices[3] = 8
- Buying at prices[4] = 4
- Selling at prices[5] = 9
The total profit is ((8 - 1) - 2) + ((9 - 4) - 2) = 8.
```

Example 2:

```
**Input:** prices = [1,3,7,5,10,3], fee = 3
**Output:** 6
```



**Constraints:**

        - `1 <= prices.length <= 5 * 10^4`

        - `1 <= prices[i] < 5 * 10^4`

        - `0 <= fee < 5 * 10^4`

## Hints
1. Consider the first K stock prices.  At the end, the only legal states are that you don't own a share of stock, or that you do.  Calculate the most profit you could have under each of these two cases.

## Similar Questions
- [Best Time to Buy and Sell Stock II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-II/) (Medium)
"""

from functools import cache
from typing import List

# --- 總結與盲點 (Conclusion & Insights) ---
# 1. 方法 a (前 i 天) vs 方法 b (以 i 結尾)：
#    - 【初期盲點】：原本直覺是思考「第 i 天這天發生了買或賣，那前面要跟哪一天接？」。
#      這屬於「方法 b」，會導致需要內層迴圈枚舉所有 j < i，複雜度 O(N^2)。
#    - 【轉向最佳化】：改為思考「這天結束時，我處於什麼狀態？」。這屬於「方法 a」。
#      既然是「前 i 天的最優解」，那麼第 i 天的結果只取決於前一天的狀態：
#      今天要持有的話，要麼是昨天就持有，要麼是昨天不持有今天買入。
#      這使得轉移降為 O(1)，總時間 O(N)。
#
# 2. 狀態機 DP (State Machine DP)：
#    - 透過 `holding=True/False` 將複雜的交易條件拆解成簡單的狀態轉換圖。
#    - 關鍵在於「不作為 (No Action)」的選項：`dfs(i-1, holding)`。
#      這代表了「觀望」的價值，讓 DP 陣列能自動繼承過去的最優解。
#
# 3. 邊界條件 (Base Case) 的嚴謹邏輯：
#    - i = -1 (尚未開始)：
#        - `not holding` (空手): 利潤為 0。
#        - `holding` (持股): 現實中不可能，在 max 運算中須設為 `-inf` 以防止非法狀態被誤選。
#    - 利潤初始化：避免使用 `ans = 0` 做初始賦值，因為買入動作（負獲利）可能被 0 掩蓋，直接比較狀態轉移的 return 值。


class Solution:
    def maxProfit(self, prices: List[int], fee: int) -> int:

        # 方法 a：考慮「前 i 天」結束後的狀態（持有/不持有），最大利潤是多少
        @cache
        def dfs(i: int, holding: bool) -> int:
            """
            核心思維：方法 a (前 i 個元素的最優值) + 狀態機。
            不只是考慮「最後一天做什麼」，而是考慮「到這天結束時我們處於什麼狀態」。
            """
            # Base Case: i = -1 代表交易尚未開始
            if i == -1:
                # 初始狀態：不持有股票利潤為 0；「持有股票」在尚未開始前是不可能的，給予極小值以避開 max 選擇。
                return 0 if not holding else float("-inf")

            if holding:
                # 盲點提醒：不要看成「方法 b (枚舉 j<i)」，那會變成 O(N^2)。
                # 既然是「方法 a (前 i 天最優)」，我們只需要看「昨天」的狀態。
                return max(
                    # 1. 昨天不持有，今天買入 (-prices[i])
                    dfs(i - 1, False) - prices[i],
                    # 2. 昨天就持有，今天不做事 (維持狀態)
                    dfs(i - 1, True),
                )
            else:
                return max(
                    # 1. 昨天持有，今天賣出 (+prices[i] - fee)
                    dfs(i - 1, True) + prices[i] - fee,
                    # 2. 昨天就不持有，今天不做事 (維持狀態)
                    dfs(i - 1, False),
                )

        return dfs(len(prices) - 1, False)


def main():
    solution = Solution()

    # Case 1
    prices1 = [1, 3, 2, 8, 4, 9]
    fee1 = 2
    assert solution.maxProfit(prices1, fee1) == 8

    # Case 2
    prices2 = [1, 3, 7, 5, 10, 3]
    fee2 = 3
    assert solution.maxProfit(prices2, fee2) == 6

    print("All tests passed!")


if __name__ == "__main__":
    main()
