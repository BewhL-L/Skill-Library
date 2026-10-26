.PHONY: help install test lint format clean

help: ## 显示帮助
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## 安装依赖
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test: ## 运行测试
	python -m pytest tests/ -v

lint: ## 代码检查
	flake8 scripts/
	mypy scripts/

format: ## 代码格式化
	black scripts/
	isort scripts/

clean: ## 清理临时文件
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov
