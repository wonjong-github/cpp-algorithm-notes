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

### 매개변수 탐색 (답을 이분 탐색)

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
- `m.contains(key)`는 **C++20** 문법. 채점 사이트가 C++17이면 컴파일 에러 → `m.count(key)` 또는 `m.find(key) != m.end()` 사용이 안전 (로컬 컴파일러가 C++20이면 통과해서 놓치기 쉬움).
