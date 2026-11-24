#!/usr/bin/env python3
"""도트풍: 같은 색이 냄비에 3번 모이면 '냄비 펑' — 그림 속 그 색 칸을 아래쪽부터 탄 수만큼 바로 지우고 냄비를 비움 (2026-11-24 차별화)"""
import sys, pathlib
P = pathlib.Path(__file__).resolve().parent.parent / 'play/dotpung/index.html'; s = P.read_text(encoding='utf-8')
if 'POTBURST_V1' in s: print('already'); sys.exit(0)
def rep(a, b):
    global s; assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
rep("    K.pop('냄비 합체!', slotX(same), L.potY - L.potW * 0.5, { size: 24, c1: '#ffe0f3', c2: '#ff6bc1', life: 0.8 }); JE.sfx.pop(6); return;",
    """    const PT = G.slots[same]; PT.mc = (PT.mc || 0) + 1;
    if (PT.mc >= 2) { // POTBURST_V1 같은 색 3번 → 냄비 펑: 그 색 칸을 아래부터 탄 수만큼 지움
      const x0 = slotX(same), y0 = L.potY - L.potW * 0.4; let n = 0;
      for (let r = N - 1; r >= 0 && PT.ammo > 0; r--) for (let c = 0; c < N && PT.ammo > 0; c++) if (G.grid[r][c] === PT.col) {
        G.grid[r][c] = null; PT.ammo--; n++; G.left--; G.cleared++;
        G.shots.push({ x0, y0, x1: L.bx + (c + 0.5) * L.cs, y1: L.by + (r + 0.5) * L.cs, col: PT.col, t: -n * 0.03, r, c });
      }
      G.score += n * 15; G.slots[same] = null; JE.fx.burst(x0, y0, PT.col, 18, 260); JE.shake.add(6); JE.sfx.pop(9); JE.haptic('heavy');
      K.pop(n ? `냄비 펑! ${n}칸` : '냄비 펑!', L.W / 2, L.potY - L.potW * 0.6, { size: 28, c1: '#fff3c8', c2: '#ff6bc1', life: 1 }); return;
    }
    K.pop('냄비 합체!', slotX(same), L.potY - L.potW * 0.5, { size: 24, c1: '#ffe0f3', c2: '#ff6bc1', life: 0.8 }); JE.sfx.pop(6); return;""")
rep("로 쏙!<br>냄비 3개가 다 차면 끝.'", "로 쏙!<br>같은 색 3번이면 <b style=\"color:#ff9ad5\">냄비 펑</b>! 그림을 바로 지워요.<br>냄비 3개가 다 차면 끝.'")
P.write_text(s, encoding='utf-8'); print('ok')
