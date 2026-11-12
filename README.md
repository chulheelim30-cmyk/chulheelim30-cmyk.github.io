# chulheelim30-cmyk.github.io

- `aigyeot/` — 아이곁: 아픈 반려동물 케어 기록 웹앱 (https://chulheelim30-cmyk.github.io/aigyeot/)
  - 저장소: Supabase 프로젝트 pbmocpzclvndlevuvfto의 `aigyeot_*` 테이블, RPC `ag_*` (자세한 내용은 ttokttok 저장소 CLAUDE.md '별개 앱: 아이곁')
  - 톡톡(ttokttok) 앱 주소 범위(/ttokttok/) 밖에 두려고 이 저장소로 옮김(11/12). 톡톡이 설치된 휴대폰에서 링크가 톡톡 앱으로 열리던 문제 때문.

## 아이곁 데이터 구조 메모 (11/12)
- `aigyeot_family.pet` = `{ pets: [ {id, name, species, weightKg, foods[{id,name,kcal,per,unit,gw?}], tasks, ...} ] }` (예전 한 마리 형식은 앱이 pets[0](id 'p1')로 읽음)
- 기록(`aigyeot_log.data`)에 `petId`. petId 없는 예전 기록은 첫째 아이 것. 보고 있는 아이는 기기별 localStorage `aigyeot-pet-<코드>`.
- 사료 `gw` = 1캔·1포 무게(g) → g↔캔 환산해 칼로리 자동 계산(kcalOf).
