class Bin:
    def __init__(self, module: int, led: int, colour: list[int]):
        self.module = module
        self.led = led
        self.colour = colour


class Day:
    SUN = 0
    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    FRI = 5
    SAT = 6

    def __init__(self, value: int) -> None:
        self.value = value % 7

    @property
    def name(self) -> str:
        for name, value in self.__class__.__dict__.items():
            if value == self.value:
                return name
        return None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"

    def __lt__(self, other) -> int:  # noqa: ANN001
        if not isinstance(other, type(self)):
            raise NotImplementedError
        return self.value < other.value

    def __eq__(self, other) -> bool:  # noqa: ANN001
        if not isinstance(other, type(self)):
            raise NotImplementedError
        return self.value == other.value

    def __hash__(self) -> int:
        return hash((type(self), self.value))
    
    @staticmethod
    def sunday() -> "Day":
        return Day(value=Day.SUN)
    
    @staticmethod
    def monday() -> "Day":
        return Day(value=Day.MON)
    
    @staticmethod
    def tuesday() -> "Day":
        return Day(value=Day.TUE)
    
    @staticmethod
    def wednesday() -> "Day":
        return Day(value=Day.WED)
    
    @staticmethod
    def thursday() -> "Day":
        return Day(value=Day.THU)
    
    @staticmethod
    def friday() -> "Day":
        return Day(value=Day.FRI)
    
    @staticmethod
    def saturday() -> "Day":
        return Day(value=Day.SAT)
