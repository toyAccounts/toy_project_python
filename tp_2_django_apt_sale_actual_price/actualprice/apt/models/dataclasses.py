from dataclasses import dataclass


@dataclass
class Region():
    signguCode: str
    emdCode: str
    ctprvnNm: str

@dataclass
class City(Region):
    signguNm: str