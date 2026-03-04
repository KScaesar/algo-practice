"""
# [124. Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/)
**Difficulty:** 🔴 Hard
**Tags:** Dynamic Programming, Tree, Depth-First Search, Binary Tree

## Problem Description

A **path** in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence **at most once**. Note that the path does not need to pass through the root.

The **path sum** of a path is the sum of the node's values in the path.

Given the `root` of a binary tree, return _the maximum **path sum** of any **non-empty** path_.

 

Example 1:**

```

**Input:** root = [1,2,3]
**Output:** 6
**Explanation:** The optimal path is 2 -> 1 -> 3 with a path sum of 2 + 1 + 3 = 6.

```

Example 2:**

```

**Input:** root = [-10,9,20,null,null,15,7]
**Output:** 42
**Explanation:** The optimal path is 15 -> 20 -> 7 with a path sum of 15 + 20 + 7 = 42.

```

 

**Constraints:**

        - The number of nodes in the tree is in the range `[1, 3 * 10^4]`.

        - `-1000 <= Node.val <= 1000`

## Similar Questions
- [Path Sum](https://leetcode.com/problems/path-sum/) (Easy)
- [Sum Root to Leaf Numbers](https://leetcode.com/problems/sum-root-to-leaf-numbers/) (Medium)
- [Path Sum IV](https://leetcode.com/problems/path-sum-iv/) (Medium)
- [Longest Univalue Path](https://leetcode.com/problems/longest-univalue-path/) (Medium)
- [Time Needed to Inform All Employees](https://leetcode.com/problems/time-needed-to-inform-all-employees/) (Medium)
- [Difference Between Maximum and Minimum Price Sum](https://leetcode.com/problems/difference-between-maximum-and-minimum-price-sum/) (Hard)
"""

from typing import List, Optional, Dict, Tuple
from tool import TreeNode, build_tree

# ─── 思考筆記 ──────────────────────────────────────────────
# 【問題理解】
#   Q: 兩個子樹的 path sum，什麼條件下可以連接成一條路徑？
#   A: 只有透過「共同的父節點」才能連接。
#      左子樹某條路徑的端點、父節點、右子樹某條路徑的端點，
#      這三者恰好形成一條合法路徑（無分叉）。
#      → 父節點即為這條路徑的「最高點/轉彎點」，左右各選一條
#        向下延伸的單向路徑接上去，就是合法的連接。
#      → 這也是為什麼「回傳給父節點只能選一側」：
#        若父節點的父節點還想繼續接，就不能再同時往左右延伸。
#
#   路徑不能分叉：任一節點在路徑中最多連接兩個鄰居。
#   路徑一定有一個「最高點」（離根最近的點），
#   遍歷所有節點，假設每個節點都是最高點，取最大值即為答案。
#
# 【DFS 設計】
#   讓遞迴函數扮演「雙重身分」。
#   想像你是一個節點，你面對你的父節點時，你要提供資訊
#   同時，你也要偷偷觀察，以你為中心的路徑會不會是全域最大的。
#   ① 更新全域答案（以當前節點為最高點）
#      → 左貢獻 + 右貢獻 + node.val → 更新 max_sum
#   ② 回傳給父節點的零件（作為路徑的一段，提供資訊）
#      → 只能單向：node.val + max(左貢獻, 右貢獻)
#   ⚠️  ① 可以兩側都接；② 只能選一側，混淆即路徑分叉
#
# 【邊界處理】
#   貢獻值為負時取 max(0, gain)，等同於在此切斷路徑重啟。
#   max_sum 初始為 float('-inf')，確保全負數樹也能正確回答。
#
# 【複雜度】
#   時間 O(N)：每個節點拜訪一次
#   空間 O(H)：遞迴深度 = 樹高（worst case skewed tree = O(N)）
# ────────────────────────────────────────────────────────────

class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        # 初始化為最小值，確保即使所有節點都是負的也能正確更新
        self.max_sum = float('-inf')

        # oneSideMaxSum(node) 的定義：
        #   回傳「以 node 為起點，向下延伸的單向最大路徑和」
        #   即：若父節點想接上 node，node 最多能提供多少貢獻值。
        #   副作用：同時更新全域 max_sum（以 node 為轉彎點的路徑）
        def oneSideMaxSum(node):
            if not node:
                return 0

            # 遞迴：只取大於 0 的貢獻
            left_gain = max(oneSideMaxSum(node.left), 0)
            right_gain = max(oneSideMaxSum(node.right), 0)

            # 更新全域最大值 (當前節點作為路徑的最高點/轉彎點)
            current_path_sum = node.val + left_gain + right_gain
            self.max_sum = max(self.max_sum, current_path_sum)

            # 回傳給父節點：當前節點值 + 左右較大的一邊
            return node.val + max(left_gain, right_gain)

        oneSideMaxSum(root)
        return self.max_sum


def main():
    solution = Solution()

    # Case 1: root = [1,2,3], expected = 6
    assert solution.maxPathSum(build_tree([1, 2, 3])) == 6

    # Case 2: root = [-10,9,20,null,null,15,7], expected = 42
    assert solution.maxPathSum(build_tree([-10, 9, 20, None, None, 15, 7])) == 42

    print("All tests passed!")


if __name__ == "__main__":
    main()
