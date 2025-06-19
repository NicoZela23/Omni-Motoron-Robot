import time
import motoron
import RPi.GPIO as GPIO
import sys
import termios
import tty
import select

# --- CONFIGURACIÓN MOTORON ---
try:
    mc1 = motoron.MotoronI2C(address=17)
except Exception as e:
    print(f"Error inicializando Motoron. Verifica la conexión I2C. Error: {e}")
    exit()

# --- CONFIGURACIÓN ENCODERS ---
ENCODER_PINS = {
    1: {'pin_a': 22, 'pin_b': 27},
    2: {'pin_a': 18, 'pin_b': 15},
    3: {'pin_a': 17, 'pin_b': 14},
}

encoder_counts = {1: 0, 2: 0, 3: 0}
last_pin_b_state = {}
PIN_TO_MOTOR = {}
previous_encoder_counts = encoder_counts.copy()
previous_velocity_time = time.time()
encoder_velocities = {1: 0, 2: 0, 3: 0}
ENCODER_CPR = 1000

# --- CONFIGURACIÓN INICIAL MOTORON ---
def setup_motoron(mc, address):
    mc.reinitialize()
    mc.disable_crc()
    mc.clear_reset_flag()
    print(f"Motoron en dirección {address} configurado correctamente.")

# --- CONFIGURACIÓN GPIO PARA ENCODERS ---
def setup_gpio_encoders():
    GPIO.setmode(GPIO.BCM)
    print("Configurando pines GPIO para encoders...")

    for motor_num, pins in ENCODER_PINS.items():
        pin_a = pins['pin_a']
        pin_b = pins['pin_b']

        GPIO.setup(pin_a, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(pin_b, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        last_pin_b_state[pin_a] = GPIO.input(pin_b)
        PIN_TO_MOTOR[pin_a] = motor_num
        PIN_TO_MOTOR[pin_b] = motor_num

        GPIO.add_event_detect(pin_a, GPIO.BOTH, callback=encoder_callback)

    print("Configuración de encoders completada.")

def encoder_callback(channel):
    motor_num = PIN_TO_MOTOR[channel]
    pin_a = ENCODER_PINS[motor_num]['pin_a']
    pin_b = ENCODER_PINS[motor_num]['pin_b']

    pin_a_state = GPIO.input(pin_a)
    pin_b_state = GPIO.input(pin_b)

    if pin_a_state != last_pin_b_state[pin_a]:
        encoder_counts[motor_num] += 1
    else:
        encoder_counts[motor_num] -= 1

    last_pin_b_state[pin_a] = pin_b_state

def calculate_velocities():
    global previous_velocity_time, previous_encoder_counts, encoder_velocities
    current_time = time.time()
    dt = current_time - previous_velocity_time

    if dt > 0:
        for motor_num in encoder_counts:
            delta_counts = encoder_counts[motor_num] - previous_encoder_counts[motor_num]
            encoder_velocities[motor_num] = delta_counts / dt
            previous_encoder_counts[motor_num] = encoder_counts[motor_num]

        previous_velocity_time = current_time

def calculate_rpm(encoder_velocity, counts_per_revolution):
    if counts_per_revolution == 0:
        return 0
    return (encoder_velocity * 60) / counts_per_revolution

def print_status():
    calculate_velocities()
    print("\n--- ESTADO DE MOTORES ---")
    for motor in [1, 2, 3]:
        count = encoder_counts[motor]
        velocity = encoder_velocities[motor]
        rpm = calculate_rpm(velocity, ENCODER_CPR)
        print(f"Motor {motor}: Count={count:7d}, Vel={velocity:8.1f} c/s, RPM={rpm:7.1f}")

def get_key_nonblocking(timeout=0.1):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setraw(fd)
    try:
        rlist, _, _ = select.select([fd], [], [], timeout)
        if rlist:
            return sys.stdin.read(1).lower()
        return None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def set_motors(speed1, speed2, speed3):
    mc1.set_speed(1, speed1)
    mc1.set_speed(2, speed2)
    mc1.set_speed(3, speed3)

def stop_motors():
    set_motors(0, 0, 0)

# --- PROGRAMA PRINCIPAL ---
if __name__ == "__main__":
    try:
        setup_motoron(mc1, 16)
        setup_gpio_encoders()

        for motor in range(1, 4):
            mc1.set_max_acceleration(motor, 80)
            mc1.set_max_deceleration(motor, 300)

        speed = 750  # velocidad de los motores

        print("""
=========== CONTROL MANUAL ===========

Usa las siguientes teclas para controlar el auto:

 W → Adelante (motores 1-3)
 S → Atrás    (motores 1-3)
 A → Izquierda (solo motor 2)
 D → Derecha   (solo motor 1)
 Q →  Diagonal izquierda (motores 2 y 3)
 E →  Diagonal derecha  (motores 1 y 3)
 P → Salir

Presiona ENTER para comenzar...
        """)
        input()

        print("Mantén presionada una tecla para mover el auto.")

        current_key = None
        key_press_start = None
        print_interval = 5  # segundos
        last_key_time = None

        while True:
            key = get_key_nonblocking()
            now = time.time()

            if key:
                if key == 'p':
                    print("⛔ Saliendo...")
                    break

                if key in ['w', 's', 'a', 'd', 'q', 'e']:
                    if current_key != key:
                        key_press_start = now
                        print(f"➡️ Tecla '{key.upper()}' presionada.")
                    current_key = key
                    last_key_time = now

            # Acción basada en tecla activa
            if current_key:
                if now - last_key_time > 0.5:
                    current_key = None
                    stop_motors()
                    continue

                if current_key == 'w':
                    set_motors(speed, speed, speed)
                elif current_key == 's':
                    set_motors(-1050, -400, -speed)
                elif current_key == 'a':
                    set_motors(0, speed, 0)
                elif current_key == 'd':
                    set_motors(speed, 0, 0)
                elif current_key == 'q':
                    set_motors(0, speed, speed)
                elif current_key == 'e':
                    set_motors(speed, 0, speed)

                if now - key_press_start >= print_interval:
                    print_status()
                    key_press_start = now
            else:
                stop_motors()

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        stop_motors()
        GPIO.cleanup()
        print("\nGPIO limpiado. Programa finalizado.")
