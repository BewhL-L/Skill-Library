# 四大技术栈项目模板与 README 模板

> 供 code-practice-generator 生成代码实践项目时参考，按对应技术栈的模板执行。

---

## 通用项目结构

```
project-name/
├── README.md              # 项目说明（概念介绍、运行步骤、练习指引）
├── 项目配置文件            # pom.xml / package.json / requirements.txt 等
├── src/                   # 源代码
│   ├── main/              # 核心演示代码
│   └── exercise/          # 练习题（只有题目，答案在 solutions/）
├── solutions/             # 练习题答案与解析
│   ├── basic/
│   ├── advanced/
│   └── challenge/
└── docs/                  # 补充文档（可选）
```

---

## README.md 模板

```markdown
# 项目名称

## 概念说明
本项目演示 [[技术概念]] 的核心用法。
- 对应知识库笔记：[[笔记链接]]
- 难度：⭐⭐⭐
- 预计学习时间：2 小时

## 环境要求
- 技术栈版本：XXX
- 其他依赖：XXX

## 快速运行
```bash
# 步骤1：安装依赖
XXX
# 步骤2：启动项目
XXX
# 步骤3：验证结果
XXX
```

## 核心演示
- 演示1：XXX（对应 src/main/xxx）
- 演示2：XXX

## 练习题
### 基础题（3道）
1. XXX
2. XXX
3. XXX

### 进阶题（2道）
1. XXX
2. XXX

### 挑战题（1道）
1. XXX

答案见 `solutions/` 目录。

## 学习建议
1. 先运行核心演示，理解概念用法
2. 完成基础题，巩固基本操作
3. 尝试进阶题，深入理解机制
4. 挑战题检验掌握程度
```

---

## Java / Spring Boot 项目模板

```
demo-project/
├── README.md
├── pom.xml
├── src/main/java/com/example/demo/
│   ├── DemoApplication.java
│   ├── controller/
│   ├── service/
│   ├── entity/
│   └── config/
├── src/main/resources/
│   └── application.yml
├── src/test/java/          # 练习题
└── solutions/
```

**pom.xml 关键依赖**：
- spring-boot-starter-web
- spring-boot-starter-data-jpa / mybatis-spring-boot-starter
- mysql-connector-java
- lombok
- spring-boot-starter-test

**application.yml 关键配置**：
```yaml
server:
  port: 8080
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/demo?useUnicode=true&characterEncoding=utf8
    username: root
    password: root
    driver-class-name: com.mysql.cj.jdbc.Driver
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
```

---

## Vue3 + TypeScript 项目模板

```
demo-project/
├── README.md
├── package.json
├── vite.config.ts
├── tsconfig.json
├── index.html
├── src/
│   ├── main.ts
│   ├── App.vue
│   ├── components/
│   ├── composables/
│   └── types/
├── exercises/               # 练习题
└── solutions/
```

**package.json 关键依赖**：
- vue ^3.4
- vue-router ^4
- pinia ^2
- axios ^1
- typescript ^5
- vite ^5
- vitest ^1

**vite.config.ts 关键配置**：
```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true
      }
    }
  }
})
```

---

## Python / FastAPI 项目模板

```
demo-project/
├── README.md
├── requirements.txt
├── main.py
├── app/
│   ├── __init__.py
│   ├── api/
│   ├── models/
│   ├── services/
│   └── config.py
├── exercises/
└── solutions/
```

**requirements.txt 关键依赖**：
```
fastapi==0.104.0
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pytest==7.4.3
httpx==0.25.2
```

**main.py 入口**：
```python
from fastapi import FastAPI
from app.api import router

app = FastAPI(title="Demo API", version="1.0.0")
app.include_router(router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
```

**启动命令**：
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## AI 应用 / LangChain 项目模板

```
demo-project/
├── README.md
├── requirements.txt
├── .env.example
├── main.py
├── src/
│   ├── chains/
│   ├── agents/
│   ├── retrievers/
│   └── utils/
├── data/                    # 示例数据
├── exercises/
└── solutions/
```

**requirements.txt 关键依赖**：
```
langchain==0.1.0
langchain-openai==0.0.2
langchain-community==0.0.10
chromadb==0.4.22
tiktoken==0.5.2
python-dotenv==1.0.0
fastapi==0.104.0
uvicorn==0.24.0
pypdf==3.17.1
unstructured==0.11.2
```

**.env.example**：
```
OPENAI_API_KEY=your-api-key
OPENAI_API_BASE=https://api.openai.com/v1
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

**main.py 入口**：
```python
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_openai import ChatOpenAI

load_dotenv()
app = FastAPI(title="AI Demo", version="1.0.0")

llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

@app.get("/chat")
async def chat(query: str):
    response = await llm.ainvoke(query)
    return {"response": response.content}
```

**启动命令**：
```bash
cp .env.example .env  # 然后编辑 .env 填入 API Key
uvicorn main:app --reload --port 8000
```
