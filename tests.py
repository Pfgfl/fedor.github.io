parent = []
rank = []


def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]


def union(x, y):
    if rank[x] < rank[y]:
        parent[x] = y
    elif rank[x] > rank[y]:
        parent[y] = x
    else:
        parent[y] = x
        rank[x] += 1


ch = 0
n, m = map(int, input().split())

parent = [i for i in range(n)]
rank = [0] * n

result = []

for i in range(m):
    u, v = map(int, input().split())
    a = find(u)
    b = find(v)
    if a == b:
        result.append(str(i + 1))
        ch += 1
    else:
        union(a, b)

print(ch)
print(' '.join(result))
