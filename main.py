import sys
import src.Tarea1 as tr
import src.Tarea2 as tr2
import src.Tarea3 as tr3
import src.Tarea4 as tr4

if __name__ == "__main__":
    argumento = sys.argv[1]
    if argumento == "tarea1":
        tr.mostrar()

    elif argumento == "tarea2":
        tr2.mostrar(float(sys.argv[2]))

    elif argumento == "tarea3":
        tr3.mostrar(float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]))
    
    elif argumento == "tarea4":
        tr4.mostrar(int(sys.argv[2]))
    