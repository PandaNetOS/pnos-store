#!/usr/bin/env python3
"""同步商店清单中的应用版本号。

数据源：各应用仓库的 GitHub「latest release」。
被 index.json 引用的每个应用，其仓库约定为 `<OWNER>/<app_id>`。

写回：
- index.json 中该应用的 version，以及顶层 updated_at
- apps/<id>/app.yml 中的顶层 version 字段

设计要点：只改 version 字段，不动 download_url（清单使用
`releases/latest/download/<asset>` 稳定别名，无需随版本改动）。
"""

import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.request

OWNER = "PandaNetOS"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""


def api(path: str):
    req = urllib.request.Request(f"https://api.github.com{path}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "pnos-store-sync")
    if TOKEN:
        req.add_header("Authorization", f"token {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def latest_version(repo: str):
    """返回去掉前缀 v 的版本号；无 release 返回 None。"""
    try:
        data = api(f"/repos/{OWNER}/{repo}/releases/latest")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    tag = (data.get("tag_name") or "").strip()
    tag = tag.lstrip("vV")
    return tag or None


def set_app_yml_version(path: str, version: str) -> bool:
    if not os.path.isfile(path):
        print(f"    ! 缺少 {path}，跳过")
        return False
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    changed = False
    for i, line in enumerate(lines):
        if re.match(r"^version\s*:", line):
            wanted = f"version: {version}\n"
            if line != wanted:
                lines[i] = wanted
                changed = True
            break
    if changed:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.writelines(lines)
    return changed


def main() -> int:
    index_path = os.path.join(ROOT, "index.json")
    with open(index_path, encoding="utf-8") as f:
        index = json.load(f)

    changed_apps = []
    for app in index.get("apps", []):
        app_id = app.get("id")
        if not app_id:
            continue
        try:
            version = latest_version(app_id)
        except Exception as e:  # noqa: BLE001 - 单个应用失败不应中断整体同步
            print(f"  ! {app_id}: 查询 latest release 失败: {e}")
            continue
        if not version:
            print(f"  - {app_id}: 无 release，跳过")
            continue

        if app.get("version") != version:
            print(f"  * {app_id}: {app.get('version')} -> {version}")
            app["version"] = version
            changed_apps.append(app_id)
        else:
            print(f"  = {app_id}: {version}（无变化）")

        app_yml = os.path.join(ROOT, app.get("app_yml", f"apps/{app_id}/app.yml"))
        if set_app_yml_version(app_yml, version):
            print(f"    app.yml: version -> {version}")

    if not changed_apps:
        print("无版本变更")
        return 0

    index["updated_at"] = datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    with open(index_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"已更新: {', '.join(changed_apps)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
