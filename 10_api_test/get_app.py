from pathlib import Path
import sys
import importlib


def get_app(directory: str = None, filename: str = "app.py", absolute_path: str = None):
    """
    FastAPI app 객체를 가져오는 함수.

    Args:
        directory (str): 상위 디렉터리의 이름을 전달하여 해당 디렉터리에서 app 객체를 검색.
        absolute_path (str): 절대 경로를 전달하여 app 객체를 검색.

    Returns:
        app: FastAPI app 객체.

    Raises:
        ImportError: app 객체를 찾을 수 없을 때 발생.
    """
    # 절대 경로를 사용하는 경우
    if absolute_path:
        absolute_dir = Path(absolute_path).resolve()
        sys.path.append(str(absolute_dir.parent))
        module_name = absolute_dir.stem
    else:
        # 기본적으로 상위 디렉터리 경로 설정
        base_dir = Path(__file__).resolve().parent.parent

        # 특정 디렉터리를 지정한 경우 해당 디렉터리에서 검색
        if directory:
            base_dir = base_dir / directory

        # 디렉터리를 경로에 추가
        sys.path.append(str(base_dir))
        module_name = Path(filename).stem  # 파일명에서 확장자 제거

    try:
        # 동적으로 app 모듈을 로드
        app_module = importlib.import_module(module_name)
        return getattr(app_module, "app")  # app 객체 반환
    except (ModuleNotFoundError, AttributeError) as e:
        raise ImportError(f"Cannot find 'app' object in {module_name}: {e}")


if __name__ == "__main__":
    app = get_app(directory="09_auth", filename="basic_auth_sqlite.py")
    print(app)
