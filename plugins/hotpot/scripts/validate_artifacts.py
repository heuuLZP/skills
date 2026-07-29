#!/usr/bin/env python3

import argparse
from pathlib import Path


REQUIRED_ENTRY_HEADINGS = (
    "## 入口与目标",
    "## 主流程",
    "## 分支场景",
    "## 失败与竞态",
    "## 非目标",
    "## 验收场景",
    "## 页面 / 行为改动",
    "## 本入口局部规则",
    "## 接口依赖",
    "## 验证",
    "## 业务边界",
    "## Metadata",
)


def validate_module(module_dir: Path) -> tuple[str, list[str]]:
    readme = module_dir / "README.md"
    shared_rules = module_dir / "shared-rules.md"
    entries_dir = module_dir / "entries"
    entries = sorted(entries_dir.glob("*.md")) if entries_dir.is_dir() else []
    single_files = [
        path
        for path in (module_dir / "use-cases.md", module_dir / "spec.md")
        if path.exists()
    ]
    bundle_signals = readme.exists() or shared_rules.exists() or entries_dir.exists()
    errors: list[str] = []

    if not bundle_signals:
        return "single-file", errors

    if not readme.exists():
        errors.append("entry-bundle 缺少 README.md")
    if not shared_rules.exists():
        errors.append("entry-bundle 缺少 shared-rules.md")
    if not entries:
        errors.append("entry-bundle 至少需要一个 entries/*.md")
    if single_files:
        names = ", ".join(path.name for path in single_files)
        errors.append(f"entry-bundle 与单文件产物同时存在：{names}")

    if errors:
        return "entry-bundle", errors

    readme_text = readme.read_text(encoding="utf-8")
    if "- Artifact mode: entry-bundle" not in readme_text:
        errors.append("README.md Metadata 缺少 Artifact mode: entry-bundle")

    shared_text = shared_rules.read_text(encoding="utf-8")
    for heading in ("## 共享行为规则", "## 共享待确认项", "## Metadata"):
        if heading not in shared_text:
            errors.append(f"shared-rules.md 缺少章节：{heading}")
    if "- Artifact mode: entry-bundle" not in shared_text:
        errors.append("shared-rules.md Metadata 缺少 Artifact mode: entry-bundle")

    for entry in entries:
        entry_text = entry.read_text(encoding="utf-8")
        if entry.name not in readme_text:
            errors.append(f"README.md 业务入口索引未引用 {entry.name}")
        for heading in REQUIRED_ENTRY_HEADINGS:
            if heading not in entry_text:
                errors.append(f"{entry.name} 缺少章节：{heading}")
        if "- Scope: module" not in entry_text:
            errors.append(f"{entry.name} Metadata 缺少 Scope: module")
        if "- Business entry:" not in entry_text:
            errors.append(f"{entry.name} Metadata 缺少 Business entry")
        if "- Artifact mode: entry-bundle" not in entry_text:
            errors.append(f"{entry.name} Metadata 缺少 Artifact mode: entry-bundle")

    return "entry-bundle", errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a Hotpot module's single-file or entry-bundle artifacts."
    )
    parser.add_argument("module_dir", type=Path)
    args = parser.parse_args()

    if not args.module_dir.is_dir():
        parser.error(f"module directory does not exist: {args.module_dir}")

    mode, errors = validate_module(args.module_dir)
    print(f"Artifact mode: {mode}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Hotpot artifact validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
