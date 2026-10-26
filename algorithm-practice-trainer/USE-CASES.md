# 使用案例与最佳实践

## 案例 1: 基本使用场景

### 场景描述
适用于初学者的基本使用流程。

### 操作步骤

```bash
# 1. 初始化
python main.py init --name "示例项目"

# 2. 执行操作
python main.py run --input data.txt

# 3. 查看结果
python main.py report
```

### 最佳实践
- 先使用 `--dry-run` 预览效果
- 定期备份重要数据
- 查看日志排查问题

---

## 案例 2: 批量处理场景

### 场景描述
需要处理大量文件或数据时。

### 操作步骤

```bash
# 准备输入列表
cat > list.json << EOF
["file1.txt", "file2.txt", "file3.txt"]
EOF

# 批量执行
python main.py batch --list list.json --output results/
```

### 最佳实践
- 分批处理，避免内存溢出
- 使用 `--parallel` 启用并行处理
- 处理完成后验证结果完整性

---

## 案例 3: 集成到工作流

### 场景描述
与 CI/CD 或其他工具集成。

### 操作步骤

```yaml
# GitHub Actions 示例
- name: Run Skill
  run: |
    python main.py run --input ${{ github.workspace }}/data
    python main.py report --format json
```

### 最佳实践
- 在 CI 中使用固定版本
- 添加失败重试机制
- 输出结构化日志便于分析

---

## 案例 4: 自定义扩展

### 场景描述
需要添加自定义功能或模板。

### 操作步骤

```python
# 自定义插件
from skill import BasePlugin

class MyPlugin(BasePlugin):
    def execute(self, data):
        # 自定义逻辑
        return processed_data
```

### 最佳实践
- 遵循现有代码风格
- 添加单元测试
- 更新文档说明
