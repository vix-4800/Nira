import agent.tools.memory_manager_tool as mm
from agent.core.persistent_memory import PersistentMemory
from agent.tools import memory_manager


class TestMemoryManagerTool:
    def test_roundtrip(self, tmp_path, monkeypatch):
        db = tmp_path / "mem.db"

        def factory():
            return PersistentMemory(db)

        monkeypatch.setattr(mm, "PersistentMemory", factory)

        assert memory_manager.func("set", key="x", value="1") == "Saved"
        assert memory_manager.func("get", key="x") == "1"
        assert memory_manager.func("list") == {"x": "1"}
        assert memory_manager.func("delete", key="x") == "Deleted"
        assert memory_manager.func("get", key="x") == "(not found)"
