---
layout: post
title: "5. C++ 기초: 헷갈리는 것들"
date: 2026-09-27 09:05:00 +0900
categories: notes
order: 5
---
{% raw %}
## 값 전달 vs 참조 전달

```cpp
void f1(int a)        { a = 10; }   // 복사본 수정 → 원본 그대로
void f2(int &a)       { a = 10; }   // 원본 수정
void f3(const vector<int> &v) {}    // 복사 없이 읽기만 (큰 컨테이너는 이렇게)
```

- 큰 `vector`, `string`을 값으로 넘기면 **매 호출마다 전체 복사** → 재귀 DFS에서 시간 초과의 흔한 원인.

## range-for에서 `&` 빠뜨리기

```cpp
for (auto x : v) x *= 2;          // 복사본만 바뀜. v는 그대로!
for (auto &x : v) x *= 2;         // v가 바뀜
for (const auto &s : strs) {}     // 읽기만 할 때 (string 복사 방지)
```

## `size()`는 unsigned

```cpp
vector<int> v;                              // 비어 있음
for (int i = 0; i < v.size() - 1; i++)      // v.size() - 1 = 엄청 큰 수 → 범위 밖 접근!
for (int i = 0; i + 1 < (int)v.size(); i++) // 안전
```

## 정수 오버플로우

```cpp
int a = 100000, b = 100000;
long long c = a * b;              // 틀림! int끼리 곱해서 이미 오버플로우 후 대입
long long d = (long long)a * b;   // 맞음
long long e = 1LL * a * b;        // 맞음

accumulate(v.begin(), v.end(), 0);    // 결과 타입이 int! 합이 크면 오버플로우
accumulate(v.begin(), v.end(), 0LL);  // long long으로 누적
```

- `int` 범위: 약 ±21억 (2 × 10⁹). 합/곱이 이걸 넘을 수 있으면 무조건 `long long`.

## 정수 나눗셈 / 나머지

```cpp
7 / 2;          // 3 (소수점 버림)
7 / 2.0;        // 3.5
-7 / 2;         // -3 (0 방향 버림. 파이썬은 -4)
-7 % 3;         // -1 (파이썬은 2) → 양수로 만들기: ((x % m) + m) % m
(a + b - 1) / b // a/b 올림 (a, b 양수)
```

## char ↔ int ↔ string

```cpp
'7' - '0';          // 7   (char → 숫자)
'a' + 1;            // 98  (int가 됨!)
char(('a' + 1));    // 'b'
string(1, 'a');     // "a"  (char → string)
to_string(7);       // "7"
"abc" + 'd';        // 틀림! 문자열 리터럴(포인터) + char → 이상한 결과
string("abc") + 'd' // "abcd"
```

## `map[]`은 없는 키를 만든다

```cpp
map<string, int> m;
if (m["kim"] == 0) {}   // "kim"이 없어도 m에 {"kim", 0}이 추가됨!
if (m.count("kim")) {}  // 존재 확인은 이렇게
```

## 반복자 무효화

```cpp
// 순회 중 erase는 반환값을 받아야 함
for (auto it = v.begin(); it != v.end(); ) {
    if (*it % 2 == 0) it = v.erase(it);
    else ++it;
}
// push_back으로 재할당이 일어나면 기존 반복자/포인터/참조 모두 무효
```

## 평가 순서는 정해져 있지 않음

```cpp
f(i, ++i);          // 어떤 인자가 먼저 평가될지 모름 → 쓰지 말 것
swap(it, --it);     // 같은 문제 (6장 Q2 참고)
```

## 전역 vs 지역 변수 초기화

```cpp
int g[100];         // 전역: 0으로 초기화됨
int main() {
    int l[100];     // 지역: 쓰레기값! → int l[100] = {}; 또는 vector 사용
    int big[10000000];   // 지역에 큰 배열 → 스택 오버플로우. 전역이나 vector로
}
```

## priority_queue 비교는 sort와 반대

```cpp
sort(..., greater<>());                               // 내림차순
priority_queue<int, vector<int>, greater<int>> pq;   // 최소 힙 (top이 가장 작음)
```

## 2차원 vector 선언

```cpp
vector<vector<int>> g(R, vector<int>(C, 0));   // R x C, 0으로 채움
g.assign(R, vector<int>(C, 0));                 // 재초기화 (테스트케이스 여러 개일 때)
```

## 구조화 바인딩 (C++17)

```cpp
pair<int, int> p = {1, 2};
auto [a, b] = p;                   // 복사
for (auto &[k, v] : m) v++;        // map 값 수정
```
{% endraw %}

---

[← 전체 목록](../../)
