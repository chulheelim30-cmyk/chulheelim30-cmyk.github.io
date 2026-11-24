# SuziQ 다음 작업 (2026-11-24 기준) — 새 대화는 이 파일과 HANDOFF.md부터 읽기

## 지금 상태
- 앱 본 주소: https://chulheelim30-cmyk.github.io/suji/ (main 푸시 = 바로 배포, `python3 _suji_src/build_prod.py`로 빌드, sw.js 캐시 번호 +1)
- 디자인: 에메랄드 #10B981 다크, 사업개요 4단계(토지→상품→분양가→결과)
- 건축개요 붙여넣기·사진·PDF 자동 입력, 분양면적 비면 [확인] 경고
- 베타 기간 보고서 누구나 생성(무료판 표시)
- 전국 토지 실거래 수집(6분마다, 2026-07 개편 코드 반영) + 시세 통계 `suji_land_price` 매주 월 04:41 재계산 → 앱이 받아 씀
- 로그인(카카오·구글·이메일 인증번호) 만들어 둠, **숨김**(`SJ_LOGIN_ON=false`, 관리자·`?login=1`만 보임). 회원 탈퇴 함수 `suji-account-delete`, 가입일+14일 체험(`suji_profiles`)
- 개인정보처리방침 개정안 `suji/privacy-20261201.html`(12/1 시행 예고 중), 계정 삭제 안내 `suji/account-delete.html`
- 안드로이드 앱 프로젝트 `_suji_app/`(Capacitor 8, com.pungnyeon.suziq, SDK 36) + 스토어 자료 `_suji_app/store/`
- 2026-11-24 애드몹 보상형 광고 연결(**테스트 ID, 꺼 둠** `SJ_ADS_ON=false`). 앱에서 `?adtest=1`로 시험. 웹은 광고 없음 → 무료 하루 1건 그대로. 앱 안 보고서는 새 창 대신 화면 위 덮개(iframe)로 표시

## 결정된 것
- 런칭 = D-U-N-S 번호 발급 완료 시점(플레이 **조직 계정**으로 등록 → 12명·14일 테스트 면제)
- 요금: 가입일부터 14일 무료, 프로 월 4,900원/연 49,000원, 무료는 광고 보고 하루 1건. 웹=토스페이먼츠, 앱=구글 플레이 결제(같은 Supabase 계정으로 묶기)
- 요금 공지(12/21) 날짜는 런칭 날짜 정해지면 한 번에 맞춤(지금은 이용자 없음)
- 수집 주기: 시세 통계 주간

## 사람이 할 일(계정 주인)
1. Supabase·GitHub·카카오·구글 관리 계정 2단계 인증
2. D-U-N-S: 홈택스 영문 사업자등록증명 → D&B 무료 신청(상호·주소 철자 모든 곳 동일)
3. Supabase Auth: URL 설정(사이트 https://chulheelim30-cmyk.github.io/suji/, 리다이렉트에 `com.pungnyeon.suziq://login-callback` 추가), 카카오(비즈앱)·구글 OAuth 키 등록, 메일 템플릿에 `{{ .Token }}`, SMTP(Resend 등)
4. 애드몹 가입 → 앱 추가 → 보상형 광고 단위 → **앱 ID(~), 광고 단위 ID(/), 게시자 ID(pub-)** 전달 → Claude가 교체
5. 토스페이먼츠 빌링(자동결제) 신청
6. PC에 Android Studio → `_suji_app/README.md` 순서로 .aab 빌드(서명 키 따로 보관)

## Claude가 이어서 할 일
- [x] 애드몹 보상형 광고 연결(테스트 ID) + `app-ads.txt`(틀, 게시자 ID 대기) + 처리방침(12/1판 1-4·3-1)·데이터 보안 답안 (2026-11-24)
- [ ] 실제 ID 받으면: `base.html` SJ_ADMOB(rewardId, test:false) · `AndroidManifest.xml` APPLICATION_ID · `app-ads.txt` 주석 해제 → 빌드
- [ ] 유료 전환일: `BETA_OPEN=false`, `SJ_ADS_ON=true` (무료 한도는 지금 기기 저장값 → 로그인 공개 후 서버 기록으로)
- [ ] 앱 안 보고서 'PDF로 저장·인쇄' 버튼이 웹뷰에서 안 될 수 있음 → 실기기 확인 후 공유/다운로드 방식 검토
- [ ] 12/1: 3번 끝났으면 `privacy-20261201.html` → `privacy.html` 교체, `SJ_LOGIN_ON=true`
- [ ] 관리자 모드를 로그인 계정 기준으로 변경(지금은 브라우저 저장값)
- [ ] 인증번호 메일 폭탄 방지 캡차(Cloudflare Turnstile, 사이트 키 필요)
- [ ] 관리자 접속 기록 1년 보관 장치, 유출 72시간 통지 양식
- [ ] 토스 빌링·구글 플레이 결제 연결(승인 후)
- [ ] 수집기에서 틀린 코드 12320·12340 제거(다음 배포 때)
- [ ] 런칭일 확정 시 요금 공지·약관 날짜 정리
