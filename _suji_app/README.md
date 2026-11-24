# SuziQ 안드로이드 앱 (Capacitor 8)

본 서비스(https://chulheelim30-cmyk.github.io/suji/)를 앱으로 여는 껍데기 앱. 웹을 고치면 앱도 바로 바뀐다(앱 재심사 불필요).

- 패키지 이름: `com.pungnyeon.suziq` (한 번 올리면 바꿀 수 없음)
- target/compile SDK 36 (2026-08-31부터 신규 앱 필수), min SDK 24
- 인터넷 없을 때: `www/index.html` 안내 화면
- 로그인 복귀 주소: `com.pungnyeon.suziq://login-callback` (카카오·구글 로그인은 시스템 브라우저로 열고 이 주소로 돌아옴 — 구글은 앱 내부 화면 로그인을 막음)
- 보상형 광고: `@capacitor-community/admob`. 앱 ID는 `AndroidManifest.xml`의 `com.google.android.gms.ads.APPLICATION_ID`(지금은 구글 테스트 ID), 광고 단위 ID는 웹 쪽 `_suji_src/base.html`의 `SJ_ADMOB`. 앱 ID를 바꾸면 .aab를 다시 빌드해야 함(광고 단위 ID는 웹만 고치면 됨)
- 아이콘·스플래시: `android/app/src/main/res/` (에메랄드, `suji/icon-*.png`에서 생성)

## 빌드 (PC, Android Studio 필요)
1. Node 20+ 설치 → 이 폴더에서 `npm install` → `npx cap sync android`
2. `npx cap open android` (Android Studio가 열림, Gradle 동기화 대기)
3. Build → Generate Signed App Bundle → **새 업로드 키 만들기** (`.jks` 파일과 비밀번호는 저장소에 올리지 말고 따로 보관 — 잃어버리면 업데이트 불가, Play 앱 서명으로 복구 요청 가능)
4. `android/app/release/app-release.aab` 를 Play Console에 업로드
5. 버전 올릴 때: `android/app/build.gradle` 의 `versionCode`(+1), `versionName`

## Play Console 설정 전에 할 일
- Supabase → Authentication → URL Configuration → Redirect URLs 에 `com.pungnyeon.suziq://login-callback` 추가
- 등록 자료(설명·스크린샷·데이터 보안 답안)는 `store/LISTING.md`
