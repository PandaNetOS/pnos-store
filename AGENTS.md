# pnos-store AGENTS.md

> 本文件是 AI 代理进入 pnos-store 仓库时的首读指南。
> 生态级全局约束请参考 [根目录 AGENTS.md](../AGENTS.md)。

## 仓库定位

pnos-store 是 PandaNetOS 生态的**官方应用商店**数据源（系统级项目，不是独立 Agent），负责应用的分发、安装、版本管理，是 pnos-runtime 应用商店的数据来源。

## 目录结构

```
pnos-store/
├── apps/               # 应用定义：apps/{app-id}/app.yml + icon.png
│   ├── pk/
│   ├── spde/
│   └── pdc/
├── index.json          # 应用索引（version、图标、分类）
├── SCHEMA.md           # app.yml 格式规范
├── scripts/            # 版本同步等辅助脚本
└── README.md
```

## 注意事项

1. pnos-store 是系统级数据仓库，不是独立 Agent
2. 新增/更新应用需同时维护 `apps/{id}/app.yml` 与 `index.json`，格式遵循 SCHEMA.md
3. 应用安装/运行须遵循生态统一的工作目录规范（由 pnos-runtime 执行安装）

## 变更历史

| 日期 | 版本 | 变更内容 |
|---|---|---|
| 2026-09-16 | v1.0 | 初始版本 |
| 2026-09-29 | v1.1 | 目录结构对齐实际（index.json/SCHEMA.md），定位明确为系统级商店数据源 |
