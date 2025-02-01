# 목적:
# - Kubernetes 배포 관련 파일 및 설정을 관리합니다.
# 목표:
# - 클러스터 환경에서 안정적으로 애플리케이션을 배포 및 운영.
# 구현해야 할 기능:
# 1. `deployment.yaml`:
#    - 애플리케이션의 배포 설정.
#    - 리소스 요청/제한, 레플리카 수, 컨테이너 이미지 정보 포함.
# 2. `service.yaml`:
#    - 외부 접근을 위한 서비스 설정 (LoadBalancer, ClusterIP 등).
# 3. `ingress.yaml`:
#    - 도메인 및 경로 설정.
#    - SSL/TLS 인증서 적용.
# 4. `configmap.yaml`:
#    - 애플리케이션의 환경 변수와 설정을 외부에서 관리.
# 5. `secret.yaml`:
#    - 민감한 정보(API 키 등)를 안전하게 저장.
# 6. `namespace.yaml`:
#    - 배포 시 격리된 네임스페이스 설정.
# 7. `daemonset.yaml`:
#    - 애플리케이션의 렌림 연동.