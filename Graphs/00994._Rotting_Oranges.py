"""
# [994. Rotting Oranges](https://leetcode.com/problems/rotting-oranges/)
**Difficulty:** 🟡 Medium
**Tags:** Array, Breadth-First Search, Matrix

## Problem Description

You are given an `m x n` `grid` where each cell can have one of three values:

        - `0` representing an empty cell,

        - `1` representing a fresh orange, or

        - `2` representing a rotten orange.

Every minute, any fresh orange that is **4-directionally adjacent** to a rotten orange becomes rotten.

Return _the minimum number of minutes that must elapse until no cell has a fresh orange_. If _this is impossible, return_ `-1`.

Example 1:

**Input:** grid = [[2,1,1],[1,1,0],[0,1,1]]
**Output:** 4

Example 2:

**Input:** grid = [[2,1,1],[0,1,1],[1,0,1]]
**Output:** -1
**Explanation:** The orange in the bottom left corner (row 2, column 0) is never rotten, because rotting only happens 4-directionally.

Example 3:

**Input:** grid = [[0,2]]
**Output:** 0
**Explanation:** Since there are already no fresh oranges at minute 0, the answer is just 0.

**Constraints:**

        - `m == grid.length`
        - `n == grid[i].length`
        - `1 <= m, n <= 10`
        - `grid[i][j]` is `0`, `1`, or `2`.

## Similar Questions
- [Walls and Gates](https://leetcode.com/problems/walls-and-gates/) (Medium)
- [Battleships in a Board](https://leetcode.com/problems/battleships-in-a-board/) (Medium)
- [Detonate the Maximum Bombs](https://leetcode.com/problems/detonate-the-maximum-bombs/) (Medium)
- [Escape the Spreading Fire](https://leetcode.com/problems/escape-the-spreading-fire/) (Hard)
"""

from collections import deque
from typing import List


class Solution:
    # Time:  O(m * n) — 每個格子最多進出 queue 一次
    # Space: O(m * n) — queue 最壞情況存下所有格子
    def orangesRotting(self, grid: List[List[int]]) -> int:
        if grid is None or len(grid) == 0:
            return 0

        queue = deque([])
        total = 0
        rotten = 0
        rows, cols = len(grid), len(grid[0])

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != 0:
                    total += 1
                if grid[r][c] == 2:
                    rotten += 1
                    queue.append((r, c))

        if total == rotten:
            return 0

        minute = 0
        while len(queue) > 0:
            size = len(queue)
            for _ in range(size):
                r, c = queue.popleft()
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    row, col = r + dr, c + dc
                    if 0 <= row < rows and 0 <= col < cols and grid[row][col] == 1:
                        grid[row][col] = 2
                        queue.append((row, col))
                        rotten += 1
            minute += 1  # 划重点：更新步数在 level traversal 之後
            if total == rotten:
                return minute

        # 走到這裡表示 queue 已清空，但迴圈內 `if total == rotten: return minute` 從未成立。
        # → total != rotten 是此處的不變量（invariant），`minute if total == rotten` 永遠不會被執行。
        # → 可以直接寫 `return -1`。
        # return minute if total == rotten else -1
        return -1


def main():
    solution = Solution()

    # Case 1
    assert solution.orangesRotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4

    # Case 2
    assert solution.orangesRotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1

    # Case 3
    assert solution.orangesRotting([[0, 2]]) == 0

    print("All tests passed!")


if __name__ == "__main__":
    main()
