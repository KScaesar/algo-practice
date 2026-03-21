from typing import List


class Solution:
    """
    Write a function that, given an array A of N integers, returns the smallest
    positive integer (greater than 0) that does not occur in A.

    For example, given A = [1, 3, 6, 4, 1, 2], the function should return 5.
    Given A = [1, 2, 3], the function should return 4.
    Given A = [-1, -3], the function should return 1.

    Assumptions:
    - N is an integer within the range [1..100,000];
    - each element of array A is an integer within the range [-1,000,000..1,000,000].
    """

    def _naive(self, nums: List[int]) -> int:
        """
        Time Complexity: O(N)
        Space Complexity: O(N)
        """
        size = len(nums)
        seen = [False] * (size + 1)
        for num in nums:
            if 1 <= num <= size:
                seen[num] = True

        for i in range(1, size + 1):
            if not seen[i]:
                return i

        return size + 1

    def _cyclic_sort(self, nums: List[int]) -> int:
        """
        Time Complexity: O(N)
        Space Complexity: O(1)
        """
        size = len(nums)

        # 1. 進行 Cyclic Sort (將數字放回它應該在的 Index)
        # 尋找的目標是 1 ~ size，數字 x 應該被放在 index x - 1 的位子
        for i in range(size):
            # 交換條件：
            # (1) 數字在合法範圍內 1 <= nums[i] <= size
            # (2) 該數字尚未被放在正確的位子 nums[i] != nums[nums[i] - 1]
            # 使用 while 是因為：從別的地方換過來的新數字，可能也不在正確的位子上，需要繼續換
            while 1 <= nums[i] <= size and nums[i] != nums[nums[i] - 1]:
                # 取出它該去的位置 (避免 Python swap tuple 解構順序的雷)
                correct_idx = nums[i] - 1
                nums[i], nums[correct_idx] = nums[correct_idx], nums[i]

        # 2. 檢查哪個位置的數字是不對的
        for i in range(size):
            if nums[i] != i + 1:
                return i + 1

        # 如果 1 ~ size 都各就各位，那缺失的就是接下來的那個數字
        return size + 1

    def firstMissingPositive(self, nums: List[int]) -> int:
        # return self._naive(nums)
        return self._cyclic_sort(nums)


def main():
    solution = Solution()

    # Case 1
    assert solution.firstMissingPositive([1, 3, 6, 4, 1, 2]) == 5

    # Case 2
    assert solution.firstMissingPositive([1, 2, 3]) == 4

    # Case 3
    assert solution.firstMissingPositive([-1, -3]) == 1

    print("All tests passed!")


if __name__ == "__main__":
    main()
