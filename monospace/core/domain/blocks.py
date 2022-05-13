from dataclasses import dataclass, field
from typing import List


@dataclass
class Block:
    main: List[str] = field(default_factory=list)
    sides: List[List[str]] = field(default_factory=list)
    side_offset: int = 0
    block_offset: int = 1
    break_before: bool = False
