from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class VolleyballCourtConfiguration:
    width: int = 900  # [cm]
    length: int = 1800  # [cm]
    attack_line_distance: int = 300  # [cm] from the net
    centre_line: int = 0  # [cm], represents the middle of the court
    net_height: int = 243  # [cm] for men, 224 cm for women

    @property
    def vertices(self) -> List[Tuple[int, int]]:
        return [
            (0, self.width),  # Top-left corner, new-point-0
            (0, 0),  # Bottom-left corner, new-point-1
            (self.length / 2 - self.attack_line_distance, 0),  # Attack line left-bottom, new-point-2
            (self.length / 2 - self.attack_line_distance, self.width),  # Attack line left-top, new-point-3
            (self.length / 2, self.width),  # Center-top (net position), new-point-4
            (self.length / 2, 0),  # Center-bottom (net position), new-point-5
            (self.length / 2 + self.attack_line_distance, 0),  # Attack line right-bottom, new-point-6
            (self.length / 2 + self.attack_line_distance, self.width),  # Attack line right-top, new-point-7
            (self.length, self.width),  # Top-right corner, new-point-8
            (self.length, 0),  # Bottom-right corner, new-point-9
        ]

    edges: List[Tuple[int, int]] = field(default_factory=lambda: [
        (1, 2), (2, 10), (10, 9), (9, 1),  # Court boundary
        (5, 6),  # Net
        (3, 4),  # Left attack line
        (7, 8)  # Right attack line
    ])

    boundary_vertices_indices: List[int] = field(default_factory=lambda: [
        # vertices that define the court boundaries
        1, 2, 10, 9
    ])

    labels: List[str] = field(default_factory=lambda: [
        "new-point-0", # Top-Left
        "new-point-1", # Bottom-Left
        "new-point-2", # Left Attack Bottom
        "new-point-3", # Left Attack Top
        "new-point-4", # Net Top
        "new-point-5", # Net Bottom
        "new-point-6", # Right Attack Bottom
        "new-point-7", # Right Attack Top
        "new-point-8", # Top-Right
        "new-point-9", # Bottom-Right
    ])

    colors: List[str] = field(default_factory=lambda: [
        "#FF1493", "#FF1493", "#FF1493", "#FF1493",  # Court boundary
        "#00BFFF", "#00BFFF",  # Net
        "#FF6347", "#FF6347",  # Left attack line
        "#FF6347", "#FF6347"   # Right attack line
    ])

    # backup ###
    # @property
    # def vertices(self) -> List[Tuple[int, int]]:
    #     return [
    #         (0, 0),  # Bottom-left corner, new-point-1
    #         (0, self.width),  # Top-left corner, new-point-0
    #         (self.length, self.width),  # Top-right corner, new-point-8
    #         (self.length, 0),  # Bottom-right corner, new-point-9
    #         (self.length / 2, 0),  # Center-bottom (net position), new-point-5
    #         (self.length / 2, self.width),  # Center-top (net position), new-point-4
    #         (self.length / 2 - self.attack_line_distance, 0),  # Attack line left-bottom, new-point-2
    #         (self.length / 2 - self.attack_line_distance, self.width),  # Attack line left-top, new-point-3
    #         (self.length / 2 + self.attack_line_distance, 0),  # Attack line right-bottom, new-point-6
    #         (self.length / 2 + self.attack_line_distance, self.width)  # Attack line right-top, new-point-7
    #     ]

    # edges: List[Tuple[int, int]] = field(default_factory=lambda: [
    #     (1, 2), (2, 3), (3, 4), (4, 1),  # Court boundary
    #     (5, 6),  # Net
    #     (7, 8),  # Left attack line
    #     (9, 10)  # Right attack line
    # ])

    # labels: List[str] = field(default_factory=lambda: [
    #     "new-point-1", # Bottom-Left
    #     "new-point-0", # Top-Left
    #     "new-point-8", # Top-Right
    #     "new-point-9", # Bottom-Right
    #     "new-point-5", # Net Bottom
    #     "new-point-4", # Net Top
    #     "new-point-2", # Left Attack Bottom
    #     "new-point-3", # Left Attack Top
    #     "new-point-6", # Right Attack Bottom
    #     "new-point-7", # Right Attack Top
    # ])