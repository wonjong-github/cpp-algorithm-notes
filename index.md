---
layout: default
---

C++ 코딩 테스트(백준 · 프로그래머스)용 노트입니다.
템플릿과 STL 사용법은 **주제별 정리**에, 자주 헷갈리는 포인트는 **Q&A**에 모았습니다.

## 주제별 정리

{% assign notes = site.categories.notes | sort: 'order' %}
<ul>
{% for p in notes %}
  <li><a href="{{ p.url | relative_url }}">{{ p.title }}</a></li>
{% endfor %}
</ul>

## Q&A (최신순)

{% assign qs = site.categories.qna | sort: 'order' | reverse %}
<ul>
{% for p in qs %}
  <li>
    <a href="{{ p.url | relative_url }}">{{ p.title }}</a>
    <small>· {{ p.date | date: "%Y-%m-%d" }}</small>
  </li>
{% endfor %}
</ul>
