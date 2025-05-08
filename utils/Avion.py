from dataclasses import dataclass, field
from typing import List

@dataclass
class Avion:
    id: int
    early: int
    ideal: int
    late: int
    early_penalty: float
    late_penalty: float
    time_diffs: List[int] = field(default_factory=list)
    landing_time: int = field(default=-1) # Inicializamos el tiempo de aterrizaje como no asignado

    def __str__(self):
        return (f"Avión {self.id + 1} | Ideal: {self.ideal} | "
                f"Penalización Temprana: {self.early_penalty} | "
                f"Penalización Tardía: {self.late_penalty} | "
                f"Aterrizaje: {self.landing_time if self.landing_time != -1 else 'No asignado'}")
