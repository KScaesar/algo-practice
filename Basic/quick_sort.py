# -------------------------------
# Lomuto Partition 實踐原理
# -------------------------------
def partition_lomuto(nums: list[int], low: int, high: int) -> int:
    """
    Lomuto Partition：
    - pivot 選最後一個元素（原因：
        1. 保證掃描過程中 pivot 不會被讀取或交換
        2. 掃描邏輯簡單，不需要特例判斷
        3. p 指標邊界設計明確，可維持穩定不變式）
    - 將陣列重新排列：
        左側 < pivot，右側 >= pivot
    - 回傳 pivot 最終索引 p

    不變式（loop invariant）：
    1. nums[low ... p]     < pivot
    2. nums[p+1 ... j-1]   >= pivot
    3. nums[high] = pivot（尚未移動前）

    時間複雜度：
    - 單次 partition：O(n)
    - Quick Sort 最壞時間：O(n^2)
    空間複雜度：
    - O(1) 原地操作

    💡 指標定義與實作選擇 (兩種常見寫法)：
    寫法 A (本實作): `p = low - 1`
    - 物理意義：`p` 指向「最後一個 < pivot 的元素」。
    - 運作方式：遇到小元素時，需要先擴充區域 (`p += 1`) 再放入 (`swap`)。
    - 結束狀態：`p` 站在小於區段的尾巴，故 pivot 最終放在 `p + 1`。

    寫法 B (另一種常見寫法): `p = low`
    - 物理意義：`p` 指向「大於等於區段的第一個元素」(即下一個準備放小元素的位置)。
    - 運作方式：遇到小元素時，直接放入該空位 (`swap`)，再將空位往右推 (`p += 1`)。
    - 結束狀態：`p` 剛好站在所有大數字的最前方，故 pivot 最終直接跟 `p` 交換。
    """

    pivot_value = nums[high]  # pivot 固定為最後元素
    p = low - 1               # p 永遠指向「最後一個 < pivot 的元素位置」
                              # 掃描開始前，尚未檢查任何元素，< pivot 的元素數量為 0
                              # p 放在區間外

    # j 為掃描指標，範圍 low 到 high - 1
    for j in range(low, high):
        if nums[j] < pivot_value:
            p += 1
            nums[p], nums[j] = nums[j], nums[p]

    # 掃描結束後，pivot 放回正確位置
    nums[p + 1], nums[high] = nums[high], nums[p + 1]

    # Lomuto 最終 pivot index = p + 1
    p = p + 1
    return p


# -------------------------------
# Hoare Partition 實踐原理
# -------------------------------
def partition_hoare(nums: list[int], left: int, right: int) -> int:
    """
    Hoare Partition：
    - pivot 選最左元素（原因：
        1. 左右雙指標交錯掃描，pivot 固定最左避免覆蓋
        2. 掃描順序先右後左，保證 pivot 不被破壞）
    - 將陣列重新排列：
        左側 ≤ pivot，右側 ≥ pivot
    - 回傳 pivot 最終索引 p

    不變式（loop invariant）：
    - 左側元素 ≤ pivot
    - 右側元素 ≥ pivot
    - pivot 最後放回交錯位置，保證正確分割區域

    時間複雜度：
    - 單次 partition：O(n)
    - Quick Sort 最壞時間：O(n^2)
    空間複雜度：
    - O(1) 原地操作
    """

    pivot_value = nums[left]  # pivot 固定為最左元素
    p_left, p_right = left, right  # 左右掃描指標

    while p_left < p_right:
        # 先從右邊掃描，找小於 pivot 的元素
        while p_left < p_right and nums[p_right] >= pivot_value:
            p_right -= 1
        nums[p_left] = nums[p_right]

        # 再從左邊掃描，找大於 pivot 的元素
        while p_left < p_right and nums[p_left] <= pivot_value:
            p_left += 1
        nums[p_right] = nums[p_left]

    nums[p_left] = pivot_value
    p = p_left  # Hoare 最終 pivot index
    return p

def quick_sort(nums: list[int], low: int, high: int, method: str = 'lomuto') -> None:
    """
    快速排序 (Quick Sort)
    
    時間複雜度:
    - 最佳/平均: O(N log N)
      -> `N`: 每次 partition 需要掃描當前區間的所有元素一次。
      -> `log N`: 遞迴的深度。當每次 pivot 都能將陣列大致平分時，陣列會被切分 log N 次才到底。
    - 最壞: O(N^2) (當每次 partition 極度不平衡時)
    空間複雜度:
    - 最佳/平均: O(log N) (遞迴 Call Stack 深度)
    - 最壞: O(N) (退化為單邊遞迴，每次分割都極度不平衡)
    """
    if low < high:
        # 選擇 partition 函數
        if method == 'lomuto':
            p = partition_lomuto(nums, low, high)
        elif method == 'hoare':
            p = partition_hoare(nums, low, high)
        else:
            raise ValueError("method must be 'lomuto' or 'hoare'")

        # 遞迴排序左右子陣列
        quick_sort(nums, low, p - 1, method)
        quick_sort(nums, p + 1, high, method)


if __name__ == '__main__':
    test_cases = [
        [2, 3, 9, 1, 7, 4],
        [2, 5, 3, 4, 1],
        [5, 9, 2, 1, 4, 7, 5, 8, 3, 6],
        [],
        [1],
        [3, 2],
        [2, 2, 2, 2],
    ]

    for nums in test_cases:
        for method in ['lomuto', 'hoare']:
            nums_copy = nums.copy()
            quick_sort(nums_copy, 0, len(nums_copy) - 1, method=method)
            assert nums_copy == sorted(nums), f"{method} failed: {nums_copy}"

    print("All test cases passed!")