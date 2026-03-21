"""
# [831. Largest Sum of Averages](https://leetcode.com/problems/largest-sum-of-averages/)
**Difficulty:** 🟡 Medium
**Tags:** Array, Dynamic Programming, Prefix Sum

## Problem Description

You are given an integer array `nums` and an integer `k`. You can partition the array into **at most** `k` non-empty adjacent subarrays. The **score** of a partition is the sum of the averages of each subarray.

Note that the partition must use every integer in `nums`, and that the score is not necessarily an integer.

Return _the maximum **score** you can achieve of all the possible partitions_. Answers within `10^-6` of the actual answer will be accepted.



Example 1:**

```

**Input:** nums = [9,1,2,3,9], k = 3
**Output:** 20.00000
**Explanation:**
The best choice is to partition nums into [9], [1, 2, 3], [9]. The answer is 9 + (1 + 2 + 3) / 3 + 9 = 20.
We could have also partitioned nums into [9, 1], [2], [3, 9], for example.
That partition would lead to a score of 5 + 2 + 6 = 13, which is worse.

```

Example 2:**

```

**Input:** nums = [1,2,3,4,5,6,7], k = 4
**Output:** 20.50000

```



**Constraints:**

        - `1 <= nums.length <= 100`

        - `1 <= nums[i] <= 10^4`

        - `1 <= k <= nums.length`
"""

import math
from functools import cache
from typing import List

# --- 複雜度分析與切分組合圖解 ---
#
# Q: 為什麼「每個空隙切或不切，共 2^(N-1) 種可能」？
# A: 想像我們陣列有 N = 4 個元素 (A, B, C, D)
#
#   Elements:   A       B       C       D
#               |       |       |       |
#     Gaps:       Gap 1   Gap 2   Gap 3    => 總共有 N-1 個空隙
#
# 對於每一個空隙，我們都有 2 種選擇：
# [X] 切一刀 (把左右元素分開)
# [ ] 不切 (讓左右元素連在一起)
#
# 所有可能的切法組合：
# 1. [ ] [ ] [ ] -> (ABCD)                  => 1 組
# 2. [X] [ ] [ ] -> (A), (BCD)              => 2 組
# 3. [ ] [X] [ ] -> (AB), (CD)              => 2 組
# 4. [ ] [ ] [X] -> (ABC), (D)              => 2 組
# 5. [X] [X] [ ] -> (A), (B), (CD)          => 3 組
# 6. [X] [ ] [X] -> (A), (BC), (D)          => 3 組
# 7. [ ] [X] [X] -> (AB), (C), (D)          => 3 組
# 8. [X] [X] [X] -> (A), (B), (C), (D)      => 4 組
#
# 結論：
# - 每一個空隙都有 2 種選擇。
# - 總共有 N-1 個空隙。
# - 總組合數 = 2 * 2 * ... (乘 N-1 次) = 2^(N-1)。
# - 如果我們再加上「最多只能 k 組」的限制，就等同於在 N-1 個空隙裡面，
#   恰好 / 最多挑選 k-1 個位置來切刀，也就是組合數學中的 C(N-1, k-1)。
#
# --- 遞迴樹 (Recursion Tree) 與重疊子問題 ---
# 以陣列 [9, 1, 2, 3], k = 3 為例：
# 狀態定義：(i, k)
#           i = 當前處理到第幾個 index
#           k = 剩下幾組可以切
#
#                              (0, 3)
#                       [處理 9, 1, 2, 3]
#                      /                 \
#             割 [9] /                    \ 割 [9, 1]
#                  /                       \
#              (1, 2)                     (2, 2)
#         [處理 1, 2, 3]                [處理 2, 3]
#           /          \                     /
#   割 [1] /            \ 割 [1, 2]         / 割 [2]
#        /                \               /
#     (2, 1)             *(3, 1)*      *(3, 1)*
#  [處理 2, 3]           [處理 3]      [處理 3]
#      |                    |              |
#  (Base Case)          (Base Case)    (Base Case)
#  只剩1堆不切了         只剩1堆不切了    只剩1堆不切了
#  回傳 avg([2,3])       回傳 avg([3])    回傳 avg([3])
#
# 重點觀察：
# 1. 發現重疊子問題 (Overlapping Subproblem) *(3, 1)* 運算了兩次。
# 2. Base Case 是 k=1，必定把剩下的元素全部當成最後一組。

# https://leetcode.cn/problems/largest-sum-of-averages/solutions/630637/dong-tai-gui-hua-xiang-jie-by-wang-nmana-v1vk/


class Solution:
    def largestSumOfAverages(self, nums: List[int], k: int) -> float:
        # ==========================================
        # 解題思路與複雜度分析 (Top-down DP + Prefix Sum)
        # ==========================================
        # 為什麼是 方法 a (輸入視角)？
        # - 我們站在當前元素 i 的面前，決定「這次要包幾個元素 (從 i 包到 j)」。
        # - 包完之後，剩下的元素 j+1 獨立交給下一層處理，前後數值互不牽制。
        #
        # 狀態定義 dfs(i, k)：
        # - 從第 i 個元素到最後，最多切成 k 堆，能獲得的最大「平均數總和」。
        #
        # 轉移方程式 (Recursive Step)：
        # - 嘗試切一刀在 j 的位置 (i <= j <= n-k)，使得這一堆是 nums[i...j]。
        # - dfs(i, k) = max( avg(nums[i...j]) + dfs(j+1, k-1) ) for all valid j.
        #
        # 前綴和 (Prefix Sum) 優化：
        # - 為了在 O(1) 內算出 avg(nums[i...j])，我們預處理 prefix_sum。
        #
        # 為什麼有了 @cache，還需要 Prefix Sum？（兩者分工完全不同）
        # - @cache 省下的是「狀態的重複展開（樹狀分支）」。
        #   當其他遞迴路徑也遇到了曾經計算過的 dfs(i, k) 時，它可以瞬間給出最佳解。
        #   這省下了重複執行整個 O(N) for 迴圈以及更深層的遞迴分支。
        # - Prefix Sum 省下的是「狀態內部（單一節點中）的迴圈加總成本」。
        #   每次 dfs 測試不同切法 nums[i...j] 時，都需要計算這一段的總和。
        #   如果每次都開 for 迴圈硬加，會讓每一個狀態的執行成本從 O(N) 變成 O(N^2)。
        #   有了 Prefix Sum 預算表，就能瞬間 O(1) 查出任何區間的總和。
        #
        # 複雜度分析：
        # - Time Complexity: O(N^2 * K)
        #   - 總共有 N * K 個狀態 (i 範圍 0~N, k 範圍 1~K)。
        #   - 每個狀態內部需要一個長度最多為 N 的 for 迴圈來枚舉切點 j。
        #   - 狀態數 O(N*K) × 單次回圈遍歷 O(N) = 總時間 O(N^2 * K)。
        # - Space Complexity: O(N * K)
        #   - @cache 最多記錄 N * K 個狀態結果。
        #   - DFS 遞迴深度最多為 K。
        #   - prefix_sum 陣列長度為 N+1。
        #   - 總結空間被 DP table 主導，為 O(N * K)。
        # ==========================================
        n = len(nums)

        prefix_sum = [0] * (n + 1)
        for i in range(n):
            prefix_sum[i + 1] = prefix_sum[i] + nums[i]

        @cache
        def dfs(i, k) -> float:
            if k == 1:
                # prefix_sum[i] = nums[0] + ... + nums[i-1]
                # prefix_sum[n] = nums[0] + ... + nums[n-1]
                return (prefix_sum[n] - prefix_sum[i]) / (n - i)

            # range(i, n) 的 j 一路跑到 n-1（陣列最後一個數）
            # 但下來還有 k-1 堆要分
            # 所以必須保留至少 k-1 個元素
            ans = 0.0
            for j in range(i, n - (k - 1)):
                ans = max(
                    ans,
                    dfs(j + 1, k - 1)
                    + (prefix_sum[j + 1] - prefix_sum[i]) / (j - i + 1),
                )
            return ans

        return dfs(0, k)


def main():
    solution = Solution()

    # Example 1
    assert math.isclose(
        solution.largestSumOfAverages([9, 1, 2, 3, 9], 3), 20.00000, abs_tol=1e-5
    )

    # Example 2
    assert math.isclose(
        solution.largestSumOfAverages([1, 2, 3, 4, 5, 6, 7], 4), 20.50000, abs_tol=1e-5
    )

    print("All tests passed!")


if __name__ == "__main__":
    main()
