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

## 이분 탐색 총정리

> 범위를 **절반씩** 줄여 가며 찾기. 크기 N이면 약 log₂N번 → 10억 범위도 **30번**, 10¹⁵ 범위도 **50번**.

### 언제 쓰나 (신호)

| 신호 | 예 |
|---|---|
| **정렬된** 배열에서 값 / 위치 / 개수 찾기 | "x 이상인 첫 위치", "x의 개수" |
| 답의 범위가 엄청 큼 (10⁹, 10¹⁵) + **답을 정하면 가능한지 판정은 쉬움** | 입국심사, 퍼즐 게임 챌린지 |
| "~하는 **최솟값**" / "~하는 **최댓값**" / "최소의 최대" | 랜선 자르기, 징검다리 건너기 |
| 답이 커질수록 조건이 **한 방향으로만** 바뀜 (단조성) | 숙련도↑ → 시간↓ |

### 1. STL로 하기 (정렬된 배열, `<algorithm>`)

```cpp
vector<int> v = {1, 3, 3, 3, 5, 8};                 // 반드시 정렬된 상태

binary_search(v.begin(), v.end(), 3);               // 있나? → true
lower_bound(v.begin(), v.end(), 3) - v.begin();     // 3 이상인 첫 위치 → 1
upper_bound(v.begin(), v.end(), 3) - v.begin();     // 3 초과인 첫 위치 → 4
upper_bound(...) - lower_bound(...);                // 3의 개수 → 3
lower_bound(v.begin(), v.end(), 4) - v.begin();     // 없는 값 → 들어갈 자리 4
lower_bound(v.begin(), v.end(), 9) == v.end();      // 전부 작으면 end() → 먼저 확인!

auto [b, e] = equal_range(v.begin(), v.end(), 3);   // [lower, upper) 한 번에 → e - b = 3

vector<int> d = {8, 5, 3, 3, 1};                    // 내림차순 배열은 비교 함수도 같이
lower_bound(d.begin(), d.end(), 3, greater<int>()) - d.begin();   // 2

set<int> s = {1, 3, 5, 8};
*s.lower_bound(4);                                  // 5  (set/map은 멤버 함수로! O(log n))
```

- `set`에 `std::lower_bound(s.begin(), s.end(), x)`를 쓰면 **O(n)** → 반드시 `s.lower_bound(x)`.

### 2. 직접 구현: 정렬된 배열에서 값 찾기

```cpp
int findIndex(const vector<int> &v, int x) {
    int lo = 0, hi = (int)v.size() - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (v[mid] == x) return mid;
        if (v[mid] < x) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;                                       // 없음
}
```

### 3. 매개변수 탐색: "답"을 이분 탐색

**순서**: ① 답의 범위 `[lo, hi]` 정하기 → ② `check(답)` 판정 함수 만들기 → ③ 최솟값/최댓값 중 무엇을 찾는지 정하기 → ④ 아래 틀에 넣기

```cpp
// (A) 조건을 만족하는 "최솟값": check가  F F F T T T  → 첫 T
long long lo = 1, hi = 1e18;
while (lo < hi) {
    long long mid = lo + (hi - lo) / 2;      // 내림
    if (check(mid)) hi = mid;                // mid도 답 후보 → 남김
    else lo = mid + 1;
}
// lo가 답

// (B) 조건을 만족하는 "최댓값": check가  T T T F F F  → 마지막 T
long long lo = 1, hi = maxLen;
while (lo < hi) {
    long long mid = lo + (hi - lo + 1) / 2;  // ★ 올림! (내림이면 lo = mid에서 무한 루프)
    if (check(mid)) lo = mid;                // mid도 답 후보 → 남김
    else hi = mid - 1;
}
// lo가 답
```

```cpp
// 예 (A): 입국심사 — 시간 T 안에 n명 이상 심사할 수 있나?   times = {7, 10}, n = 6 → 28
bool check(long long T) {
    long long cnt = 0;
    for (int t : times) cnt += T / t;
    return cnt >= n;
}

// 예 (B): 랜선 자르기 — 길이 L로 잘랐을 때 K개 이상 나오나?   {802, 743, 457, 539}, K = 11 → 200
bool check(long long L) {
    long long cnt = 0;
    for (long long c : cables) cnt += c / L;
    return cnt >= K;
}
```

- 반복문 형태(`lo <= hi` / `lo < hi` / 답 따로 기록)는 Q32 참고. **한 가지로 정해서 계속 같은 형태로**.

### 4. 함정 체크리스트

| 함정 | 대처 |
|---|---|
| `(lo + hi) / 2`가 넘침 (둘 다 10¹⁸ 근처) | `lo + (hi - lo) / 2` |
| `check` 안의 합계가 `int`를 넘음 | `long long cnt` / `long long total` |
| 최댓값 찾기에서 `lo = mid`인데 `mid` 내림 → 무한 루프 | `mid = lo + (hi - lo + 1) / 2` (올림) |
| 범위 `[lo, hi]`에 답이 없음 | `hi`는 "확실히 되는 값"으로 (예: 최대 난이도, 가장 느린 심사관 × n) |
| 마지막 `mid`를 답으로 반환 | 끝난 뒤의 `lo` (또는 따로 기록한 answer) |
| `check`가 단조가 아님 | 이분 탐색 불가 → 다른 방법 |
| 정렬 안 된 배열에 `lower_bound` | 결과가 의미 없음 → 먼저 `sort` |

### 5. 실수(소수) 범위

```cpp
double lo = 0, hi = 2;
for (int it = 0; it < 100; it++) {          // 조건 대신 횟수로 반복 (100번이면 충분히 정밀)
    double mid = (lo + hi) / 2;
    if (mid * mid < 2) lo = mid;
    else hi = mid;
}
// lo ≈ 1.414214 (√2)
```

### 대표 문제

| 문제 | 유형 |
|---|---|
| [PCCP 기출] 퍼즐 게임 챌린지 (Lv2) | 최솟값 (A), `long long` |
| 입국심사 (Lv3) | 최솟값 (A), 범위 10¹⁸ |
| 징검다리 건너기 (2019 카카오 인턴, Lv3) | 최댓값 (B) |
| 백준 1654 랜선 자르기 / 2805 나무 자르기 / 2110 공유기 설치 | 최댓값 (B) |

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
