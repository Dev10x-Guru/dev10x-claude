"""Tests for the --summary flag on `dev10x permission` subcommands."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from dev10x.commands.permission import clean, update_paths


@pytest.fixture
def project_with_settings(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Build a temporary project with settings files and a fake plugin cache.

    Patches Path.home, find_config, and detect_latest_version on
    update_paths so the tests stay isolated from the real environment.
    """
    cache = tmp_path / ".claude" / "plugins" / "cache" / "Dev10x-Guru" / "Dev10x"
    (cache / "0.10.0").mkdir(parents=True)
    (cache / "0.20.0").mkdir(parents=True)

    config_dir = tmp_path / ".claude" / "memory" / "Dev10x"
    config_dir.mkdir(parents=True)
    config_path = config_dir / "projects.yaml"
    config_path.write_text(
        f"plugin_cache: {cache}\nroots: []\ninclude_user_settings: true\nbase_permissions: []\n"
    )

    user_settings = tmp_path / ".claude" / "settings.local.json"
    user_settings.write_text(
        json.dumps(
            {
                "permissions": {
                    "allow": [
                        f"Bash({cache}/0.10.0/foo:*)",
                        f"Bash({cache}/0.10.0/bar:*)",
                    ]
                }
            }
        )
    )

    fake_home = tmp_path
    monkeypatch.setattr(
        "dev10x.skills.permission.update_paths.Path.home",
        classmethod(lambda cls: fake_home),
    )
    monkeypatch.setattr(
        "dev10x.skills.permission.update_paths.find_config",
        lambda: config_path,
    )
    monkeypatch.setattr(
        "dev10x.skills.permission.update_paths.detect_latest_version",
        lambda _cache: "0.20.0",
    )
    monkeypatch.setattr(
        "dev10x.skills.permission.update_paths.find_settings_files",
        lambda **_kw: [user_settings],
    )
    return tmp_path


class TestUpdatePathsSummary:
    """`update-paths --summary` prints one line per changed file."""

    def test_summary_prints_per_file_count(self, project_with_settings: Path) -> None:
        runner = CliRunner()
        result = runner.invoke(update_paths, ["--summary"])

        assert result.exit_code == 0
        # One per-file count line, no decorative blank lines
        assert "settings.local.json: 2 replacements" in result.output

    def test_summary_omits_per_replacement_detail(
        self,
        project_with_settings: Path,
    ) -> None:
        runner = CliRunner()
        result = runner.invoke(update_paths, ["--summary"])

        # Verbose per-rule lines (`  0.10.0 -> 0.20.0`) should not appear
        assert "  0.10.0 -> 0.20.0" not in result.output

    def test_default_mode_keeps_full_detail(
        self,
        project_with_settings: Path,
    ) -> None:
        runner = CliRunner()
        result = runner.invoke(update_paths, [])

        assert result.exit_code == 0
        # Default output includes per-file headers and detail
        assert "0.10.0 -> 0.20.0" in result.output


class TestCleanSummary:
    """`clean --summary` prints one line per changed file."""

    @pytest.fixture
    def project_with_clean_targets(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> Path:
        global_settings = tmp_path / ".claude" / "settings.json"
        global_settings.parent.mkdir(parents=True, exist_ok=True)
        global_settings.write_text(
            json.dumps({"permissions": {"allow": ["Bash(git log:*)", "Bash(git status:*)"]}})
        )

        config_dir = tmp_path / ".claude" / "memory" / "Dev10x"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_path = config_dir / "projects.yaml"
        project_root = tmp_path / "project"
        project_root.mkdir()
        config_path.write_text(
            f"plugin_cache: {tmp_path}/.claude/plugins/cache/Dev10x-Guru/Dev10x\n"
            f"roots: ['{project_root}']\n"
            f"base_permissions: []\n"
        )

        proj_settings = project_root / ".claude" / "settings.local.json"
        proj_settings.parent.mkdir()
        proj_settings.write_text(
            json.dumps(
                {
                    "permissions": {
                        "allow": [
                            "Bash(git log:*)",  # duplicate of global
                            "Bash(git status:*)",  # duplicate of global
                            "Bash(make test:*)",  # kept
                        ]
                    }
                }
            )
        )

        monkeypatch.setattr(
            "dev10x.skills.permission.clean_project_files.find_config",
            lambda: config_path,
        )
        monkeypatch.setattr(
            "dev10x.skills.permission.clean_project_files.GLOBAL_SETTINGS",
            global_settings,
        )
        monkeypatch.setattr(
            "dev10x.skills.permission.clean_project_files.find_settings_files",
            lambda **_kw: [proj_settings],
        )
        monkeypatch.setattr(
            "dev10x.skills.permission.clean_project_files.detect_current_version",
            lambda _cache: None,
        )
        return tmp_path

    def test_summary_prints_per_file_count(
        self,
        project_with_clean_targets: Path,
    ) -> None:
        runner = CliRunner()
        result = runner.invoke(clean, ["--summary", "--dry-run"])

        assert result.exit_code == 0
        assert "settings.local.json: 2 removed" in result.output
