
# ---------- 5화 s2: 친구들이 모두 모인 장면(새 배경 위에 직접) ----------
F_CROW5 = SP("b_crow2", 300, side=-1, **SS)
F_GOOSE5 = SP("b_goose", 330, side=-1, **SS)
F_ROBOT5 = SP("b_robot", 300, side=-1, **SS)
F_OWL5 = SP("b_owl2", 320, side=-1, **SS)
def s2(t):  # 4~8.4
    lt = t - 4
    c = bg_at("bridge", 0.5)
    back = GROUND - 150
    for i, (sp, x) in enumerate([(F_CROW5, 170), (F_GOOSE5, 400), (F_ROBOT5, 650), (F_OWL5, 900)]):
        k = ease((lt - 0.2 - i * 0.25) / 0.5)
        if k <= 0: continue
        shadow(c, x, back + 10, sp.width * 0.8, a=int(70 * k))
        put(c, sp, x, back - sp.height / 2 + 12 - bounce(lt + i, 4, 16) * (lt > 1.6), alpha=k)
    shadow(c, 330, GROUND + 10, 360); stand(c, LOVE, 330, lt)
    shadow(c, 740, GROUND + 10, 300); stand(c, W_SIT5, 740, lt, 0.03)
    if lt > 1.6:
        hearts(c, lt - 1.6, base=GROUND - 420)
    text(c, "다리 위 노을,\n친구들이 모두 모였어요", 330, F_CAP, alpha=fade(lt, 0.3, 4.2), fill=(255, 236, 150))
    return c
SCENES = [(0, 4, s1), (4, 8.4, s2), (8.4, 12.4, s3), (12.4, 16.8, s4), (16.8, 21, s5), (21, 26, s6), (26, 28, s7), (28, 30.01, s8)]
