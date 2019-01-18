from fortnum import Fortnum


class Apple(Fortnum):
    pass


apple = Fortnum("Apple")


class Fruits(Fortnum):
    apple = Fortnum("Apple")
    pear = Fortnum("Pear")
    banana = Fortnum("Banana")
    mango = Fortnum("Mango")

print(list(Fruits)) # --> [Apple, Pear, Banana, Mango]


class ExceptionLevels(Fortnum):
    info = Fortnum("Info")
    warning = Fortnum("Warning")
    error = Fortnum("Error")

print(ExceptionLevels.info > ExceptionLevels.error)  # False
print(max(ExceptionLevels.warning, ExceptionLevels.info))  # Warning
print(sorted([ExceptionLevels.warning, ExceptionLevels.info, ExceptionLevels.warning]))  # [Info, Warning, Warning]


