import tempfile
from pathlib import Path


from agent.tools.file_manager_tool import file_manager


class TestFileManagerWrite:
    def test_write_and_append(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            path = Path(f.name)
        try:
            out = file_manager.func("write", path=str(path), text="hello")
            assert "Wrote to" in out
            assert path.read_text(encoding="utf-8") == "hello"

            out = file_manager.func("write", path=str(path), text=" world", append=True)
            assert "Wrote to" in out
            assert path.read_text(encoding="utf-8") == "hello world"
        finally:
            path.unlink()
