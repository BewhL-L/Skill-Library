#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""项目流程化 Skill 的可复用脚本包。

包含四个核心 CLI：
  - scan_project_facts: 扫描项目可信事实（行数/测试数/组件/依赖/服务）
  - validate_md:        校验学习指南 Markdown 结构（围栏/层级/表格/双链）
  - verify_zero_cut:    比对原文零删减
  - make_toc:           生成 GitHub slug 折叠目录
"""

__version__ = "1.0.0"
