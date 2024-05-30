import asyncio 




class Context():
	_current_type = {}

	def __init__(self):
		pass

	@classmethod
	def set_current_type(cls,current_type):
		task_id = get_task_id()
		cls._current_type[task_id] =  current_type

	@classmethod
	def get_current_type(cls):
		task_id = get_task_id()
		return cls._current_type[task_id]


context = Context()


def get_task_id() -> int:
    """Return the ID of the current asyncio task."""
    try:
        return id(asyncio.current_task())
    except RuntimeError:
        return 0