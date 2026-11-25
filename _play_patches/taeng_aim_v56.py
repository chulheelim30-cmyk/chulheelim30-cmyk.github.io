# v56 탱탱풍 조준선: 첫 블록 또는 벽 1번까지만, 더 가늘게
P = 'play/taengtaengpung/index.html'
s = open(P, encoding='utf8').read()
if 'AIM_V56' not in s:
    def rep(o, n):
        global s
        assert s.count(o) == 1, o[:60]; s = s.replace(o, n)
    rep("for (let i = 0; i < 1400 && bounces < 5; i++) {", "for (let i = 0; i < 1400 && bounces < 2; i++) { /* AIM_V56 */")
    rep("hits.push([x, y]); pts.push([x, y]); bounces++; after = 0; continue;", "hits.push([x, y]); pts.push([x, y]); bounces = 9; break;")
    rep("if (bounces >= 4) { after += st; if (after > L.cs * 2) break; }", "if (bounces >= 1) { after += st; if (after > L.cs * 1.2) break; }")
    rep("c.setLineDash([8, 7]); c.lineWidth = 5; c.strokeStyle = 'rgba(255,253,246,.9)';", "c.setLineDash([5, 7]); c.lineWidth = 3; c.strokeStyle = 'rgba(255,253,246,.85)';")
    rep("c.lineWidth = 2.6; c.strokeStyle = 'rgba(43,43,43,.78)'; c.stroke();", "c.lineWidth = 1.3; c.strokeStyle = 'rgba(43,43,43,.7)'; c.stroke();")
    rep("c.lineWidth = 2; c.strokeStyle = 'rgba(43,43,43,.8)'; c.fillStyle = 'rgba(255,253,246,.85)'; c.beginPath(); c.arc(hx, hy, r * 1.15,", "c.lineWidth = 1.3; c.strokeStyle = 'rgba(43,43,43,.7)'; c.fillStyle = 'rgba(255,253,246,.85)'; c.beginPath(); c.arc(hx, hy, r * 0.9,")
    open(P, 'w', encoding='utf8').write(s); print('OK')
