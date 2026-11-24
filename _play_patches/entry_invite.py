"""풍년게임즈: 게임에 들어오면(홈 화면) 닉네임 없는 사람에게 하루 1번 '닉네임 등록' 카드를 띄운다 (2026-11-24 대표 요청).
build.py 로 play/*/index.html 을 다시 만들면 이 패치가 사라질 수 있으니, 빌드 뒤 저장소 루트에서 다시 실행:
    python3 _play_patches/entry_invite.py
이미 적용된 파일은 건너뛴다."""
import glob, re, sys

MARK = 'PR.entryInvite = function'
ADD = r"""
  // 입장 알림(11-24 대표): 닉네임 없으면 게임 홈 화면에서 하루 1번 등록 권유 카드. 판 중이면 띄우지 않음
  const kstDay = () => new Date(Date.now() + 9 * 36e5).toISOString().slice(0, 10);
  PR.entryInvite = function (game, opts = {}) {
    try {
      if (me() || inviting || LS.get('inv:day', '') === kstDay()) return false;
      const onHome = opts.onlyIf || (() => { const b = document.querySelector('.pr-homecta'); return !!(b && b.offsetParent); });
      setTimeout(() => {
        if (me() || inviting || !onHome()) return;
        LS.set('inv:day', kstDay()); inviting = true; ensureCSS();
        openUI(game, Object.assign({}, opts, { invite: { score: 0 } })).then(() => {
          inviting = false;
          if (me()) document.querySelectorAll('.pr-homecta').forEach(x => x.remove());
          if (opts.done) try { opts.done(); } catch (e) {}
        });
      }, opts.delay != null ? opts.delay : 1200);
      return true;
    } catch (e) { return false; }
  };
"""
JE_OLD = "if (baseInit) JE.init = function (o) { const r = baseInit(o); try { PR.legacy(JE.gameId, JE.best.get('main')); setTimeout(flush, 1500); } catch (e) {} return r; };"
JE_NEW = "if (baseInit) JE.init = function (o) { const r = baseInit(o); try { PR.legacy(JE.gameId, JE.best.get('main')); setTimeout(flush, 1500); } catch (e) {} try { PR.entryInvite(JE.gameId); } catch (e) {} return r; };"
PN_OLD = "try { PungRank.legacy('pungadventure', +localStorage.getItem('pa2_best') || 0); setTimeout(() => PungRank.flush(), 1500); } catch (e) {}"
PN_NEW = PN_OLD + "\ntry { PungRank.entryInvite('pungadventure', { host: wrap, onlyIf: () => !$('home').hidden, done: () => { if (PungRank.me()) { const rb = $('rank-btn'); rb.textContent = '랭킹'; rb.style.cssText = ''; } } }); } catch (e) {}"

n = 0
for f in sorted(glob.glob('play/*/index.html')):
    s = open(f, encoding='utf-8').read()
    if MARK in s: print('skip', f); continue
    assert s.count('  global.PungRank = PR;\n') == 1, f
    s = s.replace('  global.PungRank = PR;\n', '  global.PungRank = PR;\n' + ADD, 1)
    if '/pungnyeon/' in f:
        assert s.count(PN_OLD) == 1, f; s = s.replace(PN_OLD, PN_NEW)
    else:
        assert s.count(JE_OLD) == 1, f; s = s.replace(JE_OLD, JE_NEW)
    open(f, 'w', encoding='utf-8').write(s); n += 1; print('ok', f)
print('patched', n)
