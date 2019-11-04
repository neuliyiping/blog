# n = int(input())
# while n > 0:
#     s = input()
#     res = []
#     for e in s:
#         if len(res) < 2:
#             res.append(e)
#             continue
#         if len(res) >= 2:
#             if e == res[-1] and e == res[-2]:
#                 continue
#         if len(res) >= 3:
#             if e == res[-1] and res[-2] == res[-3]:
#                 continue
#         res.append(e)
#     print("".join(res))
#     n -= 1

# n, dist = map(int, input().split())
# nums = list(map(int, input().split()))
#
# res = 0
# left = 0
# right = 2
#
# while left < n - 2:
#     while right < n and nums[right] - nums[left] <= dist:
#         right += 1
#     if right - 1 - left >= 2:
#         num = right - left - 1
#         res += num * (num - 1) // 2
#     left += 1
#
# print(res % 99997867)

# def isHu(nums):
#     """
#     判断是否可以胡牌
#     :param nums:
#     :return:
#     """
#     if not nums:
#         return True
#     n = len(nums)
#     count0 = nums.count(nums[0])
#     # 没出现过雀头，且第一个数字出现的次数 >= 2,去掉雀头剩下的能不能和牌
#     if n % 3 != 0 and count0 >= 2 and isHu(nums[2:]) == True:
#         return True
#     # 如果第一个数字出现次数 >= 3，去掉这个刻子后看剩下的能和牌
#     if count0 >= 3 and isHu(nums[3:]) == True:
#         return True
#     # 如果存在顺子，移除顺子后剩下的能和牌
#     if nums[0] + 1 in nums and nums[0] + 2 in nums:
#         last_nums = nums.copy()
#         last_nums.remove(nums[0])
#         last_nums.remove(nums[0] + 1)
#         last_nums.remove(nums[0] + 2)
#         if isHu(last_nums) == True:
#             return True
#     # 以上条件都不满足，则不能和牌
#     return False
#
#
# def main(nums):
#     """
#     遍历所有可以抓到的牌看能不能胡牌
#     :return:
#     """
#     d = {}
#     for i in nums:
#         d[i] = d.get(i, 0) + 1
#     card_list = set(range(1, 10)) - {i for i, v in d.items() if v == 4}
#     res = []
#     for i in card_list:
#         if isHu(sorted(nums + [i])):  # 如果这种抽牌方式可以和牌
#             res.append(i)  # 加入和牌类型列表
#     res = ' '.join(str(x) for x in sorted(res)) if res else '0'
#     print(res)
#
#
# s = input()
# nums = [int(x) for x in s.split()]
# main(nums)

# include <bits/stdc++.h>
# using
# namespace
# std;
#
# int
# main()
# {
#     int
# n, m, k, Max = 1, x, y;
# cin >> n;
# while (n - -){
# cin >> m;
# map < pair < int, int >, int > M, T;
# for (int i=1;i <= m;i++){
# cin >> k;
# for (int j=0;j < k;j++){
# pair < int, int > p;
# cin >> p.first >> p.second;
# if (M.find(p) == M.end())
# T[p] = 1;
# else {
# if (M[p] == i-1){
# T[p]++;
# Max = max(Max, T[p]);
# } else
# T[p] = 1;
# }
# M[p] = i;
# }
# }
# cout << Max << endl;
# }
# return 0;
# }


# 方法二
# 动态规划
# 全部通过
# # include<iostream>
# # include<vector>
# # include<unordered_map>
# using
# namespace
# std;
#
# int
# getAns(vector < vector < int >> & nums)
# {
#
#     int
# M = 0x7ffffff;
# int
# n = nums.size();
# vector < vector < int >> dp(1 << n, vector < int > (n, M));
# dp[1][0] = 0;
# for (int i=1; i < n; i++)
# dp[1 << i][i] = M;
# for (int i=1; i < (1 << n);
# i + +){
# for (int j=0; j < n; j++){
# if (dp[i][j] != M){
# for (int k=0; k < n; k++){
# if ((i & (1 << k)) == 0){
# dp[i | (1 << k)][k] = min(dp[i | (1 << k)][k], dp[i][j]+nums[j][k]);
# }
# }
# }
# }
# }
# int ans = M;
# for (int i=1; i < n; i++){
# ans = min(ans, dp[(1 << n)-1][i]+nums[i][0]);
# }
# return ans;
# }
# int
# main()
# {
# int
# n;
# while (cin >> n){
# vector < vector < int >> edges(n, vector < int > (n, 0));
# int x;
# for (int i=0; i < n; i++){
# for (int j=0; j < n; j++){
# cin >> edges[i][j];
# }
# }
# cout << getAns(edges) << endl;
# }
# return 0;
# }

#
# n = int(input())
# m = []
# for i in range(n):
#     m.append(list(map(int, input().split())))
#
# V = 1 << (n - 1)  # 从左至右每一位二进制代表第i个城市是否被访问 如1000代表，第一个城市被访问，而其他城市没有
# dp = [[float("inf")] * V for i in range(n)]  # dp[i][j]:从节点i只经过集合j所有点再回到0点所需要的最小开销
#
# for i in range(n):
#     dp[i][0] = m[i][0]
#
# for j in range(1, V):
#     for i in range(n):
#         for k in range(1, n):  # 能不能先到k城市
#             if (j >> (k - 1) & 1) == 1:  # 可以途径k
#                 dp[i][j] = min(dp[i][j], m[i][k] + dp[k][j ^ (1 << (k - 1))])
#
# # 从0出发，经过所有点，再回到0的费用
# print(dp[0][(1 << (n - 1)) - 1])




# n = int(input())
# s=input()
# lis=[]
# for i in range(n):
#     if s[i]=='O':
#         lis.append(i)
# print(lis)
# for i in range(n):
#     if s[i] == 'X':
#         count=[]
#         for j in range(len(lis)):
#             count.append(abs(i-lis[j]))
#         print(min(count),end=' ')
#     else:
#         print(0, end=' ')



p = int(input())
for count in range(p):
    n,m=input().split()
    zxy=0
    lis=input().split()
    lis=list(map(int,lis))
    k=0
    dp = [0] * int(n)
    for tmp in range(int(n)):
        k+=lis[tmp]
        if k <= int(m):
            dp[tmp] =0
        else:
            pp=lis[tmp]
            for j in range(tmp):
                pp+=lis[j]
                if pp<=int(m):
                    dp[j]=min(dp[j],dp[j-1]+1)
                else:
                    pp-=lis[j]
                    dp[tmp]+=1
    dp=list(map(str,dp))
    print(' '.join(dp))






















