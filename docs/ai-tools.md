# AI 코딩 도구에서 쓰기

Claude Code · Cursor · Copilot · Codex 같은 AI 코딩 도구가 kiwoom-client 를 **틀리지 않게** 쓰도록 이 레포가 주는 것들입니다.
전부 코드에서 생성하고 테스트가 지키므로 메서드 이름·엔드포인트 목록이 실제 코드와 어긋나지 않습니다.

| 파일 | 누가 읽나 | 담긴 것 |
|---|---|---|
| [`llms.txt`](https://raw.githubusercontent.com/younghwan91/kiwoom-client/main/llms.txt) | 웹을 읽는 LLM ([llmstxt.org](https://llmstxt.org) 형식) | 한 단락 요약, 코드 쓸 때 규칙, 문서 링크 |
| [`llms-full.txt`](https://raw.githubusercontent.com/younghwan91/kiwoom-client/main/llms-full.txt) | 컨텍스트에 통째로 넣을 때 | 공개 API 시그니처·docstring 전부 + 엔드포인트 전체 목록 |
| [`AGENTS.md`](https://github.com/younghwan91/kiwoom-client/blob/main/AGENTS.md) | 이 레포를 연 에이전트 (Codex 등) | 사용 규칙 + 이 레포에서 일할 때의 규칙 |
| [`skills/kiwoom-client/`](https://github.com/younghwan91/kiwoom-client/tree/main/skills/kiwoom-client) | Claude Code · Agent Skills | 규칙·작업 순서·예제 + 엔드포인트 목록 |
| [`.cursor/rules/kiwoom-client.mdc`](https://github.com/younghwan91/kiwoom-client/blob/main/.cursor/rules/kiwoom-client.mdc) | Cursor | 같은 규칙 (파이썬 파일을 열 때 붙음) |
| [`.github/copilot-instructions.md`](https://github.com/younghwan91/kiwoom-client/blob/main/.github/copilot-instructions.md) | GitHub Copilot | 같은 규칙 |
| MCP 서버 (`kiwoom-client-mcp`) | MCP 클라이언트 | 엔드포인트를 도구로 직접 호출 — [README 의 MCP 절](https://github.com/younghwan91/kiwoom-client#mcp-서버로-사용하기) |

모든 규칙의 첫 줄은 같습니다: **`is_mock` 기본값은 `False` = 실서버이고, `api.order.*` · `api.credit_order.*` 는 실주문입니다.**
AI 가 만든 코드는 모의투자(`is_mock=True`)에서 먼저 돌리세요.

## Claude Code 스킬

### 플러그인으로 설치

이 레포가 플러그인 마켓플레이스를 겸합니다. Claude Code 안에서:

```text
/plugin marketplace add younghwan91/kiwoom-client
/plugin install kiwoom-client@kiwoom-client
```

설치하면 `kiwoom_client` 를 쓰는 코드나 "키움 REST API" 이야기가 나올 때 스킬이 저절로 불려 오고,
직접 부를 때는 `/kiwoom-client:kiwoom-client` 입니다.

### 내 프로젝트에 복사

스킬 폴더(파일 두 개)를 프로젝트의 `.claude/skills/` 에 넣으면 됩니다. 모든 프로젝트에서 쓰려면 `~/.claude/skills/` 에.

```bash
mkdir -p .claude/skills/kiwoom-client
for f in SKILL.md endpoints.md; do
  curl -fsSL -o ".claude/skills/kiwoom-client/$f" \
    "https://raw.githubusercontent.com/younghwan91/kiwoom-client/main/skills/kiwoom-client/$f"
done
```

복사한 스킬은 `/kiwoom-client` 로 부릅니다. 라이브러리를 올린 뒤에는 같은 명령으로 다시 받아 최신 목록으로 맞추세요.

## Cursor · GitHub Copilot

이 레포를 열면 그대로 적용됩니다. 내 프로젝트에서 쓰려면 파일을 같은 자리에 받아 두세요
(이미 `copilot-instructions.md` 가 있다면 내용을 덧붙이세요).

```bash
mkdir -p .cursor/rules .github
curl -fsSL -o .cursor/rules/kiwoom-client.mdc \
  https://raw.githubusercontent.com/younghwan91/kiwoom-client/main/.cursor/rules/kiwoom-client.mdc
curl -fsSL https://raw.githubusercontent.com/younghwan91/kiwoom-client/main/.github/copilot-instructions.md \
  >> .github/copilot-instructions.md
```

## 다른 도구

- **Codex 등 `AGENTS.md` 를 읽는 도구**: 이 레포를 열면 [`AGENTS.md`](https://github.com/younghwan91/kiwoom-client/blob/main/AGENTS.md) 를 읽습니다.
  내 프로젝트에서 쓰려면 그 파일의 "Writing code that uses kiwoom-client" 절을 내 `AGENTS.md` 에 옮겨 두세요.
- **웹 검색·문서 URL 을 읽는 도구**: `llms.txt` 주소를 알려 주면 됩니다.
