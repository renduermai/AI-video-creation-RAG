import os
from RAGPipeline import RAGPipeline
from config import KNOWLEDGE_DIR


def main():
    rag = RAGPipeline()

    # 分类目录 -> 分类标签（目录名就是标签，入库后按它过滤）
    categories = {
        "script_paradigm": "剧本范式",
        "storyboard_rule": "分镜规则",
        "character_profile": "角色设定",
        "platform_policy": "平台审核规则",
    }

    for folder, label in categories.items():
        path = os.path.join(KNOWLEDGE_DIR, folder)
        if not os.path.isdir(path):
            print(f"跳过 [{label}]，目录不存在: {path}")
            continue

        count = 0
        for filename in os.listdir(path):
            if filename.endswith(('.txt', '.md')):
                file_path = os.path.join(path, filename)
                rag.ingest(file_path, category=folder)
                count += 1
        print(f"已导入 [{label}] {count} 个文件")


if __name__ == "__main__":
    main()
