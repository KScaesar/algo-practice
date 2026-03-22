"""
Shortest Fragment (Codility Task 3)

Given an array A of N integers and two integers L and R, find the length of
the shortest fragment (contiguous subarray) of A that contains every integer
from L to R inclusive.

Return -1 if no such fragment exists.

Constraints:
  - N is an integer within the range [1..100,000]
  - 1 <= L <= R <= 1,000,000,000
  - each element of A is an integer within the range [1..1,000,000,000]

Examples:
  A = [2, 1, 4, 3, 2, 1, 1, 4], L = 2, R = 4 → 3
    The shortest fragment containing 2, 3, 4 starts at index 2: [4, 3, 2, 1, 1, 4]
    Wait — shortest is [4, 3, 2] at index 2..4 → length 3

  A = [10^9, 1, 1, 1, 1, 1, 10^9-1], L = 10^9-1, R = 10^9 → 7 (whole array)

  A = [1, 3, 5, 7], L = 3, R = 5 → -1 (4 is missing)
"""


def solution(A, L, R):
    # ─── 題目要求解析 (釐清題意) ────────────────────────────────────────────────
    # 題目：「最短的連續子陣列 (fragment)，包含從 L 到 R 的『每一個』整數」
    # 注意盲點：
    # 1. 不是只包含 L 和 R 這兩個點，而是 {L, L+1, ..., R} 共 R-L+1 個「不同的數字」都要出現。
    # 2. 例如 L=3, R=5，必須要有 3, 4, 5。只要缺了 4，就算包住 3 和 5 也是不合法的（回傳 -1）。
    # 3. 陣列裡可能有不在 [L, R] 範圍內的數字 (例如過大或過小的數字)，這些是「雜訊」，
    #    把它們包在區間裡沒關係，但它們對「達成條件」沒有幫助。
    #
    # ─── 設計思路 (Sliding Window 收縮型) ───────────────────────────────────────
    # 只要看到「找符合某條件」的「最短/最長連續區間」，第一直覺就是 Sliding Window。
    #
    # 1. 狀態追蹤：
    #    - `need`: 目標需要集齊幾種不同的數字 (R - L + 1)。
    #    - `have`: 目前 window 內已經集齊了幾種「我們需要的」數字。
    #    - `window_count`: dict，只記錄 [L, R] 範圍內的數字在 window 的出現次數。
    #      (L, R 最大值高達 10^9，不能開陣列對應 index，必須用 Hash Map，且過濾掉雜訊以省空間)
    #
    # 2. 擴張 (Expand) - right 往前走：
    #    - 吃進右邊新元素，如果是我們要的 (L <= val <= R)，計數 +1。
    #    - 當這個數字是「第一次」出現時 (count == 1)，代表我們湊齊了一種數字 (have += 1)。
    #
    # 3. 收縮 (Shrink) - left 往前走：
    #    - 當 `have == need` 時，代表目前區間合法，先記錄當前長度 `right - left + 1`更新最佳解。
    #    - 接著嘗試「吐出」最左邊的元素 (left += 1)，看看區間還能不能更短。
    #    - 如果吐出的是目標數字，且計數歸 0，代表破壞了合法狀態 (have -= 1)，就必須停止收縮，繼續向右擴張。
    #
    # ─── 複雜度分析 ─────────────────────────────────────────────────────────────
    # [時間複雜度] O(N) 
    #   - 雖然 for 裡面包著 while，但 right 最多往右走 N 步，left 也只加不減，最多走 N 步。
    #   - 每個元素最多被「吃進視窗」一次、「吐出視窗」一次。這叫作「攤還分析 (Amortized Analysis)」。
    # [空間複雜度] O(min(N, R - L + 1))
    #   - 我們只將 [L, R] 內的「有效數字」記錄進 `window_count` 字典，最大 key 類型有 R-L+1 種。
    #   - 而最差狀況把整個陣列塞滿字典，key 數量也不會超過 N。
    #   - 取決於誰更小，空間將被嚴格約束在 min(N, R-L+1) 以內。
    #   - 這巧妙防禦了 L 和 R 可能高達 10^9 所引發的問題，若改宣告陣列來存計數，則會爆擊記憶體上限 (MLE)。
    # ────────────────────────────────────────────────────────────────────────

    need = R - L + 1  # 需要涵蓋的不同整數個數
    window_count = {}  # 當前 window 內 [L,R] 各值的出現次數
    have = 0  # 目前已涵蓋的不同整數個數
    min_len = float("inf")
    left = 0

    for right in range(len(A)):
        r_val = A[right]

        # 只追蹤落在 [L, R] 範圍內的元素
        if L <= r_val <= R:
            window_count[r_val] = window_count.get(r_val, 0) + 1
            if window_count[r_val] == 1:  # 這個值第一次出現 → 新增一個覆蓋
                have += 1

        # 當滿足條件，嘗試從左側縮小 window
        while have == need:
            min_len = min(min_len, right - left + 1)

            l_val = A[left]
            if L <= l_val <= R:
                window_count[l_val] -= 1
                if window_count[l_val] == 0:  # 這個值消失了 → 失去一個覆蓋
                    have -= 1
            left += 1

    return min_len if min_len != float("inf") else -1


def main():
    # Case 1: A = [2,1,4,3,2,1,1,4], L=2, R=4 → 3
    assert solution([2, 1, 4, 3, 2, 1, 1, 4], 2, 4) == 3

    # Case 2: A = [10**9, 1,1,1,1,1, 10**9-1], L=10**9-1, R=10**9 → 7
    assert solution([10**9, 1, 1, 1, 1, 1, 10**9 - 1], 10**9 - 1, 10**9) == 7

    # Case 3: A = [1,3,5,7], L=3, R=5 → -1
    assert solution([1, 3, 5, 7], 3, 5) == -1

    print("All tests passed!")


if __name__ == "__main__":
    main()
