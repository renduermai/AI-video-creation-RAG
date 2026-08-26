## 项目目标
### AI 自动生成视频的创作过程中灵感和规则问答，通过实现 RAG 问答，快速了解平台规则，转场规则，角色设定...
### 后续可升级为混合检索，添加 langgraph ，MCP，视频生成功能

## 当前能力（已实现）
- 创作知识库：支持按分类（剧本范式/分镜规则/角色设定/平台审核）存储与检索
- RAG 问答：基于知识库回答创作相关问题
- 复用模块：document_loader / embedding_client / vector_store / llm_client / models

## 知识库分类
| 分类标签 | 目录 | 用途 |
|---|---|---|
| script_paradigm | DATA/knowledge/script_paradigm | 剧本范式 |
| storyboard_rule | DATA/knowledge/storyboard_rule | 分镜规则 |
| character_profile | DATA/knowledge/character_profile | 角色设定 |
| platform_policy | DATA/knowledge/platform_policy | 平台审核规则 |

## 使用说明
1，创建一个名为 `.env` 的文件，并添加以下内容：
```
# Deepseek
DEEPSEEK_API_KEY='sk-密钥'
DEEPSEEK_API_URL='https://api.deepseek.com'
DEEPSEEK_API_MODEL='deepseek-chat'

# 阿里云百炼
DASHSCOPE_API_KEY='sk-密钥'
DASHSCOPE_API_URL='https://llm-qwe2oxuia5qhvcmo.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
DASHSCOPE_API_MODEL='qwen3.7-plus-2026-05-26' # 2026.9.1到期

# 向量模型
DASHSCOPE_API_EMBEDDING_MODEL='qwen3.7-text-embedding'
```
2，运行 ingest_knowledge.py。加载 knowledge 文件夹下的剧本相关文档
3，运行 main.py 启动问答服务

## 效果展示
```
欢迎进入 AIGC 创作知识库，按 q 退出
请输入问题：转场规则

ai回答：根据已知信息，转场规则如下：
1. **硬切**：在情绪激烈或节奏加快时使用。
2. **淡入淡出**：用于时间跳跃或场景转换。
3. **匹配剪辑**：当前后镜头的动作或形状相似时使用，以保持流畅。
```

## 定制功能
### 1，只在某个文件中搜索。把 RAGPipeline.py 中的下面这段代码进行替换，选择要找的文件即可
```
answer = self.query(question)
# 可替换：只限定在某个txt 文件里面搜索
# answer = self.query(question, category="script_paradigm")
```

## 常见错误
### 1，文档命名。.env文件写错成 .env.py；knowledge 文件夹下，文件名忘写.txt后缀

## 后续路线（终极项目）
- 混合检索（向量 + 关键词）
- LangGraph 多 Agent 编排（规划/剧本/分镜/生成 Agent）
- LLM-as-a-Judge 自动评测
- MCP 协议工具封装 + Seedance/Kling 视频生成
