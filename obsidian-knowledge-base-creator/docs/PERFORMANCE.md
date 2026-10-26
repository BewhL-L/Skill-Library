# 性能优化指南

## 📋 概述

本文档介绍 Obsidian 知识库标准化生成器的性能优化方法，适用于处理大型知识库（1000+ 笔记）的场景。

---

## 📊 性能基准

### 测试环境

| 组件 | 配置 |
|------|------|
| 操作系统 | Windows 11 / macOS 14 / Ubuntu 22.04 |
| CPU | Intel i5-10400 / Apple M1 / AMD Ryzen 5 5600X |
| 内存 | 16 GB |
| 存储 | SSD (NVMe) |
| Python | 3.11 |

### 基准测试结果

| 知识库规模 | init | audit | validate | fix-fm | fix-link | fix-tags | standardize |
|-----------|------|-------|----------|--------|----------|----------|-------------|
| 100 笔记 | 2s | 3s | 5s | 2s | 4s | 3s | 10s |
| 500 笔记 | 5s | 12s | 20s | 8s | 15s | 10s | 40s |
| 1000 笔记 | 8s | 25s | 45s | 15s | 30s | 20s | 80s |
| 5000 笔记 | 20s | 120s | 200s | 60s | 150s | 100s | 400s |

> **注意**：以上数据仅供参考，实际性能因硬件、磁盘速度、文件复杂度而异。

---

## ⚡ 通用优化技巧

### 1. 使用增量更新

**问题**：每次运行都全库扫描，浪费时间。

**解决方案**：
```bash
# 只处理特定目录
python scripts/kb.py audit --path "./my-kb/01-前端开发"

# 只处理最近修改的文件（需要结合 find）
# Linux/macOS
find ./my-kb -name "*.md" -mtime -7 -exec python scripts/kb.py validate --path {} \;

# Windows PowerShell
Get-ChildItem -Path "./my-kb" -Filter "*.md" -Recurse |
  Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-7) } |
  ForEach-Object { python scripts/kb.py validate --path $_.FullName }
```

### 2. 使用 dry-run 预览

**问题**：不确定修改范围，直接运行可能误操作。

**解决方案**：
```bash
# 预览模式，不实际修改文件
python scripts/kb.py fix-tags --kb-root "./my-kb" --dry-run
python scripts/kb.py fix-link --kb-root "./my-kb" --dry-run
python scripts/kb.py fix-fm --kb-root "./my-kb" --dry-run
```

### 3. 分批处理

**问题**：大知识库一次性处理太慢或内存不足。

**解决方案**：
```bash
# 按分类分批处理
for dir in ./my-kb/0*/; do
  echo "处理: $dir"
  python scripts/kb.py audit --path "$dir"
done

# 按文件数量分批（Linux/macOS）
find ./my-kb -name "*.md" | split -l 100 - batch_
for f in batch_*; do
  cat "$f" | xargs python scripts/kb.py validate
done
```

### 4. 关闭不必要的检查

**问题**：validate 命令检查项太多，速度慢。

**解决方案**：
```bash
# 只检查 Frontmatter（跳过结构和排版检查）
python scripts/kb.py validate --kb-root "./my-kb" --check frontmatter

# 只检查死链
python scripts/kb.py validate --kb-root "./my-kb" --check links

# 跳过严格模式（更快）
python scripts/kb.py validate --kb-root "./my-kb"
```

---

## 🚀 各命令优化技巧

### init 命令

**优化点**：
1. **使用默认主题**：避免复杂的主题定制
2. **减少初始笔记数**：先创建骨架，后续逐步添加
3. **使用 SSD**：文件创建密集型操作，SSD 比 HDD 快 5-10 倍

```bash
# 快速初始化（只创建骨架）
python scripts/kb.py init --name "我的知识库" --path "./my-kb" --theme "全栈+AI" --minimal
```

### audit 命令

**优化点**：
1. **指定目录**：只检查需要的目录
2. **跳过详细输出**：使用 `--quiet` 只显示统计
3. **缓存结果**：结果变化不大时，减少运行频率

```bash
# 只检查特定目录
python scripts/kb.py audit --path "./my-kb/01-前端开发"

# 安静模式（只显示统计）
python scripts/kb.py audit --kb-root "./my-kb" --quiet

# 输出 JSON 格式（便于程序处理）
python scripts/kb.py audit --kb-root "./my-kb" --format json
```

### validate 命令

**优化点**：
1. **选择检查项**：只检查需要的项目
2. **跳过严格模式**：非严格模式更快
3. **并行处理**：多进程并行验证

```bash
# 只检查 Frontmatter
python scripts/kb.py validate --kb-root "./my-kb" --check frontmatter

# 只检查链接
python scripts/kb.py validate --kb-root "./my-kb" --check links

# 非严格模式（更快）
python scripts/kb.py validate --kb-root "./my-kb"
```

### fix-fm 命令

**优化点**：
1. **使用 dry-run**：先预览修改范围
2. **指定目录**：只处理需要的目录
3. **备份文件**：修改前备份，便于回滚

```bash
# 预览模式
python scripts/kb.py fix-fm --kb-root "./my-kb" --dry-run

# 只处理特定目录
python scripts/kb.py fix-fm --path "./my-kb/01-前端开发"

# 备份原文件
python scripts/kb.py fix-fm --kb-root "./my-kb" --backup
```

### fix-link 命令

**优化点**：
1. **调整阈值**：只修复高频死链，减少创建笔记数
2. **使用 dry-run**：先预览要创建的笔记
3. **分批修复**：阈值从高到低逐步修复

```bash
# 只修复引用 ≥10 次的死链
python scripts/kb.py fix-link --kb-root "./my-kb" --threshold 10

# 预览模式
python scripts/kb.py fix-link --kb-root "./my-kb" --dry-run

# 逐步降低阈值
python scripts/kb.py fix-link --kb-root "./my-kb" --threshold 20
python scripts/kb.py fix-link --kb-root "./my-kb" --threshold 10
python scripts/kb.py fix-link --kb-root "./my-kb" --threshold 5
```

### fix-tags 命令

**优化点**：
1. **使用 dry-run**：先预览标签变更
2. **指定目录**：只处理需要的目录
3. **跳过备份**：不需要备份时跳过

```bash
# 预览模式
python scripts/kb.py fix-tags --kb-root "./my-kb" --dry-run

# 只处理特定目录
python scripts/kb.py fix-tags --path "./my-kb/01-前端开发"

# 输出变更报告
python scripts/kb.py fix-tags --kb-root "./my-kb" --report
```

### standardize 命令

**优化点**：
1. **分步骤执行**：先单独运行各步骤，确认无误后再一键标准化
2. **使用 dry-run**：预览所有变更
3. **调整阈值**：降低死链修复阈值，减少创建笔记数

```bash
# 分步骤执行（推荐大知识库）
python scripts/kb.py fix-fm --kb-root "./my-kb" --dry-run
python scripts/kb.py fix-fm --kb-root "./my-kb"

python scripts/kb.py fix-link --kb-root "./my-kb" --threshold 10 --dry-run
python scripts/kb.py fix-link --kb-root "./my-kb" --threshold 10

python scripts/kb.py fix-tags --kb-root "./my-kb" --dry-run
python scripts/kb.py fix-tags --kb-root "./my-kb"

python scripts/kb.py moc --category "前端开发" --path "./my-kb/01-前端开发"

python scripts/kb.py audit --kb-root "./my-kb"
```

---

## 💾 内存优化

### 问题症状

- 处理大知识库时内存占用持续增长
- 程序崩溃或被系统杀死
- 系统变得非常慢

### 优化方法

#### 1. 使用生成器而非列表

```python
# 不好的做法：一次性加载所有文件到内存
files = list(Path(".").rglob("*.md"))
for f in files:
    process(f)

# 好的做法：使用生成器，逐个处理
for f in Path(".").rglob("*.md"):
    process(f)
```

#### 2. 及时释放大对象

```python
def process_library(path):
    data = load_all_files(path)  # 大对象
    result = analyze(data)
    del data  # 及时释放
    return result
```

#### 3. 逐行读取大文件

```python
# 不好的做法：一次性读取整个文件
with open("large.md", "r", encoding="utf-8") as f:
    content = f.read()
    lines = content.split("\n")

# 好的做法：逐行读取
with open("large.md", "r", encoding="utf-8") as f:
    for line in f:
        process_line(line)
```

#### 4. 限制并发数

```python
from concurrent.futures import ThreadPoolExecutor

# 根据 CPU 核心数和内存限制并发数
max_workers = min(4, os.cpu_count() or 2)

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    results = list(executor.map(process_file, files))
```

---

## 📈 监控与分析

### 性能监控

```bash
# Linux/macOS：使用 time 命令测量执行时间
time python scripts/kb.py audit --kb-root "./my-kb"

# Windows PowerShell：使用 Measure-Command
Measure-Command { python scripts/kb.py audit --kb-root "./my-kb" }

# 使用 Python cProfile 分析性能瓶颈
python -m cProfile -s cumulative scripts/kb.py audit --kb-root "./my-kb" | head -30
```

### 内存监控

```bash
# Linux：使用 /usr/bin/time -v
/usr/bin/time -v python scripts/kb.py audit --kb-root "./my-kb"

# macOS：使用 activity monitor 或 ps
ps -o pid,rss,command -p <pid>

# Windows：使用任务管理器或 Get-Process
Get-Process python | Select-Object Id, WorkingSet, CPU
```

### 生成性能报告

```python
# 使用 cProfile 生成性能报告
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# 运行代码
main()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats("cumulative")
stats.print_stats(30)  # 显示前 30 个函数
stats.dump_stats("performance.prof")  # 保存报告
```

---

## 🔧 高级优化

### 1. 使用 PyPy 替代 CPython

PyPy 对 CPU 密集型操作有显著性能提升：

```bash
# 安装 PyPy
# 参考：https://www.pypy.org/download.html

# 使用 PyPy 运行
pypy3 scripts/kb.py audit --kb-root "./my-kb"
```

> **注意**：PyPy 对某些 C 扩展支持不完善，建议先测试兼容性。

### 2. 使用多进程并行

```python
from multiprocessing import Pool, cpu_count

def process_directory(dir_path):
    # 处理单个目录
    return audit_directory(dir_path)

if __name__ == "__main__":
    directories = ["./my-kb/01-前端开发", "./my-kb/02-后端开发", ...]

    # 使用所有 CPU 核心
    with Pool(cpu_count()) as pool:
        results = pool.map(process_directory, directories)
```

### 3. 文件系统优化

- **使用 SSD**：文件操作密集型任务，SSD 比 HDD 快 5-10 倍
- **关闭杀毒软件实时扫描**：将项目目录添加到排除列表
- **使用本地磁盘**：避免网络驱动器或云同步目录
- **整理磁盘碎片**：HDD 用户定期整理碎片

### 4. Python 优化

```bash
# 使用最新版本的 Python（3.11+ 有显著性能提升）
python --version

# 使用 -O 选项优化（移除断言和调试）
python -O scripts/kb.py audit --kb-root "./my-kb"

# 设置 PYTHONOPTIMIZE 环境变量
export PYTHONOPTIMIZE=1  # Linux/macOS
$env:PYTHONOPTIMIZE=1     # Windows PowerShell
```

---

## 📋 性能优化检查清单

- [ ] 使用增量更新，避免全库扫描
- [ ] 使用 dry-run 预览变更范围
- [ ] 大知识库分批处理
- [ ] 关闭不必要的检查项
- [ ] 调整死链修复阈值
- [ ] 使用 SSD 存储
- [ ] 关闭杀毒软件实时扫描（项目目录）
- [ ] 使用 Python 3.11+
- [ ] 监控内存使用，及时释放大对象
- [ ] 使用生成器而非列表
- [ ] 限制并发数，避免内存溢出
- [ ] 定期运行性能基准测试
- [ ] 使用 cProfile 分析性能瓶颈

---

## 📞 相关文档

- [DEBUGGING.md](DEBUGGING.md) - 调试与问题排查
- [TESTING.md](TESTING.md) - 测试策略与指南
- [ARCHITECTURE.md](ARCHITECTURE.md) - 项目架构设计
- [FAQ.md](FAQ.md) - 常见问题

---

> **最后更新**：2026-08-30
>
> **适用版本**：v3.1.0
