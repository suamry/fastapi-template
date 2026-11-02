from pathlib import Path

# 获取项目根目录
# 或使用绝对路径，指到项目根目录为止，例如 windows：BasePath = D:\Project\ccontrol-test-engine
WORKSPACE_PATH = Path(__file__).resolve().parent.parent.parent
CWD_PATH = Path.cwd()


def get_user_mode():
    """
    获取用户模式

    Returns:
        bool: True 为用户模式（pip install），False 为开发模式（源码运行）
    """
    return "site-packages" in str(Path(__file__).resolve())


USER_MODE = get_user_mode()

# 基础路径
BASE_PATH = CWD_PATH if USER_MODE else WORKSPACE_PATH

# 静态文件路径
STATIC_PATH = Path.joinpath(WORKSPACE_PATH, "static")

# 日志文件路径
LOG_PATH = Path.joinpath(BASE_PATH, "logs")

# 模型文件夹
MODEL_PATH = Path.joinpath(WORKSPACE_PATH, "models")


if __name__ == "__main__":
    print(f"getcwd: {Path.cwd()}")
    print(f"USER_MODE: {USER_MODE}")
    print(f"WORKSPACE_PATH: {WORKSPACE_PATH}")
    print(f"CWD_PATH: {CWD_PATH}")
    print(f"BASE_PATH: {BASE_PATH}")
    print(f"LOG_PATH: {LOG_PATH}")
    print(f"MODEL_PATH: {MODEL_PATH}")
