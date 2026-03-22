"""
Vertices Stop Disappearing (Codility)
======================================
You are given an undirected graph consisting of N vertices, numbered from 0 to
N-1, connected with M edges.  The graph is described by two arrays A and B,
both of length M.  A pair (A[K], B[K]), for K from 0 to M-1, describes an edge
between vertex A[K] and vertex B[K].

Each second, every vertex with at most one edge connected to it disappears
(every edge connected to one of the disappearing vertices also disappears).

Return the number of seconds after which the vertices stop disappearing,
or 0 if no vertices will ever disappear.

Constraints:
- N is an integer within the range [2, 100000]
- M is an integer within the range [1, 100000]
- All elements of A and B are integers within the range [0, N-1]
- There are no self-loops (edges with A[K] == B[K]) in the graph
- There are no multiple edges between the same vertices

Function signature:
    def solution(N, A, B) -> int

Examples:
    N=7, A=[0,1,2,3,4], B=[1,2,4,5,6]  => 2
    N=4, A=[0,1,2], B=[1,2,3]          => 2
    N=4, A=[0,1,0], B=[1,2,3]          => 0
    N=4, A=[0,1,2], B=[1,2,0]          => 1
"""


def solution(N, A, B):
    # ─── 暴力解思路 ────────────────────────────────────────────
    # 核心觀察：degree(v) <= 1 的頂點本秒消失（0 條邊 = 孤立、1 條邊 = 葉節點）
    #
    # 演算法（逐秒模擬）：
    #   1. 建鄰接表 vertex[v]，每個 v 存它所有鄰居的 set
    #   2. 每一輪：
    #      a. 掃所有存活頂點，找出 degree <= 1 的 → to_remove（同時判定）
    #      b. 若 to_remove 為空 → 停止，回傳目前 seconds
    #      c. 移除 to_remove 中的頂點：
    #         - 通知每個鄰居把自己（v）從其鄰接表中刪掉
    #         - 清空 v 自己的鄰接表
    #         - 從 alive 集合移除 v
    #      d. seconds += 1
    #
    # 複雜度：
    #   Time  O(N²) - 最差情況：鏈狀圖（Path Graph）0-1-2-...-N-1
    #     每輪只移除兩端葉節點，但仍需掃描所有存活頂點：
    #       第1輪: 掃 N 個   → 移除 0, N-1
    #       第2輪: 掃 N-2 個 → 移除 1, N-2
    #       第3輪: 掃 N-4 個 → 移除 2, N-3  ...
    #     總工作量 ≈ N + (N-2) + (N-4) + ... ≈ N²/4 = O(N²)
    #   Space O(N + M) - 鄰接表 + alive 集合
    # ───────────────────────────────────────────────────────────

    # vertex[v] = 與 v 直接相連的鄰居集合（鄰接表）
    vertex = [set() for _ in range(N)]
    for a, b in zip(A, B):
        vertex[a].add(b)
        vertex[b].add(a)

    alive = set(range(N))
    seconds = 0

    while True:
        # 找出本輪度數 <= 1 的頂點（同時消失）
        to_remove = {v for v in alive if len(vertex[v]) <= 1}
        if not to_remove:
            break

        # 移除這些頂點，並通知其鄰居更新鄰接表
        for v in to_remove:
            for neighbor in vertex[v]:
                # 告訴每個鄰居：「把我（v）從你的鄰居表裡刪掉」
                vertex[neighbor].discard(v)
            vertex[v].clear()  # 我（v）自己的鄰居表清空（v 已死，不再維護）
            alive.discard(v)  # 從存活集合中移除 v

        seconds += 1

    return seconds


def solution_v2(N, A, B):
    # ─── 優化解思路（BFS 分層）────────────────────────────────
    # 瓶頸：暴力解每輪掃全部存活頂點 O(N)，但大多數頂點 degree 沒變
    #
    # 關鍵觀察：當頂點 v 被移除時，只有 v 的「鄰居」degree 才會下降
    #   → 只需追蹤「degree 剛降到 <= 1」的頂點，不用掃全部
    #
    # 演算法（BFS 分層 = 模擬每一秒）：
    #   1. 建 degree[] 陣列，初始化 queue（degree <= 1 的頂點）
    #   2. 逐層（每層 = 1 秒）處理 queue：
    #      a. 取出本層所有頂點（current_wave）
    #      b. 對每個 v：通知鄰居 degree 減 1
    #         若鄰居 degree 降到 <= 1 且尚未移除 → 加入 next_wave
    #      c. next_wave 非空 → seconds += 1，繼續下一層
    #
    # 複雜度：
    #   Time  O(N + M) - 每個頂點、每條邊各處理一次
    #   Space O(N + M) - degree 陣列 + 鄰接表
    # ───────────────────────────────────────────────────────────

    from collections import deque

    # 建 degree 陣列 + 鄰接表（用 list 即可，不需 set）
    degree = [0] * N
    vertex = [[] for _ in range(N)]
    for a, b in zip(A, B):
        vertex[a].append(b)
        vertex[b].append(a)
        degree[a] += 1
        degree[b] += 1

    removed = [False] * N  # 避免重複加入 queue

    # 初始化：把所有 degree <= 1 的頂點放入第一波
    queue = deque()
    for v in range(N):
        if degree[v] <= 1:
            queue.append(v)
            removed[v] = True

    seconds = 0

    while queue:
        # 本輪（current_wave）全部同時消失
        current_wave = list(queue)
        queue.clear()

        for v in current_wave:
            for neighbor in vertex[v]:
                if removed[neighbor]:
                    continue
                degree[neighbor] -= 1
                # 鄰居 degree 降到 <= 1 → 下一秒消失，加入下一波
                if degree[neighbor] <= 1:
                    removed[neighbor] = True
                    queue.append(neighbor)

        seconds += 1
        # 若下一波空，代表沒有更多頂點消失，不再 +1

    return seconds

def main():
    # Case 1: 鏈 0-1-2-4, 3-5, 4-6
    # 第1秒: 移除 0,3,5,6 | 第2秒: 移除 1,4 | 第3秒: 移除 2 => 3
    assert solution(7, [0, 1, 2, 3, 4], [1, 2, 4, 5, 6]) == 3

    # Case 2: 鏈 0-1-2-3
    # 第1秒: 移除 0,3 | 第2秒: 移除 1,2 => 2
    assert solution(4, [0, 1, 2], [1, 2, 3]) == 2

    # Case 3: 0-1, 1-2, 0-3
    # 第1秒: 移除 2,3 | 第2秒: 移除 0,1 => 2
    assert solution(4, [0, 1, 0], [1, 2, 3]) == 2

    # Case 4: 三角形 0-1-2-0, N=4 → 頂點 3 孤立(deg 0) => 第1秒消失 => 1
    assert solution(4, [0, 1, 2], [1, 2, 0]) == 1

    # ── 優化版交叉驗證 ──────────────────────────────────────────
    assert solution_v2(7, [0, 1, 2, 3, 4], [1, 2, 4, 5, 6]) == 3
    assert solution_v2(4, [0, 1, 2], [1, 2, 3]) == 2
    assert solution_v2(4, [0, 1, 0], [1, 2, 3]) == 2
    assert solution_v2(4, [0, 1, 2], [1, 2, 0]) == 1

    print("All tests passed!")


if __name__ == "__main__":
    main()
