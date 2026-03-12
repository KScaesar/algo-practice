"""
# [300. Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/)
**Difficulty:** 🟡 Medium
**Tags:** Array, Binary Search, Dynamic Programming

## Problem Description

Given an integer array `nums`, return _the length of the longest **strictly increasing **__**subsequence**_.



Example 1:**

```

**Input:** nums = [10,9,2,5,3,7,101,18]
**Output:** 4
**Explanation:** The longest increasing subsequence is [2,3,7,101], therefore the length is 4.

```

Example 2:**

```

**Input:** nums = [0,1,0,3,2,3]
**Output:** 4

```

Example 3:**

```

**Input:** nums = [7,7,7,7,7,7,7]
**Output:** 1

```



**Constraints:**

        - `1 <= nums.length <= 2500`

        - `-10^4 <= nums[i] <= 10^4`



**Follow up:** Can you come up with an algorithm that runs in `O(n log(n))` time complexity?

## Similar Questions
- [Increasing Triplet Subsequence](https://leetcode.com/problems/increasing-triplet-subsequence/) (Medium)
- [Russian Doll Envelopes](https://leetcode.com/problems/russian-doll-envelopes/) (Hard)
- [Maximum Length of Pair Chain](https://leetcode.com/problems/maximum-length-of-pair-chain/) (Medium)
- [Number of Longest Increasing Subsequence](https://leetcode.com/problems/number-of-longest-increasing-subsequence/) (Medium)
- [Minimum ASCII Delete Sum for Two Strings](https://leetcode.com/problems/minimum-ascii-delete-sum-for-two-strings/) (Medium)
- [Minimum Number of Removals to Make Mountain Array](https://leetcode.com/problems/minimum-number-of-removals-to-make-mountain-array/) (Hard)
- [Find the Longest Valid Obstacle Course at Each Position](https://leetcode.com/problems/find-the-longest-valid-obstacle-course-at-each-position/) (Hard)
- [Minimum Operations to Make the Array K-Increasing](https://leetcode.com/problems/minimum-operations-to-make-the-array-k-increasing/) (Hard)
- [Longest Ideal Subsequence](https://leetcode.com/problems/longest-ideal-subsequence/) (Medium)
- [Maximum Number of Books You Can Take](https://leetcode.com/problems/maximum-number-of-books-you-can-take/) (Hard)
- [Longest Increasing Subsequence II](https://leetcode.com/problems/longest-increasing-subsequence-ii/) (Hard)
- [Find the Maximum Length of a Good Subsequence II](https://leetcode.com/problems/find-the-maximum-length-of-a-good-subsequence-ii/) (Hard)
- [Find the Maximum Length of a Good Subsequence I](https://leetcode.com/problems/find-the-maximum-length-of-a-good-subsequence-i/) (Medium)
- [Find the Maximum Length of Valid Subsequence I](https://leetcode.com/problems/find-the-maximum-length-of-valid-subsequence-i/) (Medium)
- [Find the Maximum Length of Valid Subsequence II](https://leetcode.com/problems/find-the-maximum-length-of-valid-subsequence-ii/) (Medium)
- [Longest Subsequence With Decreasing Adjacent Difference](https://leetcode.com/problems/longest-subsequence-with-decreasing-adjacent-difference/) (Medium)
"""

from functools import cache
from typing import List

# https://www.bilibili.com/video/BV1ub411Q7sB/?vd_source=deac8b505de301c629b87c1abebac9f3

class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        # Time Complexity: O(N^2)
        #   - 有 N 個 state (i 從 0 到 N-1)
        #   - 每個 state 會跑一次 O(N) 的 for 迴圈 (找前面的元素)
        #   - 狀態總數 × 每個狀態執行時間 = O(N) * O(N) = O(N^2)
        #   - 最後的 max(...) 也是 O(N)，不會改變複雜度。
        #
        # Space Complexity: O(N)
        #   - @cache 的記憶體最多存 N 個狀態，O(N)
        #   - 遞迴呼叫堆疊 (Call Stack) 最深到 N 層，O(N)
        
        # 注意 sequence 和 array 的差異
        # sequence 不需要連續, 只需要保持 order
        # array 需要連續, 不能跳過元素

        size = len(nums)

        # 站在「答案」的角度, 以 i 為結尾的 LIS 最多多長
        @cache
        def dfs(i: int) -> int:
            if i == size:
                return 0

            # Base case：自己就算一個長度為 1 的子序列
            max_len = 1
            for j in range(i - 1, -1, -1):
                if nums[j] < nums[i]:
                    max_len = max(max_len, dfs(j) + 1)

                # 既然 dfs(i) 的定義是「必須把 nums[i] 當作最後一個數字接上去」
                # 當遇到 nums[j] >= nums[i] 時
                # 意味著 nums[i] 根本接不上去，不需要考慮
            return max_len

        return max(dfs(i) for i in range(size))


def main():
    solution = Solution()

    # Case 1
    assert solution.lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18]) == 4

    # Case 2
    assert solution.lengthOfLIS([0, 1, 0, 3, 2, 3]) == 4

    # Case 3
    assert solution.lengthOfLIS([7, 7, 7, 7, 7, 7, 7]) == 1

    print("All tests passed!")


if __name__ == "__main__":
    main()
