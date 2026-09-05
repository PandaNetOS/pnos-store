# pnos-store

pnos 官方应用商店。包含所有官方应用的描述文件（app.yml）和图标。

## 仓库结构

```
pnos-store/
├── apps/
│   ├── pk/
│   │   ├── app.yml
│   │   └── icon.png
│   ├── spde/
│   │   ├── app.yml
│   │   └── icon.png
│   └── pdc/
│       ├── app.yml
│       └── icon.png
├── index.json       # 应用索引
├── SCHEMA.md        # app.yml 格式规范
└── README.md
```

## 提交新应用

1. 在 `apps/` 下创建 `{app-id}/` 目录
2. 编写 `app.yml`（参考 [SCHEMA.md](./SCHEMA.md)）
3. 添加 `icon.png`（建议 256x256）
4. 更新 `index.json`，添加应用条目
5. 提交 PR

## 官方应用

| ID | 名称 | 分类 | 说明 |
|----|------|------|------|
| pk | 调度主控台 | system/download | PandaNetOS 控制面，任务调度与节点管理 |
| spde | SPDE 下载节点 | download | 多协议下载执行引擎 |
| pdc | Peer 发现中心 | download/network | BitTorrent Peer 发现（Tracker+DHT+PEX） |

## 索引格式

`index.json` 由 pnos-runtime 拉取，用于展示应用列表。每个应用包含：

- `id`：唯一标识
- `name`：显示名称
- `version`：版本
- `description`：描述
- `icon`：图标相对路径
- `categories`：分类
- `app_yml`：app.yml 相对路径

## 许可证

MIT
