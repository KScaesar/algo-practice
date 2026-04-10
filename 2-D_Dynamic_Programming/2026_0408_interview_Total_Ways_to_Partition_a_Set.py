"""
題目：集合分組總數

給定一個整數陣列 nums，其長度為 n，每個元素視為彼此可區分的元素。
請計算將這些元素劃分為若干個非空子集合（groups）的所有不同分組方式數量，並回傳該總數。

規則說明：
1. 每個元素必須且只能屬於一個子集合
2. 每個子集合至少包含一個元素
3. 子集合之間沒有順序差異
4. 子集合內元素的排列順序不影響分組結果

範例 1：
Input: nums = [1]
Output: 1
說明：(1)

範例 2：
Input: nums = [1, 2]
Output: 2
說明：(1)(2), (1,2)

範例 3：
Input: nums = [1, 2, 3]
Output: 5
說明：(1)(2)(3), (1,2)(3), (1)(2,3), (1,3)(2), (1,2,3)

範例 4：
Input: nums = [1, 2, 3, 4]
Output: 15
"""

# [思考過程：為什麼需要增加維度 k？]
#
# 1. 初始嘗試 (1D DP):
#    定義 f(i) 為處理到第 i 個元素的方法數。
#    - 第 i 個元素自己開一組：方法數 = f(i-1)
#    - 第 i 個元素加入現有組：?? (需要知道目前有幾組才有辦法計算選擇)
#
# 2. 發現「資訊欠債 (Information Deficiency)」:
#    「加入現有組」這個動作，依賴於「過去歷史中的分組數量」。
#    如果目前的狀態 (i) 不足以做出完整的下一步決策，
#    那個缺少的資訊就是必須增加的維度。
#
# 3. 維度擴張 (2D DP):
#    定義 f(i, k) = 前 i 個元素劃分為 k 個非空子集合的方法數。
#    - 情境 A (自己開一組)：前 i-1 個元素必須已組成 k-1 組。
#      => f(i-1, k-1)
#    - 情境 B (加入現有組)：前 i-1 個元素已經組成 k 組，第 i 個元素有 k 個選擇。
#      => k * f(i-1, k)
#
# 這就是 Stirling Numbers of the Second Kind 的推導邏輯。

# [邊界條件思考 (Base Cases)]
# 1. k > i:
#    當袋子數量多於數字數量時，因為規定袋子不能為空，所以是不可能的任務。
#    => return 0
#
# 2. k == 1:
#    不論有多少數字，通通塞進同一個袋子的方法只有一種。
#    => return 1
#
# 3. k == i:
#    數字剛好一人一袋的方法也只有一種。
#    => return 1 (其實也可由遞迴推出，但作為邊界可加速)
#
# 4. i == 0:
#    雖然題目通常 n >= 1，但在遞迴中這是重要的終止條件。

# [複雜度分析 (Complexity Analysis)]
# 1. 暴力解 (Brute Force):
#    - Time: O(k^n) - 枚舉每個元素去哪個組。
#    - Space: O(n) - 遞迴深度。
#
# 2. 動態規劃 (Top-down DP):
#    - Time: O(n^2) - 狀態總數共 n * k 個，每個狀態轉移為 O(1)。
#    - Space: O(n^2) - memo 表格儲存狀態空間，加上 O(n) 的遞迴深度。
#
# 3. 動態規劃 (Bottom-up DP):
#    - Time: O(n^2) - 雙迴圈填充表格。
#    - Space: O(n) - 滾動陣列最佳化後只需儲存兩列狀態。

import math
from functools import cache
from typing import List


class Solution:
    def count_partitions(self, nums: List[int]) -> int:
        n = len(nums)
        # return self._by_input(n)
        return self._by_result(n)

    def _by_input(self, n: int) -> int:
        """
        方法 a (輸入視角):
        站在元素的角度，決定「開新組」或「加入舊組」。
        使用 Stirling Numbers of the Second Kind 加總。
        """
        if n == 0:
            return 1

        @cache
        def dfs(i, k):
            """
            定義 dfs(i, k): 將前 i 個『可區分元素』劃分為『恰好 k 個非空子集合』的方法數。
            """
            # 邊界條件 (依據剛才討論的邏輯)
            if k == 1 or k == i:
                return 1
            if k == 0 or k > i:
                return 0

            # 遞迴轉移
            # 自己開一組: dfs(i - 1, k - 1)
            # 加入現有組: k * dfs(i - 1, k)
            # (原因：因為數字可區分，加入這 k 個內容物不同的組，會產生 k 種不同的分組結果)
            return dfs(i - 1, k - 1) + k * dfs(i - 1, k)

        # 由於題目要求的是「劃分為若干個非空子集合」，並未指定組數。
        # 因此我們必須考慮所有可能的組數 k (從 1 到 n)，並將其結果累加 (Accumulate)。
        # 這個『分組總數』在數學上被定義為 Bell Number。
        return sum(dfs(n, k) for k in range(1, n + 1))

    def _by_result(self, n: int) -> int:
        """
        方法 b (結果視角):
        站在「結果結構」的角度來拆解問題。
        邏輯：思考「最後一個元素」會在哪一組？這一組還包含了誰？

        站在「最後一組」的角度，枚舉「這一組到底包了多少人」。
        使用 Bell Number 的一維遞迴公式。
        """

        @cache
        def bell(i):
            """
            狀態定義 bell(i)：將『i 個不同的元素』進行隨意分組的總方法數。
            
            解題核心：我們隨便抓一個「主角」出來，看他最後的分組結果。
            完成一次完整分組可以拆解為兩個「獨立步驟」，因此使用【乘法原理】：
            
            1. 第一步：其餘分組 (Not Teaming Up) —— 定義子問題
               - 我們枚舉「不跟主角組隊」的人數 j (從 0 到 i-1)。
               - 這些被排除在主角小組外的人，他們自己要進行隨意分組。
               - 方法數就是子問題的答案：bell(j)。
            
            2. 第二步：組隊狀態 (Teaming Up) —— 選擇成員
               - 既然有 j 個人「不組隊」，代表剩下的 (i-1)-j 個人要「跟主角組隊」。
               - 從 i-1 人中挑選這群組員的方法數原本是：math.comb(i-1, i-1-j)。
               - 利用【組合對稱性】C(n, k) = C(n, n-k)，這等同於：math.comb(i-1, j)。
               - 這一步決定了主角那一組的數量。
            
            3. 總結：
               - 將這兩步相乘：bell(j) * math.comb(i-1, j)。
               - 代表每一種「主角組成員組合」都可以搭配「其餘路人的所有分法」。
               - 最後將所有可能的 j (0 到 i-1) 加總，得到 bell(i)。
            """
            # Base Case: 0 個人有 1 種空分法
            if i == 0:
                return 1

            # [具體舉例：i=3，成員是{1, 2, 3}，主角是 3 號]
            # 程式碼中的 j 會從 0 到 2 跑一遍：
            #
            # - 當 j=2 : 
            #   【第一步：其餘】這2人隨便分 (B(2)=2)。
            #   【第二步：組隊】從{1,2}挑2人不組隊 (C(2,2)=1)。主角組固定為 (3)。
            #   【相乘】：2 * 1 = 2 種結果。(即 (3)(1,2) 和 (3)(1)(2))
            #
            # - 當 j=1 : 
            #   【第一步：其餘】這1人隨便分 (B(1)=1)。
            #   【第二步：組隊】從{1,2}挑1人不組隊 (C(2,1)=2)。主角組可能是 (3,1) 或 (3,2)。
            #   【相乘】：1 * 2 = 2 種結果。(即 (3,1)(2) 和 (3,2)(1))
            #
            # - 當 j=0 : 
            #   【第一步：其餘】剩下0人 (B(0)=1)。
            #   【第二步：組隊】從{1,2}挑0人不組隊 (C(2,0)=1)。主角組固定為 (3,1,2)。
            #   【相乘】：1 * 1 = 1 種結果。(即 (3,1,2))
            # 
            # 總計：2 + 2 + 1 = 5 種。
            return sum(bell(j) * math.comb(i - 1, j) for j in range(i))

        return bell(n)


def main():
    solution = Solution()

    # Case 1
    assert solution.count_partitions([1]) == 1

    # Case 2
    assert solution.count_partitions([1, 2]) == 2

    # Case 3
    assert solution.count_partitions([1, 2, 3]) == 5

    # Case 4
    assert solution.count_partitions([1, 2, 3, 4]) == 15

    print("All tests passed!")


if __name__ == "__main__":
    main()
