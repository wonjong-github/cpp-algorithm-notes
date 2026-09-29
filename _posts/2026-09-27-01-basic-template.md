---
layout: post
title: "1. 기본 템플릿"
date: 2026-09-27 09:01:00 +0900
categories: notes
order: 1
---
{% raw %}
## 백준 (표준 입출력)

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

## 프로그래머스 (solution 함수)

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

## 로컬 테스트 템플릿 (프로그래머스)

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

## 백준용 로컬 테스트

백준은 표준 입력을 받으므로 코드를 고치지 않고 **입력 파일을 리다이렉트**하는 게 편함.

```bash
# input.txt에 예제 입력 붙여넣기
g++ -std=c++17 -O2 main.cpp -o main && ./main < input.txt
# 기대 출력과 비교
./main < input.txt | diff - output.txt && echo PASS
```

- CLion: Run Configuration → "Redirect input from"에 `input.txt` 지정.
- 코드 안에서 처리하려면 `main` 맨 앞에 `freopen("input.txt", "r", stdin);` (제출 전 반드시 삭제!)
{% endraw %}

---

[← 전체 목록](../../)
