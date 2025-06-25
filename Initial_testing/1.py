import time
import motoron
import sys
import termios
import tty
import select

# --- CONFIGURACIÓN DEL CONTROLADOR MOTORON ---
try:
    # Intenta inicializar el controlador en la dirección I2C 17
    mc1 = motoron.MotoronI2C(address=17)
    mc1.reinitialize()
    mc1.disable_crc()
    mc1.clear_reset_flag()
    print("Controlador Motoron configurado correctamente.")

except Exception as e:
    print(f"Error inicializando Motoron. Verifica la conexión I2C. Error: {e}")
    exit()

# --- FUNCIÓN PARA LEER TECLAS (SIN BLOQUEO) ---
def get_key_nonblocking(timeout=0.1):
    """Obtiene una tecla presionada por el usuario sin detener el programa."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setraw(fd)
    try:
        rlist, _, _ = select.select([sys.stdin], [], [], timeout)
        if rlist:
            return sys.stdin.read(1).lower()
        return None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

# --- FUNCIONES DE CONTROL DE MOTORES ---
def set_motors(speed1, speed2, speed3):
    """Establece la velocidad para cada motor."""
    mc1.set_speed(1, speed1)
    mc1.set_speed(2, speed2)
    mc1.set_speed(3, speed3)

def stop_motors():
    """Detiene todos los motores."""
    set_motors(0, 0, 0)

# --- PROGRAMA PRINCIPAL ---
if __name__ == "__main__":
    try:
        # Configuración inicial de los motores
        for motor in range(1, 4):
            mc1.set_max_acceleration(motor, 80)
            mc1.set_max_deceleration(motor, 300)

        speed = 800  # Velocidad base para los movimientos

        print("""
=========== CONTROL MANUAL DE MOTORES ===========

Usa las siguientes teclas para mover el robot:

  W: Adelante      S: Atrás
  A: Izquierda     D: Derecha
  Q: Diagonal Izq. E: Diagonal Der.
  
  P: Salir
-------------------------------------------------
Mantén presionada una tecla para mover el robot.
        """)

        last_key_time = 0

        while True:
            key = get_key_nonblocking()

            if key:
                if key == 'p':
                    print("⛔ Saliendo...")
                    break
                
                last_key_time = time.time() # Registra la última vez que se presionó una tecla
                
                # Asigna velocidades según la tecla presionada
                if key == 'w':
                    set_motors(speed, speed, speed)
                elif key == 's':
                    set_motors(-speed, -speed, -speed)
                elif key == 'a':
                    set_motors(0, speed, 0) # Ajusta según la cinemática de tu robot
                elif key == 'd':
                    set_motors(speed, 0, 0) # Ajusta según la cinemática de tu robot
                elif key == 'q':
                    set_motors(0, speed, speed)
                elif key == 'e':
                    set_motors(speed, 0, speed)
            
            # Si ha pasado más de 0.2 segundos sin presionar una tecla, detiene los motores
            if time.time() - last_key_time > 0.2:
                stop_motors()

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
    except Exception as e:
        print(f"\nHa ocurrido un error: {e}")
    finally:
        # Asegura que los motores se detengan al finalizar
        print("Deteniendo motores...")
        stop_motors()
        print("Programa finalizado.")