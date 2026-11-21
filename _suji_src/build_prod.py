import subprocess
subprocess.run(['python3','_suji_src/apply.py'],check=True,cwd='.')
p='suji/beta/index.html'; s=open(p).read()
def R(o,n):
  global s; assert s.count(o)==1,o[:50]; s=s.replace(o,n)
R("register('../sw.js', { updateViaCache: 'none', scope: '../' })","register('sw.js', { updateViaCache: 'none' })")
R('href="../manifest.webmanifest?v=1"','href="manifest.webmanifest?v=1"'); R('href="../apple-touch-icon.png?v=1"','href="apple-touch-icon.png?v=1"')
R(', React.createElement("span", { style: { marginLeft: 6, fontSize: 10, fontWeight: 800, color: "#0E1116", background: "#C5F04A", borderRadius: 5, padding: "1px 5px", verticalAlign: 3 } }, "BETA")','')
open('suji/index.html','w').write(s)
open(p,'w').write('<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=../"><link rel="canonical" href="../"><title>SuziQ</title></head><body><p>SuziQ는 <a href="../">여기</a>로 옮겼습니다.</p><script>location.replace("../"+location.search+location.hash)</script></body></html>')
print('built')
