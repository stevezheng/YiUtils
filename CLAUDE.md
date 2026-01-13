# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

YiUtils 是一个个人工具集合，包含 Python 和 Node.js 两部分的实用工具。项目主要用于网络配置生成和验证工具。

## Project Structure

```
YiUtils/
├── python/                 # Python 工具集
│   ├── v2rayn/            # V2RayN 配置生成器
│   │   └── gen_config.py  # 生成 Clash 配置文件
│   ├── x_ui/              # X-UI 相关工具
│   │   ├── gen_xray.py    # X-Ray 配置 JSON 生成
│   │   └── multi.py       # X-UI 数据库操作 (SQLAlchemy)
│   └── greencloud/        # IPv6 地址生成工具
│       ├── ipv6_gen.py    # IPv6 批量生成
│       ├── ipv6_gen_80.py # IPv6 生成 (80端口相关)
│       └── ipv6_gen_de.py # IPv6 生成 (德国相关)
├── node/                  # Node.js 工具集
│   └── index.js          # 验证工具 (QQ/邮箱/手机号)
└── .venv/                # Python 虚拟环境
```

## Common Commands

### Python 环境
```bash
# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
pip install -r python/requirements.txt

# 运行 V2RayN 配置生成器
cd python/v2rayn && python gen_config.py

# 运行 X-UI 配置生成
cd python/x_ui && python gen_xray.py

# 运行 IPv6 生成
cd python/greencloud && python ipv6_gen.py
```

### Node.js
```bash
cd node && npm install
```

## Architecture Notes

### Python 模块

**v2rayn/gen_config.py**
- `gen(local_port, remote_port, count, ip, uuid, path)` - 生成 Clash 格式的代理配置
- 返回元组：完整配置、listeners配置、proxies配置
- 输出三个 YAML 文件：`{prefix}_config.yml`, `{prefix}_listeners_config.yml`, `{prefix}_proxies_config.yml`

**x_ui/gen_xray.py**
- `get_ip_list(begin_ip, count, netmask)` - 使用 IPy 库生成 IP 地址列表
- `generate_xray_json(start_port, begin_ipv6, count, netmask)` - 生成 X-Ray JSON 配置
- 输出到 `result.json`
- 支持批量生成入站/出站配置和路由规则

**x_ui/multi.py**
- 使用 SQLAlchemy ORM 操作 x-ui.db SQLite 数据库
- `Inbounds` 模型定义入站配置表结构
- 包含示例的插入操作

**greencloud/ipv6_gen.py**
- 核心函数与 gen_xray.py 相同的 `get_ip_list()`
- 生成用于网络接口配置的 shell 命令输出
- 输出到 `ipv6.txt`

### 共享依赖

- `IPy` - IP 地址处理库，用于 IPv4/IPv6 地址运算和列表生成

### Node.js 模块

导出验证函数对象：
- `is.QQ(qq)` - QQ 号码验证
- `is.email(email)` - 邮箱验证（支持 qq/163/126 域名）
- `is.phone(phone)` - 手机号验证

## Development Notes

- Python 代码使用 f-string 格式化
- IPv6 地址计算使用位运算：`2 ** (128 - netmask)`
- 所有配置生成脚本都是可独立运行的
- 无测试框架配置
- 使用 `python/requirements.txt` 管理依赖
