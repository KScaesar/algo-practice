"""
# [207. Course Schedule](https://leetcode.com/problems/course-schedule/)
**Difficulty:** 🟡 Medium
**Tags:** Depth-First Search, Breadth-First Search, Graph Theory, Topological Sort

## Problem Description

There are a total of `numCourses` courses you have to take, labeled from `0` to `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [ai, bi]` indicates that you **must** take course `bi` first if you want to take course `ai`.

        - For example, the pair `[0, 1]`, indicates that to take course `0` you have to first take course `1`.

Return `true` if you can finish all courses. Otherwise, return `false`.



Example 1:**

```

**Input:** numCourses = 2, prerequisites = [[1,0]]
**Output:** true
**Explanation:** There are a total of 2 courses to take.
To take course 1 you should have finished course 0. So it is possible.

```

Example 2:**

```

**Input:** numCourses = 2, prerequisites = [[1,0],[0,1]]
**Output:** false
**Explanation:** There are a total of 2 courses to take.
To take course 1 you should have finished course 0, and to take course 0 you should also have finished course 1. So it is impossible.

```



**Constraints:**

        - `1 <= numCourses <= 2000`

        - `0 <= prerequisites.length <= 5000`

        - `prerequisites[i].length == 2`

        - `0 <= ai, bi < numCourses`

        - All the pairs prerequisites[i] are **unique**.

## Hints
1. This problem is equivalent to finding if a cycle exists in a directed graph. If a cycle exists, no topological ordering exists and therefore it will be impossible to take all courses.
2. Topological Sort via DFS - A great tutorial explaining the basic concepts of Topological Sort.
3. Topological sort could also be done via BFS.

## Similar Questions
- [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) (Medium)
- [Graph Valid Tree](https://leetcode.com/problems/graph-valid-tree/) (Medium)
- [Minimum Height Trees](https://leetcode.com/problems/minimum-height-trees/) (Medium)
- [Course Schedule III](https://leetcode.com/problems/course-schedule-iii/) (Hard)
- [Build a Matrix With Conditions](https://leetcode.com/problems/build-a-matrix-with-conditions/) (Hard)
"""

from collections import deque
from typing import List


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # return self._canFinish_dfs(numCourses, prerequisites)
        return self._canFinish_bfs(numCourses, prerequisites)

    # ── DFS 三色標記 ──
    # Time: O(V + E)  建 graph O(E) + 每個節點與邊各訪問一次
    # Space: O(V + E) graph 大小 O(E) + state 陣列 O(V) + call stack O(V)
    def _canFinish_dfs(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # 邊方向：往「依賴來源」走，追蹤是否形成環，與 BFS 方向相反
        # DFS: graph[course] = [前置課]   → 追蹤依賴來源，偵測回邊
        # BFS: graph[pre]    = [下游課]   → 沿拓撲順序往外擴散，減少 indegree
        #
        # [延伸 LC 210] 回傳合法修課順序 → reverse postorder DFS
        #   邊方向（拓撲）：pre → course（pre 必須在 course 之前）
        #   DFS 走法：    course → pre （沿依賴往回追）
        #   後序（postorder）加入 stack：先遞迴走完 pre，再把 course push 進 stack
        #     → stack 裡 pre 在下面，course 在上面
        #     → reverse(stack) 後 pre 在前，course 在後
        #   若偵測到環 → 回傳 []
        graph = [[] for _ in range(numCourses)]
        for course, pre in prerequisites:
            graph[course].append(pre)

        # 狀態: unseen, path, seen
        state = ["unseen"] * numCourses

        def dfs(course: int) -> bool:
            if state[course] == "path":
                return False
            if state[course] == "seen":
                return True

            state[course] = "path"

            for pre in graph[course]:
                # 錯誤實作：
                # state 的變化應該是每個節點只做一次的事
                # 放在迴圈反而像在描述每條邊的操作
                # 應該把 state 的變化放在 for 迴圈外面

                # state[course] = "path"
                if not dfs(pre):
                    return False
                # state[course] = "seen"

            state[course] = "seen"

            # ── postorder ──────────────────────────────────────
            # 所有前置課（pre）的 DFS 都完成後，才標記 seen
            # 這就是 postorder：「先處理完所有依賴，才記錄自己」
            #
            # 為什麼不能用 preorder？
            #   preorder = 進入節點就記錄，此時依賴可能還沒走完
            #   → 無法保證「記錄自己時，所有依賴已全部完成」
            #
            # [延伸 LC 210] 若需回傳修課順序，在此改為：
            #   result.append(course)   ← 所有依賴確認無環後才加入
            #   最後 reverse(result) 即為合法修課順序
            # ───────────────────────────────────────────────────

            return True

        # 要考慮 graph 可能沒有 connected, 所以每個 vertex 都要嘗試走一次
        for course in range(numCourses):
            if not dfs(course):
                return False

        return True

    # ── BFS Kahn's Algorithm（拓撲排序）──
    # Time: O(V + E)  建 graph O(E) + 每個節點出隊一次 O(V) + 每條邊減 indegree 一次 O(E)
    # Space: O(V + E) graph 大小 O(E) + indegree 陣列 O(V) + queue 最大 O(V)
    def _canFinish_bfs(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # 邊方向：往「被解鎖的下游」走，與 DFS 方向相反
        # DFS: graph[course] = [前置課]   → 追蹤依賴來源，偵測回邊
        # BFS: graph[pre]    = [下游課]   → 沿拓撲順序往外擴散，減少 indegree
        #
        # [延伸 LC 210] 回傳合法修課順序 → queue pop 順序即為結果
        #   indegree == 0 的課（沒有前置課）先修
        #   pop course → 加入結果 → 對下游課減少 indegree
        #   queue 的 pop 順序直接就是合法修課順序，不需要 reverse
        #   若最終結果長度 < numCourses → 有環，回傳 []
        graph = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses

        for course, pre in prerequisites:
            graph[pre].append(course)
            indegree[course] += 1

        # indegree == 0 代表沒有前置課程，可以直接修
        queue = deque([course for course, cnt in enumerate(indegree) if cnt == 0])

        while queue:
            course = queue.popleft()
            for next_course in graph[course]:
                indegree[next_course] -= 1
                if indegree[next_course] == 0:
                    queue.append(next_course)

        # 若有環，環內的課 indegree 永遠不會降到 0
        return all(cnt == 0 for cnt in indegree)


def main():
    solution = Solution()

    # Case 1
    assert solution.canFinish(2, [[1, 0]]) == True

    # Case 2
    assert solution.canFinish(2, [[1, 0], [0, 1]]) == False

    print("All tests passed!")


if __name__ == "__main__":
    main()
