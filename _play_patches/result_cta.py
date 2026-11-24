"""풍년게임즈: 점수 결과 화면에 '닉네임 등록하고 ○점 랭킹에 올리기' 버튼 (2026-11-24 대표 요청). 등록 전까지 매 판.
빌드로 덮이면 저장소 루트에서 다시 실행: python3 _play_patches/result_cta.py (entry_invite.py 먼저)"""
import glob
MARK = 'PR.resultCTA = function'
ADD_AFTER = "  global.PungRank = PR;\n"
ADD = r"""
  // 결과 화면 버튼(11-24 대표): 등록 전까지 매 판 점수 아래에 표시. 누르면 홈 버튼과 같은 참여 화면(.pr-homecta)
  PR.resultCTA = function (score) {
    if (me()) return ''; try { ensureCSS(); } catch (e) {}
    return `<button class="pr-homecta pr-rescta" type="button">🏆 <b>닉네임 등록</b>하고 이 점수 랭킹에 올리기</button>`;
  };
"""
JE_OLD = "      JE.brand.homeHTML = function (o) { return baseHome.call(this, o) + PR.homeCTA(); };\n    }\n"
JE_NEW = JE_OLD + """    // 결과 화면에 참여 버튼 (등록 전까지)
    if (JE.brand && JE.brand.resultHTML) {
      const baseRes = JE.brand.resultHTML;
      JE.brand.resultHTML = function (o) { return baseRes.call(this, o) + PR.resultCTA(o && o.score); };
    }
"""
PN_OLD = "try { if (!PungRank.me()) { const rb = $('rank-btn'); rb.textContent = '🏆 닉네임 등록하고 랭킹 참여'; rb.style.cssText = 'background:#fff3c4;border:2px dashed #c26a10;color:#7a3a00'; } } catch (e) {}"
PN_NEW = PN_OLD + "\ntry { if (!PungRank.me()) { const ob = $('ov-rank'); ob.textContent = '🏆 닉네임 등록하고 랭킹에 올리기'; ob.style.cssText += ';background:#fff3c4;border:2px dashed #c26a10;color:#7a3a00'; } } catch (e) {}"
CSS_OLD = "  .pr-homecta b{color:#e08a00}\n"
CSS_NEW = CSS_OLD + "  .pr-rescta{margin:12px 0 2px;font-size:16px;white-space:nowrap}\n"
n = 0
for f in sorted(glob.glob('play/*/index.html')):
    s = open(f, encoding='utf-8').read()
    if MARK in s: print('skip', f); continue
    assert s.count(ADD_AFTER) == 1 and s.count(CSS_OLD) == 1, f
    s = s.replace(ADD_AFTER, ADD_AFTER + ADD, 1).replace(CSS_OLD, CSS_NEW, 1)
    if '/pungnyeon/' in f: assert s.count(PN_OLD) == 1, f; s = s.replace(PN_OLD, PN_NEW)
    else: assert s.count(JE_OLD) == 1, f; s = s.replace(JE_OLD, JE_NEW)
    open(f, 'w', encoding='utf-8').write(s); n += 1
print('patched', n)
