# tree-sims

나무의사·식물보호기사 공부용 칠판 시뮬레이션 모음. https://lig7oo7-cloud.github.io/tree-sims/

- `index.html` — 목록 화면 (분야 탭, 검색)
- `list.json` — 시뮬레이션 목록 (빌드할 때 자동 갱신)
- `sims/*.html` — 완성된 시뮬레이션 (외부 파일 없이 단독 실행)
- `src/*.html` — 시뮬레이션 원본 조각 (설명·시뮬레이션·시험 포인트·쪽지시험)
- `build/shell.html` — 공통 칠판 디자인·도우미 함수·쪽지시험 틀
- `build/build.py` — `python3 build/build.py` 로 src → sims 빌드 + list.json 갱신

`sims/codit.html` 은 첫 번째로 손으로 만든 파일이라 src 없이 그대로 둔다.
