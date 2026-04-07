"""
# [874. Walking Robot Simulation](https://leetcode.com/problems/walking-robot-simulation/)
**Difficulty:** 🟡 Medium
**Tags:** Array, Hash Table, Simulation

## Problem Description

A robot on an infinite XY-plane starts at point `(0, 0)` facing north. The robot receives an array of integers `commands`, which represents a sequence of moves that it needs to execute. There are only three possible types of instructions the robot can receive:

        - `-2`: Turn left `90` degrees.

        - `-1`: Turn right `90` degrees.

        - `1 <= k <= 9`: Move forward `k` units, one unit at a time.

Some of the grid squares are `obstacles`. The `i^th` obstacle is at grid point `obstacles[i] = (xi, yi)`. If the robot runs into an obstacle, it will stay in its current location (on the block adjacent to the obstacle) and move onto the next command.

Return the **maximum squared Euclidean distance** that the robot reaches at any point in its path (i.e. if the distance is `5`, return `25`).

**Note:**

        - There can be an obstacle at `(0, 0)`. If this happens, the robot will ignore the obstacle until it has moved off the origin. However, it will be unable to return to `(0, 0)` due to the obstacle.

        - North means +Y direction.

        - East means +X direction.

        - South means -Y direction.

        - West means -X direction.



Example 1:**

**Input:** commands = [4,-1,3], obstacles = []

**Output:** 25

**Explanation: **

The robot starts at `(0, 0)`:

        - Move north 4 units to `(0, 4)`.

        - Turn right.

        - Move east 3 units to `(3, 4)`.

The furthest point the robot ever gets from the origin is `(3, 4)`, which squared is `3^2 + 4^2 = 25` units away.

Example 2:**

**Input:** commands = [4,-1,4,-2,4], obstacles = [[2,4]]

**Output:** 65

**Explanation:**

The robot starts at `(0, 0)`:

        - Move north 4 units to `(0, 4)`.

        - Turn right.

        - Move east 1 unit and get blocked by the obstacle at `(2, 4)`, robot is at `(1, 4)`.

        - Turn left.

        - Move north 4 units to `(1, 8)`.

The furthest point the robot ever gets from the origin is `(1, 8)`, which squared is `1^2 + 8^2 = 65` units away.

Example 3:**

**Input:** commands = [6,-1,-1,6], obstacles = [[0,0]]

**Output:** 36

**Explanation:**

The robot starts at `(0, 0)`:

        - Move north 6 units to `(0, 6)`.

        - Turn right.

        - Turn right.

        - Move south 5 units and get blocked by the obstacle at `(0,0)`, robot is at `(0, 1)`.

The furthest point the robot ever gets from the origin is `(0, 6)`, which squared is `6^2 = 36` units away.



**Constraints:**

        - `1 <= commands.length <= 10^4`

        - `commands[i]` is either `-2`, `-1`, or an integer in the range `[1, 9]`.

        - `0 <= obstacles.length <= 10^4`

        - `-3 * 10^4 <= xi, yi <= 3 * 10^4`

        - The answer is guaranteed to be less than `2^31`.

## Similar Questions
- [Walking Robot Simulation II](https://leetcode.com/problems/walking-robot-simulation-ii/) (Medium)
"""

from typing import List

# ┌─────────────────────────────────────────────────────────────────────────────┐
# │ 解法比較                                                                     │
# │                                                                             │
# │  #  解法              Time                Space      說明                   │
# │  1  Brute Force       O(n × m × k)        O(m)       每步線性掃描所有障礙物   │
# │  2  Binary Search     O(n × k × log m)    O(m log m) 固定一維，二分搜另一維  │
# │  3  HashSet ✅        O(n × k) ≈ O(n)     O(m)       障礙物存 set，逐格查詢  │
# │                                                                             │
# │  n = commands.length, m = obstacles.length, k ≤ 9（常數）                   │
# │  HashSet 為面試首選：時間最優且實作最簡單                                       │
# └─────────────────────────────────────────────────────────────────────────────┘


class Solution:
    def robotSim(self, commands: List[int], obstacles: List[List[int]]) -> int:
        # 四個方向依順時針順序排列：北、東、南、西
        # index:  0       1        2        3
        # dir:  North   East    South    West
        #       (0,1)  (1,0)   (0,-1)  (-1,0)
        DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        # 用 set 儲存障礙物座標，查詢 O(1)
        # 轉成 tuple 才能被 hash
        obstacle_set = set(map(tuple, obstacles))

        dir_idx = 0      # 初始朝北（index 0）
        x, y = 0, 0      # 起始座標
        max_dist_sq = 0  # 紀錄最大平方距離

        for cmd in commands:
            if cmd == -1:
                # 右轉：index + 1，mod 4 自動循環
                dir_idx = (dir_idx + 1) % 4
            elif cmd == -2:
                # 左轉：index - 1，mod 4 自動循環（Python負數mod正常運作）
                dir_idx = (dir_idx - 1) % 4
            else:
                # 移動 cmd 步，每次走一格，遇障礙就停
                dx, dy = DIRS[dir_idx]
                for _ in range(cmd):
                    next_x, next_y = x + dx, y + dy
                    if (next_x, next_y) in obstacle_set:
                        break  # 撞牆，停在原地，跳出此 command
                    x, y = next_x, next_y
                    # 每走一步都更新最大距離
                    max_dist_sq = max(max_dist_sq, x * x + y * y)

        return max_dist_sq


def main():
    solution = Solution()

    # Case 1
    assert solution.robotSim([4, -1, 3], []) == 25

    # Case 2
    assert solution.robotSim([4, -1, 4, -2, 4], [[2, 4]]) == 65

    # Case 3
    assert solution.robotSim([6, -1, -1, 6], [[0, 0]]) == 36

    print("All tests passed!")


if __name__ == "__main__":
    main()
