import sys
import operator as op

#-- Debemos tener en cuenta si no meten ningun argumento
if len(sys.argv) != 4:
    sys.exit("Usage Error:  python3 calcu.py operacion operando operando")

operation = sys.argv[1]

#-- Debemos tener en cuenta de que me esta enviando int o float.
try:
    operator_1 = int(sys.argv[2])
    operator_2 = int(sys.argv[3])
except ValueError:
    sys.exit("Operands must be numbers")

if operator_2 == 0:
    sys.exit ("Can't divided by 0")

#-- Lógica del negocio cocina
dic = {
    "suma": op.add,
    "resta": op.sub,
    "multiplicacion": op.mul,
    "division": op.truediv,
    "xor": op.xor
}

#-- Check
if operation not in dic:
    sys.exit ("Operación no Válida")

resultado = dic[operation](operator_1, operator_2)

print(resultado)
