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


ENTRY_HEADINGS = "\n".join(validate_artifacts.ENTRY_HEADINGS)


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
        "# Shared\n\n## 共享行为规则\n\n## 共享待确认项\n\n## Metadata\n\n"
        "- Artifact mode: entry-bundle\n",
    )
    write(
        module_dir / "entries" / entry_name,
        f"# Entry\n\n{ENTRY_HEADINGS}\n\n"
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


if __name__ == "__main__":
    unittest.main()
