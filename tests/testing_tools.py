from dataclasses import dataclass
from typing import Type


@dataclass(frozen=True)
class WillRaise:
    exception_type: Type[Exception]

