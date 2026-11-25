"""랭킹 점수 서버 검증 v48 (2026-11-25)

- 판 시작(페이지 열기, start(), 지난 제출 직후)마다 서버에서 1회용 번호(pung_run)를 받는다.
- 점수 제출은 pung_submit2: 플레이 시간을 서버가 번호 발급 시각부터 직접 잰다.
  화면이 보고하던 플레이 시간과 코드 속 서명 비밀값은 더 이상 쓰지 않는다.
- 사용: python3 _play_patches/rank_run_v48.py   (저장소 루트에서, play/*/index.html 전부)
"""
import glob
import sys

REPL = [
    ("let markT = Date.now(), inviting = false;",
     "let markT = Date.now(), inviting = false, runTok = null;\n"
     "  async function newRun() { runTok = null; try { const r = await rpc('pung_run', {}); runTok = (r && r.run) || null; } catch (e) { runTok = null; } }\n"
     "  newRun();"),
    ("function pendSet(game, s, dur) { const p = LS.get('pend', {}); if (!p[game] || s > p[game].s) { p[game] = { s, dur }; LS.set('pend', p); } }",
     "function pendSet(game, s, dur, run) { const p = LS.get('pend', {}); if (!p[game] || s > p[game].s) { p[game] = { s, dur, run }; LS.set('pend', p); } }"),
    ("async function send(game, s, dur) {",
     "async function send(game, s, dur, run) {"),
    ("rpc('pung_submit', { p_id: m.id, p_secret: m.secret, p_game: game, p_score: Math.floor(s), p_dur_ms: Math.floor(dur), p_sig: await sig(game, Math.floor(s), m.id) })",
     "rpc('pung_submit2', { p_id: m.id, p_secret: m.secret, p_game: game, p_score: Math.floor(s), p_run: run || null })"),
    ("for (const g of Object.keys(p)) await send(g, p[g].s, p[g].dur);",
     "for (const g of Object.keys(p)) await send(g, p[g].s, p[g].dur, p[g].run);"),
    ("const now = Date.now(), dur = durMs != null ? durMs : now - markT; markT = now;",
     "const now = Date.now(), dur = durMs != null ? durMs : now - markT; markT = now; const run = runTok; newRun();"),
    ("if (!me()) { pendSet(game, score, dur); return Promise.resolve({ queued: true }); }\n      return send(game, score, dur);",
     "if (!me()) { pendSet(game, score, dur, run); return Promise.resolve({ queued: true }); }\n      return send(game, score, dur, run);"),
    ("start() { markT = Date.now(); },",
     "start() { markT = Date.now(); newRun(); },"),
]

# send() 안에서만 pendSet 에 run 을 넘긴다
SEND_INNER = ("pendSet(game, s, dur)", "pendSet(game, s, dur, run)")


def patch(path):
    s = open(path, encoding="utf-8").read()
    if "pung_submit2" in s:
        return "skip(already)"
    for old, new in REPL:
        assert s.count(old) == 1, (path, old[:60], s.count(old))
        s = s.replace(old, new)
    a = s.find("async function send(game, s, dur, run) {")
    b = s.find("async function flush()", a)
    seg = s[a:b]
    n = seg.count(SEND_INNER[0])
    assert n == 3, (path, "send pendSet count", n)
    s = s[:a] + seg.replace(SEND_INNER[0], SEND_INNER[1]) + s[b:]
    open(path, "w", encoding="utf-8").write(s)
    return "ok"


if __name__ == "__main__":
    files = sys.argv[1:] or sorted(glob.glob("play/*/index.html"))
    for f in files:
        print(f, patch(f))
