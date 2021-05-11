from enum import Enum


class Interval(Enum):
    KLINE1_M  = 60
    KLINE3_M  = KLINE1_M  * 3
    KLINE5_M  = KLINE1_M  * 5
    KLINE15_M = KLINE3_M  * 5
    KLINE30_M = KLINE15_M * 2
    KLINE1_H  = KLINE30_M * 2
    KLINE2_H  = KLINE1_H  * 2
    KLINE4_H  = KLINE2_H  * 2
    KLINE6_H  = KLINE2_H  * 3
    KLINE8_H  = KLINE4_H  * 2
    KLINE12_H = KLINE6_H  * 2
    KLINE1_D  = KLINE12_H * 2
    KLINE3_D  = KLINE1_D  * 3
    KLINE1_W  = KLINE1_D  * 7
    KLINE1_M  = KLINE1_D  * 30
