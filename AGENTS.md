# pnos-store AGENTS.md

> 本文件是 AI 代理进入 pnos-store 仓库时的首读指南。
> 生态级全局约束请参考 [根目录 AGENTS.md](../AGENTS.md)。

## 仓库定位

pnos-store 是 PandaNetOS 生态的**应用商店**，负责应用的分发、安装、管理。包含应用定义、安装脚本、版本管理等。

## 目录结构

```
pnos-store/
├── apps/           # 应用定义
├── scripts/        # 安装/管理脚本
└── README.md
```

## 注意事项

1. pnos-store 是应用场景级项目，不是独立 Agent
2. 应用安装脚本需遵循生态统一的工作目录规范
3. 应用配置需通过 pnos-spec 的配置标准管理

## 变更历史

| 日期 | 版本 | 变更内容 |
|---|---|---|
| 2026-09-16 | v1.0 | 初始版本 |
