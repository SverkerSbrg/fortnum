from fortnum import Fortnum


class Apple(Fortnum):
    pass


apple = Fortnum("Apple")


class StoneFruits(Fortnum):
    peach = Fortnum("Peach")
    plum = Fortnum("Plum")
    lychee = Fortnum("Lychee")
    mango = Fortnum("Mango")

print(list(StoneFruits)) # [Peach, Plum, Lychee, Mango]
print(StoneFruits.peach.parent)  # StoneFruits


class TropicalFruits(Fortnum):
    lychee = StoneFruits.lychee
    mango = StoneFruits.mango
    pineapple = Fortnum("Pineapple")

print(StoneFruits.mango in TropicalFruits)  # True
print(TropicalFruits.pineapple in StoneFruits)  # False


class ExceptionLevels(Fortnum):
    info = Fortnum("Info")
    warning = Fortnum("Warning")
    error = Fortnum("Error")

print(ExceptionLevels.info > ExceptionLevels.error)  # False
print(max(ExceptionLevels.warning, ExceptionLevels.info))  # Warning
print(sorted([ExceptionLevels.warning, ExceptionLevels.info, ExceptionLevels.warning]))
# [Info, Warning, Warning]


