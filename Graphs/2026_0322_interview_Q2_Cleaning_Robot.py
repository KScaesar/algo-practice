"""
Codility - Cleaning Robot (Grid Simulation)

Problem:
    A cleaning robot starts at (0, 0) facing right on an N×M grid.
    It moves in a straight line as long as the next cell ahead is empty ('.').
    When it cannot move forward (blocked by 'X' or grid boundary), it rotates
    90° clockwise and tries again. The robot moves indefinitely.
    Return the number of distinct clean squares (cells visited at least once).

    Grid representation:
        '.' = empty square
        'X' = obstacle (cannot move through)

Examples:
    R = [".X", ".."]                  -> 2
    R = ["..", "X."]                  -> 3
    R = ["...", ".X.", "..."]         -> 8
    R = [".....", ".XXX.", "....."]   -> 12
    R = ["."]                          -> 1

Constraints:
    - N and M are integers in [1..20]
    - Top-left cell (0, 0) is always empty
    - Each string in R consists only of '.' and 'X'
    - Performance is not the focus; correctness is

Source: Codility
Category: Graphs (Grid Simulation)
"""




def solution(R):
    N = len(R)
    M = len(R[0])

    # 方向順序：右 → 下 → 左 → 上（順時針）
    # ⚠️ 常見誤解：「往右不是 (1, 0) 嗎？」
    #   → 混淆了 x/y 座標（x=水平）和 grid 索引（第一維=row=垂直）
    #   → grid 用 R[row][col]，「往右」是 col+1，對應 dc=+1，dr=0
    #   → (1, 0) 代表 dr=1，是「往下」，不是往右
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    row, col = 0, 0
    dir_idx = 0  # 指向 directions 的索引，初始面朝右

    visited_cells = set()   # 記錄「踩過哪些格子」→ 最終答案
    visited_states = set()  # 記錄「(位置, 方向)」組合 → 用來偵測停止條件

    # ─── 停止條件設計思路 ────────────────────────────────────────────────
    # 題目說機器人「永遠移動」，所以不存在自然終止點。
    # 但機器人的下一步完全由「目前位置 + 目前面朝的方向」決定：
    #   若 state = (row, col, dir_idx) 曾經出現過，
    #   代表之後的軌跡會完全重複上一次 → 不會踩到任何新格子 → 可停止。
    #
    # 比喻：想像錄影帶，一旦播到之前出現過的畫面（同場景同鏡頭方向），
    #        後面的內容必然和上次完全一樣，可以直接 eject。
    #
    # 另一個終止情況：四個方向全部被封住（`moved == False`），
    # 機器人完全動不了，也可以直接停止。
    # ────────────────────────────────────────────────────────────────────

    while True:
        visited_cells.add((row, col))  # 先記錄「踩到這格」

        # 用 (位置, 方向) 作為狀態快照
        state = (row, col, dir_idx)
        if state in visited_states:
            # 發現循環：這個狀態之後的行為完全可預測，停止
            break
        visited_states.add(state)

        # 嘗試往當前方向前進，若被擋住就順時針轉向，最多試 4 次
        #
        # 為什麼不用 `for dr, dc in directions`？
        #   → `for dr, dc in directions` 每次都從 index 0（右）開始，
        #     機器人會「忘記」目前面朝哪個方向，導致路徑錯誤。
        #   → 必須從 dir_idx 出發，繞 4 個方向一圈，所以用
        #     range(4) + `dir_idx = (dir_idx + 1) % 4`：
        #     當 dir_idx 從 3（上）再 +1，% 4 讓它回到 0（右），
        #     實現「環狀」的方向切換。
        moved = False
        for _ in range(4):
            dr, dc = directions[dir_idx]
            nr, nc = row + dr, col + dc
            if 0 <= nr < N and 0 <= nc < M and R[nr][nc] == '.':
                # 成功前進：更新位置，保留 dir_idx 供下一輪使用
                row, col = nr, nc
                moved = True
                break
            # 前進失敗：順時針轉 90°，下一次 loop 試新方向
            dir_idx = (dir_idx + 1) % 4

        if not moved:
            # 四個方向都被封住，機器人困住，停止
            break

    return len(visited_cells)  # set 的大小 = 不重複的清潔格數


def main():
    # Case 1: 2x2, X blocks right at (0,1)
    assert solution([".X", ".."]) == 2

    # Case 2: 2x2, X blocks down-left
    assert solution(["..", "X."]) == 3

    # Case 3: 3x3 with center X
    assert solution(["...", ".X.", "..."]) == 8

    # Case 4: 3x5, X wall in middle row
    assert solution([".....", ".XXX.", "....."]) == 12

    # Case 5: single cell
    assert solution(["."])==1

    print("All tests passed!")


if __name__ == "__main__":
    main()
