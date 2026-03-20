git status 현재 변경 상태 확인
git log --oneline 커밋 이력 간략 조회
git remote -v 연결된 원격 저장소 확인
git remote remove origin 원격 저장소 연결 해제
fatal: not a git repository git init 미실행 git init 실행
error: src refspec main does not
match any
커밋 없이 push
시도
git add . + git commit 먼저 실
행
remote: Permission denied GitHub 인증 실패 GitHub 로그인 확인
fatal: remote origin already exists
origin 이미 등록
됨
git remote remove origin 후 재
추가
현재 폴더 확인 pwd pwd
지금 어디 폴더에 있는지 보여
줌
파일/폴더 목록 보기 ls 또는 dir ls 현재 폴더의 파일 목록
폴더 이동 cd 폴더이름 cd 폴더이름 해당 폴더로 이동
상위 폴더로 이동 cd .. cd .. 한 단계 위 폴더로 이동
폴더 만들기 mkdir 폴더이름 mkdir 폴더이름 새 폴더 생성
파일 내용 보기 cat 파일이름 cat 파일이름 파일 전체 내용 출력
파일 복사 cp 원본 대상 cp 원본 대상 파일 복사
파일 이동/이름 변경 mv 원본 대상 mv 원본 대상 파일 이동 또는 이름 변경
파일 삭제 rm 파일이름 rm 파일이름 파일 삭제 (주의!)
폴더 삭제 (안에 파일 포
함)
rm -Recurse 폴더이름
rm -rf 폴더이름
폴더와 그 안의 모든 파일 삭제
화면 지우기 cls 또는 clear clear 터미널 화면 깨끗하게

grep 검색어 파일 Select-String "검색어" 파일 파일에서 특정 텍스트 검
색
ls \| grep 키워드 ls \| Where-Object { $_.Name -like "*키워드
*" }
파일 목록에서 필터링
touch 파일이름 New-Item 파일이름 빈 파일 만들기
echo 내용 > 파일 "내용" \| Out-File 파일 파일에 내용 쓰기
cat 파일 \| head
-5
Get-Content 파일 -Head 5 파일 처음 5줄만 보기
cat 파일 \| tail
-5
Get-Content 파일 -Tail 5 파일 마지막 5줄만 보기