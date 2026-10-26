# 调试指南

## 📋 概述

本文档描述项目的调试方法、常见问题排查、日志分析和性能调优技巧。

---

## 🔧 调试工具

### 1. Python 内置调试器（pdb）

**基本用法**：

```python
import pdb

# 在代码中设置断点
pdb.set_trace()

# 或者使用 breakpoint()（Python 3.7+）
breakpoint()
```

**常用命令**：

| 命令 | 缩写 | 功能 |
|------|------|------|
| `next` | `n` | 执行下一行（不进入函数） |
| `step` | `s` | 执行下一行（进入函数） |
| `continue` | `c` | 继续执行到下一个断点 |
| `break` | `b` | 设置断点 |
| `list` | `l` | 显示当前代码上下文 |
| `print` | `p` | 打印变量值 |
| `pprint` | `pp` | 美化打印变量值 |
| `where` | `w` | 显示调用堆栈 |
| `up` | `u` | 上移堆栈帧 |
| `down` | `d` | 下移堆栈帧 |
| `quit` | `q` | 退出调试器 |

### 2. 命令行调试

```bash
# 使用 pdb 运行脚本
python -m pdb scripts/kb.py init --name test --path ./test

# 启用详细输出
python scripts/kb.py init --name test --path ./test -v

# 启用调试模式（如果支持）
python scripts/kb.py init --name test --path ./test --debug
```

### 3. 日志调试

**配置日志级别**：

```python
import logging

# 设置日志级别
logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.WARNING)
logging.basicConfig(level=logging.ERROR)

# 配置日志格式
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='debug.log',
    filemode='w'
)
```

**在代码中添加日志**：

```python
import logging

logger = logging.getLogger(__name__)

def process_file(filepath):
    logger.debug(f"开始处理文件: {filepath}")
    logger.info(f"读取文件: {filepath}")

    try:
        content = read_file(filepath)
        logger.debug(f"文件内容长度: {len(content)}")
    except Exception as e:
        logger.error(f"处理文件失败: {filepath}, 错误: {e}", exc_info=True)
        raise

    logger.info(f"文件处理完成: {filepath}")
    return content
```

### 4. 打印调试

```python
# 简单打印
print(f"变量值: {variable}")

# 美化打印
from pprint import pprint
pprint(data_structure)

# 打印类型
print(f"变量类型: {type(variable)}")

# 打印对象属性
print(f"对象属性: {vars(obj)}")

# 打印目录内容
import os
print(f"目录内容: {os.listdir('.')}")
```

---

## 🐛 常见问题排查

### 1. 命令执行失败

**症状**：命令执行后返回非零退出码，显示错误信息。

**排查步骤**：

```bash
# 1. 查看完整错误信息
python scripts/kb.py init --name test --path ./test 2>&1

# 2. 使用详细模式
python scripts/kb.py init --name test --path ./test -v

# 3. 检查 Python 版本
python --version

# 4. 检查依赖安装
pip list | grep -E "pyyaml|argparse"

# 5. 检查文件权限
ls -la scripts/kb.py
chmod +x scripts/kb.py  # Linux/macOS

# 6. 检查路径是否正确
pwd
ls -la
```

**常见原因**：
- Python 版本过低（需要 3.8+）
- 缺少依赖包
- 文件权限不足
- 路径包含特殊字符
- 磁盘空间不足

### 2. 生成的文件内容不正确

**症状**：命令执行成功，但生成的文件内容不符合预期。

**排查步骤**：

```python
# 1. 检查模板文件
cat assets/note-template.md

# 2. 检查输入参数
python scripts/kb.py note --title "测试" --category "测试分类" --kb-root ./test --debug

# 3. 检查 Frontmatter 解析
python -c "
import yaml
content = open('test.md', encoding='utf-8').read()
parts = content.split('---')
if len(parts) >= 3:
    fm = yaml.safe_load(parts[1])
    print('Frontmatter:', fm)
"

# 4. 检查编码
python -c "
import chardet
with open('test.md', 'rb') as f:
    result = chardet.detect(f.read())
    print('编码:', result)
"
```

**常见原因**：
- 模板文件被修改
- 输入参数不正确
- Frontmatter 格式错误
- 文件编码问题（应为 UTF-8）
- 变量未正确替换

### 3. 死链检测不准确

**症状**：audit 命令报告的死链数量或内容不符合预期。

**排查步骤**：

```python
# 1. 手动检查链接
grep -r '\[\[' . --include="*.md" | head -20

# 2. 检查链接格式
# Wiki 链接: [[笔记名]]
# Markdown 链接: [文字](笔记名.md)
# 带别名: [[笔记名|显示文字]]

# 3. 检查文件是否存在
ls -la "笔记名.md"
find . -name "笔记名*"

# 4. 检查大小写敏感性
# Linux/macOS 区分大小写，Windows 不区分
ls -la | grep -i "笔记名"

# 5. 检查路径问题
# 链接中的路径是否相对于知识库根目录
```

**常见原因**：
- 链接格式不规范
- 文件名大小写不匹配
- 路径引用错误
- 笔记在子目录中但链接未包含路径
- 别名未正确配置

### 4. Frontmatter 补全不正确

**症状**：fix-fm 命令补全的 Frontmatter 字段不符合预期。

**排查步骤**：

```python
# 1. 检查文件夹命名规范
ls -la
# 应为: 01-分类名, 02-分类名, ...

# 2. 检查推断逻辑
python -c "
from pathlib import Path
folder = Path('01-前端开发')
category = folder.name.split('-', 1)[1] if '-' in folder.name else folder.name
print('推断分类:', category)
"

# 3. 检查难度推断
python -c "
title = 'Vue3 高级用法'
difficulty = '⭐⭐⭐' if '高级' in title else '⭐⭐'
print('推断难度:', difficulty)
"

# 4. 检查现有 Frontmatter
head -20 test.md
```

**常见原因**：
- 文件夹命名不规范（缺少编号前缀）
- 文件名无法推断难度
- 现有 Frontmatter 格式错误
- 字段覆盖逻辑问题
- 特殊字符处理问题

### 5. 标签统一不生效

**症状**：fix-tags 命令执行后标签没有变化或变化不符合预期。

**排查步骤**：

```python
# 1. 使用 dry-run 模式预览
python scripts/kb.py fix-tags --kb-root ./test --dry-run

# 2. 检查标签映射规则
grep -r "标签映射" scripts/fix-tags.py

# 3. 检查现有标签
grep -r "^tags:" . --include="*.md" | head -20

# 4. 检查标签格式
# 应为 YAML 列表: tags: [标签1, 标签2]
# 或: tags:
#       - 标签1
#       - 标签2

# 5. 检查核心标签集
cat references/tag-taxonomy.md | head -50
```

**常见原因**：
- 标签格式不规范（不是 YAML 列表）
- 标签不在映射规则中
- dry-run 模式未实际修改
- 标签大小写问题
- 核心标签集未更新

### 6. MOC 生成不完整

**症状**：generate-moc 命令生成的 MOC 缺少部分笔记或内容不完整。

**排查步骤**：

```python
# 1. 检查目录扫描
find ./01-前端开发 -name "*.md" -type f

# 2. 检查 Frontmatter 解析
for f in ./01-前端开发/*.md; do
    echo "=== $f ==="
    head -15 "$f"
done

# 3. 检查排序逻辑
# 按难度/优先级/创建时间排序

# 4. 检查 MOC 模板
cat assets/moc-template.md

# 5. 检查输出文件
cat ./01-前端开发/MOC.md
```

**常见原因**：
- 目录中存在非 Markdown 文件
- 部分笔记缺少 Frontmatter
- 排序逻辑问题
- 模板变量未正确替换
- 文件写入权限问题

---

## 📊 性能调优

### 1. 大知识库运行慢

**症状**：知识库文件数量多（>1000）时，命令执行时间过长。

**优化方法**：

```python
# 1. 使用生成器而非列表
def scan_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                yield os.path.join(root, file)

# 2. 延迟加载
def parse_frontmatter(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip() == '---':
                break
            # 只解析 Frontmatter，不读取整个文件

# 3. 缓存结果
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_file_info(filepath):
    # 缓存文件信息，避免重复解析
    return parse_file(filepath)

# 4. 并行处理
from concurrent.futures import ThreadPoolExecutor

def process_files(files):
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(process_file, files))
    return results
```

### 2. 内存占用过高

**症状**：处理大知识库时内存占用持续增长。

**优化方法**：

```python
# 1. 使用 with 语句确保文件关闭
def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()  # 读取后自动关闭

# 2. 逐行处理大文件
def process_large_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            process_line(line)  # 逐行处理，不加载整个文件

# 3. 及时释放大对象
def process_data(data):
    result = heavy_computation(data)
    del data  # 及时释放
    return result

# 4. 使用生成器
def read_lines(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            yield line.strip()
```

### 3. 磁盘 IO 频繁

**症状**：命令执行时磁盘读写频繁，速度慢。

**优化方法**：

```python
# 1. 批量写入
def write_files(updates):
    for filepath, content in updates.items():
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

# 2. 使用内存缓存
class FileCache:
    def __init__(self):
        self.cache = {}

    def read(self, filepath):
        if filepath not in self.cache:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.cache[filepath] = f.read()
        return self.cache[filepath]

    def write(self, filepath, content):
        self.cache[filepath] = content
        # 延迟写入或批量写入

# 3. 减少重复扫描
def scan_once(directory):
    # 只扫描一次，缓存结果
    if not hasattr(scan_once, 'cache'):
        scan_once.cache = list(Path(directory).rglob('*.md'))
    return scan_once.cache
```

---

## 🔍 高级调试技巧

### 1. 跟踪函数调用

```python
import sys

def trace_calls(frame, event, arg):
    if event == 'call':
        print(f"调用: {frame.f_code.co_name} 在 {frame.f_code.co_filename}:{frame.f_lineno}")
    return trace_calls

sys.settrace(trace_calls)
# 运行代码
sys.settrace(None)
```

### 2. 性能分析

```python
import cProfile
import pstats

# 运行性能分析
cProfile.run('main()', 'profile.out')

# 查看分析结果
p = pstats.Stats('profile.out')
p.sort_stats('cumulative')  # 按累计时间排序
p.print_stats(20)  # 显示前 20 个函数

# 按调用次数排序
p.sort_stats('calls')
p.print_stats(20)

# 按总时间排序
p.sort_stats('tottime')
p.print_stats(20)
```

### 3. 内存分析

```python
# 使用 tracemalloc
import tracemalloc

tracemalloc.start()

# 运行代码
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("[Top 10 memory usage]")
for stat in top_stats[:10]:
    print(stat)

# 使用 memory_profiler（需要安装）
# pip install memory-profiler
from memory_profiler import profile

@profile
def my_function():
    # 函数代码
    pass
```

### 4. 远程调试

```python
# 使用 debugpy（需要安装）
# pip install debugpy
import debugpy

# 监听 5678 端口
debugpy.listen(('0.0.0.0', 5678))
print("等待调试器连接...")
debugpy.wait_for_client()  # 阻塞直到调试器连接

# 或者在 VS Code 中配置 launch.json
```

---

## 📝 调试检查清单

提交 Bug 报告或寻求帮助前，请检查以下事项：

- [ ] 已确认使用最新版本
- [ ] 已确认 Python 版本 ≥ 3.8
- [ ] 已确认所有依赖已正确安装
- [ ] 已尝试使用 `--dry-run` 模式预览
- [ ] 已查看完整的错误信息和堆栈跟踪
- [ ] 已尝试在干净的环境中复现
- [ ] 已检查文件权限和磁盘空间
- [ ] 已搜索现有 Issue 和讨论
- [ ] 已准备好复现步骤和环境信息

---

## 📞 相关文档

- [ARCHITECTURE.md](ARCHITECTURE.md) - 项目架构
- [TESTING.md](TESTING.md) - 测试指南
- [FAQ.md](FAQ.md) - 常见问题
- [SUPPORT.md](SUPPORT.md) - 支持指南
- [SECURITY.md](SECURITY.md) - 安全策略

---

> **最后更新**：2026-08-30
>
> **版本**：v3.1
