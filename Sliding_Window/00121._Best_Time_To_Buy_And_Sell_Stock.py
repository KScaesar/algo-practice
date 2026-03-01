"""
# [121. Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)
**Difficulty:** 🟢 Easy
**Tags:** Array, Dynamic Programming

## Problem Description

You are given an array `prices` where `prices[i]` is the price of a given stock on the `i^th` day.

You want to maximize your profit by choosing a **single day** to buy one stock and choosing a **different day in the future** to sell that stock.

Return _the maximum profit you can achieve from this transaction_. If you cannot achieve any profit, return `0`.



Example 1:**

```

**Input:** prices = [7,1,5,3,6,4]
**Output:** 5
**Explanation:** Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.

```

Example 2:**

```

**Input:** prices = [7,6,4,3,1]
**Output:** 0
**Explanation:** In this case, no transactions are done and the max profit = 0.

```



**Constraints:**

        - `1 <= prices.length <= 10^5`

        - `0 <= prices[i] <= 10^4`

"""

from typing import List


class Solution:
    def _brute_force(self, prices: List[int]) -> int:
        """
        暴力解：外迴圈枚舉買入日，內迴圈枚舉賣出日，兩兩相減取最大正利潤。
        Time:  O(n²)
        Space: O(1)

        思考暴力解的瓶頸在哪？
        有沒有哪些資訊是被「重複計算」的？
        """
        max_profit = 0
        for i in range(len(prices)):  # 買入日
            for j in range(i + 1, len(prices)):  # 賣出日（必須在買之後）
                profit = prices[j] - prices[i]
                max_profit = max(max_profit, profit)
        return max_profit

    def _single_pass(self, prices: List[int]) -> int:
        """
        最優解：Single Pass（Two Pointers / Sliding Window 概念）
        Time:  O(n)
        Space: O(1)

        【思路演進】
        直覺：找最大最小相減 → 但有時間線性要素，最小值可能出現在最大值之後，不能直接用。

        換個方向思考:
          想像外迴圈變成「賣出日」，內迴圈變成「買入日」?
          對於每一個「賣出日」，我真的需要檢查它之前「所有的可能買入日」嗎？
          如果今天是「賣出日」，需要知道的買入資訊是什麼？

        最優解關鍵洞察：
          對於每個賣出日，我只需要「它之前見過的最低價」即可，
          不需要重新掃描 → 用一個變數 min_price 邊走邊記，化成 O(n)。

        【Sliding Window 對應關係】
        - 左指針 L（買入日） → min_price：L 停留位置的「價格快照」，只在找到更低價時跳過去
        - 右指針 R（賣出日） → for 迴圈的 price：R 每步固定往右一格
        - 窗口的「價值」      → price - min_price：L~R 這段窗口的利潤
        """
        min_price = prices[0]  # 歷史最低買入價，初始為第一天
        max_profit = 0

        for price in prices:
            # 1. 更新歷史最低買入價（今天比之前還便宜就更新）
            min_price = min(min_price, price)

            # 2. 假設今天賣出，利潤 = 今日價 − 歷史最低，更新最大值
            max_profit = max(max_profit, price - min_price)

        return max_profit

    def _kadane(self, prices: List[int]) -> int:
        """
        解法3：Kadane's Algorithm 變體

        關鍵問題： prices[j] - prices[i]（買入 i，賣出 j）可以拆解嗎？
        → 買在第 i 天、賣在第 j 天的利潤 = diff[i+1] + ... + diff[j]
        → 這就是 diff 陣列上的「子數組總和」！
        → 最大利潤 = diff 陣列上的最大子數組和 = Kadane's Algorithm！

        將問題轉換為「差分陣列上的最大子數組和」。
        Time:  O(n)
        Space: O(n)  → 若邊走邊算 diff 可降為 O(1)

        【思路演進】
        洞察： prices[j] - prices[i] 可以拆成逐日漲跌的累加：
        疑問： 這個做法只能把第一天當買入，怎麼讓它「換日重新計算」？
        解答： Kadane's 的關鍵一行 —— if current_sum < 0: current_sum = 0
              當累積漲跌為負，代表從更早買入已不划算，
              「歸零」的語意就是：放棄之前的買入點，以今天為新起點。

        另外踩過的坑：
          ❌ prices[i-1] - prices[i]  ← 差分方向反了（算的是跌幅）
          ✅ prices[i] - prices[i-1]  ← 漲幅才對
        """
        diff = [prices[i] - prices[i - 1] for i in range(1, len(prices))]

        max_profit = 0
        current_sum = 0
        for d in diff:
            current_sum += d
            max_profit = max(max_profit, current_sum)
            if current_sum < 0:
                current_sum = 0  # 歸零 = 放棄舊買入點，從下一天重新開始

        return max_profit

    def maxProfit(self, prices: List[int]) -> int:
        # return self._brute_force(prices)
        # return self._single_pass(prices)
        return self._kadane(prices)


def main():
    solution = Solution()

    # Case 1
    assert solution.maxProfit([7, 1, 5, 3, 6, 4]) == 5

    # Case 2
    assert solution.maxProfit([7, 6, 4, 3, 1]) == 0

    print("All tests passed!")


if __name__ == "__main__":
    main()
