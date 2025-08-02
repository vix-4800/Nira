from agent.core.persistent_memory import PersistentMemory


class TestPersistentMemory:
    def test_set_get_delete(self, tmp_path):
        db = tmp_path / "mem.db"
        mem = PersistentMemory(db)
        mem.set("foo", "bar")
        assert mem.get("foo") == "bar"
        mem.set("foo", "baz")
        assert mem.get("foo") == "baz"
        mem.delete("foo")
        assert mem.get("foo") is None
        mem.set("a", "1")
        mem.set("b", "2")
        assert mem.all() == {"a": "1", "b": "2"}
        mem.close()
