import importlib.util
import tempfile
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PLUGIN_ROOT / "scripts" / "validate_artifacts.py"
SPEC = importlib.util.spec_from_file_location("validate_artifacts", SCRIPT_PATH)
validate_artifacts = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validate_artifacts)


REQUIRED_ENTRY_HEADINGS = "\n".join(
    validate_artifacts.REQUIRED_ENTRY_HEADINGS
)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def create_bundle(module_dir: Path, include_index: bool = True) -> None:
    entry_name = "01-admin-login.md"
    index = entry_name if include_index else "missing-entry.md"
    write(
        module_dir / "README.md",
        f"# Module\n\n## 业务入口\n\n{index}\n\n## Metadata\n\n"
        "- Artifact mode: entry-bundle\n",
    )
    write(
        module_dir / "shared-rules.md",
        "# Shared\n\n## 共享行为规则\n\n## 共享待确认项\n\n"
        "## 额外工作项（代码外）\n\n## Metadata\n\n"
        "- Artifact mode: entry-bundle\n",
    )
    write(
        module_dir / "entries" / entry_name,
        f"# Entry\n\n{REQUIRED_ENTRY_HEADINGS}\n\n"
        "- Scope: module\n"
        "- Business entry: 01-admin-login\n"
        "- Artifact mode: entry-bundle\n",
    )


class ArtifactValidatorTests(unittest.TestCase):
    def test_single_file_mode_remains_valid(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            module_dir = Path(temp_dir)
            write(module_dir / "use-cases.md", "# Use cases\n")
            write(module_dir / "spec.md", "# Spec\n")

            mode, errors = validate_artifacts.validate_module(module_dir)

            self.assertEqual("single-file", mode)
            self.assertEqual([], errors)

    def test_complete_entry_bundle_is_valid(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            module_dir = Path(temp_dir)
            create_bundle(module_dir)

            mode, errors = validate_artifacts.validate_module(module_dir)

            self.assertEqual("entry-bundle", mode)
            self.assertEqual([], errors)

    def test_entry_local_questions_heading_is_optional(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            module_dir = Path(temp_dir)
            create_bundle(module_dir)

            _, errors = validate_artifacts.validate_module(module_dir)

            self.assertFalse(any("本入口相关问题" in error for error in errors))

    def test_missing_required_entry_heading_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            module_dir = Path(temp_dir)
            create_bundle(module_dir)
            entry = module_dir / "entries" / "01-admin-login.md"
            entry_text = entry.read_text(encoding="utf-8")
            write(entry, entry_text.replace("## 接口依赖", "## 非必需标题"))

            _, errors = validate_artifacts.validate_module(module_dir)

            self.assertTrue(any("缺少章节：## 接口依赖" in error for error in errors))

    def test_missing_entry_external_work_heading_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            module_dir = Path(temp_dir)
            create_bundle(module_dir)
            entry = module_dir / "entries" / "01-admin-login.md"
            entry_text = entry.read_text(encoding="utf-8")
            write(
                entry,
                entry_text.replace(
                    "## 额外工作项（代码外）",
                    "## 非必需标题",
                ),
            )

            _, errors = validate_artifacts.validate_module(module_dir)

            self.assertTrue(
                any("缺少章节：## 额外工作项（代码外）" in error for error in errors)
            )

    def test_missing_shared_external_work_heading_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            module_dir = Path(temp_dir)
            create_bundle(module_dir)
            shared = module_dir / "shared-rules.md"
            shared_text = shared.read_text(encoding="utf-8")
            write(
                shared,
                shared_text.replace(
                    "## 额外工作项（代码外）",
                    "## 非必需标题",
                ),
            )

            _, errors = validate_artifacts.validate_module(module_dir)

            self.assertTrue(
                any(
                    "shared-rules.md 缺少章节：## 额外工作项（代码外）"
                    in error
                    for error in errors
                )
            )

    def test_partial_bundle_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            module_dir = Path(temp_dir)
            write(module_dir / "README.md", "# Module\n")

            _, errors = validate_artifacts.validate_module(module_dir)

            self.assertTrue(any("shared-rules.md" in error for error in errors))
            self.assertTrue(any("entries/*.md" in error for error in errors))

    def test_dual_sources_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            module_dir = Path(temp_dir)
            create_bundle(module_dir)
            write(module_dir / "spec.md", "# Spec\n")

            _, errors = validate_artifacts.validate_module(module_dir)

            self.assertTrue(any("同时存在" in error for error in errors))

    def test_unindexed_entry_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            module_dir = Path(temp_dir)
            create_bundle(module_dir, include_index=False)

            _, errors = validate_artifacts.validate_module(module_dir)

            self.assertTrue(any("未引用" in error for error in errors))


class SkillContractTests(unittest.TestCase):
    def test_legacy_work_area_terms_are_removed(self):
        forbidden = ("工作面", "Work Area", "work-area", ".last-work-area")
        files = list((PLUGIN_ROOT / "skills").glob("*/SKILL.md"))
        files.extend((PLUGIN_ROOT / "references").glob("*.md"))

        for path in files:
            text = path.read_text(encoding="utf-8")
            for term in forbidden:
                self.assertNotIn(term, text, f"{path} still contains {term}")

    def test_module_consumers_use_artifact_resolution(self):
        skills = (
            "hot-pre-analysis",
            "hot-use-cases",
            "hot-spec",
            "hot-plan",
            "hot-plan-review",
            "hot-check",
        )
        for skill in skills:
            text = (PLUGIN_ROOT / "skills" / skill / "SKILL.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("Artifact Resolution", text)

    def test_entry_templates_define_section_ownership(self):
        text = (PLUGIN_ROOT / "references" / "artifact-templates.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("## 业务入口文档包：模块 README", text)
        self.assertIn("## 业务入口文档包：共享规则", text)
        self.assertIn("## 业务入口文档包：Entry", text)
        self.assertIn("章节所有权", text)

    def test_spec_question_lifecycle_is_consistent(self):
        skill_text = (
            PLUGIN_ROOT / "skills" / "hot-spec" / "SKILL.md"
        ).read_text(encoding="utf-8")
        convention_text = (
            PLUGIN_ROOT / "references" / "shared-conventions.md"
        ).read_text(encoding="utf-8")
        template_text = (
            PLUGIN_ROOT / "references" / "artifact-templates.md"
        ).read_text(encoding="utf-8")
        combined = "\n".join((skill_text, convention_text, template_text))

        self.assertNotIn("preserve the section and resolved records", combined)
        self.assertNotIn("已有章节和已解决记录不得自动删除", combined)
        self.assertNotIn("问题解决后保留记录", combined)
        self.assertIn("统一删除整个问题区", combined)
        self.assertIn("`共享待确认项` 不采用删除式生命周期", combined)

    def test_plan_blocks_unconfirmed_blocking_questions(self):
        plan_text = (
            PLUGIN_ROOT / "skills" / "hot-plan" / "SKILL.md"
        ).read_text(encoding="utf-8")
        review_text = (
            PLUGIN_ROOT / "skills" / "hot-plan-review" / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn("`是否阻断：是` and is not `已确认`", plan_text)
        self.assertIn("blocking question is unconfirmed", review_text)

    def test_architecture_decision_gate_is_consistent(self):
        conventions = (
            PLUGIN_ROOT / "references" / "shared-conventions.md"
        ).read_text(encoding="utf-8")
        plan = (PLUGIN_ROOT / "skills" / "hot-plan" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        review = (
            PLUGIN_ROOT / "skills" / "hot-plan-review" / "SKILL.md"
        ).read_text(encoding="utf-8")
        check = (PLUGIN_ROOT / "skills" / "hot-check" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("高影响架构变更", conventions)
        self.assertIn("用户确认的“架构决策摘要”", plan)
        self.assertIn("停止生成 `plan.md`", plan)
        self.assertIn("缺失列为阻断 finding", review)
        self.assertIn("架构决策依据", check)

    def test_architecture_handoff_is_manual(self):
        guarded_files = (
            PLUGIN_ROOT / "references" / "shared-conventions.md",
            PLUGIN_ROOT / "skills" / "hot-pre-analysis" / "SKILL.md",
            PLUGIN_ROOT / "skills" / "hot-module-split" / "SKILL.md",
            PLUGIN_ROOT / "skills" / "hot-plan" / "SKILL.md",
            PLUGIN_ROOT / "skills" / "hot-plan-review" / "SKILL.md",
            PLUGIN_ROOT / "skills" / "hot-check" / "SKILL.md",
        )
        combined = "\n".join(path.read_text(encoding="utf-8") for path in guarded_files)

        self.assertIn("$arch-coach decide", combined)
        self.assertIn("不自动调用", combined)
        self.assertIn("不读取固定", combined)


if __name__ == "__main__":
    unittest.main()
