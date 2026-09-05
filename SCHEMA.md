# app.yml 格式规范（二进制部署）

## 基础信息

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | ✅ | 唯一标识，小写字母+数字+连字符 |
| name | string | ✅ | 显示名称 |
| version | string | ✅ | 语义化版本 (MAJOR.MINOR.PATCH) |
| description | string | ✅ | 一句话描述 |
| author | string | ❌ | 作者 |
| homepage | string | ❌ | 项目主页 |
| icon | string | ✅ | 图标文件名，相对当前目录 |
| categories | string[] | ❌ | 分类标签 |
| tags | string[] | ❌ | 搜索标签 |

## 二进制下载配置 (binary)

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| download_url | string | ✅ | - | 二进制压缩包下载地址 |
| sha256 | string | ❌ | "" | SHA256 校验值，空则不校验 |
| binary_name | string | ✅ | - | 解压后的可执行文件名 |
| install_dir | string | ❌ | {{app_data}}/bin | 安装目录，支持变量 |

```yaml
binary:
  download_url: https://github.com/PandaNetOS/pk/releases/download/v0.1.0/pk-linux-amd64.tar.gz
  sha256: "abc123..."
  binary_name: pk
  install_dir: "{{app_data}}/bin"
```

## 运行配置 (run)

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| args | string[] | ❌ | [] | 启动参数 |
| env | array | ❌ | [] | 环境变量 |
| port | int | ✅ | - | 应用监听端口 |
| working_dir | string | ❌ | {{app_data}} | 工作目录，支持变量 |
| restart | string | ❌ | unless-stopped | 重启策略：always/unless-stopped/no |

### env
```yaml
env:
  - name: TZ
    value: "Asia/Shanghai"
```

## Web UI 配置 (web)

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| enabled | bool | ❌ | true | 是否启用 Web UI |
| type | string | ❌ | iframe | UI 类型：iframe/native |
| path | string | ❌ | / | UI 根路径 |
| ui_package | string | ❌ | - | 原生 UI 组件包地址（type=native 时必填） |

```yaml
web:
  enabled: true
  type: iframe
  path: /
```

## 健康检查 (health_check)

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| type | string | ✅ | - | http / tcp / command |
| url | string | ❌ | - | http 类型必填 |
| interval | string | ❌ | 30s | 检查间隔 |
| timeout | string | ❌ | 5s | 超时时间 |
| retries | int | ❌ | 3 | 重试次数 |

```yaml
health_check:
  type: http
  url: /health
  interval: 30s
  timeout: 5s
  retries: 3
```

## 依赖 (depends_on)

```yaml
depends_on: [pk]   # 依赖的应用 id 列表
```

pnos-runtime 启动应用时自动注入依赖应用的地址（如 `PK_URL=http://127.0.0.1:18080`）。

## 支持的变量

| 变量 | 含义 | 默认值 |
|------|------|--------|
| `{{app_data}}` | 应用数据根目录 | /pnos/data/apps |
| `{{media_dir}}` | 媒体目录 | /pnos/media |
| `{{data_dir}}` | pnos 数据目录 | /pnos/data |

## 完整示例

```yaml
id: my-app
name: 我的应用
version: 1.0.0
description: 示例应用
author: PandaNetOS
homepage: https://github.com/PandaNetOS/my-app
icon: icon.png
categories: [download]
tags: [demo]

binary:
  download_url: https://example.com/my-app-linux-amd64.tar.gz
  sha256: ""
  binary_name: my-app
  install_dir: "{{app_data}}/bin"

run:
  args: ["--config", "{{app_data}}/config.toml"]
  env:
    - name: TZ
      value: "Asia/Shanghai"
  port: 18090
  working_dir: "{{app_data}}"
  restart: unless-stopped

web:
  enabled: true
  type: iframe
  path: /

health_check:
  type: http
  url: /health
  interval: 30s
  timeout: 5s
  retries: 3

depends_on: []
```
