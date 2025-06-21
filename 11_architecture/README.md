# architecture

## 아키텍처 개요
아키텍처 종류
- 레이어드 아키텍처(Layered)
- MVC 아키텍처(Model-View-Controller)
- DDD 아키텍처(Domain-Driven-Development)
- 클린 아키텍처(Clean)

주요 비교표
| 구분 | 레이어드 (Layered) | MVC | DDD | 클린 아키텍처 |
|------|-------------------|-----|-----|---------------|
| **구조 원칙** | 수평적 계층 분리 | 역할별 삼각 분리 | 도메인 중심 설계 | 의존성 역전 원칙 |
| **비즈니스 로직 위치** | Service/CRUD 계층 | Model + Controller | Domain Layer | Core/Entities + Use Cases |
| **주요 디렉터리** | api, crud, models, schemas | models, views, controllers | domain, application, infrastructure | core, adapters, utils |
| **의존성 방향** | Top → Down (단방향) | 순환 참조 가능 | Domain 중심 | Inside → Out (역전) |
| **확장성** | 제한적 | 보통 | 좋음 | 매우 좋음 |


## 아키텍처 상세

### 레이어드 아키텍처

#### 장점
- **단순성**: 가장 이해하기 쉬운 구조
- **빠른 개발**: MVP, 프로토타입에 최적
- **낮은 진입장벽**: 주니어 개발자도 쉽게 적응
- **프레임워크 지원**: 대부분의 웹 프레임워크가 기본 제공
#### 단점
- **강한 결합**: 상위 계층이 하위 계층에 강하게 의존
- **테스트 어려움**: 통합 테스트 위주로 진행
- **확장성 제한**: 대규모 프로젝트에서 복잡도 증가
#### 적용 사례
```python
# 전형적인 CRUD API
@app.post("/users/")
def create_user(user: UserCreate):
    return UserCRUD(db).create_user(user)  # 단순한 흐름
```


### MVC 아키텍처
#### 장점
- **명확한 역할 분리**: Model(데이터), View(표현), Controller(제어)
- **웹 개발 표준**: 대부분의 웹 프레임워크 기본 패턴
- **병렬 개발**: 각 역할별로 독립적 개발 가능
- **재사용성**: View와 Model의 독립적 재사용
#### 단점
- **복잡한 상호작용**: Controller가 비대해질 수 있음
- **순환 의존성**: Model ↔ Controller 간 의존 관계
- **테스트 복잡성**: 3개 컴포넌트 간 상호작용 테스트 필요
#### 비즈니스 로직 분산
```python
# Model: 데이터 관련 비즈니스 로직
class UserModel:
    def validate_email(self): pass  # 데이터 검증
    def encrypt_password(self): pass  # 데이터 처리

# Controller: 흐름 제어 비즈니스 로직
class UserController:
    def create_user(self, request):  # 요청 처리 흐름
        # 검증 → 생성 → 응답 흐름 제어
```

### DDD 아키텍처
#### 장점
- **도메인 중심**: 비즈니스 로직이 명확히 분리
- **복잡성 관리**: 복잡한 비즈니스 규칙 체계적 관리
- **유지보수성**: 도메인 변경 시 영향 범위 최소화
- **팀 커뮤니케이션**: 도메인 전문가와 개발자 간 공통 언어
#### 단점
- **높은 복잡도**: 초기 구조 설계 복잡
- **학습비용**: DDD 개념 이해 필요
- **과도한 추상화**: 단순한 프로젝트에 오버엔지니어링
#### 계층별 책임
```python
# Domain Layer: 순수 비즈니스 로직
class User(Entity):
    def change_email(self, new_email: Email):  # 도메인 규칙
        if not self.can_change_email():
            raise DomainException("Cannot change email")

# Application Layer: 유스케이스 조합
class ChangeEmailUseCase:
    def execute(self, user_id, new_email):  # 워크플로우
        user = self.repository.find(user_id)
        user.change_email(new_email)
        self.repository.save(user)
```

### 클린 아키텍처
#### 장점
- **의존성 역전**: 외부 변경에 안정적
- **테스트 용이**: 모든 계층 독립 테스트 가능
- **기술 독립**: 프레임워크, DB 변경 용이
- **확장성**: 대규모 시스템에 적합
#### 단점
- **초기 비용**: 구조 설계 시간 많이 소요
- **러닝 커브**: 의존성 역전 원칙 이해 필요
- **보일러플레이트**: 많은 인터페이스와 구현체
#### 의존성 방향
```python
# Core → Adapter (의존성 역전)
class UserRepository(ABC):  # 인터페이스 (Core)
    def save(self, user): pass

class SqlUserRepository(UserRepository):  # 구현체 (Adapter)
    def save(self, user): pass  # 구체적 구현

class CreateUserUseCase:  # Core
    def __init__(self, repo: UserRepository):  # 추상화에 의존
        self.repo = repo
```
