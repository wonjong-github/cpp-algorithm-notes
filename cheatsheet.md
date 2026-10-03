# C++ 알고리즘 치트시트 (코딩 테스트용)

> 백준 / 프로그래머스 기준. 코딩 테스트 직전에 빠르게 훑어보는 용도.

---

## 목차

1. [기본 템플릿](#1-기본-템플릿)
2. [입출력 패턴](#2-입출력-패턴)
3. [자주 쓰는 STL](#3-자주-쓰는-stl)
4. [알고리즘 템플릿](#4-알고리즘-템플릿)
5. [C++ 기초: 헷갈리는 것들](#5-c-기초-헷갈리는-것들)
6. [자주 헷갈리는 것들 Q&A](#6-자주-헷갈리는-것들-qa)

---

## 1. 기본 템플릿

### 백준 (표준 입출력)

```cpp
#include <bits/stdc++.h>   // GCC 전용. 백준/프로그래머스 OK, macOS 기본 clang에서는 X
using namespace std;

using ll = long long;
using pii = pair<int, int>;

const int INF = 1e9;
const ll LINF = 1e18;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> a(n);
    for (auto &x : a) cin >> x;

    cout << "\n";   // endl 대신 "\n" (endl은 매번 flush해서 느림)
    return 0;
}
```

### 프로그래머스 (solution 함수)

```cpp
#include <string>
#include <vector>
#include <algorithm>
#include <unordered_map>
using namespace std;

vector<string> solution(vector<string> players, vector<string> callings) {
    vector<string> answer;
    return answer;
}
```

- 프로그래머스는 `main`이 없음. 로컬 테스트할 때만 `main`을 추가하고, 제출할 때는 `solution`만.
- 쓰는 기능의 헤더는 **직접 include** (로컬에서 되는데 사이트에서 안 되는 주요 원인).

| 기능 | 헤더 |
|---|---|
| `sort`, `find`, `reverse`, `max_element`, `lower_bound`, `next_permutation` | `<algorithm>` |
| `accumulate`, `iota`, `gcd`, `lcm` | `<numeric>` |
| `unordered_map` / `unordered_set` | `<unordered_map>` / `<unordered_set>` |
| `map` / `set` | `<map>` / `<set>` |
| `queue`, `priority_queue` | `<queue>` |
| `stack` / `deque` | `<stack>` / `<deque>` |
| `pair`, `swap`, `move` | `<utility>` |
| `stringstream` | `<sstream>` |

### 로컬 테스트 템플릿 (프로그래머스)

프로그래머스 문제를 로컬(CLion)에서 돌려볼 때 `solution` 아래에 붙여 쓰는 `main`.
**바꿀 곳은 ① `TestCase` 멤버, ② `tests` 데이터, ③ `solution(...)` 호출 인자** 세 군데뿐.

```cpp
#include <iostream>
#include <string>
#include <vector>
using namespace std;

// ---- solution 함수는 여기 ----
vector<int> solution(vector<string> name, vector<int> yearning, vector<vector<string>> photo);

// 출력 헬퍼: vector면 [a, b, c], 아니면 값 그대로
template <typename T>
void print(const T &x) { cout << x; }

template <typename T>
void print(const vector<T> &v) {
    cout << '[';
    for (size_t i = 0; i < v.size(); i++) {
        if (i) cout << ", ";
        print(v[i]);                       // 2차원 vector도 재귀로 출력됨
    }
    cout << ']';
}

// ① 문제의 매개변수 + 기대값에 맞게 수정
struct TestCase {
    vector<string> name;
    vector<int> yearning;
    vector<vector<string>> photo;
    vector<int> expected;                  // solution 반환 타입과 동일하게
};

int main() {
    // ② 문제의 "입출력 예" 표를 한 줄씩 옮기기 ([ ] → { })
    vector<TestCase> tests = {
        {{"may", "kein", "kain", "radi"}, {5, 10, 1, 3},
         {{"may", "kein", "kain", "radi"}, {"may", "kein", "brin", "deny"}, {"kon", "kain", "may", "coni"}},
         {19, 15, 6}},
        {{"kali", "mari", "don"}, {11, 1, 55},
         {{"kali", "mari", "don"}, {"pony", "tom", "teddy"}, {"con", "mona", "don"}},
         {67, 0, 55}},
    };

    int passed = 0;
    for (size_t t = 0; t < tests.size(); t++) {
        const TestCase &tc = tests[t];
        auto result = solution(tc.name, tc.yearning, tc.photo);   // ③ 인자 수정

        bool ok = (result == tc.expected);
        passed += ok;
        cout << "Test " << t + 1 << ": " << (ok ? "PASS" : "FAIL") << '\n';
        if (!ok) {
            cout << "  expected: "; print(tc.expected); cout << '\n';
            cout << "  result:   "; print(result);      cout << '\n';
        }
    }
    cout << passed << " / " << tests.size() << " passed" << endl;
    return 0;
}
```

- **반환 타입이 `int`, `string`, `long long` 같은 단일 값이어도 그대로 동작** (`==` 비교, `print`가 값 그대로 출력).
- 반환값이 `double`이면 `==` 대신 `abs(result - tc.expected) < 1e-9`로 비교.
- 답이 여러 개 가능한 문제(순서 무관 등)는 비교 전에 `sort(result.begin(), result.end())`처럼 정규화.
- 매개변수가 1~2개뿐이면 `struct` 없이 `vector<pair<입력, 기대값>>`로 써도 됨:

```cpp
vector<pair<string, int>> tests = {{"abc", 3}, {"", 0}};
for (auto &[input, expected] : tests)
    cout << (solution(input) == expected ? "PASS" : "FAIL") << '\n';
```

### 백준용 로컬 테스트

백준은 표준 입력을 받으므로 코드를 고치지 않고 **입력 파일을 리다이렉트**하는 게 편함.

```bash
# input.txt에 예제 입력 붙여넣기
g++ -std=c++17 -O2 main.cpp -o main && ./main < input.txt
# 기대 출력과 비교
./main < input.txt | diff - output.txt && echo PASS
```

- CLion: Run Configuration → "Redirect input from"에 `input.txt` 지정.
- 코드 안에서 처리하려면 `main` 맨 앞에 `freopen("input.txt", "r", stdin);` (제출 전 반드시 삭제!)

---

## 2. 입출력 패턴

```cpp
// 개수를 모르는 입력 (EOF까지)
int x;
while (cin >> x) { /* ... */ }

// 공백 포함 한 줄 읽기
string line;
cin.ignore();            // 앞에서 cin >> 을 썼다면 남은 '\n' 제거 필수
getline(cin, line);

// 공백 구분 문자열 쪼개기
stringstream ss(line);
string token;
while (ss >> token) { /* ... */ }

// 특정 구분자로 쪼개기 (예: "a,b,c")
stringstream ss2("a,b,c");
while (getline(ss2, token, ',')) { /* ... */ }

// 격자 입력 (공백 없이 붙어 있는 "0101")
int R, C;
vector<string> grid(R);
for (auto &row : grid) cin >> row;   // grid[r][c] - '0' 으로 숫자 변환

// 소수점 출력
cout << fixed << setprecision(6) << 3.14159265;   // <iomanip>
```

---

## 3. 자주 쓰는 STL

### vector

```cpp
vector<int> v(n);                       // 0으로 n개
vector<int> v2(n, -1);                  // -1로 n개
vector<vector<int>> g(R, vector<int>(C, 0));   // 2차원

v.push_back(3);
v.pop_back();
v.back();  v.front();
v.size();  v.empty();
v.clear();                               // size만 0, 메모리는 유지

sort(v.begin(), v.end());                // 오름차순
sort(v.rbegin(), v.rend());              // 내림차순
sort(v.begin(), v.end(), greater<>());   // 내림차순

// 중복 제거 (정렬 먼저!)
sort(v.begin(), v.end());
v.erase(unique(v.begin(), v.end()), v.end());

reverse(v.begin(), v.end());
int mx = *max_element(v.begin(), v.end());
long long sum = accumulate(v.begin(), v.end(), 0LL);   // 0LL 주의! (5장 참고)
```

### 정렬 총정리 (자료형별)

> 모두 `<algorithm>`. 기본은 **오름차순**, 내림차순은 `greater<>()`를 넘기거나 비교 함수에서 `>`를 씀.
> 비교 함수 규칙: **`a`가 `b`보다 앞에 와야 하면 `true`**. `<=`, `>=`는 절대 쓰지 말 것 (런타임 에러 가능).

#### 내림차순 만드는 4가지 방법 (결과 동일)

```cpp
sort(v.begin(), v.end(), greater<int>());                       // 1) greater (가장 흔함)
sort(v.begin(), v.end(), greater<>());                          //    타입 생략 가능 (C++14)
sort(v.rbegin(), v.rend());                                     // 2) 역방향 반복자로 오름차순
sort(v.begin(), v.end(), [](int a, int b) { return a > b; });  // 3) 람다
sort(v.begin(), v.end()); reverse(v.begin(), v.end());          // 4) 정렬 후 뒤집기
```

#### `vector<int>` / 일반 배열

```cpp
vector<int> v = {3, 1, 2};
sort(v.begin(), v.end());                    // 1 2 3
sort(v.begin(), v.end(), greater<>());       // 3 2 1

int arr[] = {5, 2, 9};  int n = 3;
sort(arr, arr + n);                          // 배열은 포인터로 범위 지정
sort(arr, arr + n, greater<>());

// 절댓값 기준
sort(v.begin(), v.end(), [](int a, int b) { return abs(a) < abs(b); });
```

#### `vector<string>`

```cpp
vector<string> s = {"banana", "Apple", "cherry", "kiwi"};
sort(s.begin(), s.end());                    // 사전순: Apple banana cherry kiwi  (대문자가 소문자보다 앞!)
sort(s.begin(), s.end(), greater<>());       // 사전 역순

// 길이 짧은 순, 같으면 사전순
sort(s.begin(), s.end(), [](const string &a, const string &b) {
    if (a.size() != b.size()) return a.size() < b.size();
    return a < b;
});

// 대소문자 무시 (값으로 받아서 복사본을 소문자로)
sort(s.begin(), s.end(), [](string a, string b) {
    transform(a.begin(), a.end(), a.begin(), ::tolower);
    transform(b.begin(), b.end(), b.begin(), ::tolower);
    return a < b;
});
```

#### `string` 한 개 (문자 정렬)

```cpp
string str = "hello";
sort(str.begin(), str.end());                // "ehllo"
sort(str.begin(), str.end(), greater<>());   // "ollhe"
// 활용: 애너그램 판별 → 두 문자열을 각각 정렬해서 == 비교
```

#### `vector<pair<A, B>>`

```cpp
vector<pair<int, string>> ps = {{2, "b"}, {1, "z"}, {2, "a"}};
sort(ps.begin(), ps.end());                  // first 오름차순, 같으면 second 오름차순 (자동)
                                             // → (1,z) (2,a) (2,b)
sort(ps.begin(), ps.end(), greater<>());     // first 내림차순, 같으면 second 내림차순

// first 내림차순, 같으면 second 오름차순 (섞인 경우는 람다 필수)
sort(ps.begin(), ps.end(), [](const auto &x, const auto &y) {
    if (x.first != y.first) return x.first > y.first;
    return x.second < y.second;
});

// second만 기준
sort(ps.begin(), ps.end(), [](const auto &x, const auto &y) { return x.second < y.second; });
```

#### `vector<vector<int>>` (2차원)

```cpp
vector<vector<int>> vv = {{3, 1}, {1, 5}, {1, 2}};
sort(vv.begin(), vv.end());                  // 0번 원소 → 1번 원소 순으로 사전식 비교 (pair처럼)
                                             // → {1,2} {1,5} {3,1}
// 특정 열 기준 (예: 1번 열)
sort(vv.begin(), vv.end(), [](const vector<int> &a, const vector<int> &b) { return a[1] < b[1]; });
```

#### `struct`

```cpp
struct Person { string name; int age; };
vector<Person> pp = {{"kim", 30}, {"lee", 25}, {"park", 30}};

// 나이 내림차순, 같으면 이름 오름차순
sort(pp.begin(), pp.end(), [](const Person &a, const Person &b) {
    if (a.age != b.age) return a.age > b.age;
    return a.name < b.name;
});

// 모든 기준이 오름차순이면 tie로 한 줄 (<tuple>)
sort(pp.begin(), pp.end(), [](const Person &a, const Person &b) {
    return tie(a.age, a.name) < tie(b.age, b.name);
});
```

#### 원본은 두고 순서(인덱스)만 정렬

```cpp
vector<int> score = {70, 90, 80};
vector<int> idx(score.size());
iota(idx.begin(), idx.end(), 0);             // 0, 1, 2  (<numeric>)
sort(idx.begin(), idx.end(), [&](int a, int b) { return score[a] > score[b]; });
// idx = {1, 2, 0}  → 점수 높은 사람의 번호 순서 (등수 매기기 문제)
```

#### 자동 정렬 컨테이너의 내림차순

```cpp
set<int, greater<int>> s;                          // 큰 값부터 순회
map<int, string, greater<int>> m;                  // 키 큰 순
priority_queue<int> maxpq;                         // top = 최댓값 (기본)
priority_queue<int, vector<int>, greater<int>> minpq;   // top = 최솟값 ← sort와 반대 느낌 주의!
```

#### 그 밖의 정렬 함수

```cpp
stable_sort(v.begin(), v.end(), cmp);              // 같은 값끼리 원래 순서 유지
partial_sort(v.begin(), v.begin() + k, v.end());   // 앞 k개만 정렬 (상위 k개)
is_sorted(v.begin(), v.end());                     // 정렬돼 있는지 확인
```

| 자료형 | 오름차순 | 내림차순 |
|---|---|---|
| `vector<int>` | `sort(b, e)` | `sort(b, e, greater<>())` |
| 배열 `int a[n]` | `sort(a, a + n)` | `sort(a, a + n, greater<>())` |
| `string` (문자) | `sort(s.begin(), s.end())` | `sort(..., greater<>())` |
| `vector<string>` | `sort(b, e)` (사전순) | `sort(b, e, greater<>())` |
| `pair` / `vector<vector>` | `sort(b, e)` (앞 원소부터) | `greater<>()`, 기준이 섞이면 람다 |
| `struct` | 람다 필수 | 람다 필수 |
| `set` / `map` | 기본 | 템플릿 3번째 인자 `greater<T>` |
| `priority_queue` | `greater<T>` (최소 힙) | 기본 (최대 힙) |

### string

```cpp
string s = "hello";
s.size();  s.substr(1, 3);          // substr(시작, 길이) → "ell"
s.find("ll");                        // 없으면 string::npos
if (s.find("x") == string::npos) {}
s += 'c';  s += "abc";
reverse(s.begin(), s.end());

to_string(123);                      // int → string
stoi("123");  stoll("12345678901");  // string → int / long long

char c = '7';
int d = c - '0';                     // 7
char up = toupper('a');              // 'A'  (<cctype>)
isdigit(c);  isalpha(c);
```

### map / unordered_map

```cpp
unordered_map<string, int> cnt;      // 평균 O(1), 순서 없음
map<string, int> ordered;            // O(log n), 키 오름차순 정렬됨

cnt["a"]++;                          // 없으면 0으로 자동 생성 후 ++
if (cnt.count("b")) {}               // 존재 확인 (자동 생성 X)
if (cnt.find("b") != cnt.end()) {}   // 존재 확인

for (auto &[key, val] : cnt) {}      // C++17 구조화 바인딩
cnt.erase("a");
```

### set

```cpp
set<int> s;                          // 정렬 + 중복 제거
s.insert(3);  s.erase(3);  s.count(3);
auto it = s.lower_bound(5);          // 5 이상인 첫 원소
*s.begin();  *s.rbegin();            // 최솟값 / 최댓값
```

### stack / queue / deque

```cpp
stack<int> st;   st.push(1);  st.top();   st.pop();
queue<int> q;    q.push(1);   q.front();  q.pop();
deque<int> dq;   dq.push_front(1);  dq.push_back(2);  dq.pop_front();  dq.pop_back();
// pop()은 값을 반환하지 않음! top()/front()로 먼저 읽고 pop()
```

### priority_queue

```cpp
priority_queue<int> maxpq;                                  // 최대 힙 (기본)
priority_queue<int, vector<int>, greater<int>> minpq;       // 최소 힙

// pair는 first 기준, 같으면 second 기준
priority_queue<pii, vector<pii>, greater<pii>> pq;          // (거리, 노드) 최소 힙

// 커스텀 비교: sort와 반대로 동작함에 주의!
auto cmp = [](const pii &a, const pii &b) { return a.second > b.second; };  // second 최소 힙
priority_queue<pii, vector<pii>, decltype(cmp)> pq2(cmp);
```

### 이분 탐색 (정렬된 배열)

```cpp
// lower_bound: x 이상인 첫 위치 / upper_bound: x 초과인 첫 위치
int idx = lower_bound(v.begin(), v.end(), x) - v.begin();
int cntX = upper_bound(v.begin(), v.end(), x) - lower_bound(v.begin(), v.end(), x);
bool found = binary_search(v.begin(), v.end(), x);
```

### 순열 / 조합

```cpp
// 순열 (정렬된 상태에서 시작해야 모든 순열이 나옴)
sort(v.begin(), v.end());
do {
    // v 사용
} while (next_permutation(v.begin(), v.end()));

// 조합 nCr: 선택 마스크를 순열로 돌리기
vector<int> mask(n, 0);
fill(mask.end() - r, mask.end(), 1);
do {
    for (int i = 0; i < n; i++) if (mask[i]) { /* v[i] 선택 */ }
} while (next_permutation(mask.begin(), mask.end()));
```

---

## 4. 알고리즘 템플릿

### 격자 이동 (2차원 좌표)

> 좌표는 **(행 r, 열 c)** = `grid[r][c]`. 수학의 (x, y)와 반대 순서라 헷갈리기 쉬움.
> **북(N) = 위 = r - 1**, 남(S) = r + 1, 동(E) = c + 1, 서(W) = c - 1.

#### 방식 0. 방향마다 배열 + `switch` 복붙 (처음 짤 때 흔한 방식)

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

#### 방식 1. 가장 많이 쓰는 방식: `dr` / `dc` 배열 + 방향 인덱스

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

#### 방식 2. `map<char, pair<int,int>>`: 문자 명령이 바로 방향일 때

```cpp
map<char, pair<int, int>> dir = {
    {'N', {-1, 0}}, {'S', {1, 0}}, {'E', {0, 1}}, {'W', {0, -1}}
};
auto [dr1, dc1] = dir[route[0]];      // 'E' → (0, 1)
```

- `'U' 'D' 'L' 'R'`, `'N' 'S' 'E' 'W'`처럼 명령 문자가 주어지는 시뮬레이션 문제에서 읽기 좋음.
- 단점: 회전(시계/반시계)을 표현하기 어려움 → 회전이 있으면 방식 1.

#### 회전 / 반대 방향 (방식 1에서 시계 방향 순서로 배열했을 때)

```cpp
d = (d + 1) % 4;   // 시계 방향 90도 (N → E)
d = (d + 3) % 4;   // 반시계 90도   (N → W)   ※ (d - 1) % 4는 d=0일 때 -1이 됨!
d = (d + 2) % 4;   // 반대 방향     (N → S)
```

#### 8방향 (대각선 포함)

```cpp
int dr8[] = {-1, -1, -1,  0, 0,  1, 1, 1};
int dc8[] = {-1,  0,  1, -1, 1, -1, 0, 1};
for (int d = 0; d < 8; d++) { int nr = r + dr8[d], nc = c + dc8[d]; /* ... */ }
```

#### 이동 규칙 두 가지: 문제를 꼭 확인!

```cpp
// (a) 전부 아니면 무시: 도중에 막히면 명령 전체 취소 (공원 산책)
//     → 위 방식 1 코드처럼 nr, nc로 미리 가보고 ok일 때만 반영

// (b) 막힐 때까지 미끄러지기: 벽 앞에서 멈춤 (리코쳇 로봇, 얼음 미끄러지기)
while (inRange(r + dr[d], c + dc[d]) && grid[r + dr[d]][c + dc[d]] != 'X') {
    r += dr[d];
    c += dc[d];
}
```

#### 좌표 표현 방법

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

### BFS (격자 최단거리)

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

### DFS (그래프, 재귀)

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

### 백트래킹 (N과 M 스타일)

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

### 다익스트라

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

### 유니온 파인드

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

### 이분 탐색 총정리

> 범위를 **절반씩** 줄여 가며 찾기. 크기 N이면 약 log₂N번 → 10억 범위도 **30번**, 10¹⁵ 범위도 **50번**.

#### 언제 쓰나 (신호)

| 신호 | 예 |
|---|---|
| **정렬된** 배열에서 값 / 위치 / 개수 찾기 | "x 이상인 첫 위치", "x의 개수" |
| 답의 범위가 엄청 큼 (10⁹, 10¹⁵) + **답을 정하면 가능한지 판정은 쉬움** | 입국심사, 퍼즐 게임 챌린지 |
| "~하는 **최솟값**" / "~하는 **최댓값**" / "최소의 최대" | 랜선 자르기, 징검다리 건너기 |
| 답이 커질수록 조건이 **한 방향으로만** 바뀜 (단조성) | 숙련도↑ → 시간↓ |

#### 1. STL로 하기 (정렬된 배열, `<algorithm>`)

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

#### 2. 직접 구현: 정렬된 배열에서 값 찾기

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

#### 3. 매개변수 탐색: "답"을 이분 탐색

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

#### 4. 함정 체크리스트

| 함정 | 대처 |
|---|---|
| `(lo + hi) / 2`가 넘침 (둘 다 10¹⁸ 근처) | `lo + (hi - lo) / 2` |
| `check` 안의 합계가 `int`를 넘음 | `long long cnt` / `long long total` |
| 최댓값 찾기에서 `lo = mid`인데 `mid` 내림 → 무한 루프 | `mid = lo + (hi - lo + 1) / 2` (올림) |
| 범위 `[lo, hi]`에 답이 없음 | `hi`는 "확실히 되는 값"으로 (예: 최대 난이도, 가장 느린 심사관 × n) |
| 마지막 `mid`를 답으로 반환 | 끝난 뒤의 `lo` (또는 따로 기록한 answer) |
| `check`가 단조가 아님 | 이분 탐색 불가 → 다른 방법 |
| 정렬 안 된 배열에 `lower_bound` | 결과가 의미 없음 → 먼저 `sort` |

#### 5. 실수(소수) 범위

```cpp
double lo = 0, hi = 2;
for (int it = 0; it < 100; it++) {          // 조건 대신 횟수로 반복 (100번이면 충분히 정밀)
    double mid = (lo + hi) / 2;
    if (mid * mid < 2) lo = mid;
    else hi = mid;
}
// lo ≈ 1.414214 (√2)
```

#### 대표 문제

| 문제 | 유형 |
|---|---|
| [PCCP 기출] 퍼즐 게임 챌린지 (Lv2) | 최솟값 (A), `long long` |
| 입국심사 (Lv3) | 최솟값 (A), 범위 10¹⁸ |
| 징검다리 건너기 (2019 카카오 인턴, Lv3) | 최댓값 (B) |
| 백준 1654 랜선 자르기 / 2805 나무 자르기 / 2110 공유기 설치 | 최댓값 (B) |

### 투 포인터 (합이 S 이상인 최소 구간 길이)

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

### 누적합

```cpp
vector<ll> pre(n + 1, 0);
for (int i = 0; i < n; i++) pre[i + 1] = pre[i] + a[i];
// 구간 [l, r] 합 (0-indexed) = pre[r + 1] - pre[l]
```

### DP 예시 (배낭 문제, 1차원)

```cpp
// W: 용량, (w[i], v[i]): 무게, 가치
vector<int> dp(W + 1, 0);
for (int i = 0; i < n; i++)
    for (int c = W; c >= w[i]; c--)       // 0/1 배낭은 역순!
        dp[c] = max(dp[c], dp[c - w[i]] + v[i]);
```

### 수학

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

---

## 5. C++ 기초: 헷갈리는 것들

### 값 전달 vs 참조 전달

```cpp
void f1(int a)        { a = 10; }   // 복사본 수정 → 원본 그대로
void f2(int &a)       { a = 10; }   // 원본 수정
void f3(const vector<int> &v) {}    // 복사 없이 읽기만 (큰 컨테이너는 이렇게)
```

- 큰 `vector`, `string`을 값으로 넘기면 **매 호출마다 전체 복사** → 재귀 DFS에서 시간 초과의 흔한 원인.

### range-for에서 `&` 빠뜨리기

```cpp
for (auto x : v) x *= 2;          // 복사본만 바뀜. v는 그대로!
for (auto &x : v) x *= 2;         // v가 바뀜
for (const auto &s : strs) {}     // 읽기만 할 때 (string 복사 방지)
```

### `size()`는 unsigned

```cpp
vector<int> v;                              // 비어 있음
for (int i = 0; i < v.size() - 1; i++)      // v.size() - 1 = 엄청 큰 수 → 범위 밖 접근!
for (int i = 0; i + 1 < (int)v.size(); i++) // 안전
```

### 정수 오버플로우

```cpp
int a = 100000, b = 100000;
long long c = a * b;              // 틀림! int끼리 곱해서 이미 오버플로우 후 대입
long long d = (long long)a * b;   // 맞음
long long e = 1LL * a * b;        // 맞음

accumulate(v.begin(), v.end(), 0);    // 결과 타입이 int! 합이 크면 오버플로우
accumulate(v.begin(), v.end(), 0LL);  // long long으로 누적
```

- `int` 범위: 약 ±21억 (2 × 10⁹). 합/곱이 이걸 넘을 수 있으면 무조건 `long long`.

### 정수 나눗셈 / 나머지

```cpp
7 / 2;          // 3 (소수점 버림)
7 / 2.0;        // 3.5
-7 / 2;         // -3 (0 방향 버림. 파이썬은 -4)
-7 % 3;         // -1 (파이썬은 2) → 양수로 만들기: ((x % m) + m) % m
(a + b - 1) / b // a/b 올림 (a, b 양수)
```

### char ↔ int ↔ string

```cpp
'7' - '0';          // 7   (char → 숫자)
'a' + 1;            // 98  (int가 됨!)
char(('a' + 1));    // 'b'
string(1, 'a');     // "a"  (char → string)
to_string(7);       // "7"
"abc" + 'd';        // 틀림! 문자열 리터럴(포인터) + char → 이상한 결과
string("abc") + 'd' // "abcd"
```

### `map[]`은 없는 키를 만든다

```cpp
map<string, int> m;
if (m["kim"] == 0) {}   // "kim"이 없어도 m에 {"kim", 0}이 추가됨!
if (m.count("kim")) {}  // 존재 확인은 이렇게
```

### 반복자 무효화

```cpp
// 순회 중 erase는 반환값을 받아야 함
for (auto it = v.begin(); it != v.end(); ) {
    if (*it % 2 == 0) it = v.erase(it);
    else ++it;
}
// push_back으로 재할당이 일어나면 기존 반복자/포인터/참조 모두 무효
```

### 평가 순서는 정해져 있지 않음

```cpp
f(i, ++i);          // 어떤 인자가 먼저 평가될지 모름 → 쓰지 말 것
swap(it, --it);     // 같은 문제 (6장 Q2 참고)
```

### 전역 vs 지역 변수 초기화

```cpp
int g[100];         // 전역: 0으로 초기화됨
int main() {
    int l[100];     // 지역: 쓰레기값! → int l[100] = {}; 또는 vector 사용
    int big[10000000];   // 지역에 큰 배열 → 스택 오버플로우. 전역이나 vector로
}
```

### priority_queue 비교는 sort와 반대

```cpp
sort(..., greater<>());                               // 내림차순
priority_queue<int, vector<int>, greater<int>> pq;   // 최소 힙 (top이 가장 작음)
```

### 2차원 vector 선언

```cpp
vector<vector<int>> g(R, vector<int>(C, 0));   // R x C, 0으로 채움
g.assign(R, vector<int>(C, 0));                 // 재초기화 (테스트케이스 여러 개일 때)
```

### 구조화 바인딩 (C++17)

```cpp
pair<int, int> p = {1, 2};
auto [a, b] = p;                   // 복사
for (auto &[k, v] : m) v++;        // map 값 수정
```

---

## 6. 자주 헷갈리는 것들 Q&A

### Q1. 벡터를 스왑하는 방법?

```cpp
// 벡터 전체를 서로 교환: O(1) (내부 포인터만 교환, 원소 복사 X)
a.swap(b);
std::swap(a, b);

// 벡터 안 원소끼리 교환
std::swap(v[i], v[j]);
std::iter_swap(v.begin() + i, v.begin() + j);

// 메모리까지 비우기 (swap trick)
vector<int>().swap(v);
```

- 벡터 전체를 스왑해도 반복자는 무효화되지 않고, **상대편 벡터**를 가리키게 됨.

### Q2. `swap(iter, --iter)`는 왜 동작하지 않나? (달리기 경주)

```cpp
auto iter = find(players.begin(), players.end(), calling);
swap(iter, --iter);        // ❌
```

문제가 두 가지:

1. **반복자 변수끼리 교환됨**: 인자가 반복자라서 `std::swap`이 반복자 두 개를 바꿀 뿐, 벡터 안의 원소는 그대로임.
2. **평가 순서 미정**: 같은 변수에 `--iter`를 쓰면서 다른 인자로도 넘김 → 결과가 컴파일러마다 다름.

```cpp
iter_swap(iter, iter - 1);        // ✅ 원소 교환
swap(*iter, *(iter - 1));         // ✅ 같은 의미
```

### Q3. 직접 만든 `swap(int a, int b)`가 안 바뀌는 이유?

```cpp
void swap(int a, int b)   { int c = a; a = b; b = c; }   // ❌ 복사본만 바뀜
void swap(int &a, int &b) { int c = a; a = b; b = c; }   // ✅ 참조로 원본 수정
```

- 게다가 `using namespace std;` 상태에서 `swap`이라는 이름을 직접 만들면 `std::swap`과 헷갈리거나 모호해질 수 있음 → 그냥 `std::swap` 사용.

### Q4. 달리기 경주: `find`를 매번 쓰면 시간 초과

- `find`는 O(n) → 호출이 많으면 O(n × m).
- **이름 → 등수 해시맵**을 따로 관리하면 호출 1회당 O(1).

```cpp
#include <string>
#include <vector>
#include <unordered_map>
using namespace std;

vector<string> solution(vector<string> players, vector<string> callings) {
    unordered_map<string, int> rank;
    for (int i = 0; i < (int)players.size(); i++) rank[players[i]] = i;

    for (const string &calling : callings) {
        int idx = rank[calling];
        string &front = players[idx - 1];

        rank[calling] = idx - 1;
        rank[front] = idx;
        swap(players[idx - 1], players[idx]);
    }
    return players;
}
```

### Q5. 코테 사이트에서 `error: no template named 'unordered_map'`

- 원인: `#include <unordered_map>` 누락.
- 로컬(macOS clang/libc++)에서는 다른 헤더를 통해 **우연히 딸려 들어와서(전이적 포함)** 컴파일됐지만, 표준이 보장하지 않으므로 사이트 컴파일러에서는 실패.
- `find`를 `<algorithm>` 없이 써도 로컬에서 컴파일되는 것도 같은 이유.
- 해결: 쓰는 기능의 헤더를 직접 include하거나, 제출용 코드에서는 `#include <bits/stdc++.h>` 사용.

### Q6. 로컬 테스트 케이스 작성법 (프로그래머스 문제)

```cpp
int main() {
    vector<string> players  = {"mumu", "soe", "poe", "kai", "mine"};   // [ ] 가 아니라 { }
    vector<string> callings = {"kai", "kai", "mine", "mine"};
    vector<string> expected = {"mumu", "kai", "mine", "soe", "poe"};

    vector<string> result = solution(players, callings);
    cout << (result == expected ? "PASS" : "FAIL") << endl;   // vector는 == 로 비교 가능
}
```

- C++에는 `["a", "b"]` 같은 배열 리터럴이 없음 → 중괄호 초기화 `{...}` 사용.
- 예시가 여러 개면 1장의 [로컬 테스트 템플릿](#로컬-테스트-템플릿-프로그래머스) 사용.

### Q7. 입출력 예가 여러 개일 때 테스트 케이스를 한 번에 돌리려면? (추억 점수)

- 입력들과 기대값을 `struct TestCase`로 묶고 `vector<TestCase>`를 반복문으로 검사.
- 중첩 중괄호는 타입 구조를 그대로 따라감:
  - `vector<vector<string>>` → `{{"may"}, {"kein", "deny"}}`
  - `struct` → 멤버 **선언 순서대로** `{name, yearning, photo, expected}`
- 풀이 포인트: `name_yearn[photo[i][j]]`는 모르는 이름이면 0을 반환(하면서 키를 추가)하므로 이 문제에선 결과가 맞음. 키 추가가 싫으면:

```cpp
auto it = name_yearn.find(person);
if (it != name_yearn.end()) sum += it->second;
```

### Q8. `map` vs `ordered_map` vs `unordered_map` 언제 쓰나?

**`ordered_map`은 C++ 표준에 없음!** 정렬되는 맵이 바로 `std::map`. (`ordered_map`이라고 쓰면 컴파일 에러)

| | `map` | `unordered_map` |
|---|---|---|
| 내부 구조 | 레드-블랙 트리 | 해시 테이블 |
| 조회/삽입/삭제 | O(log n) 보장 | 평균 O(1), 최악 O(n) |
| 순회 순서 | **키 오름차순** | 뒤죽박죽 (예측 불가) |
| `lower_bound` 등 범위 탐색 | O | X |
| 키 조건 | `<` 비교 가능 (`pair`, `vector`, `string` 모두 OK) | 해시 가능 (`pair` 키는 **해시 직접 작성 필요**) |
| 헤더 | `<map>` | `<unordered_map>` |

**`map`을 쓸 때**
- 결과를 **키 순서대로 출력**해야 할 때 (예: 이름 사전순, 날짜순)
- "x 이상인 가장 작은 키", 최솟값/최댓값 키가 필요할 때 → `lower_bound`, `begin()`, `rbegin()`
- 키가 `pair<int,int>` 같은 복합 타입이라 해시 작성이 귀찮을 때
- 데이터가 작아서(수천 개 이하) 속도 차이가 의미 없을 때

**`unordered_map`을 쓸 때**
- **순서 상관없이 존재 확인 / 개수 세기 / 이름 → 값 매핑**만 할 때 (예: 달리기 경주, 추억 점수, 완주하지 못한 선수)
- 데이터가 많고(10만 개 이상) 조회가 많아서 속도가 중요할 때

```cpp
map<int, string> m = {{5, "e"}, {1, "a"}, {3, "c"}};
for (auto &[k, v] : m) {}          // 1, 3, 5 순서로 순회
m.lower_bound(2)->first;           // 3 (2 이상인 첫 키)
m.begin()->first;                  // 1 (최소 키)
m.rbegin()->first;                 // 5 (최대 키)

unordered_map<string, int> u;
u.reserve(200000);                 // 크기를 미리 알면 rehash 방지 → 더 빠름

// pair를 unordered_map 키로 쓰려면 해시 함수 필요
struct PairHash {
    size_t operator()(const pair<int, int> &p) const {
        return hash<long long>()(((long long)p.first << 32) ^ (unsigned)p.second);
    }
};
unordered_map<pair<int, int>, int, PairHash> grid;
// 귀찮으면 그냥 map<pair<int,int>, int> 사용
```

- 헷갈리는 이유: 다른 언어와 이름이 다름. Java `TreeMap` = C++ `map`, Java `HashMap` / Python `dict` = C++ `unordered_map`.
- **입력 순서 유지하는 맵은 STL에 없음** (Python `dict`, Java `LinkedHashMap`과 다름). 필요하면 `vector`에 순서를 따로 저장.
- `set` / `unordered_set`도 똑같은 기준으로 고르면 됨.
- 판단이 어려우면: **순서가 필요하면 `map`, 아니면 `unordered_map`**.

### Q9. vector / string에서 특정 값을 찾고 인덱스 구하기 (공원 산책)

**vector → `find` + 반복자 빼기** (`<algorithm>`)

```cpp
vector<int> v = {4, 7, 2, 7};
auto it = find(v.begin(), v.end(), 7);    // 반복자 반환
if (it != v.end()) {                      // 못 찾으면 v.end() → 반드시 확인!
    int idx = it - v.begin();             // 1  (distance(v.begin(), it)도 같음)
}

// 조건으로 찾기
auto it2 = find_if(v.begin(), v.end(), [](int x) { return x < 3; });   // 2의 위치

// 마지막으로 등장하는 위치
int last = v.rend() - find(v.rbegin(), v.rend(), 7) - 1;   // 3
```

**string → 멤버 함수 `s.find()`** (인덱스를 바로 반환)

```cpp
string s = "OSO";
size_t p = s.find('S');                   // 1  (문자, 문자열 모두 가능)
if (p != string::npos) {}                 // 못 찾으면 string::npos (-1 아님!)
s.find('O', 1);                           // 1번 인덱스부터 검색 → 2
s.rfind('O');                             // 뒤에서부터 → 2
```

**2차원 격자에서 시작점 찾기**

```cpp
int sr = 0, sc = 0;
for (int i = 0; i < (int)park.size(); i++) {
    size_t j = park[i].find('S');
    if (j != string::npos) { sr = i; sc = j; break; }
}
```

- `std::find`(알고리즘)는 **반복자**, `string::find`(멤버)는 **인덱스(size_t)** 를 반환 → 이름은 같지만 다른 함수.
- string에 `std::find(s.begin(), s.end(), 'S')`를 써도 되지만, 인덱스가 필요하면 `s.find('S')`가 더 간단.
- `string::npos`는 `size_t`의 최댓값. `int p = s.find(...)`로 받으면 `-1`처럼 보이지만, 비교는 항상 `== string::npos`로.
- 여러 번 조회해야 하면 매번 `find`(O(n)) 대신 `unordered_map`에 값 → 인덱스를 저장 (Q4 참고).

### Q10. 공원 산책: 예시 일부만 통과하는 이유 (격자 이동 시뮬레이션)

**버그 1: 장애물을 만나면 "명령 전체 무시"인데 "가다가 멈춤"으로 구현**

```cpp
for (...) {
    if (갈 수 있음) now = next;
    else break;              // 여기서 멈춘 now를
}
start = now;                 // ❌ 그대로 반영해 버림 → 중간까지 이동한 상태가 됨
```

→ 성공 여부를 `bool ok`로 기록하고 **끝까지 성공했을 때만** 위치 갱신.

**버그 2: 지나갈 수 있는 칸을 `== 'O'`로 판단**

- 시작 칸 `'S'`도 지나갈 수 있는 칸인데, `'O'`만 허용하면 시작점을 다시 지나갈 때 막힘.
- 격자 문제에서는 **"갈 수 있는 것"을 나열하지 말고 "막힌 것"을 검사** → `park[r][c] == 'X'`이면 불가.
- 주의: 버그 1만 고쳐도 예시 3개는 전부 통과하지만, 시작 칸을 다시 지나가는 추가 테스트(`{"SOO"}`, `{"E 2", "W 2"}`)는 여전히 `[0, 2]`로 실패 → 제출하면 숨은 테스트에서 틀림.

**리팩터링: 방향 4개를 `switch`로 복붙하지 말고 방향 벡터 하나로**

```cpp
for (const string &route : routes) {
    char dir = route[0];
    int cnt = stoi(route.substr(2));       // "E 2" → 2
    int dr = 0, dc = 0;
    if (dir == 'E') dc = 1;
    else if (dir == 'W') dc = -1;
    else if (dir == 'S') dr = 1;
    else dr = -1;                          // 'N'

    int nr = r, nc = c;
    bool ok = true;
    for (int k = 0; k < cnt; k++) {
        nr += dr; nc += dc;
        if (nr < 0 || nr >= H || nc < 0 || nc >= W || park[nr][nc] == 'X') { ok = false; break; }
    }
    if (ok) { r = nr; c = nc; }            // 전부 성공했을 때만 이동
}
```

- 코드를 4번 복붙하면 버그도 4번 복붙됨 → 한 곳만 고치고 나머지를 놓치기 쉬움.
- `switch`문 안에서 `break`는 **switch를 빠져나가고**, `for` 안의 `break`는 **for만** 빠져나감. 중첩되면 어느 쪽인지 헷갈리므로 `bool` 플래그가 안전.
- 테스트 팁: 예시가 우연히 통과하는 경우가 많음 → **"시작 칸을 다시 지나가기"** 같은 경계 케이스를 직접 추가.

### Q11. 이중 for문 안의 `break`는 어디까지 빠져나가나?

**`break`는 자신을 감싼 가장 가까운 `for` / `while` / `switch` 하나만 빠져나감.** 바깥 반복문은 계속 돎.

```cpp
for (int i = 0; i < R; i++) {
    for (int j = 0; j < C; j++) {
        if (조건) break;       // 안쪽 for만 종료 → 바깥 for는 i+1로 계속
    }
    // break 후 여기로 옴
}
```

**둘 다 빠져나가는 방법**

```cpp
// 1) bool 플래그 (가장 무난)
bool found = false;
for (int i = 0; i < R && !found; i++) {      // 바깥 조건에 !found
    for (int j = 0; j < C; j++) {
        if (g[i][j] == 'S') { sr = i; sc = j; found = true; break; }
    }
}

// 2) 함수 / 람다로 분리해서 return (깔끔)
auto findStart = [&]() -> pair<int, int> {
    for (int i = 0; i < R; i++)
        for (int j = 0; j < C; j++)
            if (g[i][j] == 'S') return {i, j};   // return은 모든 반복문을 한 번에 탈출
    return {-1, -1};
};
auto [sr, sc] = findStart();

// 3) goto (C++에서 합법, 다중 루프 탈출에는 종종 쓰임)
for (int i = 0; i < R; i++)
    for (int j = 0; j < C; j++)
        if (g[i][j] == 'S') { sr = i; sc = j; goto done; }
done:;
```

**`switch` 안의 `break` 주의 (공원 산책 코드에서 나온 구조)**

```cpp
for (...) {                    // 바깥: routes 순회
    switch (command) {
        case 'E':
            if (범위 밖) break;       // ← switch 탈출 (다음 route로). for 탈출 아님!
            for (...) {
                if (장애물) break;    // ← 안쪽 for만 탈출. switch는 계속 진행
            }
            break;                   // ← switch 탈출
    }
}
```

- `switch` 안에서 바깥 반복문을 다음으로 넘기고 싶으면 `continue`를 쓰면 됨 (`continue`는 `switch`에 반응하지 않고 반복문에 적용됨).
- Java의 `break label;` 같은 문법은 C++에 없음 → 위 3가지 중 선택.

### Q12. 2차원 좌표 이동 코드: 방향별 분기 vs 방향 배열

→ 4장 [격자 이동 (2차원 좌표)](#격자-이동-2차원-좌표)에 정리.

- **방향별 분기**: 방향마다 `int e[] = {0, 1}` 같은 배열 + `switch`로 방향별 코드 4벌.
- **많이 쓰는 방식**: `dr[4]`, `dc[4]` 배열에 방향을 **인덱스 d**로 표현 → 이동 코드 한 벌, `(d + 1) % 4`로 회전.
- 문자 명령이 방향 그 자체면 `map<char, pair<int,int>>`도 깔끔.
- 핵심 차이: **"방향"을 코드(분기)가 아닌 데이터(배열 값)로 표현** → 반복되는 로직이 사라짐.

### Q13. 덧칠하기는 어떻게 접근하나? (그리디)

**문제 요약**: 길이 n 벽, 폭 m 롤러, 다시 칠할 구역 번호 `section`(오름차순). 최소 몇 번 칠하나?

**접근: 아직 안 칠한 가장 왼쪽 구역에 롤러의 왼쪽 끝을 맞춘다 (그리디)**

1. 가장 왼쪽의 칠해야 할 구역 `s`는 **어차피 누군가 칠해야 함**.
2. `s`를 덮는 롤러 위치 중 오른쪽으로 가장 멀리 가는 건 `[s, s + m - 1]` → 다음 구역들을 최대한 많이 덮음.
3. 그 범위 안의 구역은 건너뛰고, 범위 밖의 다음 구역에서 1번 반복.

```
n=8, m=4, section=[2, 3, 6]
2 → 칠함 [2~5], 횟수 1
3 → 3 ≤ 5, 이미 칠해짐
6 → 6 > 5, 칠함 [6~9], 횟수 2   → 답 2
```

```cpp
int solution(int n, int m, vector<int> section) {
    int answer = 0;
    int painted = 0;                 // 여기까지(포함) 칠해진 마지막 구역
    for (int s : section) {
        if (s <= painted) continue;  // 이미 칠해진 구역이면 건너뜀
        answer++;
        painted = s + m - 1;         // s에 롤러 왼쪽 끝을 맞춰 칠함
    }
    return answer;
}
```

- **벽 전체를 배열로 만들 필요 없음**: `section`만 보면 됨 (O(section 길이)).
- 롤러가 벽 밖으로 나가면 안 되지만(`s + m - 1 > n`), 그 경우 롤러를 왼쪽으로 당겨도 **덮는 section 구역은 똑같음** → 계산에는 영향 없음.
- 그리디가 맞는지 확인하는 질문: "지금 선택이 이후에 손해를 볼 수 있나?" → 가장 왼쪽 구역은 반드시 칠해야 하고, 오른쪽으로 최대한 밀어두는 게 항상 이득이라 손해 없음.
- 비슷한 유형: 구간 덮기, 단속카메라(프로그래머스), 회의실 배정(백준 1931).

### Q14. 오름차순 / 내림차순 정렬을 자료형별로?

→ 3장 [정렬 총정리 (자료형별)](#정렬-총정리-자료형별)에 정리.

- 기본은 오름차순, 내림차순은 **`greater<>()`** 한 개만 기억해도 대부분 해결.
- `pair`, `vector<vector<int>>`, `string`은 **앞 원소부터 사전식 비교**가 자동 → 기준이 "첫째 내림, 둘째 오름"처럼 섞일 때만 람다.
- `struct`는 비교 기준이 없으므로 람다 필수.
- 헷갈림 주의: `priority_queue`는 `greater`를 주면 **최소** 힙 (sort와 반대 느낌).
- 대문자가 소문자보다 사전순으로 앞 (`'A'`=65 < `'a'`=97) → `"Apple" < "banana"`, `"Zoo" < "apple"`.

### Q15. 덧칠하기: 롤러가 벽 끝(n)을 넘어가는 경우는 왜 따로 처리 안 해도 되나?

`painted = s + m - 1`이 `n`보다 커져도(예: n=5, m=3, s=4 → painted=6) 답이 맞는 이유.

**1. `painted`는 "어디까지 칠했나"를 비교하는 기준일 뿐, 벽을 실제로 칠하지 않음**

- 벽을 배열로 만들어 `wall[6]`에 쓴다면 범위 초과 에러지만, 여기서는 숫자 비교(`s <= painted`)만 함.
- `section`의 모든 값은 `n` 이하 → `painted >= n`이면 **"끝까지 다 칠했다"**와 같은 뜻.
  `painted = 6`이든 `painted = 5`든 이후 모든 구역이 `s <= painted`로 판정되므로 결과 동일.

**2. 실제로는 롤러를 안쪽으로 당기면 되는데, 그래도 덮는 section 구역이 똑같음**

```
n=5, m=3, section=[4, 5]

코드상 롤러:    [4 ~ 6]   ← 6은 벽 밖
실제 롤러:    [3 ~ 5]     ← 벽 끝에 맞춰 왼쪽으로 당김

칠해야 할 구역 4, 5 → 둘 다 덮음. 횟수 1로 동일
```

- 당긴 롤러 `[n-m+1, n]`은 `[s, n]`을 전부 포함함 (넘어갔다는 건 `s + m - 1 > n`, 즉 `n - m + 1 < s`이므로).
- 당기면서 새로 덮는 왼쪽 부분 `[n-m+1, s-1]`은 **`s`보다 앞 → 이미 칠했거나 칠할 필요 없는 곳**. 이득도 손해도 없음.
- 문제 조건 `m <= n` 덕분에 롤러를 당길 공간은 항상 있음.

**일반화: 시뮬레이션에서 "실제 위치"와 "판정에 필요한 값"을 구분하기**

- 답(칠한 횟수)에 영향을 주는 건 **어떤 section 구역을 덮느냐**뿐 → 롤러의 정확한 위치는 몰라도 됨.
- 경계 처리를 할지 고민될 때: "경계를 넘는 값이 이후 **비교 결과**를 바꾸는가?"를 확인. 안 바꾸면 처리 불필요.
- 반대로 공원 산책처럼 **배열에 인덱스로 접근**하면 경계 검사가 반드시 필요함 (Q10).

### Q16. vector / map을 최댓값(무한대)으로 초기화하려면? (대충 만든 자판)

**vector / 배열**

```cpp
#include <climits>    // INT_MAX, LLONG_MAX
#include <limits>     // numeric_limits

vector<int> a(n, INT_MAX);                          // 2147483647
vector<int> b(n, numeric_limits<int>::max());       // 같은 값 (타입만 바꾸면 되는 일반형)
vector<long long> c(n, LLONG_MAX);

const int INF = 1e9;                                 // 코테에서 가장 많이 씀 (이유는 아래)
vector<int> d(n, INF);
vector<vector<int>> g(R, vector<int>(C, INF));      // 2차원

v.assign(n, INF);                                    // 이미 있는 vector 재초기화
fill(v.begin(), v.end(), INF);

int arr[26];
fill(arr, arr + 26, INF);                            // 일반 배열은 fill
// memset은 바이트 단위라 0, -1, 0x3f(≈10억) 말고는 쓰면 안 됨
memset(arr, 0x3f, sizeof(arr));                      // 각 원소 = 1061109567
```

**`INT_MAX`보다 `1e9`를 많이 쓰는 이유: 오버플로우**

```cpp
int x = INT_MAX;
x + 1;          // -2147483648 (음수가 됨!) → 최솟값 비교가 전부 망가짐
dist[u] + w     // dist[u]가 INT_MAX면 더하는 순간 오버플로우 (다익스트라, DP)

const int INF = 1e9;
INF + INF;      // 2000000000 → int 범위(약 21억) 안이라 안전
```

- **값에 뭔가를 더할 수 있으면 `1e9`**, 비교만 하면 `INT_MAX`도 OK.
- `1e9`가 실제 답이 될 수 있는 문제(답이 10억 이상)는 `long long` + `1e18` 사용.
- 최솟값(-무한대)은 `INT_MIN`, `numeric_limits<int>::min()`, 또는 `-INF`.

**map / unordered_map: "기본값"을 지정하는 기능이 없음**

`m[key]`는 없는 키를 **0으로** 만들어 버리므로 최솟값을 구할 때 문제가 됨. 방법 3가지:

```cpp
unordered_map<char, int> m;

// 1) 없으면 먼저 INF로 넣기
if (!m.count(key)) m[key] = INF;
m[key] = min(m[key], cost);

// 2) try_emplace: 없을 때만 INF로 삽입, 있으면 그대로 (C++17, 한 줄)
auto [it, inserted] = m.try_emplace(key, INF);
it->second = min(it->second, cost);

// 3) 키 범위가 정해져 있으면 처음에 전부 INF로 채우기
for (char ch = 'A'; ch <= 'Z'; ch++) m[ch] = INF;

// 조회할 때 없으면 INF로 보기
auto it2 = m.find(key);
int val = (it2 == m.end()) ? INF : it2->second;
```

- 키가 `'A'`~`'Z'`처럼 작고 정해져 있으면 map 대신 **배열 `int best[26]`** + `best[c - 'A']`가 더 빠르고 간단.
- `m.contains(key)`는 **C++20** 문법. 프로그래머스(C++20)에서는 사용 가능, 채점 사이트가 C++17 이하면 컴파일 에러 → 그때는 `m.count(key)` 또는 `m.find(key) != m.end()` (Q31).

### Q17. 2차원 배열 선언하는 방법 총정리

**`vector<vector<int>>`: 코테에서 가장 많이 씀**

```cpp
int R = 3, C = 4;                                    // R = 행(세로), C = 열(가로)

vector<vector<int>> a(R, vector<int>(C));            // R x C, 0으로 채움
vector<vector<int>> b(R, vector<int>(C, -1));        // R x C, -1로 채움
vector<vector<int>> c = {{1, 2, 3}, {4, 5, 6}};      // 값을 직접 (2 x 3)

vector<vector<int>> d;                               // 먼저 선언만 하고
d.assign(R, vector<int>(C, 0));                      // 나중에 크기 지정 / 재초기화

vector<vector<int>> e(R + 1, vector<int>(C + 1, 0)); // 1부터 시작하는 좌표를 그대로 쓰고 싶을 때

c.size();       // 행 개수 (2)
c[0].size();    // 열 개수 (3)
```

- **읽는 법**: "`vector<int>(C)` 한 줄을 `R`개 만든다" → `m[r][c]`는 **r행 c열**.
- 순서 주의: `vector<vector<int>>(행 개수, vector<int>(열 개수))`. 뒤바꾸면 `m[r][c]` 접근 시 범위를 벗어남.

**값 채우기**

```cpp
// 1, 2, 3, ... 순서대로 (행렬 테두리 회전하기)
for (int r = 0; r < R; r++)
    for (int c = 0; c < C; c++)
        m[r][c] = r * C + c + 1;

// range-for로 채우기 (& 필수! 없으면 복사본만 바뀜)
int num = 1;
for (auto &row : m)
    for (int &x : row) x = num++;

// 출력 (디버깅용)
for (const auto &row : m) {
    for (int x : row) cout << x << ' ';
    cout << '\n';
}
```

**행마다 길이가 다른 2차원 (그래프 인접 리스트)**

```cpp
vector<vector<int>> adj(n);          // 행 n개, 각 행은 비어 있음
adj[0].push_back(1);                 // 0번 노드 → 1번 노드 간선
adj[0].push_back(2);                 // adj[0].size() = 2, adj[1].size() = 0
```

**문자 격자**

```cpp
vector<string> grid = {"#..", ".#."};       // 입력이 문자열로 주어지면 그대로 사용
grid[1][1];                                 // '#'  (r행 c열 문자)
vector<vector<char>> cg(R, vector<char>(C, '.'));   // 수정이 많으면 char 2차원도 OK
```

**일반 배열 (크기가 고정일 때)**

```cpp
int g[100][100];                     // 전역: 0으로 자동 초기화
int main() {
    int local[100][100] = {};        // 지역: = {} 없으면 쓰레기값!
    memset(local, 0, sizeof(local)); // 0 / -1로 재초기화 (<cstring>)
    fill(&local[0][0], &local[0][0] + 100 * 100, 5);   // 다른 값으로 채우기
}
void f(int a[][100]) {}              // 함수 인자로 넘길 땐 열 크기 필수
```

- 크기가 입력에 따라 달라지면 `vector`, 최대 크기가 정해져 있고(예: 100 x 100) 속도가 중요하면 전역 배열.
- 지역에 큰 배열(예: `int a[1000][1000]`)은 스택 오버플로우 → 전역이나 `vector`로.

**복사 vs 참조**

```cpp
auto copy = m;                       // 전체 복사 (copy를 바꿔도 m은 그대로)
auto &ref = m;                       // 같은 것을 가리킴 (ref를 바꾸면 m도 바뀜)

void byRef(vector<vector<int>> &m);  // 함수 안에서 원본 수정 + 복사 비용 없음
void byVal(vector<vector<int>> m);   // 호출할 때마다 전체 복사 (느림, 원본 안 바뀜)
```

- 회전 전 상태를 보관해야 하면 `auto before = m;`으로 복사해 두고 비교.

**그 밖에**

```cpp
vector<int> flat(R * C);             // 1차원으로 펼치기: (r, c) → r * C + c
flat[r * C + c] = 8;

vector<vector<vector<int>>> v3(H, vector<vector<int>>(R, vector<int>(C, 0)));   // 3차원
```

| 상황 | 추천 |
|---|---|
| 크기가 입력으로 주어짐 | `vector<vector<int>> m(R, vector<int>(C, 0))` |
| 행마다 길이가 다름 (그래프) | `vector<vector<int>> adj(n)` + `push_back` |
| 문자 격자 입력 | `vector<string>` 그대로 |
| 최대 크기가 작고 고정 | 전역 `int a[MAX][MAX]` |
| visited를 좌표 하나로 관리 | 1차원 `vector<int>(R * C)` |

### Q18. `sort` 사용법: 정렬 기준 정하기, 역방향 정렬

> 자료형별 예시는 3장 [정렬 총정리 (자료형별)](#정렬-총정리-자료형별) 참고. 여기서는 **`sort`가 어떻게 동작하고 기준을 어떻게 쓰는지**를 정리.

**기본형**

```cpp
#include <algorithm>

sort(시작, 끝);              // 오름차순 (작은 것 → 큰 것)
sort(시작, 끝, 비교함수);     // 비교함수 기준

sort(v.begin(), v.end());                 // 전체
sort(v.begin() + 1, v.end());             // 0번은 두고 나머지만: {9,7,5,3,1} → {9,1,3,5,7}
sort(v.begin(), v.begin() + 3);           // 앞 3개만
sort(arr, arr + n);                       // 일반 배열
```

- `끝`은 **포함하지 않음** (`v.end()`는 마지막 원소 다음 위치).
- 시간 복잡도 O(n log n). 원소 100만 개도 문제없음.

**비교 함수 규칙 (가장 중요)**

```
comp(a, b)가 true  →  a가 b보다 앞에 온다
```

- `return a < b;` → 작은 게 앞 → **오름차순**
- `return a > b;` → 큰 게 앞 → **내림차순**
- **같을 때는 반드시 `false`** → `<=`, `>=`를 쓰면 안 됨. 같은 값이 많을 때 런타임 에러(범위 밖 접근)가 날 수 있음.

**비교 함수를 쓰는 4가지 형태 (결과 동일)**

```cpp
// 1) 람다: 가장 많이 씀
sort(v.begin(), v.end(), [](int a, int b) { return a > b; });

// 2) 일반 함수: 여러 곳에서 재사용할 때
bool cmpDesc(int a, int b) { return a > b; }
sort(v.begin(), v.end(), cmpDesc);            // 괄호 없이 이름만 넘김

// 3) 표준 함수 객체
sort(v.begin(), v.end(), greater<int>());     // 내림차순
sort(v.begin(), v.end(), less<int>());        // 오름차순 (기본값과 같음)

// 4) struct 안에 operator< 정의: sort(b, e)만 써도 이 기준이 적용됨
struct Student {
    string name; int score; int age;
    bool operator<(const Student &o) const { return score > o.score; }   // 점수 내림차순
};
sort(st.begin(), st.end());
```

- 람다 매개변수는 **`const 타입 &`** 로 받기: `[](const string &a, const string &b)`. 값으로 받으면 비교할 때마다 복사됨.

**역방향(내림차순) 정렬 방법 5가지**

```cpp
sort(v.begin(), v.end(), greater<int>());                       // 1) greater (가장 흔함)
sort(v.begin(), v.end(), greater<>());                          //    타입 생략 가능
sort(v.rbegin(), v.rend());                                     // 2) 역방향 반복자
sort(v.begin(), v.end(), [](int a, int b) { return a > b; });  // 3) 람다
sort(v.begin(), v.end(), cmpDesc);                              // 4) 함수
sort(v.begin(), v.end()); reverse(v.begin(), v.end());          // 5) 오름차순 후 뒤집기
```

**기준이 여러 개일 때 (1순위 → 2순위 → 3순위)**

```cpp
// 점수 내림차순 → 같으면 나이 오름차순 → 같으면 이름 오름차순
sort(st.begin(), st.end(), [](const Student &a, const Student &b) {
    if (a.score != b.score) return a.score > b.score;   // 1순위가 다르면 1순위로 결정
    if (a.age != b.age)     return a.age < b.age;       // 2순위
    return a.name < b.name;                             // 마지막 기준
});

// 같은 기준을 tuple로 한 줄에 (<tuple>): 내림차순인 숫자는 부호를 뒤집음
sort(st.begin(), st.end(), [](const Student &a, const Student &b) {
    return make_tuple(-a.score, a.age, a.name) < make_tuple(-b.score, b.age, b.name);
});
```

- 패턴: **"다르면 그 기준으로 return, 같으면 다음 기준으로"**.
- 부호 뒤집기(`-a.score`)는 숫자에만 가능. 문자열 내림차순이 섞이면 `if` 방식 사용.
- 기준에 없는 값끼리 같으면 순서는 **정해지지 않음** → 입력 순서를 유지해야 하면 `stable_sort`.

**자주 쓰는 정렬 기준 패턴**

```cpp
// 계산한 값 기준 (절댓값 등)
sort(q.begin(), q.end(), [](int a, int b) { return abs(a) < abs(b); });

// 다른 배열의 값 기준 → [&]로 바깥 변수 캡처
sort(idx.begin(), idx.end(), [&](int a, int b) { return score[a] > score[b]; });

// 정해진 우선순위 순서 (gold → silver → bronze)
map<string, int> rank = {{"gold", 0}, {"silver", 1}, {"bronze", 2}};
sort(medals.begin(), medals.end(), [&](const string &a, const string &b) { return rank[a] < rank[b]; });

// 2차원 vector의 특정 열 기준
sort(m.begin(), m.end(), [](const vector<int> &a, const vector<int> &b) { return a[1] < b[1]; });

// 이어 붙였을 때 더 큰 쪽이 앞 (프로그래머스 "가장 큰 수")
sort(s.begin(), s.end(), [](const string &a, const string &b) { return a + b > b + a; });
// {"3","30","34","5","9"} → 9 5 34 3 30
```

**함정**

```cpp
vector<string> ns = {"10", "9", "2"};
sort(ns.begin(), ns.end());          // "10" "2" "9"  ← 문자열은 사전순! 숫자 크기순 아님
sort(ns.begin(), ns.end(), [](const string &a, const string &b) { return stoi(a) < stoi(b); });   // 2 9 10
```

**`next_permutation`과 함께 쓸 때: 반드시 먼저 오름차순 정렬**

```cpp
vector<vector<int>> d = {{80, 20}, {50, 40}, {30, 10}};

do { /* ... */ } while (next_permutation(d.begin(), d.end()));   // 정렬 안 함 → 1가지만 시도!
sort(d.begin(), d.end());
do { /* ... */ } while (next_permutation(d.begin(), d.end()));   // 정렬 후 → 6가지 모두
```

- `next_permutation`은 "사전순으로 다음 순열"로 바꾸고, 마지막 순열(내림차순 상태)이면 `false`를 반환. 그래서 시작이 오름차순이어야 모든 순열을 돎.
- 위 예시는 이미 내림차순이라 정렬 없이 돌리면 **첫 순서 하나만 보고 끝남** (에러 없이 오답).
- 원본 순서를 건드리기 싫으면 인덱스 배열 `{0, 1, 2, ...}`을 만들어 그걸 `next_permutation`으로 돌림 (인덱스는 처음부터 오름차순이라 정렬 불필요).
- 같은 원소가 있으면 중복 순열은 건너뜀 (`{{1,1},{1,1},{2,2}}` → 3가지). 완전히 같은 원소라면 결과에 영향 없음.

### Q19. 피로도를 DFS(백트래킹)로 푸는 방법

**아이디어**: "다음에 어느 던전에 들어갈까?"를 한 단계로 보고, 들어갈 수 있는 던전을 하나씩 골라 **더 깊이 들어갔다가(재귀) 돌아와서(원상복구) 다른 던전을 고름**.

```
피로도 80에서 시작
├─ A(80,20) 선택 → 60
│   ├─ B(50,40) 선택 → 20
│   │   └─ C(30,10): 20 < 30 → 못 들어감 → 2개로 끝
│   └─ C(30,10) 선택 → 50
│       └─ B(50,40) 선택 → 10 → 3개 ★
├─ B(50,40) 선택 → 40
│   └─ ...
└─ C(30,10) 선택 → 70
    └─ ...
```

```cpp
int answer = 0;
vector<bool> visited;

// fatigue: 현재 피로도, count: 지금까지 탐험한 던전 수
void dfs(int fatigue, int count, const vector<vector<int>> &dungeons) {
    answer = max(answer, count);                 // 지금 멈추는 경우도 답 후보

    for (int i = 0; i < (int)dungeons.size(); i++) {
        int need = dungeons[i][0];
        int cost = dungeons[i][1];
        if (visited[i] || fatigue < need) continue;   // 이미 갔거나 못 들어가면 건너뜀

        visited[i] = true;                        // 1) 선택
        dfs(fatigue - cost, count + 1, dungeons); // 2) 다음 단계로
        visited[i] = false;                       // 3) 원상복구
    }
}

int solution(int k, vector<vector<int>> dungeons) {
    answer = 0;                                   // 전역 변수는 매번 초기화!
    visited.assign(dungeons.size(), false);
    dfs(k, 0, dungeons);
    return answer;
}
```

**백트래킹 3단계 (치트시트 4장 백트래킹 템플릿과 같은 틀)**

1. **선택**: `visited[i] = true`
2. **다음 단계로**: `dfs(fatigue - cost, count + 1, ...)`. 바뀐 상태(피로도, 개수)는 **인자로 넘김** → 돌아오면 자동으로 원래 값
3. **원상복구**: `visited[i] = false` → 다른 던전을 고르는 경우를 위해 되돌림

- `answer = max(answer, count)`를 **함수 맨 앞**에서 함 → "여기서 멈추는 경우"도 모두 답 후보가 됨.
- 전역 변수(`answer`, `visited`)는 `solution` 안에서 **매번 초기화**. 채점 시 `solution`이 여러 번 호출될 수 있음.

**`next_permutation` 풀이와 비교**

| | `next_permutation` | DFS (백트래킹) |
|---|---|---|
| 방식 | 모든 순서(8! = 40,320가지)를 만든 뒤 순서대로 시뮬레이션 | 들어갈 수 있는 던전만 골라 가며 탐색 |
| 못 들어가는 던전 | 순열 안에서 건너뜀 | 그 가지는 **아예 탐색 안 함** (가지치기) |
| 속도 | 항상 모든 순열을 돎 | 막히는 가지가 많을수록 빠름 |
| 코드 | 짧고 실수할 곳이 적음 | 틀이 조금 길지만 다른 문제에 그대로 응용 가능 |
| 주의 | 시작 전 **오름차순 정렬 필수** (Q18) | **원상복구 빠뜨리지 않기** |

- 입력이 작으면(n ≤ 8~10) 둘 다 OK. 조건에 따라 가지를 많이 자를 수 있는 문제(N-Queen, 조합 합 등)는 DFS가 유리.

### Q20. `erase`, `unique`, `iota` 정리 (+ `remove`)

**`erase`: 원소 지우기 (컨테이너의 멤버 함수)**

```cpp
vector<int> v = {10, 20, 30, 40, 50};
v.erase(v.begin() + 1);              // 인덱스 1 삭제       → 10 30 40 50
v.erase(v.begin(), v.begin() + 2);   // [0, 2) 구간 삭제     → 40 50
v.erase(v.end() - 1);                // 마지막 삭제 (= pop_back())

string s = "hello world";
s.erase(5);                          // 5번부터 끝까지 삭제 → "hello"
s.erase(0, 6);                       // (시작, 개수)        → "world"
s.erase(s.begin() + 1);              // 반복자 위치 한 글자  → "hllo"

set<int> st;       st.erase(2);      // 값으로 삭제
map<string, int> m; m.erase("a");    // 키로 삭제
```

- vector / string은 **위치(반복자)** 로 지움. 값으로 지우려면 아래 `remove`와 함께.
- string의 `erase(pos, len)`은 **인덱스 + 개수** (반복자 아님) → 헷갈리기 쉬움.
- vector 중간 삭제는 뒤 원소를 전부 당기므로 **O(n)**. 반복문 안에서 많이 지우면 느림.

```cpp
// 반복문 안에서 지울 때: erase가 돌려주는 "다음 위치"를 받아야 함
for (auto it = v.begin(); it != v.end(); ) {
    if (*it % 2 == 0) it = v.erase(it);   // 지우면 it를 새 위치로
    else ++it;                            // 안 지울 때만 ++
}
```

**`unique`: 연속된 중복 제거 (`<algorithm>`)**

```cpp
vector<int> u = {3, 1, 3, 2, 1, 3};
sort(u.begin(), u.end());                  // 1 1 2 3 3 3   ← 정렬 먼저!
auto newEnd = unique(u.begin(), u.end());  // 앞쪽을 1 2 3으로 만들고, 새 끝 위치를 반환
                                           // u = 1 2 3 ? ? ?  (뒤쪽 값은 보장 안 됨, 크기는 그대로 6)
u.erase(newEnd, u.end());                  // 뒤쪽 잘라내기   → 1 2 3

// 보통 한 줄로 씀 (정렬 + 중복 제거)
sort(v.begin(), v.end());
v.erase(unique(v.begin(), v.end()), v.end());
```

- `unique`는 **실제로 지우지 않음**. 중복 아닌 값을 앞으로 모으고 "새 끝"만 알려줌 → 반드시 `erase`와 같이.
- **붙어 있는 중복만** 없앰: 정렬 안 하면 `{5, 5, 1, 1, 5}` → `5 1 5`.
- 문자열도 가능: `"aaabbbcca"` → `"abca"` (연속 글자 압축).
- 순서가 필요 없으면 `set`에 넣는 것도 방법: `set<int>(v.begin(), v.end())`.

**`remove` / `remove_if`: 값·조건으로 지우기 (erase-remove 관용구)**

```cpp
vector<int> r = {1, 2, 3, 2, 4};
r.erase(remove(r.begin(), r.end(), 2), r.end());                        // 값 2 모두 삭제 → 1 3 4
r.erase(remove_if(r.begin(), r.end(), [](int x) { return x % 2 == 0; }), r.end());   // 짝수 삭제

string sp = "a b c";
sp.erase(remove(sp.begin(), sp.end(), ' '), sp.end());                  // 공백 제거 → "abc"
```

- `unique`와 같은 원리: `remove`도 **남길 값을 앞으로 모으고 새 끝을 반환**할 뿐 → `erase`로 잘라냄.
- C++20부터는 `erase(v, 2);`, `erase_if(v, 조건);` 한 줄로 가능 (채점 사이트가 C++17이면 사용 불가).

**`iota`: 연속된 값으로 채우기 (`<numeric>`)**

```cpp
vector<int> a(5);
iota(a.begin(), a.end(), 0);         // 0 1 2 3 4
iota(a.begin(), a.end(), 1);         // 1 2 3 4 5
int arr[4]; iota(arr, arr + 4, 10);  // 10 11 12 13
string al(5, ' '); iota(al.begin(), al.end(), 'a');   // "abcde"
```

- 이름 뜻: 그리스 문자 ι (APL 언어에서 "0부터 n까지 수열"을 만드는 기호에서 유래). **i-o-t-a** 철자 주의 (itoa 아님).
- 크기를 먼저 정해야 함: `vector<int> a(5);` 후 `iota` (빈 vector에 쓰면 아무것도 안 들어감).

```cpp
// 활용 1: 유니온 파인드 부모 배열 초기화 (자기 자신이 부모)
vector<int> parent(n + 1);
iota(parent.begin(), parent.end(), 0);

// 활용 2: 원본은 두고 인덱스만 정렬 (등수 매기기)
vector<int> idx(score.size());
iota(idx.begin(), idx.end(), 0);
sort(idx.begin(), idx.end(), [&](int x, int y) { return score[x] > score[y]; });

// 활용 3: 순서 번호 배열로 순열 돌리기 (정렬 필요 없음)
vector<int> order(n);
iota(order.begin(), order.end(), 0);
do { /* order 순서대로 처리 */ } while (next_permutation(order.begin(), order.end()));
```

| 함수 | 헤더 | 실제로 지우나? | 한 줄 요약 |
|---|---|---|---|
| `v.erase(it)` | 멤버 함수 | O | 위치로 삭제 |
| `unique(b, e)` | `<algorithm>` | X (새 끝 반환) | 정렬 후 `erase`와 함께 → 중복 제거 |
| `remove(b, e, x)` | `<algorithm>` | X (새 끝 반환) | `erase`와 함께 → 값 삭제 |
| `iota(b, e, start)` | `<numeric>` | - | start, start+1, … 로 채움 |

### Q21. `set`에 있는 값을 조회하는 방법

`set`은 **인덱스(`s[0]`)로 접근할 수 없음** (컴파일 에러). 순회 · 검색 · 범위 탐색으로 조회함.

**전체 순회 (자동으로 오름차순)**

```cpp
set<int> s = {11, 7, 101, 2, 7};     // 중복 7은 하나만 → {2, 7, 11, 101}

for (int x : s) cout << x << ' ';                                   // 2 7 11 101
for (auto it = s.begin(); it != s.end(); ++it) cout << *it << ' ';  // 반복자 (값은 *it)
for (auto it = s.rbegin(); it != s.rend(); ++it) cout << *it << ' ';// 역순: 101 11 7 2

// 소수 찾기처럼 "모은 값을 하나씩 검사"
int cnt = 0;
for (int x : s) if (isPrime(x)) cnt++;
```

**값이 있는지 확인**

```cpp
s.count(7);                          // 있으면 1, 없으면 0
if (s.count(7)) { }

auto it = s.find(11);                // 있으면 그 위치, 없으면 s.end()
if (it != s.end()) cout << *it;

s.contains(7);                       // C++20 전용 (프로그래머스 OK, C++17 이하 사이트에서는 count 사용)
```

**최솟값 / 최댓값 / 개수**

```cpp
*s.begin();       // 최솟값 2
*s.rbegin();      // 최댓값 101
s.size();         // 원소 개수 4
s.empty();        // 비었는지 (비어 있으면 *s.begin()은 오류!)
```

**범위 탐색 (정렬돼 있어서 가능, O(log n))**

```cpp
*s.lower_bound(8);    // 8 이상인 첫 값 → 11
*s.upper_bound(11);   // 11 초과인 첫 값 → 101
if (s.lower_bound(200) == s.end()) { }   // 조건 맞는 값이 없으면 end() → 먼저 확인!
```

**k번째 값이 필요할 때**

```cpp
*next(s.begin(), 2);                  // 앞에서 3번째 → 11  (O(k), <iterator>)
vector<int> v(s.begin(), s.end());    // 여러 번 인덱스 접근할 거면 vector로 복사
v[2];                                 // 11
```

**삽입 결과 확인 / 순회하며 삭제**

```cpp
auto [pos, inserted] = s.insert(7);   // 이미 있으면 inserted == false (C++17)

for (auto it = s.begin(); it != s.end(); ) {
    if (*it % 2 == 0) it = s.erase(it);   // erase가 다음 위치를 돌려줌
    else ++it;
}
```

| 하고 싶은 것 | 방법 | 시간 |
|---|---|---|
| 전부 보기 | `for (int x : s)` | O(n) |
| 있는지 확인 | `s.count(x)` / `s.find(x) != s.end()` | O(log n) |
| 최소 / 최대 | `*s.begin()` / `*s.rbegin()` | O(1) |
| x 이상인 첫 값 | `s.lower_bound(x)` | O(log n) |
| k번째 값 | `*next(s.begin(), k)` 또는 vector로 복사 | O(k) |

- `unordered_set`도 `count`, `find`, 순회는 같지만 **순서가 없어서** `begin()`이 최솟값이 아니고 `lower_bound`도 없음.
- 같은 값을 여러 개 저장하려면 `multiset` (`count`가 개수를 돌려줌).

### Q22. `set`은 기본으로 정렬되나?

**네. `set`은 넣는 순서와 상관없이 항상 오름차순으로 정렬된 상태를 유지함.** (내부가 레드-블랙 트리)

```cpp
set<int> s;
for (int x : {50, 10, 40, 20, 30}) s.insert(x);
for (int x : s) cout << x << ' ';    // 10 20 30 40 50

set<string> w = {"banana", "Apple", "cherry"};     // 사전순: Apple banana cherry (대문자가 앞)
set<pair<int, int>> pr = {{2, 1}, {1, 9}, {1, 3}}; // first → second 순: (1,3) (1,9) (2,1)
```

- 기준은 `<` 연산 (= `less<T>`). `pair`, `string`, `vector`는 앞에서부터 비교하는 사전순.
- 새 값을 넣을 때마다 제자리에 들어가므로 **`sort`를 할 필요도, 할 수도 없음** (`sort(s.begin(), s.end())`는 컴파일 에러).
- 원소 값을 직접 바꿀 수 없음 (`*it = 5` 불가) → 지우고 다시 넣기.

**정렬 기준 바꾸기**

```cpp
set<int, greater<int>> d = {50, 10, 40};           // 내림차순: 50 40 10

struct ByLenThenAlpha {                             // 길이순, 같으면 사전순
    bool operator()(const string &a, const string &b) const {
        if (a.size() != b.size()) return a.size() < b.size();
        return a < b;
    }
};
set<string, ByLenThenAlpha> bs = {"aa", "bb", "c", "ddd"};   // c aa bb ddd

auto cmp = [](int a, int b) { return a % 10 < b % 10 || (a % 10 == b % 10 && a < b); };
set<int, decltype(cmp)> lc(cmp);                   // 람다는 decltype + 생성자에 전달
```

**함정: 비교 기준에서 "같다"고 판단되면 중복으로 보고 버림**

```cpp
struct ByLen {
    bool operator()(const string &a, const string &b) const { return a.size() < b.size(); }
};
set<string, ByLen> bl = {"aa", "bb", "c", "ddd"};  // c aa ddd  ← "bb"가 사라짐!
```

- `set`은 `comp(a, b)`도 `comp(b, a)`도 거짓이면 **같은 값**으로 취급. 길이만 비교하면 길이가 같은 문자열은 하나만 남음.
- 기준을 바꿀 때는 **마지막에 값 자체 비교(`a < b`)를 붙여서** 서로 다른 값이 같다고 판단되지 않게 할 것.

| 컨테이너 | 정렬 | 중복 |
|---|---|---|
| `set` | O (오름차순, 기준 변경 가능) | X |
| `multiset` | O | O |
| `unordered_set` | **X** (순서 예측 불가) | X |
| `map` | O (키 기준) | 키 중복 X |

### Q23. DFS로 순열(카드 조합) 만들 때 흔한 실수 4가지 (소수 찾기)

```cpp
set<int> numset;

void dfs(string numbers, vector<bool> &visited, int index, string nownum) {
    for (int i = index; i < numbers.size(); i++) {      // ❌ 2
        if (!visited[i]) {
            nownum += numbers[i];                        // ❌ 3
            numset.insert(stoi(nownum));
            visited[i] = true;
            dfs(numbers, visited, i + 1, nownum);
            visited[i] = false;
        }
    }
}
int solution(string numbers) {
    vector<bool> visited(numbers.size(), false);         // ❌ 1 (numset 초기화 없음)
    dfs(numbers, visited, 0, "");
    ...
    for (int i = 2; i * i < num; i++)                    // ❌ 4
```

**❌ 1. 전역 컨테이너를 `solution`에서 초기화하지 않음**

- `solution`이 여러 번 호출되면(로컬 테스트, 채점 서버) 이전 입력에서 만든 수가 **계속 쌓임**.
- `"0"`을 넣었는데 이전 테스트의 소수가 남아 답이 2가 됨.
- → `solution` 첫 줄에 `numset.clear();`. 전역 변수는 **항상 solution에서 초기화**.

**❌ 2. `i = index`부터 시작 → 순열이 아니라 "앞에서 뒤로 고르는 조합"이 됨**

- `dfs(..., i + 1, ...)`로 넘기면 **뒤쪽 카드만** 고를 수 있어서 `"17"`에서 71을 못 만듦.
- 순서를 바꿔 쓰는 **순열**은 `visited`로 중복 사용만 막고 **항상 0부터** 돌아야 함.

| 만들고 싶은 것 | 반복 시작 | 중복 방지 |
|---|---|---|
| 순열 (순서 다르면 다른 것: 17 ≠ 71) | `i = 0` | `visited` |
| 조합 (순서 상관없음: {1,7} = {7,1}) | `i = start` + `dfs(i + 1)` | 시작 위치로 자동 방지 |

**❌ 3. 반복문 안에서 `nownum`을 직접 수정 → 원상복구가 안 됨**

- `i = 0`에서 `nownum = "1"`로 바뀐 채로 `i = 1`로 넘어가면 `"1" + "7" = "17"`이 되어, 한 자리 수 7을 못 만듦.
- 2번만 고치면 문자열이 끝없이 길어져 **`stoi: out of range`로 프로그램이 멈춤** (21억 넘는 수).
- → 바꾼 값을 **새 변수로 만들어 인자로 넘김**. 인자로 넘긴 값은 돌아오면 원래대로라 원상복구가 필요 없음.

```cpp
string next = nownum + numbers[i];     // nownum 자체는 그대로
numset.insert(stoi(next));
dfs(numbers, visited, next);
```

- `visited`처럼 **참조(&)로 공유하는 것만** `true` → 재귀 → `false`로 직접 원상복구.

**❌ 4. 소수 판별 범위 `i * i < num` → 제곱수를 소수로 셈**

- 4, 9, 25, 49는 약수가 딱 √n 하나뿐인데, `<`면 그 값을 검사하지 않아 소수로 판정.
- → `i * i <= num`.

**고친 DFS**

```cpp
set<int> numset;

void dfs(const string &numbers, vector<bool> &visited, const string &nownum) {
    for (int i = 0; i < (int)numbers.size(); i++) {
        if (visited[i]) continue;
        string next = nownum + numbers[i];
        numset.insert(stoi(next));
        visited[i] = true;
        dfs(numbers, visited, next);
        visited[i] = false;
    }
}

int solution(string numbers) {
    numset.clear();
    vector<bool> visited(numbers.size(), false);
    dfs(numbers, visited, "");
    int count = 0;
    for (int num : numset) if (isPrime(num)) count++;   // isPrime: i * i <= n
    return count;
}
```

- `numbers`는 바뀌지 않으므로 `const string &`로 넘겨 매 호출 복사를 피함.

### Q24. Python `itertools.product`를 C++로 구현하려면? (모음사전)

C++ 표준에는 `product`가 없음 → **N진수 세기**나 **DFS**로 직접 만듦.

**Python 원본**

```python
import itertools
def solution(word):
    words = []
    for i in range(0, 5):
        words.extend(''.join(p) for p in itertools.product("AEIOU", repeat=i+1))
    words.sort()
    return words.index(word) + 1
```

**C++: 5진수 세기로 product 만들기**

```cpp
// itertools.product("AEIOU", repeat=len)과 같은 역할:
// 길이 len짜리 모든 조합을 만든다 (각 자리는 5진수 한 자리처럼 0~4)
vector<string> product(const string &letters, int len) {
    vector<string> result;
    int base = letters.size();
    int total = 1;
    for (int i = 0; i < len; i++) total *= base;      // 5^len 개

    for (int num = 0; num < total; num++) {
        string s(len, ' ');
        int x = num;
        for (int pos = len - 1; pos >= 0; pos--) {     // num을 5진수로 바꿔 각 자리 글자 결정
            s[pos] = letters[x % base];
            x /= base;
        }
        result.push_back(s);
    }
    return result;
}

int solution(string word) {
    vector<string> words;
    for (int len = 1; len <= 5; len++) {
        vector<string> part = product("AEIOU", len);
        words.insert(words.end(), part.begin(), part.end());   // words.extend(...)
    }
    sort(words.begin(), words.end());                            // words.sort()
    return find(words.begin(), words.end(), word) - words.begin() + 1;   // words.index(word) + 1
}
```

- 아이디어: 길이 3이면 `000`, `001`, …, `444`(5진수)를 세고, 각 자리 숫자를 `AEIOU`의 글자로 바꿈.
- `#include <algorithm>` 필요 (`sort`, `find`).

**Python ↔ C++ 대응표**

| Python | C++ |
|---|---|
| `itertools.product(s, repeat=n)` | 직접 구현 (N진수 세기 또는 DFS) |
| `itertools.permutations(s)` | `sort` 후 `next_permutation` (Q18) |
| `itertools.combinations(s, r)` | 0/1 마스크 + `next_permutation` (3장 "순열 / 조합") |
| `words.extend(part)` | `words.insert(words.end(), part.begin(), part.end())` |
| `words.sort()` | `sort(words.begin(), words.end())` |
| `words.index(x)` | `find(words.begin(), words.end(), x) - words.begin()` (Q9) |
| `''.join(p)` | `string`에 `+=`로 이어 붙이기 |
| `x in words` | `find(...) != words.end()` 또는 `set`의 `count` |

**DFS로 product 만들기 (자리 수가 가변이거나 조건을 넣을 때)**

```cpp
void dfs(const string &letters, const string &cur, int len, vector<string> &out) {
    if ((int)cur.size() == len) { out.push_back(cur); return; }
    for (char c : letters) dfs(letters, cur + c, len, out);   // visited 없음 = 중복 허용
}
```

- 순열(Q23)과 차이: **`visited`가 없음** → 같은 글자를 여러 번 쓸 수 있음.

### Q25. 타겟 넘버를 비트마스크 / `next_permutation`으로 푸는 방법

숫자마다 +/- 두 가지 → 전체 2ⁿ가지를 **나열하는 방법만 다르고 결과는 같음**.

**1) DFS (기본)**

```cpp
int cnt;
void dfs(const vector<int> &numbers, int target, int index, int sum) {
    if (index == (int)numbers.size()) {          // 모든 숫자를 다 쓴 뒤에만 비교
        if (sum == target) cnt++;
        return;
    }
    dfs(numbers, target, index + 1, sum + numbers[index]);
    dfs(numbers, target, index + 1, sum - numbers[index]);
}
```

**2) 비트마스크: 0 ~ 2ⁿ - 1을 세면서 각 비트를 +/-로 해석**

```cpp
// 비트마스크: mask의 i번째 비트가 1이면 numbers[i]를 더하고, 0이면 뺀다
int solution(vector<int> numbers, int target) {
    int n = numbers.size();
    int count = 0;
    for (int mask = 0; mask < (1 << n); mask++) {      // 000..0 ~ 111..1 (2^n가지)
        int sum = 0;
        for (int i = 0; i < n; i++) {
            if (mask & (1 << i)) sum += numbers[i];      // i번째 비트가 1 → +
            else sum -= numbers[i];                      // i번째 비트가 0 → -
        }
        if (sum == target) count++;
    }
    return count;
}
```

```
n = 3일 때
mask = 0 (000) → - - -
mask = 5 (101) → + - +    ← 0번, 2번 비트가 1
mask = 7 (111) → + + +
```

| 비트 연산 | 의미 |
|---|---|
| `1 << n` | 2ⁿ (n ≤ 30까지 `int`, 그 이상은 `1LL << n`) |
| `mask & (1 << i)` | i번째 비트가 1인지 확인 |
| `mask \| (1 << i)` | i번째 비트를 1로 |
| `mask & ~(1 << i)` | i번째 비트를 0으로 |
| `__builtin_popcount(mask)` | 1인 비트 개수 (GCC/Clang) |

- "각 원소마다 두 가지 선택" 문제(부분집합, 켜기/끄기)에 그대로 쓸 수 있음. 재귀 없이 반복문 두 개.

**3) `next_permutation`: "- 를 붙일 숫자 k개"를 고르는 조합을 k = 0 ~ n까지**

```cpp
// next_permutation: "-를 붙일 숫자 k개"를 고르는 모든 조합을 k = 0 ~ n까지 돌린다
int solution(vector<int> numbers, int target) {
    int n = numbers.size();
    int count = 0;
    for (int k = 0; k <= n; k++) {
        vector<int> sign(n, 0);                          // 0 = +, 1 = -
        fill(sign.end() - k, sign.end(), 1);             // 0..0 1..1 (오름차순으로 시작)
        do {
            int sum = 0;
            for (int i = 0; i < n; i++)
                sum += sign[i] ? -numbers[i] : numbers[i];
            if (sum == target) count++;
        } while (next_permutation(sign.begin(), sign.end()));
    }
    return count;
}
```

- `{0, 0, 1, 1}`처럼 0과 1이 섞인 배열을 `next_permutation`으로 돌리면 **"1의 위치"를 고르는 모든 조합**이 나옴 (3장 "순열 / 조합"과 같은 원리).
- k마다 nCk가지 → 모두 더하면 2ⁿ가지. 비트마스크보다 길어서 이 문제에선 굳이 쓸 필요 없지만, **"정확히 k개를 고르는" 문제**에서 유용.
- 시작 배열은 반드시 오름차순(0들 다음 1들) → `fill(sign.end() - k, sign.end(), 1)`.

| 방법 | 장점 | 언제 |
|---|---|---|
| DFS | 중간에 가지치기 가능, 다른 문제로 응용 쉬움 | 기본 선택 |
| 비트마스크 | 짧고 재귀 없음 | n ≤ 20 정도, 원소마다 2가지 선택 |
| `next_permutation` (0/1 배열) | 고르는 개수 k를 정할 수 있음 | "정확히 k개 선택" |

### Q26. BFS가 효율성 테스트에서 시간 초과 나는 이유와 고치는 법 (게임 맵 최단거리)

**정답은 나오는데 느린 BFS**

```cpp
vector<vector<int>> distance(x, vector<int>(y, 1e9));   // ③ 1e9로 "안 간 칸" 표시
distance[0][0] = 1;
vector<vector<int>> visit_list;                          // ① vector를 큐처럼 사용
visit_list.push_back({0, 0});                            // ② 좌표를 vector<int>로

while (!visit_list.empty()) {
    int nowx = visit_list.front()[0];
    int nowy = visit_list.front()[1];
    visit_list.erase(visit_list.begin());                // ① 맨 앞 삭제 = 뒤를 전부 당김
    for (int i = 0; i < 4; i++) {
        ...
        if (범위 안 && maps[nx][ny] == 1 && distance[nx][ny] > x * y) {
            visit_list.push_back({nx, ny});
            distance[nx][ny] = min(distance[nx][ny], distance[nowx][nowy] + 1);   // ④ min 불필요
        }
    }
}
```

**① `vector`의 맨 앞을 `erase` → 꺼낼 때마다 O(n)**

- `erase(begin())`은 나머지 원소를 전부 한 칸씩 앞으로 옮김 → BFS 전체가 O(칸 수 × 큐 길이).
- **맨 앞에서 꺼내고 맨 뒤에 넣는 구조 = `queue`** (꺼내기·넣기 모두 O(1)). 양쪽에서 넣고 빼야 하면 `deque`.

**② 좌표를 `vector<int>`로 담음 → 원소마다 메모리 할당**

- `{nx, ny}`를 넣을 때마다 작은 vector를 새로 만듦 (힙 할당). 좌표는 **`pair<int, int>`** 로.

로컬 측정 (전부 길인 N×N 맵, `-O2`):

| 맵 크기 | `vector<vector<int>>` + erase | `vector<pair>` + erase | `queue<pair>` |
|---|---|---|---|
| 100×100 | 1.8 ms | 0.4 ms | **0.2 ms** |
| 300×300 | 25 ms | 7 ms | **0.7 ms** |
| 1000×1000 | 402 ms | 62 ms | **6.6 ms** |

- 전부 길인 맵은 큐가 짧게 유지되는 편이라 이 정도. 큐가 길어지는 맵에서는 차이가 더 커짐.

**③ "안 간 칸"을 `1e9` + `> x * y`로 판단 → 0으로 단순하게**

- 거리를 **0으로 초기화**하고 `dist[nr][nc] == 0`이면 안 간 칸 (시작 칸은 1이라 겹치지 않음).
- 못 가면 도착 칸이 0으로 남음 → `-1` 반환.

**④ BFS에서는 `min` 불필요**

- BFS는 가까운 칸부터 처리 → **처음 도착한 순간이 최단 거리**. 비교 없이 `dist[r][c] + 1`을 바로 넣으면 됨.
- (칸마다 이동 비용이 다르면 이 성질이 깨짐 → 다익스트라 등 비교·갱신 필요)

**⑤ 그 밖에**

- `min`을 쓰면 `#include <algorithm>`, `queue`는 `#include <queue>`.
- 행 수·열 수를 `x`, `y`로 부르면 x = 가로처럼 읽혀 헷갈림 → `R`, `C` (또는 `rows`, `cols`).

**고친 BFS**

```cpp
#include <queue>

int solution(vector<vector<int>> maps) {
    int R = maps.size(), C = maps[0].size();
    int dr[] = {1, -1, 0, 0};
    int dc[] = {0, 0, 1, -1};

    vector<vector<int>> dist(R, vector<int>(C, 0));     // 0 = 아직 안 감
    queue<pair<int, int>> q;
    dist[0][0] = 1;                                     // 시작 칸도 1칸
    q.push({0, 0});

    while (!q.empty()) {
        auto [r, c] = q.front();
        q.pop();
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= R || nc < 0 || nc >= C) continue;   // 범위 밖
            if (maps[nr][nc] == 0 || dist[nr][nc] != 0) continue;   // 벽 또는 이미 방문
            dist[nr][nc] = dist[r][c] + 1;                          // 넣을 때 바로 기록
            q.push({nr, nc});
        }
    }
    return dist[R - 1][C - 1] ? dist[R - 1][C - 1] : -1;
}
```

| 체크리스트 | |
|---|---|
| 큐는 `queue`를 쓰나? (`vector` + `erase(begin())` 금지) | |
| 좌표는 `pair<int, int>`인가? | |
| 방문 표시는 **큐에 넣을 때** 하나? (꺼낼 때 하면 같은 칸이 여러 번 들어감) | |
| `dist`/`visited`를 `solution` 안에서 새로 만드나? | |

### Q27. `pair` 사용법 총정리

> `#include <utility>` (`<vector>`, `<map>` 등을 include하면 보통 같이 들어오지만 직접 쓰는 게 안전)

**만들기**

```cpp
pair<int, int> a = {1, 2};            // 중괄호 (가장 많이 씀)
pair<string, int> b("kim", 90);       // 생성자
auto c = make_pair(3, 'x');           // 타입 자동 추론 → pair<int, char>
pair<int, int> zero;                  // 기본값 {0, 0}

using pii = pair<int, int>;           // 자주 쓰면 별칭 (치트시트 1장 템플릿)
pii d{5, 6};
```

**값 꺼내기 / 바꾸기**

```cpp
a.first;   a.second;                  // 괄호 없음! (함수가 아니라 멤버 변수)
a.first = 10;
a.second += 5;

auto [x, y] = a;                      // 구조화 바인딩 (C++17): 복사본
auto &[rx, ry] = a;                   // 참조: rx를 바꾸면 a.first도 바뀜
rx = 99;

int p, q;
tie(p, q) = a;                        // 이미 있는 변수에 풀어 넣기 (<tuple>)
```

**비교와 정렬: first 먼저, 같으면 second**

```cpp
pii{1, 5} < pii{2, 0};                // true  (first가 작음)
pii{1, 5} < pii{1, 9};                // true  (first 같음 → second 비교)
pii{1, 5} == pii{1, 5};               // true

vector<pii> v = {{2, 1}, {1, 9}, {1, 3}};
sort(v.begin(), v.end());             // (1,3) (1,9) (2,1)
sort(v.begin(), v.end(), greater<>());// (2,1) (1,9) (1,3)
sort(v.begin(), v.end(), [](const pii &l, const pii &r) { return l.second < r.second; });   // second 기준
```

- 비교 연산이 이미 정의돼 있어서 `sort`, `set`, `map`의 키, `priority_queue`에 **그대로** 넣을 수 있음.

**컨테이너 안의 pair**

```cpp
vector<pii> v;
v.push_back({7, 7});
v.emplace_back(8, 8);                 // 중괄호 없이 바로 생성

queue<pii> q;                         // BFS 좌표 (Q26)
q.push({0, 0});
auto [r, c] = q.front();

priority_queue<pii, vector<pii>, greater<pii>> pq;   // (거리, 노드) 최소 힙 (다익스트라)
pq.push({5, 1});
pq.top().first;                       // 가장 작은 first

set<pii> visited;                     // 좌표 방문 기록
visited.insert({1, 2});
visited.count({1, 2});

map<pii, int> cost;                   // 좌표를 키로
cost[{1, 2}] = 7;
// unordered_map<pii, int>는 해시 함수가 없어서 컴파일 에러 → map 사용 (Q8)
```

**map의 원소도 pair**

```cpp
map<string, int> m = {{"a", 1}, {"b", 2}};
for (const auto &kv : m) cout << kv.first << kv.second;   // kv는 pair<const string, int>
for (auto &[key, val] : m) cout << key << val;            // 구조화 바인딩이 더 읽기 쉬움

auto [it, inserted] = m.insert({"a", 5});   // 반환값도 pair: (위치, 새로 넣었는지)
// inserted == false (이미 있음), it->second == 1 (기존 값 유지)
```

**함수에서 값 두 개 돌려주기**

```cpp
pair<int, int> minMax(const vector<int> &v) {
    return {*min_element(v.begin(), v.end()), *max_element(v.begin(), v.end())};
}
auto [lo, hi] = minMax({4, 1, 9});    // lo = 1, hi = 9
```

**세 개 이상이면**

```cpp
pair<int, pair<int, int>> nested = {1, {2, 3}};
nested.second.first;                  // 2  ← 읽기 어려움

tuple<int, int, int> t = {1, 2, 3};   // <tuple>
auto [t1, t2, t3] = t;                // 구조화 바인딩
get<2>(t);                            // 3 (인덱스로 꺼내기)
// 의미가 중요하면 struct가 가장 읽기 쉬움 (struct Point { int r, c; };)
```

| 상황 | 추천 |
|---|---|
| 좌표 (행, 열) | `pair<int, int>` + `auto [r, c]` |
| (거리, 노드) 우선순위 큐 | `pair<int, int>` + `greater<>` |
| 값 3개 | `tuple` 또는 `struct` |
| 멤버 이름이 중요할 때 | `struct` (`.first`보다 `.age`가 명확) |

### Q28. `push`와 `emplace`의 차이 (`queue`, `vector` 등)

**한 줄 요약**: `push`는 **완성된 객체**를 받아 넣고, `emplace`는 **생성자 재료**를 받아 컨테이너 안에서 **바로 만듦**.

```cpp
queue<pair<int, int>> q;
q.push({1, 2});              // pair를 만든 뒤 넣음
q.push(make_pair(3, 4));     // 위와 같음
q.emplace(5, 6);             // pair(5, 6)을 큐 안에서 바로 생성 (중괄호 없음)
// q.emplace({7, 8});        // 컴파일 에러! emplace는 중괄호 묶음을 못 받음
```

**실제 동작 차이 (생성/복사/이동 횟수를 출력해 본 결과)**

```
push(Noisy(1))  →  생성(1), 이동     // 바깥에서 만든 뒤 큐 안으로 옮김
push(2)         →  생성(2), 이동     // 임시 객체를 만든 뒤 옮김
emplace(3)      →  생성(3)           // 큐 안에서 한 번에 생성
```

- 차이는 **임시 객체 하나를 만들고 옮기는 비용**뿐.
- `pair<int, int>`, `int` 같은 작은 값은 옮기는 비용이 거의 0 → **코테에서는 성능 차이 없음**. 편한 쪽을 쓰면 됨.
- 크고 복사 비용이 큰 객체를 아주 많이 넣을 때만 의미 있는 차이.

**컨테이너별 이름**

| 컨테이너 | 넣기 | 바로 생성 |
|---|---|---|
| `queue`, `stack`, `priority_queue` | `push` | `emplace` |
| `vector`, `deque` | `push_back` / `push_front` | `emplace_back` / `emplace_front` |
| `set`, `map` | `insert` | `emplace` |

**함정: `emplace`는 생성자를 호출하므로 의미가 달라질 수 있음**

```cpp
vector<vector<int>> v;
v.push_back({3});        // 원소 하나짜리 vector → {3}
v.emplace_back(3);       // vector<int>(3) 생성자 → 크기 3짜리 {0, 0, 0} !

queue<string> sq;
sq.emplace(3, 'z');      // string(3, 'z') → "zzz"
```

- `emplace(인자들)` = `T(인자들)` 생성자 호출. 원소 타입의 생성자를 떠올려서 의도와 같은지 확인할 것.
- 헷갈리면 **`push({...})`가 가장 안전** (보이는 그대로 들어감).

### Q29. flood fill(무인도 여행)을 DFS로 푸는 방법: 재귀 vs stack

"연결된 칸을 모두 방문"만 하면 되므로 **BFS / DFS 어느 쪽이든 정답** (최단 거리가 아니라서 순서가 상관없음).

**1) 재귀 DFS: 가장 짧음**

```cpp
int R, C;
int dr[] = {0, 0, 1, -1};
int dc[] = {1, -1, 0, 0};
vector<vector<bool>> visited;

// (r, c)에서 시작해 연결된 육지를 모두 방문하고, 그 식량 합을 돌려준다
int dfs(const vector<string> &maps, int r, int c) {
    visited[r][c] = true;
    int sum = maps[r][c] - '0';
    for (int d = 0; d < 4; d++) {
        int nr = r + dr[d], nc = c + dc[d];
        if (nr < 0 || nr >= R || nc < 0 || nc >= C) continue;      // 범위 밖
        if (maps[nr][nc] == 'X' || visited[nr][nc]) continue;      // 바다 또는 방문함
        sum += dfs(maps, nr, nc);                                   // 이웃 섬 조각의 합을 더함
    }
    return sum;
}

vector<int> solution(vector<string> maps) {
    R = maps.size();
    C = maps[0].size();
    visited.assign(R, vector<bool>(C, false));                       // 전역은 매번 초기화

    vector<int> answer;
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++)
            if (maps[r][c] != 'X' && !visited[r][c])
                answer.push_back(dfs(maps, r, c));                  // 새 섬 발견

    sort(answer.begin(), answer.end());
    if (answer.empty()) answer = {-1};
    return answer;
}
```

- `dfs`가 **섬 조각의 합을 반환**하도록 만들면 `sum += dfs(...)` 한 줄로 합이 모임.
- 방문 표시는 **함수에 들어오자마자**. 재귀 호출 전에 확인(`visited[nr][nc]`)하므로 같은 칸을 두 번 부르지 않음.
- 백트래킹(Q19, Q23)과 달리 **원상복구(`visited = false`) 없음**: 한 번 칠한 칸은 다시 볼 필요가 없음.

**2) stack DFS: BFS 코드에서 두 군데만 바꿈**

```cpp
// 재귀 대신 stack으로 하는 DFS: BFS 코드에서 queue → stack, front() → top()만 바꾼 것
vector<int> solution(vector<string> maps) {
    int R = maps.size(), C = maps[0].size();
    int dr[] = {0, 0, 1, -1};
    int dc[] = {1, -1, 0, 0};
    vector<vector<bool>> visited(R, vector<bool>(C, false));

    vector<int> answer;
    for (int i = 0; i < R; i++) {
        for (int j = 0; j < C; j++) {
            if (maps[i][j] == 'X' || visited[i][j]) continue;

            stack<pair<int, int>> st;
            st.push({i, j});
            visited[i][j] = true;
            int sum = 0;
            while (!st.empty()) {
                auto [r, c] = st.top();
                st.pop();
                sum += maps[r][c] - '0';
                for (int d = 0; d < 4; d++) {
                    int nr = r + dr[d], nc = c + dc[d];
                    if (nr < 0 || nr >= R || nc < 0 || nc >= C) continue;
                    if (maps[nr][nc] == 'X' || visited[nr][nc]) continue;
                    visited[nr][nc] = true;
                    st.push({nr, nc});
                }
            }
            answer.push_back(sum);
        }
    }
    sort(answer.begin(), answer.end());
    if (answer.empty()) answer = {-1};
    return answer;
}
```

- `queue` → `stack`, `q.front()` → `st.top()`. 나머지는 BFS와 동일 (`#include <stack>`).

**재귀 깊이 주의 (로컬 측정, 기본 스택 8MB)**

| 맵 | 재귀 깊이 | 재귀 DFS | stack DFS / BFS |
|---|---|---|---|
| 100×100 섬 하나 | 최대 1만 | 통과 (스택 1MB로 줄여도 통과) | 통과 |
| 1000×1000 섬 하나 | 최대 100만 | **비정상 종료** (스택 오버플로, exit 139) | 통과 |

- 칸 수가 수만 개 이하면 재귀도 괜찮음. **수십만 칸 이상이면 stack DFS나 BFS**.
- 채점 환경의 스택 크기는 알 수 없음 → 확신이 없으면 BFS(Q26)가 가장 안전.

| | 재귀 DFS | stack DFS | BFS |
|---|---|---|---|
| 코드 길이 | 가장 짧음 | BFS와 같음 | 기준 |
| 큰 맵 | 스택 오버플로 위험 | 안전 | 안전 |
| 최단 거리 | X | X | **O** |
| 쓰는 곳 | flood fill, 백트래킹 | flood fill (큰 맵) | 최단 거리, flood fill |

### Q30. 숫자 앞에 0을 채워 자릿수 맞추기 (`"mm:ss"` 만들기)

`to_string`에는 자릿수 옵션이 없음 → 아래 방법 중 하나.

**직접 if로 붙이는 방식 (동작은 하지만 길다)**

```cpp
string seconds_to_time(int seconds) {
    string result = "";
    int min = seconds / 60, sec = seconds % 60;
    if (min < 10) result = "0" + to_string(min);
    else result = to_string(min);
    result += ":";
    if (sec < 10) result += "0" + to_string(sec);
    else result += to_string(sec);
    return result;
}
```

**1) `snprintf`: 가장 짧음 (추천)**

```cpp
#include <cstdio>

string seconds_to_time(int seconds) {
    char buf[16];
    snprintf(buf, sizeof(buf), "%02d:%02d", seconds / 60, seconds % 60);
    return buf;                        // char 배열 → string 자동 변환
}
```

- `%02d` = 정수를 **최소 2자리, 빈자리는 0**으로. `%03d`면 3자리 (`7` → `"007"`).
- 버퍼 크기는 넉넉하게 (`"100:00"`처럼 자릿수가 넘칠 수도 있음).

**2) `ostringstream` + `setw` + `setfill`: C++ 스트림 방식**

```cpp
#include <sstream>
#include <iomanip>

string seconds_to_time(int seconds) {
    ostringstream out;
    out << setw(2) << setfill('0') << seconds / 60 << ':'
        << setw(2) << setfill('0') << seconds % 60;
    return out.str();
}
```

- `setw(2)`는 **바로 다음 출력 하나에만** 적용 → 숫자마다 다시 써야 함.
- `setfill('0')`은 한 번 정하면 **계속 유지**됨 (`cout`에 쓰면 이후 출력에도 영향).
- `cout`으로 바로 출력할 때도 같은 방법: `cout << setw(2) << setfill('0') << m;`

**3) 자릿수 맞추는 함수를 직접 만들기 (재사용)**

```cpp
string pad(int x, int width) {
    string s = to_string(x);
    if ((int)s.size() < width) s = string(width - s.size(), '0') + s;   // 부족한 만큼 '0'
    return s;
}
// pad(5, 2) → "05",  pad(7, 3) → "007",  pad(1234, 2) → "1234" (넘치면 그대로)

string seconds_to_time(int seconds) { return pad(seconds / 60, 2) + ":" + pad(seconds % 60, 2); }
```

- `string(n, '0')`: `'0'`을 n개 이어 붙인 문자열.

**4) `std::format` (C++20 전용)**

```cpp
#include <format>
string s = format("{:02}:{:02}", m, sec);   // C++17에서는 컴파일 에러
```

- 채점 환경이 C++17이면 사용 불가 → 1~3번 중 선택.

| 방법 | 장점 | 헤더 |
|---|---|---|
| `snprintf("%02d")` | 한 줄, 여러 값 한 번에 | `<cstdio>` |
| `setw` + `setfill` | `cout` 출력에도 그대로 사용 | `<iomanip>`, `<sstream>` |
| `pad` 함수 | 원리가 보이고 어디서든 재사용 | 없음 |
| `format` | 가장 깔끔 | `<format>` (C++20) |

- **반대 방향(`"mm:ss"` → 초)**: `stoi(t.substr(0, 2)) * 60 + stoi(t.substr(3, 2))`. 시·분·초가 섞이면 `':'` 위치를 `find`로 찾아 자르기.

### Q31. 로컬 컴파일러 버전을 채점 환경과 맞추는 이유와 버전 확인법

> **프로그래머스 컴파일 옵션은 C++20** (2026-10 확인). 프로그래머스에서는 아래 C++20 문법을 그대로 써도 됨.

**이유: 채점 환경보다 높은 버전으로 연습하면, 로컬에서 통과한 코드가 제출 시 컴파일 에러가 남**

- 아래 문법은 **C++20 전용** → 채점 환경이 C++17 이하인 사이트(백준 언어 선택, 다른 플랫폼 등)에서는 에러.

| C++20 전용 | C++17 대체 |
|---|---|
| `s.contains(x)` (`set`, `map`) | `s.count(x)` 또는 `s.find(x) != s.end()` |
| `std::format("{:02}", x)` | `snprintf(buf, sizeof(buf), "%02d", x)` (Q30) |
| `erase(v, x)`, `erase_if(v, f)` | `v.erase(remove(...), v.end())` (Q20) |
| `str.starts_with("ab")` | `str.rfind("ab", 0) == 0` 또는 `str.substr(0, 2) == "ab"` |

- C++17 코드는 C++20에서도 그대로 동작 → 채점 버전을 **모를 때는** 낮은 쪽(17)에 맞추면 손해가 없음.
- 채점 버전을 **알면** 로컬을 그 버전과 똑같이 맞추는 게 가장 정확 (프로그래머스 → C++20).

**채점 환경 버전 확인: `__cplusplus` 출력**

```cpp
// solution 안에 잠깐 넣고 "코드 실행" → 출력 확인 후 지우기
cout << __cplusplus << endl;
```

| 출력 | 버전 |
|---|---|
| `201402` | C++14 |
| `201703` | C++17 |
| `202002` | C++20 |

- 프로그래머스는 "코드 실행" 시 `cout` 출력이 실행 결과에 보임 → 연습 문제에서 미리 확인 가능.
- 시험 환경이 연습 환경과 다를 수 있으니, 시험 안내에 버전이 있으면 그것을 따르고, 확인할 수 없으면 C++17 문법만 쓰는 게 안전.

**로컬(CMake) 버전 바꾸기**

```cmake
set(CMAKE_CXX_STANDARD 20)          # CMakeLists.txt (채점 환경 버전과 같게: 프로그래머스 = 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON) # 지원 안 하면 조용히 낮추지 말고 에러
```

- 터미널에서 직접 컴파일할 때: `g++ -std=c++20 a.cpp`

### Q32. 매개변수 탐색(이분 탐색)에서 흔한 실수 3가지 (퍼즐 게임 챌린지)

```cpp
while (minlevel <= maxlevel) {
    level = (minlevel + maxlevel) / 2;
    int total = 0;                                   // ❌ 2
    for (...) {
        ...
        int time_prev = diffs[i - 1];                // ❌ 1
        total += (time_cur + time_prev) * not_count + time_cur;
    }
    if (total > limit) minlevel = level + 1;
    else maxlevel = level - 1;
}
return level;                                        // ❌ 3
```

**❌ 1. 다른 배열을 읽음 (`diffs[i-1]` ↔ `times[i-1]`)**

- 이름이 비슷한 배열이 여러 개면 자주 생기는 실수. 이것만으로 거의 모든 테스트가 틀림.
- → 처음에 `int diff = diffs[i], time_cur = times[i], time_prev = times[i - 1];`처럼 **이름을 붙여 한 곳에서 꺼내기**.

**❌ 2. 합계를 `int`로 계산 → 오버플로우**

- 퍼즐 30만 개 × 수억 → 합이 10¹⁴ 이상. `int`(약 21억)를 넘어 음수가 되면 "제한 시간 안"으로 잘못 판정.
- → `long long total = 0;`. 곱셈 결과가 21억을 넘을 수 있으면 `(long long)a * b`로 곱하기 전에 바꾸기 (5장 "정수 오버플로우").
- 문제의 `limit`이 `long long`이면 **비교 대상(합계)도 `long long`** 이라는 신호.

**❌ 3. 마지막에 계산한 `mid`를 답으로 반환**

- 마지막으로 확인한 `mid`가 **실패한 값일 수도 있음**. `while (lo <= hi)` 형태에서는 반복이 끝나면 **`lo`가 "조건을 만족하는 최솟값"**.

```cpp
// 형태 A: lo <= hi (끝나면 lo가 답)
int lo = 1, hi = maxDiff;
while (lo <= hi) {
    int mid = (lo + hi) / 2;
    if (check(mid)) hi = mid - 1;   // 되면 더 작은 쪽도 확인
    else lo = mid + 1;
}
return lo;

// 형태 B: lo < hi (끝나면 lo == hi가 답, 4장 템플릿)
int lo = 1, hi = maxDiff;
while (lo < hi) {
    int mid = (lo + hi) / 2;
    if (check(mid)) hi = mid;       // mid도 답 후보라 남겨 둠
    else lo = mid + 1;
}
return lo;

// 형태 C: 답을 따로 기록 (가장 헷갈리지 않음)
int answer = maxDiff;
while (lo <= hi) {
    int mid = (lo + hi) / 2;
    if (check(mid)) { answer = mid; hi = mid - 1; }
    else lo = mid + 1;
}
return answer;
```

- 한 형태를 정해서 **항상 같은 형태로** 쓰는 게 실수를 줄이는 방법.
- 판정 부분은 `bool check(int level)` 또는 `long long totalTime(int level)` **함수로 분리**하면 반복문이 짧아져 실수가 줄어듦.

**그 밖에**

- 디버깅용 `cout`은 제출 전에 지우기 (출력이 많으면 느려지고, 출력으로 채점하는 문제에서는 오답).
- `max`를 쓰면 `#include <algorithm>`. 최댓값은 `*max_element(diffs.begin(), diffs.end())`로 한 줄.

### Q33. 이분 탐색 정리

→ 4장 [이분 탐색 총정리](#이분-탐색-총정리)에 정리. (STL `lower_bound` / `upper_bound`, 값 찾기, 매개변수 탐색 최솟값·최댓값 틀, 함정 체크리스트, 실수 범위, 대표 문제)

- 핵심 한 줄: **"답을 정하면 가능한지 쉽게 판정할 수 있고, 답이 커질수록 결과가 한 방향으로만 바뀌면" 답을 이분 탐색**.
- 최솟값 찾기: `if (check(mid)) hi = mid; else lo = mid + 1;` (mid 내림)
- 최댓값 찾기: `if (check(mid)) lo = mid; else hi = mid - 1;` (**mid 올림**)
- `while (low <= high)` + 성공하면 `high = mid - 1`, 실패하면 `low = mid + 1` + **끝나면 `low`가 답**: 가장 널리 쓰이는 형태 중 하나 (Q32의 형태 A). 위 (A) `lo < hi` 형태와 결과가 같음.
- **판정 중 일찍 멈추기**: 합계가 `limit`을 넘는 순간 `break` → 더 볼 필요가 없음. 계산량이 줄고, 합계가 쓸데없이 커지는 것도 막음.

```cpp
for (int i = 0; i < n; i++) {
    total += ...;
    if (total > limit) break;    // 이미 실패 확정
}
```

- 단, 일찍 멈춰도 **합계 변수는 `long long`** 이어야 함 (한 번 더하는 값 자체가 `int`에 가까울 수 있음).
