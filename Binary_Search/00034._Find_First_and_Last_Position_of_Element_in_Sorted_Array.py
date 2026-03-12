"""
# [34. Find First and Last Position of Element in Sorted Array](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/)
**Difficulty:** 🟡 Medium
**Tags:** Array, Binary Search

## Problem Description

Given an array of integers `nums` sorted in non-decreasing order, find the starting and ending position of a given `target` value.

If `target` is not found in the array, return `[-1, -1]`.

You must write an algorithm with `O(log n)` runtime complexity.

Example 1:**

```
**Input:** nums = [5,7,7,8,8,10], target = 8
**Output:** [3,4]

```
Example 2:**

```
**Input:** nums = [5,7,7,8,8,10], target = 6
**Output:** [-1,-1]

```
Example 3:**

```
**Input:** nums = [], target = 0
**Output:** [-1,-1]

```

**Constraints:**

        - `0 <= nums.length <= 10^5`

        - `-10^9 <= nums[i] <= 10^9`

        - `nums` is a non-decreasing array.

        - `-10^9 <= target <= 10^9`

## Similar Questions
- [Find Target Indices After Sorting Array](https://leetcode.com/problems/find-target-indices-after-sorting-array/) (Easy)
"""

from typing import List

# ==============================================================================
# 1. Lower Bound / Upper Bound 的標準定義
#
# 依據 C++ STL (std::lower_bound, std::upper_bound) 的定義
#
# [Lower Bound]
# 第一個 >= target 的位置 find_gte(nums, target)
# Python 對應： bisect_left(nums, target)
# 例： nums = [1,2,2,2,3], target = 2 -> lower_bound = 1
#
# [Upper Bound]
# 第一個 > target 的位置 find_gt(nums, target)
# Python 對應： bisect_right(nums, target) 或 bisect(nums, target)
# 例： nums = [1,2,2,2,3], target = 2 -> upper_bound = 4
#
# ------------------------------------------------------------------------------
# 2. 為什麼 Upper Bound 不是 find_lte (最後一個 <= target)
#
# Upper Bound 回傳的是「第一個 > target」，而不是「最後一個 <= target」。
# 但兩者可以互相換算：
#   last <= target = upper_bound(target) - 1
#
# 例： upper_bound = 4, last <= 2 -> 4 - 1 = 3
#
# ------------------------------------------------------------------------------
# 3. 四種查找的關係總結
#
# | 名稱 (對應函數)                | 正確對應條件          | 是否為 STL 標準定義
# | ---------------------------- | ------------------ | -----------------------
# | Lower Bound    (`find_gte`)  | 第一個 >= target   | ✔ Lower Bound
# | Upper Bound    (`find_gt`)   | 第一個 > target    | ✔ Upper Bound
# | last <= target (`find_lte`)  | upper_bound - 1    | ✘ (由 upper_bound - 1 衍生)
# | last < target  (`find_lt`)   | lower_bound - 1    | ✘ (由 lower_bound - 1 衍生)
#
# ==============================================================================


def find_gte(nums: List[int], target: int) -> int:
    """尋找第一個 >= target 的元素索引 (通常稱為 Lower Bound)"""
    size = len(nums)
    lo = 0
    hi = size - 1

    # 當陣列中所有元素都 < target 時，代表 target 應該插入在陣列「最尾端」。
    # 因此預設回傳 size (即 len(nums))，這與 C++ std::lower_bound 及
    # Python bisect_left 的行為完全一致，能避免在找 <= 等衍生邊界時發生越界錯誤。
    ans = size

    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] >= target:
            ans = mid
            hi = mid - 1  # [lo, mid-1] 如果是相等的情況, 會往 low 靠近
        else:
            lo = mid + 1  # [mid+1, hi]

    # 判斷 target 是否相等是 Caller (呼叫者) 自己要關心的事，Callee (底層工具) 不該處理
    # return ans if nums[ans] == target else -1

    return ans


def find_gt(nums: List[int], target: int) -> int:
    """尋找第一個 > target 的元素索引 (通常稱為 Upper Bound)"""
    size = len(nums)
    lo = 0
    hi = size - 1

    # 與 find_gte 理由相同，當所有元素都 <= target 時，第一個 > target 的位置在最尾端。
    # 這與 std::upper_bound 及 bisect_right 行為一致。
    ans = size

    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] > target:
            ans = mid
            hi = mid - 1  # [lo, mid-1]
        else:
            lo = mid + 1  # [mid+1, hi]

    return ans


def find_lte(nums: List[int], target: int) -> int:
    """尋找最後一個 <= target 的元素索引"""
    size = len(nums)
    lo = 0
    hi = size - 1

    # 當陣列中所有元素都 > target 時，代表不存在 <= target 的元素。
    # 邏輯上，這個「不存在的位置」應落在陣列的「最左邊界外」(index 0 之前)。
    # 預設回傳 -1，這也與「last <= target」等於「upper_bound - 1」在找不到時
    # (upper_bound 傳回 0) 算出 0 - 1 = -1 的結果完美吻合，不需要做任何修改。
    ans = -1

    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] <= target:
            ans = mid
            lo = mid + 1  # [mid+1, hi] 如果是相等的情況, 會往 high 靠近
        else:
            hi = mid - 1  # [lo, mid-1]

    # 判斷 target 是否相等是 Caller (呼叫者) 自己要關心的事，Callee (底層工具) 不該處理
    # return ans if nums[ans] == target else -1
    return ans


def find_lt(nums: List[int], target: int) -> int:
    """尋找最後一個 < target 的元素索引"""
    size = len(nums)
    lo = 0
    hi = size - 1

    # 與 find_lte 理由完全相同。
    # 當所有元素都 >= target 時，符合 < target 的元素落在陣列最前頭之外。
    # 預設回傳 -1，與 lower_bound(target) - 1 找不出時的極端結果一致。
    ans = -1

    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] < target:
            ans = mid
            lo = mid + 1  # [mid+1, hi]
        else:
            hi = mid - 1  # [lo, mid-1]

    return ans


def find_equal(nums: List[int], target: int) -> int:
    """尋找任一個 == target 的元素索引 (最基礎的二分搜尋)"""
    size = len(nums)
    lo = 0
    hi = size - 1
    ans = -1

    while lo <= hi:
        mid = lo + (hi - lo) // 2
        cmp = nums[mid] - target
        match cmp:
            case 0:
                ans = mid
                break
            case x if x > 0:
                hi = mid - 1  # [lo, mid-1]
            case x if x < 0:
                lo = mid + 1  # [mid+1, hi]

    return ans


class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        # ans = self._v1(nums, target)
        ans = self._v2(nums, target)
        # print(f"nums={nums}, target={target}, ans={ans}")
        return ans

    def _v1(self, nums: List[int], target: int) -> List[int]:
        def revise_index(idx: int) -> int:
            return idx if nums[idx] == target else -1

        if len(nums) == 0:
            return [-1, -1]

        lo = find_gte(nums, target)
        hi = find_lte(nums, target)

        return [revise_index(lo), revise_index(hi)]

    def _v2(self, nums: List[int], target: int) -> List[int]:
        """
        [技巧] 整數域同構轉換： target 的 upper_bound 等價於 target + 1 的 lower_bound
        [優勢] 只需要設計並維護「單一種」核心的二分搜底層函數 (find_gte)，即可推導出所有查表的邊界。
        不僅能大幅減少重複默寫各種類型二分搜的錯誤率，後續遇到變形題更能以不變應萬變。
        """

        def revise_index(idx: int) -> int:
            return idx if nums[idx] == target else -1

        if len(nums) == 0:
            return [-1, -1]

        # lo 就是標準的 lower_bound: 第一個 >= target 的位置
        lo = find_gte(nums, target)

        # hi 運用對稱性巧思：找最後一個 <= target 的位置
        # 等價於找 upper_bound(target) 再往左退 1 格
        # 在整數情況下，等價於 find_gte(nums, target + 1) - 1
        hi = find_gte(nums, target + 1) - 1

        return [revise_index(lo), revise_index(hi)]


def main():
    solution = Solution()

    # Case 1
    assert solution.searchRange([5, 7, 7, 8, 8, 10], 8) == [3, 4]

    # Case 2
    assert solution.searchRange([5, 7, 7, 8, 8, 10], 6) == [-1, -1]

    # Case 3
    assert solution.searchRange([], 0) == [-1, -1]

    assert solution.searchRange([5, 7, 7, 8, 8, 10], 10) == [5, 5]

    print("All tests passed!")


if __name__ == "__main__":
    main()
