"""풍년게임즈: 시작 화면에 '이번 주 랭킹 TOP 3'(월요일 0시 초기화) 먼저 보여 주기 (2026-11-24 대표 요청).
빌드로 덮이면 저장소 루트에서 entry_invite.py → result_cta.py → 이 파일 순서로 다시 실행."""
import glob
MARK = 'PR.homeBoard = function'
ADD_AFTER = "  global.PungRank = PR;\n"
ADD = r"""
  // 시작 화면 '이번 주 랭킹 TOP 3'(11-24 대표: 랭킹을 먼저 보여 줘서 자극). 월요일 0시(한국) 초기화. 1분 캐시
  let hbCache = {};
  PR.homeBoardHTML = function (game, compact) { try { ensureCSS(); } catch (e) {} return `<div class="pr-hb${compact ? ' pr-hb-c' : ''}" data-game="${esc(game || '')}"><div class="pr-hb-t">🏆 이번 주 랭킹 ${compact || me() ? '<small>월요일 0시 초기화</small>' : '<button class="pr-homecta pr-hb-join" type="button">✏️ 닉네임 등록하고 참여</button>'}</div><div class="pr-hb-l">불러오는 중…</div></div>`; };
  PR.homeBoard = function () {
    document.querySelectorAll('.pr-hb:not([data-done])').forEach(async el => {
      el.dataset.done = '1'; const game = el.dataset.game; const box = el.querySelector('.pr-hb-l'); const m = me();
      try {
        let r = hbCache[game];
        if (!r || Date.now() - r.t > 60000) { r = { t: Date.now(), d: await rpc('pung_board', { p_game: game, p_period: 'week', p_me: m ? m.id : null, p_limit: 3 }, 6000) }; hbCache[game] = r; }
        const top = (r.d && r.d.top) || [], mine = r.d && r.d.me;
        const medal = ['🥇', '🥈', '🥉'];
        let h = top.length ? top.map((t, i) => `<div class="pr-hb-r${t.me ? ' me' : ''}"><span>${medal[i] || (i + 1)}</span><b>${esc(t.nick)}</b><i>${fmt(t.score)}</i></div>`).join('')
          : `<div class="pr-hb-e">이번 주 1등 자리가 비어 있어요!<br>지금 한 판이면 바로 <b>1등</b></div>`;
        if (top.length && top.length < 3) h += `<div class="pr-hb-e">${top.length + 1}등 자리가 비어 있어요!</div>`;
        if (mine && mine.rank > 3) h += `<div class="pr-hb-r me"><span>${mine.rank}</span><b>나</b><i>${fmt(mine.score)}</i></div>`;
        box.innerHTML = h;
      } catch (e) { if (el.querySelector('.pr-homecta')) el.outerHTML = PR.homeCTA(); else el.remove(); }
    });
  };
  try { new MutationObserver(() => { if (document.querySelector('.pr-hb:not([data-done])')) PR.homeBoard(); }).observe(document.documentElement, { childList: true, subtree: true }); } catch (e) {}
"""
CSS_OLD = "  .pr-homecta b{color:#e08a00}\n"
CSS_NEW = CSS_OLD + r"""  .pr-hb{margin:8px 0 0;border:2.5px solid #2b2b2b;border-radius:14px;background:#fffdf5;padding:6px 10px 8px;text-align:left;font-family:var(--pr-font,inherit)}
  .pr-hb-t{font:800 15px var(--pr-font,inherit);color:#2b2b2b;margin:0 0 2px;white-space:nowrap}.pr-hb-t small{font-weight:600;font-size:11px;color:#8a7a6a;margin-left:4px}
  .pr-hb-l{font-size:14px;color:#8a7a6a}
  .pr-hb-t{display:flex;align-items:center;gap:4px;flex-wrap:nowrap}.pr-hb .pr-hb-join{display:inline-block;width:auto;margin:0 0 0 auto;font-size:13px;padding:2px 8px;border-width:2px;white-space:nowrap}
  .pr-hb-r{display:flex;align-items:center;gap:6px;font-size:15px;line-height:1.3;color:#2b2b2b}.pr-hb-r span{width:22px;text-align:center}.pr-hb-r b{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.pr-hb-r i{font-style:normal;font-weight:800;color:#e08a00}
  .pr-hb-r.me b{color:#3a7bd5}
  .pr-hb-e{font-size:13px;color:#5b5550;line-height:1.35;margin-top:2px}.pr-hb-e b{color:#e08a00}
  .pr-hb-c{max-width:340px;margin:4px auto 8px;padding:4px 10px 6px}.pr-hb-c .pr-hb-t{font-size:13px;margin:0 0 2px}.pr-hb-c .pr-hb-r{font-size:13px;line-height:1.35}
"""
JE_OLD = "      JE.brand.homeHTML = function (o) { return baseHome.call(this, o) + PR.homeCTA(); };"
JE_NEW = "      JE.brand.homeHTML = function (o) { return baseHome.call(this, Object.assign({}, o, { extra: PR.homeBoardHTML(JE.gameId) + ((o && o.extra) || '') })); }; // 랭킹을 미션 줄보다 위에"
PN_OLD = ' <div id="mis"></div>\n'
PN_NEW = ' <div id="pr-hb-slot"></div>\n' + PN_OLD
PN_JS_OLD = "try { PungRank.entryInvite('pungadventure'"
PN_JS_NEW = "try { const s = $('pr-hb-slot'); if (s) s.innerHTML = PungRank.homeBoardHTML('pungadventure', true); } catch (e) {}\n" + PN_JS_OLD
n = 0
for f in sorted(glob.glob('play/*/index.html')):
    s = open(f, encoding='utf-8').read()
    if MARK in s: print('skip', f); continue
    assert s.count(ADD_AFTER) == 1 and s.count(CSS_OLD) == 1, f
    s = s.replace(ADD_AFTER, ADD_AFTER + ADD, 1).replace(CSS_OLD, CSS_NEW, 1)
    if '/pungnyeon/' in f:
        assert s.count(PN_OLD) == 1 and s.count(PN_JS_OLD) == 1, f
        s = s.replace(PN_OLD, PN_NEW).replace(PN_JS_OLD, PN_JS_NEW)
    else:
        assert s.count(JE_OLD) == 1, f; s = s.replace(JE_OLD, JE_NEW)
    open(f, 'w', encoding='utf-8').write(s); n += 1
print('patched', n)
