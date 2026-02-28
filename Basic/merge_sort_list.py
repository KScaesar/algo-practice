from typing import Optional

from tool import ListNode, create_linklist_from_array, traversal_linklist

# -------------------------------
# 針對 ListNode 的合併 (Merge) 實踐
# -------------------------------
def merge_list(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    """
    這與陣列 (Array) 版本的 Merge 最大的差異在於：
    陣列需要額外配置 O(N) 的 temp 空間；
    而鏈結串列只需要改變「記錄下一個節點」的指標 (.next)，不需要額外的空間！
    
    時間複雜度: O(N + M) - 掃描過兩個鏈結串列的所有節點
    空間複雜度: O(1) - 原地改變指標
    """
    # 建立一個 dummy_head (哨兵節點)，可以省去很多針對第一個節點的特例檢查
    dummy = ListNode(0)
    curr = dummy
    
    # 當兩個 list 都還有節點時，比較大小，把較小的接到 curr 後面
    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
        
    # 如果 l1 還有剩，直接把剩下的整串接到 curr 後面
    if l1:
        curr.next = l1
        
    # 如果 l2 還有剩，直接把剩下的整串接到 curr 後面
    if l2:
        curr.next = l2
        
    return dummy.next

# -------------------------------
# 尋找鏈結串列中點的輔助函數
# -------------------------------
def get_mid(head: ListNode) -> ListNode:
    """
    使用「快慢指標 (Fast & Slow Pointer)」來尋找鏈結串列的中點。
    - Slow 每次走 1 步
    - Fast 每次走 2 步
    - 當 Fast 走到盡頭，Slow 剛好停在中間！
    """
    # 這裡的初始設定讓 slow 停留在前半段的尾巴，方便切斷鏈結
    slow = head
    fast = head.next
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
    return slow

def merge_sort_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    鏈結串列 (Linked List) 的 Merge Sort
    (對應 LeetCode 148: Sort List)
    
    💡 面試重要考點：
    為何 Linked List 最適合用 Merge Sort？
    因為對於 Linked List，Merge Sort 可以達到 O(N log N) 時間複雜度，
    且由於不需要「臨時陣列 temp」，空間複雜度可以降到 O(log N) (僅為遞迴的 Call Stack)。
    相對地，Quick Sort 若要在 Linked List 上實作，會非常麻煩且難以發揮優勢。
    """
    # Base Case: 如果節點是空的，或者只有一個節點，直接回傳 (天生已排序)
    if not head or not head.next:
        return head
        
    # 1. Divide (切分)：找到中點，分為 left 與 right 兩半
    left = head
    mid = get_mid(head)
    
    right = mid.next
    mid.next = None  # 關鍵：必須把中間的連結「砍斷」，才能變成獨立的兩個 List
    
    # 2. 遞迴排序左半邊與右半邊
    left = merge_sort_list(left)
    right = merge_sort_list(right)
    
    # 3. Conquer/Combine (合併)
    return merge_list(left, right)

if __name__ == '__main__':
    test_cases = [
        [4, 2, 1, 3],
        [-1, 5, 3, 4, 0],
        [],
        [1],
        [3, 2],
        [2, 2, 2, 2]
    ]
    
    for arr in test_cases:
        # 1. 將陣列轉為 Linked List
        head = create_linklist_from_array(arr)
        # 2. 對 Linked List 進行 Merge Sort
        sorted_head = merge_sort_list(head)
        # 3. 把排序後的 Linked List 轉回陣列來檢查
        result = traversal_linklist(sorted_head)
        
        expected = sorted(arr)
        assert result == expected, f"Failed for {arr}, got {result}"
        
    print("All test cases passed for ListNode Merge Sort!")
