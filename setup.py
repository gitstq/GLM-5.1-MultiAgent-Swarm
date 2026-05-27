[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "glm-5.1-multiagent-swarm"
version = "1.0.0"
description = "GLM-5.1 Multi-Agent Collaboration System"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "gitstq", email = "https://github.com/gitstq"}
]
keywords = ["multi-agent", "glm", "collaboration", "ai", "swarm"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]

dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
]

[project.urls]
Homepage = "https://github.com/gitstq/GLM-5.1-MultiAgent-Swarm"
Repository = "https://github.com/gitstq/GLM-5.1-MultiAgent-Swarm"
Documentation = "https://github.com/gitstq/GLM-5.1-MultiAgent-Swarm#readme"

[project.scripts]
glm-swarm = "src.cli:main"

[tool.setuptools]
packages = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
asyncio_mode = "auto"
