"""
# [452. Minimum Number of Arrows to Burst Balloons](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/)
**Difficulty:** 🟡 Medium
**Tags:** Array, Greedy, Sorting

## Problem Description

There are some spherical balloons taped onto a flat wall that represents the XY-plane. The balloons are represented as a 2D integer array `points` where `points[i] = [xstart, xend]` denotes a balloon whose **horizontal diameter** stretches between `xstart` and `xend`. You do not know the exact y-coordinates of the balloons.

Arrows can be shot up **directly vertically** (in the positive y-direction) from different points along the x-axis. A balloon with `xstart` and `xend` is **burst** by an arrow shot at `x` if `xstart <= x <= xend`. There is **no limit** to the number of arrows that can be shot. A shot arrow keeps traveling up infinitely, bursting any balloons in its path.

Given the array `points`, return _the **minimum** number of arrows that must be shot to burst all balloons_.

Example 1:

```
Input: points = [[10,16],[2,8],[1,6],[7,12]]
Output: 2
Explanation: The balloons can be burst by 2 arrows:
- Shoot an arrow at x = 6, bursting the balloons [2,8] and [1,6].
- Shoot an arrow at x = 11, bursting the balloons [10,16] and [7,12].
```

Example 2:

```
Input: points = [[1,2],[3,4],[5,6],[7,8]]
Output: 4
Explanation: One arrow needs to be shot for each balloon for a total of 4 arrows.
```

Example 3:

```
Input: points = [[1,2],[2,3],[3,4],[4,5]]
Output: 2
Explanation: The balloons can be burst by 2 arrows:
- Shoot an arrow at x = 2, bursting the balloons [1,2] and [2,3].
- Shoot an arrow at x = 4, bursting the balloons [3,4] and [4,5].
```

**Constraints:**
- `1 <= points.length <= 10^5`
- `points[i].length == 2`
- `-2^31 <= xstart < xend <= 2^31 - 1`

## Similar Questions
- [Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/) (Medium)
- [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) (Medium)
"""

from functools import cache
from typing import List

# ============================================================
# 💡 白板面試討論筆記：貪心演算法核心概念
# ============================================================
#
# ❌ 最初的誤解 (Bounding Box)
#    起初可能認為是找一個範圍涵蓋所有線段（找 max(start) 和 min(end)）。
#    但題目要的是「最少數量的點」，讓每個區間至少被一個點碰到。
#    如果線段很分散，就需要多個點，而不是一個大範圍。
#
# ─────────────────────────────────────────────────────────────
# 📚 理論背景：Earliest Deadline First (EDF) 演算法
# ─────────────────────────────────────────────────────────────
#
#   EDF 是作業系統排程（OS Scheduling）領域中的經典貪心演算法。
#   原始場景：有多個任務（Task），每個任務有一個「截止時間 (Deadline)」，
#   在單一 CPU 上， EDF 策略是「永遠優先執行截止時間最早的任務」。
#
#   EDF 的核心精神（對應到本題）：
#     OS Scheduling       │ 本題（氣球問題）
#     ─────────────────── │ ──────────────────────────────
#     Task                │ Balloon（氣球區間 [start, end]）
#     Deadline            │ end（氣球的右邊界）
#     「最早截止時間」優先     │ 按 end 由小到大排序
#     執行任務（佔用 CPU）   │ 射出一支箭
#
#   本題之所以能用 EDF 思維，是因為：
#   - 每顆氣球都有「死線」：它在 x = end 之後就再也打不到了。
#   - 我們必須在死線前處理它（射箭），否則就永遠錯過。
#   - 「優先處理最快到期的死線」是讓資源（箭）使用率最大化的貪心策略。
#
#   ⚠️ 注意：本題是 EDF 的「變體」，原始 EDF 解決的是
#   「所有任務能不能都在 Deadline 前完成」（Feasibility），
#   而本題是「最少用幾支箭能覆蓋所有區間」（Minimum Coverage）。
#   但按 end 排序的核心精神是共通的。
#
# ─────────────────────────────────────────────────────────────
# 概念一：為什麼按 `end` 排序，而不是按 `start`？
# ─────────────────────────────────────────────────────────────
#
# 用具體反例說明：
#   假設有三顆氣球：A=[1,10]（很長）、B=[2,3]（很短）、C=[4,5]（很短）
#
#   【按 start 排序的困境】
#   順序：A [1,10] → B [2,3] → C [4,5]
#   我們「貪心」地射第一支箭，為了最大化覆蓋，先把箭釘在 A 的 end = 10。
#   結果悲劇：這支箭在 x=10，完全「錯過」了 B [2,3] 和 C [4,5]！
#   為了避免這個錯誤，處理每顆新氣球時，都需要「回頭縮短」箭的極限：
#     - 遇到 A → 箭的極限：10
#     - 遇到 B → 必須縮短到 min(10, 3) = 3，才不會錯過 B
#     - 遇到 C → C 的 start=4 > 當前極限 3 → 無法覆蓋同一支箭，需要新的箭
#   邏輯很繞，需要維護一個隨時「縮小」的射擊視窗。
#
#   【按 end 排序的直覺】
#   順序變成：B [2,3] → C [4,5] → A [1,10]
#   現在邏輯超級簡單：
#     Step 1. B 是最早消失的，第一支箭毫無懸念釘在 x=3（B 的 end）。
#     Step 2. 看 C，它的 start=4 > 3（第一支箭的位置），碰不到 → 需要第二支箭，釘在 x=5。
#     Step 3. 看 A，它的 start=1 <= 5（第二支箭的位置），順便被射破！
#   整個過程：不需要「回頭修改」箭的位置，邏輯單向向前推進。
#
#   【總結對比】
#   按 start 排序 → 像在「預測未來」，箭的極限需要不斷往左縮小，邏輯複雜。
#   按 end 排序   → 像在「把握現在」，氣球已按最快消失者優先排隊，每支箭的決策
#                   只和「當前這顆必須被射破的目標」有關，單純向右掃描就夠了。
#
# ─────────────────────────────────────────────────────────────
# 概念二：既然要射箭，釘在哪裡最划算？（交換論證 Exchange Argument）
# ─────────────────────────────────────────────────────────────
#
#   氣球按 end 排序後，我們看著第一顆氣球 [1, 6]，必須在 x=1~6 之間射箭。
#   問題：射在 1、2、3、4、5 還是 6 最好？
#
#   論證：假設我們射在 x=4（而非 end=6）。
#   - 它確實射破了 [1,6]，看起來沒問題。
#   - 但如果我們把這支箭往右「平移（交換）」到 x=6：
#     → 它依然能射破 [1,6]（因為 6 在範圍 [1,6] 內），沒有損失。
#     → 但更有可能順便碰到後面的氣球，例如 [5,10]（射在 4 碰不到，射在 6 就破了）。
#   - 結論：釘在當前氣球的最右邊緣（end），「永遠不會」比釘在左邊差。
#     這就是貪心策略的「局部最佳解」。


class Solution:
    def findMinArrowShots(self, points: List[List[int]]) -> int:
        return self._greedy_for_loop(points)
        # return self._greedy_recursion(points)
        # return self._dp(points)

    def _greedy_for_loop(self, points: List[List[int]]) -> int:
        # Time:  O(n log n) — sorted() 排序主導，後面的單趟掃描只有 O(n)
        # Space: O(n)       — sorted() 會建立新的 list
        #                     若改用 points.sort()（in-place），可降至 O(1) 額外空間
        size = len(points)
        if size == 0:
            return 0

        # 使用 end 排序
        points = sorted(points, key=lambda line: line[1])

        # 先射出第一隻箭, 類似 linklist dummy node 的想法, 減少 邊界條件
        current_end = points[0][1]
        result = 1

        for i in range(1, size):
            start, end = points[i]
            if start > current_end:
                current_end = end
                result += 1

        return result

    def _greedy_recursion(self, points: List[List[int]]) -> int:
        # ⚠️  這個解法的本質是「遞迴版貪婪」，而非真正的 Top-Down DP。
        #
        # Time:  O(n log n) — sort O(n log n) 主導
        #                     遞迴部分：節點數 n × 每個節點均攤 O(1) = O(n)
        #                       為什麼是均攤 O(1)？
        #                       fn(i) 的 for loop 找到「第一個未覆蓋氣球」就立刻 return，不繼續掃。
        #                       各個 fn 掃描的範圍互不重疊（fn(0) 掃 [1,k)，fn(k) 掃 [k+1,m)...）
        #                       所有 fn 加起來只掃過整個陣列一次，總工作量 O(n) → 均攤每節點 O(1)。
        # Space: O(n)       — 遞迴呼叫棧深度最壞 O(n)（完全不重疊時每顆氣球都遞迴一層）
        #
        # Greedy（含此實作） vs 真正的 Top-Down DP：
        #
        # - 每個狀態的選擇數
        #     Greedy    : 只有 1 個（箭固定射在 end，無分支）
        #     Top-Down  : 多個（枚舉所有可能的分組左端點 j，取 min）
        #
        # - @cache 是否必要
        #     Greedy    : 否（fn(i) 每次只被呼叫一次，不重複）
        #     Top-Down  : 是（不同路徑可能到達相同的 fn(i)，需快取）
        #
        # - 子問題是否重疊
        #     Greedy    : 無（線性往前跳，不回頭）
        #     Top-Down  : 有（不同的前一次射箭位置可能轉移到同一個 i）
        #
        # - 決策來源
        #     Greedy    : 「局部最佳 = 全域最佳」的數學保證
        #     Top-Down  : 枚舉所有選擇，取最小值

        size = len(points)
        if size == 0:
            return 0

        # 使用 end 排序
        points.sort(key=lambda line: line[1])

        # 從第 i 顆氣球（已按 end 排序）開始，到最後，最少需要幾支箭
        # ↓ 只有一條遞迴路徑（無分支），本質是貪婪的遞迴包裝
        def fn(i):
            current_end = points[i][1]  # 貪婪選擇：箭固定射在 end
            for j in range(i + 1, size):
                start, end = points[j]
                if start > current_end:  # 找到第一顆未被覆蓋的氣球
                    return fn(j) + 1  # 唯一選擇，非枚舉
            return 1

        return fn(0)

    def _dp(self, points: List[List[int]]) -> int:
        # DP Time Complexity: O(n²)
        # 對於每個狀態 fn(i)
        # 我們會枚舉最後一支箭覆蓋的左端點 j
        #   j = i, i-1, i-2 ... 0
        #
        # 最多枚舉
        #   i+1 次  → 最壞 O(n)
        #
        # 總計
        #   n 個狀態 × O(n) 枚舉
        #
        # DP Space Complexity: O(n)
        #   1. cache 儲存 n 個狀態
        #   2. recursion stack 最深 O(n)

        size = len(points)
        if size == 0:
            return 0

        # 先按照 end 排序
        #
        # 這樣在任何區間 j..i 中：
        #   最小的 end 一定是 points[j][1]
        #
        # 這個性質可以讓我們快速判斷
        # 一支箭是否可以覆蓋 j..i
        points.sort(key=lambda line: line[1])

        # fn(i) 定義：
        #   覆蓋氣球 0..i 所需要的最少箭數
        #
        # 也就是：
        #   已排序陣列的前 i+1 顆氣球
        # @trace_recursion
        @cache
        def fn(i: int) -> int:
            # base case
            # 沒有氣球需要射
            if i < 0:
                return 0

            result = float("inf")

            # max_start 維護區間 j..i 的最大 start
            max_start = float("-inf")

            # ─────────────────────────────
            # 枚舉思考方式
            # ─────────────────────────────
            #
            # 我們不知道「最後一支箭」會射哪些氣球
            #
            # 所以枚舉所有情境：
            #   最後一支箭覆蓋的區間 j..i，每一種情況都嘗試一次
            #
            # 也就是：
            # j = i     → 箭只射第 i 顆
            # j = i-1   → 箭射第 i-1..i
            # j = i-2   → 箭射第 i-2..i
            # ...
            # j = 0     → 箭射第 0..i
            for j in range(i, -1, -1):
                # 更新 j..i 區間中的最大 start
                max_start = max(max_start, points[j][0])

                # 判斷 j..i 是否可以用同一支箭射爆
                #
                # 一支箭 x 要覆蓋所有氣球 j..i 必須滿足：
                #   max(start[j..i]) <= x <= min(end[j..i])
                #
                # 因為已按 end 排序：
                #   min(end[j..i]) = points[j][1]
                #
                # 所以條件簡化為：
                #   max_start <= points[j][1]
                if max_start <= points[j][1]:
                    # 如果 j..i 可以共用一支箭
                    #
                    # 那剩下的氣球就是：
                    #   0..j-1
                    #
                    # 這部分由 fn(j-1) 解決
                    #
                    # +1 是這支新箭
                    result = min(result, fn(j - 1) + 1)

                else:
                    # 若條件不成立，代表 j..i 已經沒有共同交集
                    #
                    # 而 j 再往左時：
                    #   max_start 只會變大
                    #   points[j][1] 只會變小
                    #
                    # 所以更左邊一定也不可能成立
                    # 可以直接停止枚舉
                    break

            return result

        # 最終答案：覆蓋 0..size-1
        return fn(size - 1)


def main():
    solution = Solution()

    # Case 1
    # Output: 2
    assert solution.findMinArrowShots([[10, 16], [2, 8], [1, 6], [7, 12]]) == 2

    # Case 2
    # Output: 4
    assert solution.findMinArrowShots([[1, 2], [3, 4], [5, 6], [7, 8]]) == 4

    # Case 3
    # Output: 2
    assert solution.findMinArrowShots([[1, 2], [2, 3], [3, 4], [4, 5]]) == 2

    print("All tests passed!")


if __name__ == "__main__":
    main()
