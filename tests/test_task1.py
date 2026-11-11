import os
from pathlib import Path

import pytest

from task1 import copy_files, parse_args


def make(path: Path, text: str = "x") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def test_parse_args_default_dest():
    args = parse_args(["src"])
    assert args.source == Path("src")
    assert args.dest == Path("dist")


def test_parse_args_custom_dest():
    assert parse_args(["src", "out"]).dest == Path("out")


def test_copies_nested_files_sorted_by_extension(tmp_path):
    src, dest = tmp_path / "src", tmp_path / "out"
    make(src / "a.txt", "A")
    make(src / "sub" / "deep" / "b.PNG")
    make(src / "sub" / "c.py")

    copy_files(src, dest)

    assert (dest / "txt" / "a.txt").read_text() == "A"
    assert (dest / "png" / "b.PNG").exists()
    assert (dest / "py" / "c.py").exists()
    assert (src / "a.txt").exists()


def test_file_without_extension(tmp_path):
    src, dest = tmp_path / "src", tmp_path / "out"
    make(src / "Makefile")
    copy_files(src, dest)
    assert (dest / "no_extension" / "Makefile").exists()


def test_name_collisions_keep_both(tmp_path):
    src, dest = tmp_path / "src", tmp_path / "out"
    make(src / "a.txt", "1")
    make(src / "sub" / "a.txt", "2")
    copy_files(src, dest)
    contents = sorted(p.read_text() for p in (dest / "txt").iterdir())
    assert contents == ["1", "2"]


def test_dest_inside_source_is_not_recopied(tmp_path):
    src = tmp_path / "src"
    dest = src / "dist"
    make(src / "a.txt")
    copy_files(src, dest)
    copy_files(src, dest)
    assert sorted(p.name for p in (dest / "txt").iterdir()) == ["a.txt", "a_1.txt"]


@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores permissions")
def test_unreadable_dir_does_not_crash(tmp_path, capsys):
    src, dest = tmp_path / "src", tmp_path / "out"
    make(src / "ok.txt")
    locked = src / "locked"
    make(locked / "secret.txt")
    locked.chmod(0)
    try:
        copy_files(src, dest)
    finally:
        locked.chmod(0o755)
    assert (dest / "txt" / "ok.txt").exists()
    assert "locked" in capsys.readouterr().err
