from functools import wraps
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def create_linklist_from_array(arr: list[int]) -> Optional[ListNode]:
    """
    從陣列 (Array/List) 建立一個單向鏈結串列 (Linked List)
    """
    if not arr:
        return None

    head = ListNode(arr[0])
    curr = head
    for val in arr[1:]:
        curr.next = ListNode(val)
        curr = curr.next

    return head


def traversal_linklist(head: Optional[ListNode]) -> list[int]:
    """
    走訪並回傳鏈結串列內的所有節點值 (轉回 Array/List 方便觀察與測試)
    """
    res = []
    curr = head
    while curr:
        res.append(curr.val)
        curr = curr.next
    return res


def trace_recursion(func):
    depth = 0
    prefix = lambda: "  " * depth

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal depth
        print(f"{depth:2d}⟶:{prefix()}args: {args}, kwargs: {kwargs}")

        depth += 1
        result = func(*args, **kwargs)
        depth -= 1

        print(f"{depth:2d}⟵:{prefix()}result: {result}, args: {args}, kwargs: {kwargs}")
        return result

    return wrapper
