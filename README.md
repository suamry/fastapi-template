# FastAPI Template

FastAPI 项目模板，快速创建 HTTP 服务

## 关键特征

- **快速**：可与**NodeJS**和**Go**并肩的极高性能（归功于 Starlette 和
  Pydantic）。[最快的 Python web 框架之一](https://fastapi.tiangolo.com/zh/#_11)。

- **高效编码**：提高功能开发速度约 200％ 至 300％。*

- **更少 bug**：减少约 40％ 的人为（开发者）导致错误。*

- **智能**：极佳的编辑器支持。处处皆可自动补全，减少调试时间。

- **简单**：设计的易于使用和学习，阅读文档的时间更短。

- **简短**：使代码重复最小化。通过不同的参数声明实现丰富功能。bug 更少。

- **健壮**：生产可用级别的代码。还有自动生成的交互式文档。

- **标准化**：基于（并完全兼容）API 的相关开放标准：[OpenAPI](https://github.com/OAI/OpenAPI-Specification)(以前被称为
  Swagger) 和[JSON Schema](https://json-schema.org/)。

## 前置环境

- python >= 3.11

- uv >= 0.8.0（python 包管理器）

## 安装依赖

```
# 激活虚拟环境
uv venv
source .venv/bin/activate

# 安装依赖
uv sync
```

## 目录结构

结构树基本大致相同，详情请查看源代码

```text
├── README.md
├── app                # 代码文件夹
│   ├── __init__.py    # 标识当前文件夹为 python package
│   ├── api            # 接口
│   ├── common         # 通用模块
│   ├── config         # 配置
│   ├── main.py        # 主程序
│   ├── middleware     # 中间件
│   ├── schemas        # 数据模型
│   ├── services       # 业务代码
│   ├── tests          # 单元测试（暂无内容）
│   └── utils          # 工具包
├── logs               # 日志文件夹
├── uv.lock            # uv 依赖锁定文件
├── pyproject.toml     # uv 依赖管理文件
└── static             # 静态资源文件夹
    └── swagger-ui
```
