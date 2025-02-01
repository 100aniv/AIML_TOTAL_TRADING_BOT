# 목적:
GitHub Actions를 활용하여 프로젝트의 CI/CD 워크플로우를 자동화합니다.

# 목표:
1. 코드 푸시 및 PR 이벤트 발생 시 빌드, 테스트, 배포를 자동으로 실행.
2. 파이프라인의 각 단계가 실패하거나 성공하면 알림 전송.
3. Docker 이미지 생성 및 Kubernetes 클러스터 배포 지원.

# 구현해야 할 파일:
1. `main.yaml`:
   - GitHub Actions 워크플로우 설정 파일.
   - Python 환경에서의 빌드, 테스트, Docker 이미지 생성, Kubernetes 배포 등 모든 작업을 정의.
2. GitHub Secrets:
   - Docker Hub, Kubernetes 인증 정보, 기타 민감한 정보 저장.
   - GitHub Actions에서 안전하게 참조.
3. 추가 스크립트:
   - 필요시 `scripts` 폴더에 있는 커스텀 스크립트를 활용하여 세부 작업 실행.

# 주요 기능:
- Python 의존성 설치 및 테스트 실행.
- Docker 이미지를 빌드하고 레지스트리에 푸시.
- Kubernetes 클러스터로 자동 배포.
- Slack 또는 Email 알림 통합 가능.
