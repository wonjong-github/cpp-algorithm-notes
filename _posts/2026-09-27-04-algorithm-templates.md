---
layout: post
title: "4. 알고리즘 템플릿"
date: 2026-09-27 09:04:00 +0900
categories: notes
order: 4
---
{% raw %}
## 격자 이동 (2차원 좌표)

> 좌표는 **(행 r, 열 c)** = `grid[r][c]`. 수학의 (x, y)와 반대 순서라 헷갈리기 쉬움.
> **북(N) = 위 = r - 1**, 남(S) = r + 1, 동(E) = c + 1, 서(W) = c - 1.

### 방식 0. 방향마다 배열 + `switch` 복붙 (처음 짤 때 흔한 방식)

```cpp
int e[] = {0, 1}, w[] = {0, -1}, s[] = {1, 0}, n[] = {-1, 0};

switch (command) {
    case 'E':
        // 범위 검사 → 한 칸씩 이동하며 장애물 검사 → 성공 시 갱신 (약 25줄)
        break;
    case 'W':
        // 위와 같은 코드, e만 w로 바뀜 (약 25줄)
        break;
    // 'S', 'N'도 동일하게 반복...
}
```

- 장점: 방향별 로직이 눈에 바로 보여서 처음 짤 때 직관적.
- 단점: **같은 코드 4벌** → 버그도 4벌. 실제로 `== 'O'` 버그를 네 군데 모두 고쳐야 했음 (Q10).

### 방식 1. 가장 많이 쓰는 방식: `dr` / `dc` 배열 + 방향 인덱스

```cpp
//              N   E  S   W      (시계 방향 순서로 두면 회전이 쉬움)
int dr[] = {-1, 0, 1,  0};
int dc[] = { 0, 1, 0, -1};
const string DIRS = "NESW";       // 문자 → 인덱스 변환용

auto inRange = [&](int r, int c) { return 0 <= r && r < H && 0 <= c && c < W; };

for (const string &route : routes) {
    int d = DIRS.find(route[0]);        // 'E' → 1
    int cnt = stoi(route.substr(2));

    int nr = r, nc = c;
    bool ok = true;
    for (int k = 0; k < cnt; k++) {
        nr += dr[d];
        nc += dc[d];
        if (!inRange(nr, nc) || park[nr][nc] == 'X') { ok = false; break; }
    }
    if (ok) { r = nr; c = nc; }
}
```

- 방향이 **숫자 d 하나**로 표현됨 → 이동 로직은 한 벌만 작성.
- BFS/DFS에서는 `for (int d = 0; d < 4; d++)`로 4방향을 전부 돌면 됨 (아래 BFS 템플릿 참고).
- 범위 검사를 `inRange` 람다로 빼두면 조건식 오타가 줄어듦.

### 방식 2. `map<char, pair<int,int>>`: 문자 명령이 바로 방향일 때

```cpp
map<char, pair<int, int>> dir = {
    {'N', {-1, 0}}, {'S', {1, 0}}, {'E', {0, 1}}, {'W', {0, -1}}
};
auto [dr1, dc1] = dir[route[0]];      // 'E' → (0, 1)
```

- `'U' 'D' 'L' 'R'`, `'N' 'S' 'E' 'W'`처럼 명령 문자가 주어지는 시뮬레이션 문제에서 읽기 좋음.
- 단점: 회전(시계/반시계)을 표현하기 어려움 → 회전이 있으면 방식 1.

### 회전 / 반대 방향 (방식 1에서 시계 방향 순서로 배열했을 때)

```cpp
d = (d + 1) % 4;   // 시계 방향 90도 (N → E)
d = (d + 3) % 4;   // 반시계 90도   (N → W)   ※ (d - 1) % 4는 d=0일 때 -1이 됨!
d = (d + 2) % 4;   // 반대 방향     (N → S)
```

### 8방향 (대각선 포함)

```cpp
int dr8[] = {-1, -1, -1,  0, 0,  1, 1, 1};
int dc8[] = {-1,  0,  1, -1, 1, -1, 0, 1};
for (int d = 0; d < 8; d++) { int nr = r + dr8[d], nc = c + dc8[d]; /* ... */ }
```

### 이동 규칙 두 가지: 문제를 꼭 확인!

```cpp
// (a) 전부 아니면 무시: 도중에 막히면 명령 전체 취소 (공원 산책)
//     → 위 방식 1 코드처럼 nr, nc로 미리 가보고 ok일 때만 반영

// (b) 막힐 때까지 미끄러지기: 벽 앞에서 멈춤 (리코쳇 로봇, 얼음 미끄러지기)
while (inRange(r + dr[d], c + dc[d]) && grid[r + dr[d]][c + dc[d]] != 'X') {
    r += dr[d];
    c += dc[d];
}
```

### 좌표 표현 방법

```cpp
int r, c;                          // 1) 변수 두 개: 가장 단순
pair<int, int> pos = {r, c};       // 2) pair: queue<pair<int,int>>에 넣기 편함
auto [r2, c2] = pos;

struct P {                         // 3) struct: 좌표 덧셈이 많을 때
    int r, c;
    P operator+(const P &o) const { return {r + o.r, c + o.c}; }
};

int id = r * W + c;                // 4) 1차원 인덱스: visited를 1차원 배열로 쓸 때
int rr = id / W, cc = id % W;      //    다시 (r, c)로
```

- 방식 0처럼 `vector<int> start = {0, 0}`로 좌표를 담으면 동작은 하지만, `start[0]`이 행인지 열인지 매번 떠올려야 함 → `r`, `c` 변수나 `pair` 권장.

## BFS (격자 최단거리)

```cpp
int dr[] = {-1, 1, 0, 0};
int dc[] = {0, 0, -1, 1};

int bfs(const vector<string> &grid, int sr, int sc, int er, int ec) {
    int R = grid.size(), C = grid[0].size();
    vector<vector<int>> dist(R, vector<int>(C, -1));
    queue<pii> q;
    q.push({sr, sc});
    dist[sr][sc] = 0;

    while (!q.empty()) {
        auto [r, c] = q.front();
        q.pop();
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= R || nc < 0 || nc >= C) continue;
            if (grid[nr][nc] == '0' || dist[nr][nc] != -1) continue;   // 벽 or 방문
            dist[nr][nc] = dist[r][c] + 1;
            q.push({nr, nc});
        }
    }
    return dist[er][ec];   // 도달 불가면 -1
}
```

## DFS (그래프, 재귀)

```cpp
vector<vector<int>> adj;
vector<bool> visited;

void dfs(int u) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (!visited[v]) dfs(v);
    }
}

// 그래프 입력 (무방향)
// adj.assign(n + 1, {});  visited.assign(n + 1, false);
// adj[a].push_back(b); adj[b].push_back(a);
```

## 백트래킹 (N과 M 스타일)

```cpp
int n, m;
vector<int> picked;
vector<bool> used;

void backtrack() {
    if ((int)picked.size() == m) {
        for (int x : picked) cout << x << ' ';
        cout << '\n';
        return;
    }
    for (int i = 1; i <= n; i++) {
        if (used[i]) continue;
        used[i] = true;  picked.push_back(i);
        backtrack();
        used[i] = false; picked.pop_back();   // 원상복구
    }
}
```

## 다익스트라

```cpp
// adj[u] = {(v, w), ...}
vector<ll> dijkstra(int start, const vector<vector<pii>> &adj) {
    vector<ll> dist(adj.size(), LINF);
    priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<>> pq;
    dist[start] = 0;
    pq.push({0, start});

    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d > dist[u]) continue;           // 이미 더 짧은 경로로 처리됨
        for (auto [v, w] : adj[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
```

## 유니온 파인드

```cpp
vector<int> parent;

int find(int x) {
    if (parent[x] == x) return x;
    return parent[x] = find(parent[x]);   // 경로 압축
}

bool unite(int a, int b) {
    a = find(a); b = find(b);
    if (a == b) return false;             // 이미 같은 집합 (사이클)
    parent[b] = a;
    return true;
}
// 초기화: parent.resize(n + 1); iota(parent.begin(), parent.end(), 0);
// 주의: using namespace std; 와 함께 쓰면 std::find와 이름이 겹칠 수 있음 → findRoot 등으로 이름 변경 권장
```

## 매개변수 탐색 (답을 이분 탐색)

```cpp
// "조건을 만족하는 최솟값" 찾기. check(mid)가 단조(F F F T T T)일 때
ll lo = 0, hi = 2e9;          // 답이 반드시 [lo, hi] 안에 있도록
while (lo < hi) {
    ll mid = (lo + hi) / 2;
    if (check(mid)) hi = mid;
    else lo = mid + 1;
}
// lo가 답
```

## 투 포인터 (합이 S 이상인 최소 구간 길이)

```cpp
int l = 0, best = INF;
ll sum = 0;
for (int r = 0; r < n; r++) {
    sum += a[r];
    while (sum >= S) {
        best = min(best, r - l + 1);
        sum -= a[l++];
    }
}
```

## 누적합

```cpp
vector<ll> pre(n + 1, 0);
for (int i = 0; i < n; i++) pre[i + 1] = pre[i] + a[i];
// 구간 [l, r] 합 (0-indexed) = pre[r + 1] - pre[l]
```

## DP 예시 (배낭 문제, 1차원)

```cpp
// W: 용량, (w[i], v[i]): 무게, 가치
vector<int> dp(W + 1, 0);
for (int i = 0; i < n; i++)
    for (int c = W; c >= w[i]; c--)       // 0/1 배낭은 역순!
        dp[c] = max(dp[c], dp[c - w[i]] + v[i]);
```

## 수학

```cpp
// 에라토스테네스의 체
vector<bool> isPrime(N + 1, true);
isPrime[0] = isPrime[1] = false;
for (int i = 2; (ll)i * i <= N; i++)
    if (isPrime[i])
        for (int j = i * i; j <= N; j += i) isPrime[j] = false;

// 최대공약수 / 최소공배수 (C++17, <numeric>)
gcd(12, 18);   // 6
lcm(4, 6);     // 12

// 모듈러 거듭제곱
ll power(ll a, ll b, ll mod) {
    ll res = 1; a %= mod;
    while (b > 0) {
        if (b & 1) res = res * a % mod;
        a = a * a % mod;
        b >>= 1;
    }
    return res;
}
```
{% endraw %}

---

[← 전체 목록](../../)
