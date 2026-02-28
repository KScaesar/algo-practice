from tool import trace_recursion


def merge(nums: list[int], left: int, mid: int, right: int) -> None:
    """
    合併兩個已排序的子陣列：
    - 左半邊：nums[left ... mid]
    - 右半邊：nums[mid+1 ... right]

    不變式（loop invariant）：
    - 每次從左右半邊挑選較小的元素放入暫存陣列 (temp) 中。
    - temp 中的元素永遠是目前看過的所有元素中由小到大排序好的。

    時間複雜度：
    - 單次合併需要掃描左右兩邊所有元素，O(N)，N 為本次合併的元素總數。

    空間複雜度：
    - O(N)，需要額外配一個 temp 陣列來暫存排序好的結果，然後再複製回原陣列 nums。

    💡 指標定義：
    - p1 指向左半邊未處理的第一個元素 (初始化為 left)
    - p2 指向右半邊未處理的第一個元素 (初始化為 mid + 1)
    """
    temp = []
    p1 = left
    p2 = mid + 1

    # 當兩邊都還有元素時，比較大小並放入 temp
    while p1 <= mid and p2 <= right:
        # 注意這裡的 `<=` 是 Merge Sort 成為「穩定排序 (Stable Sort)」的關鍵
        # 當值相同時，優先取左半邊的元素，維持相對順序不變
        if nums[p1] <= nums[p2]:
            temp.append(nums[p1])
            p1 += 1
        else:
            temp.append(nums[p2])
            p2 += 1

    # 若左半邊還有剩餘元素，直接加入 temp
    while p1 <= mid:
        temp.append(nums[p1])
        p1 += 1

    # 若右半邊還有剩餘元素，直接加入 temp
    while p2 <= right:
        temp.append(nums[p2])
        p2 += 1

    # 將暫存陣列的值複製回原陣列 nums 對應的位置
    for i in range(len(temp)):
        nums[left + i] = temp[i]


@trace_recursion
def merge_sort(nums: list[int], left: int, right: int) -> None:
    """
    合併排序 (Merge Sort)

    核心思想：Divide and Conquer (分而治之)
    1. Divide: 將陣列對半切分，直到每個子陣列只剩 1 個元素 (天生已排序)。
    2. Conquer/Combine: 將相鄰的兩個已排序子陣列，透過 `merge` 函數合併成一個大的已排序陣列。

    時間複雜度:
    - 最佳/平均/最壞: O(N log N)
      -> `log N`: 切分的深度（二元樹的高度）。
      -> `N`: 每一層級的所有 `merge` 操作加總起來，剛好會掃描過 N 個元素。
      -> 穩定表現，不管陣列本來長怎樣，都不會像 Quick Sort 退化到 O(N^2)。

    空間複雜度:
    - 總體: O(N)
      -> 每次 `merge` 都需要配置臨時陣列 `temp`，其最大長度為 N。
      -> 遞迴 Call Stack 深度 O(log N)。
      -> 總佔用空間 = 變數/陣列的空間 + 遞迴 Call Stack（呼叫堆疊）的空間。 所以 Merge Sort 的總空間在數學上是：O(N) + O(log N)。
      -> 兩者取大為 O(N)。
    """
    if left < right:
        # 避免 (left + right) integer overflow，雖然 Python 預設處理大整數，
        # 但這是在其他語言 (如 C++/Java) 中防 overflow 的好習慣。
        mid = left + (right - left) // 2

        # 遞迴排序左半邊與右半邊
        merge_sort(nums, left, mid)
        merge_sort(nums, mid + 1, right)

        # 合併兩個已排序的半邊
        merge(nums, left, mid, right)


# 為了提供更簡單的介面，寫一個包裹函數 (Wrapper)
def sort_array(nums: list[int]) -> list[int]:
    if not nums:
        return nums
    merge_sort(nums, 0, len(nums) - 1)
    return nums


if __name__ == "__main__":
    test_cases = [
        [2, 3, 9, 1, 7, 4],
        [2, 5, 3, 4, 1],
        [5, 9, 2, 1, 4, 7, 5, 8, 3, 6],
        [],
        [1],
        [3, 2],
        [2, 2, 2, 2],
    ]

    for test_nums in test_cases:
        nums_copy = test_nums.copy()
        sort_array(nums_copy)
        assert nums_copy == sorted(test_nums), f"Merge Sort failed: {nums_copy}"
        print("")

    print("All test cases passed!")
