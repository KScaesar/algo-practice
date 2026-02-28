"""
# [Kth Largest Element in an Array](https://neetcode.io/problems/kth-largest-element-in-an-array/question?list=neetcode150)
**Source:** neetcode.io

## Problem Description

Given an unsorted array of integers `nums` and an integer `k`, return the `kth` largest element in the array.

By `kth` largest element, we mean the `kth` largest element in the sorted order, not the `kth` distinct element.

Follow-up: Can you solve it without sorting?

**Example 1:**

```
Input: nums = [2,3,1,5,4], k = 2

Output: 4
```

**Example 2:**

```
Input: nums = [2,3,1,1,5,5,4], k = 3

Output: 4
```

**Constraints:**

* `1 <= k <= nums.length <= 10000`
* `-1000 <= nums[i] <= 1000`

**Recommended Time & Space Complexity:** O(nlogk) time and O(k) space
"""

import heapq
from typing import List, Optional, Dict, Tuple


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        # O(n log k) / O(k)
        # return self._heap(nums, k)

        # O(n) avg  / O(log n) （遞迴 call stack 空間）
        return self._quickselect(nums, 0, len(nums) - 1, k)

    def _heap(self, nums: List[int], k: int) -> int:
        # --- heapq API reminder ---
        # heap = []                      # 初始化（普通 list）
        # heapq.heappush(heap, val)      # push，O(log n) 預設是 min-heap
        # heapq.heappop(heap)            # pop 最小值，O(log n)
        # heap[0]                        # 查看頂端（最小值），O(1)
        # len(heap)                      # 當前大小
        # --------------------------
        heap = []
        for num in nums:
            heapq.heappush(heap, num)
            if len(heap) > k:
                heapq.heappop(heap)
        return heap[0]

    def _quickselect(self, nums: List[int], left: int, right: int, k: int) -> int:
        """
        在 nums[left..right] 範圍內找第 k 大的元素。
        1. 呼叫 _partition 取得 pivot 的最終 index p
        2. 比較 p 與 k-1，決定往左、往右，或直接回傳
        """
        p = self._partition(nums, left, right)
        if p == k-1:
            return nums[p]
        elif p > k-1:
            return self._quickselect(nums, left, p-1, k)
        else:
            return self._quickselect(nums, p+1, right, k)

    def _partition(self, nums: List[int], left: int, right: int) -> int:
        """
        以 nums[right] 為 pivot，做降序 partition（大在左、小在右）。
        回傳 pivot 最終落在的 index。
        """
        pivot = nums[right]
        fill = left
        for j in range(left, right):
            if nums[j] > pivot:          # > 而非 >= : 避免重複元素造成 O(n²) 退化
                nums[fill], nums[j] = nums[j], nums[fill]
                fill += 1
        nums[fill], nums[right] = nums[right], nums[fill]
        return fill

def main():
    solution = Solution()

    # Case 1
    assert solution.findKthLargest([2, 3, 1, 5, 4], 2) == 4

    # Case 2
    assert solution.findKthLargest([2, 3, 1, 1, 5, 5, 4], 3) == 4

    assert solution.findKthLargest([4, 3, 1, 1, 5, 5, 2], 3) == 4

    print("All tests passed!")


if __name__ == "__main__":
    main()
