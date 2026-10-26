.PHONY: help test cov lint compile audit clean

PYTHON ?= python
SKILL_PATH ?= .

help: ## 显示可用命令
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

test: ## 运行全部测试
	$(PYTHON) -m pytest tests -v

cov: ## 运行测试并生成覆盖率
	$(PYTHON) -m pytest tests --cov=scripts --cov-report=term-missing

lint: ## 静态检查（ruff）
	$(PYTHON) -m ruff check scripts tests || true

compile: ## 语法编译检查
	$(PYTHON) -m py_compile scripts/*.py

audit: ## 运行 skill-optimizer 健康检查
	$(PYTHON) ../skill-optimizer/scripts/audit-skill.py --path "$(SKILL_PATH)"

clean: ## 清理缓存与覆盖率产物
	rm -rf .pytest_cache .coverage htmlcov coverage.xml
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
