from agent.core.nira_memory import NiraMemory
from agent.core.persistent_memory import PersistentMemory


def test_loads_persistent_memory(tmp_path):
    db_path = tmp_path / "memory.db"
    store = PersistentMemory(db_path)
    store.set("name", "Alice")

    memory = NiraMemory(persistent_memory=PersistentMemory(db_path))
    loaded = memory.load_memory_variables({})

    assert memory.persistent_memory_key in loaded
    assert loaded[memory.persistent_memory_key]["name"] == "Alice"
    assert memory.memory_variables == [memory.memory_key, memory.persistent_memory_key]
