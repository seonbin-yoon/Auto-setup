from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, TypedDict


class Config(TypedDict):
    edk2_path: str
    qemu_path: str
    active_platform: str
    tool_chain_tag: str
    target_arch: str
    max_concurrent_thread_number: int
    project_name: str
    loader_name: str
    version: str
    function_in: str

class ShellTask(TypedDict):
    Message: str
    Path: str
    Exec: list[str]

class FunctionTask(TypedDict):
    Message: str
    Func: Callable[..., None]

class Edk2Check(TypedDict):
    Message: str
    Function: Callable[..., bool]
    Depends_on: str

class ShellCommand(TypedDict):
    Need_argu: bool
    Command: tuple[str, ...]
    Exec: Callable[..., Any]

@dataclass
class Contexts:
    config: Config
    distro: str
    home: str
    program: str

@dataclass
class TaskContexts:
    func_task_num: int
    shell_task_num: int
    total_num: int
