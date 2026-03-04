from functools import wraps
from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(vals: list) -> Optional[TreeNode]:
    """
    從 LeetCode 層序陣列 (BFS order) 建立二元樹。

    建立方式：BFS (Breadth-First Search / 廣度優先)
      - 用 queue 依序取出父節點，依陣列順序將下一個值
        分別指派為其左子節點、再右子節點。
      - None 代表該位置無節點（但不會再展開其子節點）。

    Example:
        vals = [-10, 9, 20, None, None, 15, 7]

        建出的樹：
              -10
             /    \
            9     20
                 /  \
                15    7
    """
    if not vals:
        return None
    root = TreeNode(vals[0])
    queue = deque([root])
    i = 1
    while queue and i < len(vals):
        node = queue.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root


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
