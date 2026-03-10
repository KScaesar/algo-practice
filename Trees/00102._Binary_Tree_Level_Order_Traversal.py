"""
# [102. Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/)
**Difficulty:** 🟡 Medium
**Tags:** Tree, Breadth-First Search, Binary Tree

## Problem Description

Given the `root` of a binary tree, return _the level order traversal of its nodes' values_. (i.e., from left to right, level by level).

 

Example 1:**

```

**Input:** root = [3,9,20,null,null,15,7]
**Output:** [[3],[9,20],[15,7]]

```

Example 2:**

```

**Input:** root = [1]
**Output:** [[1]]

```

Example 3:**

```

**Input:** root = []
**Output:** []

```

 

**Constraints:**

        - The number of nodes in the tree is in the range `[0, 2000]`.

        - `-1000 <= Node.val <= 1000`

## Hints
1. Use a queue to perform BFS.

## Similar Questions
- [Binary Tree Zigzag Level Order Traversal](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/) (Medium)
- [Binary Tree Level Order Traversal II](https://leetcode.com/problems/binary-tree-level-order-traversal-ii/) (Medium)
- [Minimum Depth of Binary Tree](https://leetcode.com/problems/minimum-depth-of-binary-tree/) (Easy)
- [Binary Tree Vertical Order Traversal](https://leetcode.com/problems/binary-tree-vertical-order-traversal/) (Medium)
- [Average of Levels in Binary Tree](https://leetcode.com/problems/average-of-levels-in-binary-tree/) (Easy)
- [N-ary Tree Level Order Traversal](https://leetcode.com/problems/n-ary-tree-level-order-traversal/) (Medium)
- [Cousins in Binary Tree](https://leetcode.com/problems/cousins-in-binary-tree/) (Easy)
- [Minimum Number of Operations to Sort a Binary Tree by Level](https://leetcode.com/problems/minimum-number-of-operations-to-sort-a-binary-tree-by-level/) (Medium)
- [Divide Nodes Into the Maximum Number of Groups](https://leetcode.com/problems/divide-nodes-into-the-maximum-number-of-groups/) (Hard)
"""

from typing import List, Optional

from tool import TreeNode, build_tree

from collections import deque

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        時間複雜度：O(N)，其中 N 是樹的節點總數。每個節點都會被精確地處理一次（入列與出列）。
        空間複雜度：O(N)，來自儲存結果的陣列與佇列 (queue) 的開銷。在最壞的情況下（完全二元樹），
                  佇列會同時保存最底層的所有節點，大約是 N/2 個節點。
        
        思考過程與 BFS 三層迴圈模板 (3-Level BFS Template)：
        1. 第一層 `while len(queue) > 0`：控制整體的 BFS 迴圈，直到所有節點都被訪問過為止。
        2. 第二層 `for _ in range(size)`：按層級 (level by level) 處理節點。藉由在每次迭代開始時
           固定當前的 size，我們可以確保這輪迴圈只處理屬於「當前這層」的節點。
        3. 第三層 `if node.left/right`：為下一層擴展子節點。（如果是 Graph 結構，這裡會是一個
           遍歷相鄰節點的 for 迴圈）。
        """
        result=[]
        if root is None:
            return result
        
        queue = deque([root])

        while len(queue) > 0:
            size=len(queue)
            level=[]
            for _ in range(size):
                node=queue.popleft()
                level.append(node.val)
                if node.left is not None:
                    queue.append(node.left)
                if node.right is not None:
                    queue.append(node.right)
            result.append(level)
        return result
            
            
def main():
    solution = Solution()

    # Case 1
    # Input: root = [3,9,20,null,null,15,7]
    root1 = build_tree([3, 9, 20, None, None, 15, 7])
    assert solution.levelOrder(root1) == [[3], [9, 20], [15, 7]]

    # Case 2
    # Input: root = [1]
    root2 = build_tree([1])
    assert solution.levelOrder(root2) == [[1]]

    # Case 3
    # Input: root = []
    root3 = build_tree([])
    assert solution.levelOrder(root3) == []

    print("All tests passed!")

if __name__ == "__main__":
    main()
