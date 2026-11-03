.PHONY: help test lint fmt baseline

help:            ## 列出可用目标
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | sed 's/:.*##/\t/'

test:            ## 跑单元测试
	python -m pytest

lint:            ## 静态检查（ruff）
	python -m ruff check .

fmt:             ## 自动格式化
	python -m ruff format .

baseline:        ## 对指定项目做工程底座自检：make baseline ROOT=../myproj
	python scripts/check_baseline.py --root $(or $(ROOT),.)
