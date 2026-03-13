"""
# [1143. Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/)
**Difficulty:** 🟡 Medium
**Tags:** String, Dynamic Programming

## Problem Description

Given two strings `text1` and `text2`, return _the length of their longest **common subsequence**. _If there is no **common subsequence**, return `0`.

A **subsequence** of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters.

        - For example, `"ace"` is a subsequence of `"abcde"`.

A **common subsequence** of two strings is a subsequence that is common to both strings.



Example 1:**

```

**Input:** text1 = "abcde", text2 = "ace"
**Output:** 3
**Explanation:** The longest common subsequence is "ace" and its length is 3.

```

Example 2:**

```

**Input:** text1 = "abc", text2 = "abc"
**Output:** 3
**Explanation:** The longest common subsequence is "abc" and its length is 3.

```

Example 3:**

```

**Input:** text1 = "abc", text2 = "def"
**Output:** 0
**Explanation:** There is no such common subsequence, so the result is 0.

```



**Constraints:**

        - `1 <= text1.length, text2.length <= 1000`

        - `text1` and `text2` consist of only lowercase English characters.

## Hints
1. Try dynamic programming.
DP[i][j] represents the longest common subsequence of text1[0 ... i] & text2[0 ... j].
2. DP[i][j] = DP[i - 1][j - 1] + 1 , if text1[i] == text2[j]
DP[i][j] = max(DP[i - 1][j], DP[i][j - 1]) , otherwise

## Similar Questions
- [Longest Palindromic Subsequence](https://leetcode.com/problems/longest-palindromic-subsequence/) (Medium)
- [Delete Operation for Two Strings](https://leetcode.com/problems/delete-operation-for-two-strings/) (Medium)
- [Shortest Common Supersequence ](https://leetcode.com/problems/shortest-common-supersequence/) (Hard)
- [Maximize Number of Subsequences in a String](https://leetcode.com/problems/maximize-number-of-subsequences-in-a-string/) (Medium)
- [Subsequence With the Minimum Score](https://leetcode.com/problems/subsequence-with-the-minimum-score/) (Hard)
"""

from typing import List, Optional, Dict, Tuple


class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        pass


def main():
    solution = Solution()

    # Case 1: Example 1 - text1 = "abcde", text2 = "ace"
    # Output: 3 (LCS is "ace")
    assert solution.longestCommonSubsequence("abcde", "ace") == 3

    # Case 2: Example 2 - text1 = "abc", text2 = "abc"
    # Output: 3 (LCS is "abc")
    assert solution.longestCommonSubsequence("abc", "abc") == 3

    # Case 3: Example 3 - text1 = "abc", text2 = "def"
    # Output: 0 (no common subsequence)
    assert solution.longestCommonSubsequence("abc", "def") == 0

    # Case 4: One empty string
    assert solution.longestCommonSubsequence("", "abc") == 0
    assert solution.longestCommonSubsequence("abc", "") == 0

    # Case 5: Single character match
    assert solution.longestCommonSubsequence("a", "a") == 1
    assert solution.longestCommonSubsequence("a", "b") == 0

    print("All tests passed!")


if __name__ == "__main__":
    main()
