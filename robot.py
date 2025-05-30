import time
import math
import motoron

class OmniRobot:
    def __init__(self):
        # Inicialización del controlador Motoron
        self.mc1 = motoron.MotoronI2C(address=16)
        self.setup_motoron()
        
        # Configuración de velocidades
        self.min_speed = 750    # Velocidad mínima de funcionamiento
        self.max_speed = 800    # Velocidad máxima
        self.default_speed = 750  # Velocidad por defecto
        
        # Ángulos de las ruedas (en radianes)
        # Para un robot de 3 ruedas omnidireccionales en configuración triangular
        self.wheel_angles = [
            math.radians(30),   # Motor 1 (trasera derecha) - 30°
            math.radians(150),  # Motor 2 (trasera izquierda) - 150°
            math.radians(270)   # Motor 3 (delantera) - 270°
        ]
        
    def setup_motoron(self):
        """Configuración inicial del Motoron"""
        self.mc1.reinitialize()
        self.mc1.disable_crc()
        self.mc1.clear_reset_flag()
        
        # Configuración de aceleración/deceleración
        for motor in range(1, 4):
            self.mc1.set_max_acceleration(motor, 80)
            self.mc1.set_max_deceleration(motor, 300)
    
    def set_motor_speeds(self, speed1, speed2, speed3):
        """Establece velocidades individuales de los motores"""
        # Función para ajustar velocidades al rango válido
        def adjust_speed(speed):
            if abs(speed) < self.min_speed and speed != 0:
                # Si la velocidad es menor al mínimo pero no cero, usar velocidad mínima
                return self.min_speed if speed > 0 else -self.min_speed
            elif abs(speed) > self.max_speed:
                # Si excede el máximo, limitarlo
                return self.max_speed if speed > 0 else -self.max_speed
            else:
                return speed
        
        speed1 = adjust_speed(speed1)
        speed2 = adjust_speed(speed2) 
        speed3 = adjust_speed(speed3)
        
        self.mc1.set_speed(1, int(speed1))  # Motor trasero derecho
        self.mc1.set_speed(2, int(speed2))  # Motor trasero izquierdo
        self.mc1.set_speed(3, int(speed3))  # Motor delantero
    
    def move_vector(self, vx, vy, vz):
        """
        Movimiento basado en vectores de velocidad
        vx: velocidad en X (adelante/atrás)
        vy: velocidad en Y (izquierda/derecha)
        vz: velocidad angular (rotación)
        """
        # Cálculo de velocidades para cada rueda usando cinemática inversa
        # Para ruedas omnidireccionales en configuración triangular
        
        speed1 = -0.5 * vx + 0.866 * vy + vz    # Rueda trasera derecha
        speed2 = -0.5 * vx - 0.866 * vy + vz    # Rueda trasera izquierda
        speed3 = vx + vz                         # Rueda delantera
        
        # Normalizar velocidades si exceden el máximo
        max_calculated = max(abs(speed1), abs(speed2), abs(speed3))
        if max_calculated > self.max_speed:
            factor = self.max_speed / max_calculated
            speed1 *= factor
            speed2 *= factor
            speed3 *= factor
        
        self.set_motor_speeds(speed1, speed2, speed3)
    
    def stop(self):
        """Detiene todos los motores"""
        self.set_motor_speeds(0, 0, 0)
    
    # Movimientos básicos predefinidos
    def move_forward(self, speed=850):
        """Mover hacia adelante"""
        self.move_vector(speed, 0, 0)
    
    def move_backward(self, speed=750):
        """Mover hacia atrás"""
        self.move_vector(-speed, 0, 0)
    
    def move_left(self, speed=750):
        """Mover hacia la izquierda (strafe)"""
        self.move_vector(0, -speed, 0)
    
    def move_right(self, speed=750):
        """Mover hacia la derecha (strafe)"""
        self.move_vector(0, speed, 0)
    
    def rotate_clockwise(self, speed=750):
        """Rotar en sentido horario"""
        self.move_vector(0, 0, speed)
    
    def rotate_counterclockwise(self, speed=750):
        """Rotar en sentido antihorario"""
        self.move_vector(0, 0, -speed)
    
    # Movimientos diagonales
    def move_forward_left(self, speed=750):
        """Mover diagonalmente adelante-izquierda"""
        self.move_vector(speed * 0.707, -speed * 0.707, 0)
    
    def move_forward_right(self, speed=750):
        """Mover diagonalmente adelante-derecha"""
        self.move_vector(speed * 0.707, speed * 0.707, 0)
    
    def move_backward_left(self, speed=750):
        """Mover diagonalmente atrás-izquierda"""
        self.move_vector(-speed * 0.707, -speed * 0.707, 0)
    
    def move_backward_right(self, speed=750):
        """Mover diagonalmente atrás-derecha"""
        self.move_vector(-speed * 0.707, speed * 0.707, 0)
    
    # Movimientos combinados (traslación + rotación)
    def move_forward_rotate_cw(self, linear_speed=750, angular_speed=750):
        """Mover adelante mientras rota en sentido horario"""
        self.move_vector(linear_speed, 0, angular_speed)
    
    def move_forward_rotate_ccw(self, linear_speed=750, angular_speed=750):
        """Mover adelante mientras rota en sentido antihorario"""
        self.move_vector(linear_speed, 0, -angular_speed)
    
    def strafe_left_rotate_cw(self, linear_speed=750, angular_speed=750):
        """Strafe izquierda mientras rota en sentido horario"""
        self.move_vector(0, -linear_speed, angular_speed)
    
    def strafe_right_rotate_ccw(self, linear_speed=750, angular_speed=750):
        """Strafe derecha mientras rota en sentido antihorario"""
        self.move_vector(0, linear_speed, -angular_speed)


# Control por consola
def console_control(robot):
    """Control interactivo por consola"""
    speed = robot.default_speed  # Usar velocidad por defecto del robot
    
    print("\n" + "="*50)
    print("🤖 CONTROL DE ROBOT OMNIDIRECCIONAL")
    print("="*50)
    print("CONTROLES BÁSICOS:")
    print("  w - Adelante          s - Atrás")
    print("  a - Izquierda        d - Derecha")
    print("  q - Rotar ↺          e - Rotar ↻")
    print("")
    print("DIAGONALES:")
    print("  r - Adelante-Derecha  t - Adelante-Izquierda")
    print("  f - Atrás-Derecha    g - Atrás-Izquierda")
    print("")
    print("COMBINADOS:")
    print("  u - Adelante + Rotar ↻    i - Adelante + Rotar ↺")
    print("  j - Izquierda + Rotar ↻   k - Derecha + Rotar ↺")
    print("")
    print("CONFIGURACIÓN:")
    print("  + - Aumentar velocidad    - - Disminuir velocidad")
    print("  v - Ver velocidad actual  h - Mostrar ayuda")
    print("  x - PARAR                 ESC/Ctrl+C - Salir")
    print("="*50)
    print(f"Velocidad actual: {speed} (mín: {robot.min_speed}, máx: {robot.max_speed})")
    print("Presiona una tecla para controlar el robot...")
    
    try:
        import termios
        import sys
        import tty
        
        def get_char():
            """Obtiene un carácter sin presionar Enter"""
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                char = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return char
        
        while True:
            char = get_char().lower()
            
            # Comandos de movimiento básico
            if char == 'w':
                print("↑ Adelante")
                robot.move_forward(speed)
            elif char == 's':
                print("↓ Atrás")
                robot.move_backward(speed)
            elif char == 'a':
                print("← Izquierda")
                robot.move_left(speed)
            elif char == 'd':
                print("→ Derecha")
                robot.move_right(speed)
            elif char == 'q':
                print("↺ Rotar antihorario")
                robot.rotate_counterclockwise(speed)
            elif char == 'e':
                print("↻ Rotar horario")
                robot.rotate_clockwise(speed)
            
            # Movimientos diagonales
            elif char == 'r':
                print("↗ Adelante-Derecha")
                robot.move_forward_right(speed)
            elif char == 't':
                print("↖ Adelante-Izquierda")
                robot.move_forward_left(speed)
            elif char == 'f':
                print("↘ Atrás-Derecha")
                robot.move_backward_right(speed)
            elif char == 'g':
                print("↙ Atrás-Izquierda")
                robot.move_backward_left(speed)
            
            # Movimientos combinados
            elif char == 'u':
                print("↑↻ Adelante + Rotar horario")
                robot.move_forward_rotate_cw(speed, speed)
            elif char == 'i':
                print("↑↺ Adelante + Rotar antihorario")
                robot.move_forward_rotate_ccw(speed, speed)
            elif char == 'j':
                print("←↻ Izquierda + Rotar horario")
                robot.strafe_left_rotate_cw(speed, speed)
            elif char == 'k':
                print("→↺ Derecha + Rotar antihorario")
                robot.strafe_right_rotate_ccw(speed, speed)
            
            # Control de velocidad
            elif char == '+' or char == '=':
                speed = min(robot.max_speed, speed + 25)
                print(f"⚡ Velocidad: {speed}")
            elif char == '-':
                speed = max(robot.min_speed, speed - 25)
                print(f"🐌 Velocidad: {speed}")
            elif char == 'v':
                print(f"📊 Velocidad actual: {speed} (rango: {robot.min_speed}-{robot.max_speed})")
            
            # Comandos especiales
            elif char == 'x' or char == ' ':
                print("⏹️  PARADO")
                robot.stop()
            elif char == 'h':
                console_control(robot)  # Mostrar ayuda de nuevo
                return
            elif char == '\x1b':  # ESC
                print("👋 Saliendo...")
                break
            elif ord(char) == 3:  # Ctrl+C
                break
            else:
                print(f"❓ Comando no reconocido: '{char}' - Presiona 'h' para ayuda")
            
            time.sleep(0.1)  # Pequeña pausa
    
    except ImportError:
        # Fallback para sistemas sin termios (Windows)
        print("⚠️  Control avanzado no disponible. Usando modo simple...")
        simple_console_control(robot)
    except Exception as e:
        print(f"Error: {e}")


def simple_console_control(robot):
    """Control simple por consola (compatible con Windows)"""
    speed = robot.default_speed
    
    print("\n🤖 CONTROL SIMPLE - Escribe comando + ENTER")
    print("Comandos: w(adelante) s(atrás) a(izq) d(der) q(rotar↺) e(rotar↻)")
    print("         +(vel+) -(vel-) x(parar) help(ayuda) quit(salir)")
    print(f"Velocidad: {speed} (rango: {robot.min_speed}-{robot.max_speed})")
    
    while True:
        try:
            cmd = input("Robot> ").lower().strip()
            
            if cmd == 'w':
                print("↑ Adelante")
                robot.move_forward(speed)
            elif cmd == 's':
                print("↓ Atrás")
                robot.move_backward(speed)
            elif cmd == 'a':
                print("← Izquierda")
                robot.move_left(speed)
            elif cmd == 'd':
                print("→ Derecha")
                robot.move_right(speed)
            elif cmd == 'q':
                print("↺ Rotar antihorario")
                robot.rotate_counterclockwise(speed)
            elif cmd == 'e':
                print("↻ Rotar horario")
                robot.rotate_clockwise(speed)
            elif cmd == '+':
                speed = min(robot.max_speed, speed + 25)
                print(f"⚡ Velocidad: {speed}")
            elif cmd == '-':
                speed = max(robot.min_speed, speed - 25)
                print(f"🐌 Velocidad: {speed}")
            elif cmd == 'x' or cmd == 'stop':
                print("⏹️  PARADO")
                robot.stop()
            elif cmd == 'help':
                simple_console_control(robot)
                return
            elif cmd == 'quit' or cmd == 'exit':
                print("👋 Saliendo...")
                break
            elif cmd == '':
                continue
            else:
                print(f"❓ Comando no reconocido: '{cmd}'")
                
        except KeyboardInterrupt:
            break
        except EOFError:
            break


# Función de demostración
def demo_movements(robot):
    """Demuestra todos los movimientos posibles"""
    movements = [
        ("Adelante", lambda: robot.move_forward(750)),
        ("Atrás", lambda: robot.move_backward(750)),
        ("Izquierda", lambda: robot.move_left(750)),
        ("Derecha", lambda: robot.move_right(750)),
        ("Rotar CW", lambda: robot.rotate_clockwise(750)),
        ("Rotar CCW", lambda: robot.rotate_counterclockwise(750)),
        ("Diagonal Adelante-Izq", lambda: robot.move_forward_left(750)),
        ("Diagonal Adelante-Der", lambda: robot.move_forward_right(750)),
        ("Diagonal Atrás-Izq", lambda: robot.move_backward_left(750)),
        ("Diagonal Atrás-Der", lambda: robot.move_backward_right(750)),
        ("Adelante + Rotar", lambda: robot.move_forward_rotate_cw(750, 750)),
        ("Strafe + Rotar", lambda: robot.strafe_left_rotate_cw(750, 750)),
    ]
    
    for name, movement in movements:
        print(f"Ejecutando: {name}")
        movement()
        time.sleep(2)
        robot.stop()
        time.sleep(0.5)


# Programa principal
if __name__ == "__main__":
    robot = OmniRobot()
    
    try:
        print("🤖 Robot de 3 ruedas omnidireccionales inicializado")
        print("Presiona Ctrl+C para salir en cualquier momento")
        
        # Menú principal
        while True:
            print("\n" + "="*40)
            print("SELECCIONA MODO DE CONTROL:")
            print("="*40)
            print("1. 🎮 Control por consola (recomendado)")
            print("2. 🎯 Control simple (Windows compatible)")
            print("3. 🎪 Demostración automática")
            print("4. 🔧 Control manual (programático)")
            print("5. ❌ Salir")
            
            try:
                choice = input("\nElige una opción (1-5): ").strip()
                
                if choice == '1':
                    console_control(robot)
                elif choice == '2':
                    simple_console_control(robot)
                elif choice == '3':
                    print("\n🎪 Iniciando demostración de movimientos...")
                    demo_movements(robot)
                    print("✅ Demostración completada")
                elif choice == '4':
                    print("\n🔧 Modo manual - Editando código para personalizar...")
                    manual_control_example(robot)
                elif choice == '5':
                    print("👋 ¡Hasta luego!")
                    break
                else:
                    print("❌ Opción no válida. Intenta de nuevo.")
                    
            except KeyboardInterrupt:
                print("\n👋 Saliendo...")
                break
            except EOFError:
                break
    
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo robot...")
        robot.stop()
        print("✅ Robot detenido correctamente")


def manual_control_example(robot):
    """Ejemplo de control manual programático"""
    print("📝 Ejecutando ejemplo de control manual...")
    
    # Ejemplo de secuencia personalizada
    movements = [
        ("Cuadrado", [
            (robot.move_forward, 750, 2),
            (robot.move_right, 750, 2),
            (robot.move_backward, 750, 2),
            (robot.move_left, 750, 2)
        ]),
        ("Círculo", [
            (lambda: robot.move_forward_rotate_cw(300, 200), None, 6)
        ]),
        ("Estrella", [
            (robot.move_forward, 750, 1),
            (robot.rotate_clockwise, 750, 0.7),
            (robot.move_forward, 750, 1),
            (robot.rotate_clockwise, 300, 0.7),
            (robot.move_forward, 750, 1),
            (robot.rotate_clockwise, 300, 0.7),
            (robot.move_forward, 750, 1),
            (robot.rotate_clockwise, 300, 0.7),
            (robot.move_forward, 750, 1),
        ])
    ]
    
    for pattern_name, pattern_moves in movements:
        print(f"\n🎯 Ejecutando patrón: {pattern_name}")
        input("Presiona ENTER para continuar...")
        
        for move_func, speed, duration in pattern_moves:
            if speed:
                move_func(speed)
            else:
                move_func()
            time.sleep(duration)
            robot.stop()
            time.sleep(0.3)
        
        print(f"✅ {pattern_name} completado")
    
    print("🎉 Todos los patrones completados")
