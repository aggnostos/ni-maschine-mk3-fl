__all__ = [
    "ROOT_NOTE",
    "CHORD_SETS",
    "SCALES",
]

# --------------------------------------------------------------------------------
# NOTES
# --------------------------------------------------------------------------------
# DO NOT CHANGE THE NOTE VALUES BELOW, UNLESS YOU KNOW WHAT YOU ARE DOING!

C1 = 0
CS1 = 1
D1 = 2
DS1 = 3
E1 = 4
F1 = 5
FS1 = 6
G1 = 7
GS1 = 8
A1 = 9
AS1 = 10
B1 = 11
C2 = 12
CS2 = 13
D2 = 14
DS2 = 15
E2 = 16
F2 = 17
FS2 = 18
G2 = 19
GS2 = 20
A2 = 21
AS2 = 22
B2 = 23
C3 = 24
CS3 = 25
D3 = 26
DS3 = 27
E3 = 28
F3 = 29
FS3 = 30
G3 = 31
GS3 = 32
A3 = 33
AS3 = 34
B3 = 35
C4 = 36
CS4 = 37
D4 = 38
DS4 = 39
E4 = 40
F4 = 41
FS4 = 42
G4 = 43
GS4 = 44
A4 = 45
AS4 = 46
B4 = 47
C5 = 48
CS5 = 49
D5 = 50
DS5 = 51
E5 = 52
F5 = 53
FS5 = 54
G5 = 55
GS5 = 56
A5 = 57
AS5 = 58
B5 = 59
C6 = 60
CS6 = 61
D6 = 62
DS6 = 63
E6 = 64
F6 = 65
FS6 = 66
G6 = 67
GS6 = 68
A6 = 69
AS6 = 70
B6 = 71
C7 = 72
CS7 = 73
D7 = 74
DS7 = 75
E7 = 76
F7 = 77
FS7 = 78
G7 = 79
GS7 = 80
A7 = 81
AS7 = 82
B7 = 83
C8 = 84
CS8 = 85
D8 = 86
DS8 = 87
E8 = 88
F8 = 89
FS8 = 90
G8 = 91
GS8 = 92
A8 = 93
AS8 = 94
B8 = 95
C9 = 96
CS9 = 97
D9 = 98
DS9 = 99
E9 = 100
F9 = 101
FS9 = 102
G9 = 103
GS9 = 104
A9 = 105
AS9 = 106
B9 = 107
C10 = 108
CS10 = 109
D10 = 110
DS10 = 111
E10 = 112
F10 = 113
FS10 = 114
G10 = 115
GS10 = 116
A10 = 117
AS10 = 118
B10 = 119
C11 = 120
CS11 = 121
D11 = 122
DS11 = 123
E11 = 124
F11 = 125
FS11 = 126
G11 = 127

ROOT_NOTE = C5

# --------------------------------------------------------------------------------
# CHORD SETS
# --------------------------------------------------------------------------------
# CHANGE THE NOTES INSIDE THE BRACKETS AS YOU PLEASE,YOU CAN EVEN ADD MORE THAN 4 NOTES FOR 7TH AND 9TH CHORDS!
# OR YOU CAN CREATE YOUR OWN CHORD SETS,
# JUST MAKE SURE THERE IS ALWAYS 16 CHORDS IN EACH CHORDSET!

MIN_1 = [  # MINOR 1
    [C4, C5, DS5, G5],  # 1
    [DS4, C5, DS5, G5],
    [F4, C4, F5, GS5],
    [G3, B4, D5, G5],
    [GS3, C5, DS5, G5],  # 5
    [DS4, AS4, DS5, G5],
    [G3, AS4, D5, G5],
    [AS3, AS4, D5, F5],
    [F3, A4, C5, F5],  # 9
    [GS3, C5, F5, GS5],
    [G3, C5, DS5, G5],
    [G3, B4, D5, G5],
    [F3, D4, F5, GS5],  # 13
    [D4, D5, F5, AS5],
    [D4, C5, D5, G5],
    [C4, C5, F5, G5],
]

MIN_2 = [  # MINOR 2
    [C4, G4, C5, DS5],
    [B3, G4, B4, DS5],
    [AS3, G4, C5, DS5],
    [G3, B4, D5, G5],
    [GS3, C5, DS5, G5],
    [DS4, AS4, DS5, G5],
    [G3, AS4, D5, G5],
    [AS3, AS4, D5, F5],
    [F3, A4, C5, F5],
    [GS3, C5, F5, GS5],
    [G3, C5, DS5, G5],
    [G3, B4, D5, G5],
    [C4, C5, DS5, G5],
    [F3, D4, F5, GS5],
    [AS3, D4, F5, AS5],
    [AS3, D4, D5, G5],
]

MIN_3 = [  # SYNTHWAVE
    [C4, G4, C5, D5, G5],
    [C4, G4, AS4, D5, F5],
    [D4, A4, C5, D5, F5],
    [D4, A5, C5, E5, G5],
    [E4, G4, C5, D5, G5],
    [D4, G4, AS4, D5, F5],
    [A3, A4, C5, D5, F5],
    [A3, A4, C5, E5, G5],
    [DS4, DS5, FS5, AS5],
    [DS4, CS5, F5, GS5],
    [CS4, CS5, F5, GS5],
    [DS4, F5, GS5, CS6],
    [CS4, F5, GS5, CS6],
    [C4, DS5, GS5, C6],
    [C4, DS5, G5, AS5],
    [AS3, D4, G5, AS5],
]

MIN_4 = [  # EPIC
    [CS3, D4, G4, AS4],
    [F3, C4, F4, A4],
    [G3, D4, G4, AS4],
    [AS3, F4, AS4, D5],
    [D3, A3, D4, F4],
    [C3, G3, C4, DS4],
    [F3, C4, F4, A4],
    [G3, D4, G4, AS4],
    [C4, C5, DS5, G5],
    [C4, C5, DS5, G5],
    [C4, C5, DS5, G5],
    [C4, C5, DS5, G5],
    [C4, C5, DS5, G5],
    [C4, C5, DS5, G5],
    [C4, C5, DS5, G5],
    [C4, C5, DS5, G5],
]

MAJ_1 = [
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
]

MAJ_2 = [
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
]

MAJ_3 = [
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
]

MAJ_4 = [
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
    [C4, C5, E5, G5],
]

# THERE MUST BE EXACTLY 8 CHORD SETS!
CHORD_SETS = [MIN_1, MIN_2, MIN_3, MIN_4, MAJ_1, MAJ_2, MAJ_3, MAJ_4]

# --------------------------------------------------------------------------------
# SCALES
# --------------------------------------------------------------------------------
# CHANGE THE NOTES INSIDE THE BRACKETS AS YOU PLEASE OR ADD YOU OWN,
# JUST MAKE SURE THAT THERE IS EXACTLY 16 NOTES IN EACH GROUP!

# fmt: off
SCALE_1 = [C4, D4, GS4, AS4, CS4, E4, A4, F4, B4, FS4, DS4, G4, C5, CS5, D5, G5]  # BATTERY
SCALE_2 = [C5, D5, DS5, F5, G5, GS5, AS5, C6, D6, DS6, F6, G6, GS6, AS6, C7, D7]  # MINOR
SCALE_3 = [C5, D5, E5, F5, G5, A5, B5, C6, D6, E6, F6, G6, A6, B6, C7, D7]        # MAJOR
SCALE_4 = [CS4, C4, FS4, AS7, E4, D4, AS4, GS4, C5, B4, A4, G4, CS5, G5, DS5, F5] # FPC
SCALE_5 = [C5, CS5, D5, DS5, E5, F5, FS5, G5, GS5, A5, AS5, B5, C6, CS6, D6, DS6] # CHROMATIC
SCALE_6 = [C5, CS5, E5, F5, G5, GS5, B5, C6, CS6, E6, F6, G6, GS6, B6, C7, CS7]	  # ARABIC
SCALE_7 = [C5, CS5, D5, DS5, E5, F5, FS5, G5, GS5, A5, AS5, B5, C6, CS6, D6, DS6] # CUSTOM
SCALE_8 = [C5, CS5, D5, DS5, E5, F5, FS5, G5, GS5, A5, AS5, B5, C6, CS6, D6, DS6] # CUSTOM
# fmt: on

# THERE MUST BE EXACTLY 8 SCALES!
SCALES = [SCALE_1, SCALE_2, SCALE_3, SCALE_4, SCALE_5, SCALE_6, SCALE_7, SCALE_8]
