# C++ 알고리즘 노트

C++ 코딩 테스트(백준 · 프로그래머스)용 템플릿과 Q&A 노트.

- 블로그: https://wonjong-github.github.io/cpp-algorithm-notes/
- 원본: [`cheatsheet.md`](cheatsheet.md) 한 파일에 모든 내용이 있음

## 구조

| 경로 | 내용 |
|---|---|
| `cheatsheet.md` | **원본.** 여기만 수정함 |
| `scripts/build_posts.py` | 원본을 블로그 글로 나눔 (1~5장 → 주제별 노트, 6장 Q&A → 질문마다 글 하나) |
| `scripts/dates.json` | 글마다 처음 올린 날짜 (새 글은 스크립트가 오늘 날짜로 추가) |
| `_posts/` | 생성된 글. **직접 수정하지 않음** (스크립트가 매번 덮어씀) |

## 업데이트 방법

```bash
python3 scripts/build_posts.py
git add -A && git commit -m "Q15 추가" && git push
```

푸시하면 GitHub Pages가 1~2분 안에 블로그를 다시 빌드한다.
