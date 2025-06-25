import time
import RPi.GPIO as GPIO

# --- CONFIGURACIÓN PINES DE ENCODERS ---
ENCODER_PINS = {
    1: {'pin_a': 22, 'pin_b': 27},  # Motor 1
    2: {'pin_a': 18, 'pin_b': 15},  # Motor 2
    3: {'pin_a': 17, 'pin_b': 14},  # Motor 3
}
ENCODER_CPR = 1000  # Pulsos (Counts) Por Revolución del encoder

# --- VARIABLES GLOBALES PARA ENCODERS ---
encoder_counts = {1: 0, 2: 0, 3: 0}
last_pin_states = {1: 0, 2: 0, 3: 0}
PIN_TO_MOTOR = {}

# --- FUNCIÓN DE CALLBACK (SE EJECUTA CON CADA PULSO) ---
def encoder_callback(channel):
    """Se activa en cada cambio de estado del pin A del encoder."""
    motor_num = PIN_TO_MOTOR[channel]
    
    pin_a_state = GPIO.input(ENCODER_PINS[motor_num]['pin_a'])
    pin_b_state = GPIO.input(ENCODER_PINS[motor_num]['pin_b'])

    # Lógica de codificación en cuadratura para determinar la dirección
    if pin_a_state == pin_b_state:
        encoder_counts[motor_num] += 1
    else:
        encoder_counts[motor_num] -= 1

# --- CONFIGURACIÓN GPIO ---
def setup_gpio_encoders():
    """Configura los pines GPIO como entradas para los encoders."""
    GPIO.setmode(GPIO.BCM)
    print("Configurando pines GPIO para los encoders...")

    for motor_num, pins in ENCODER_PINS.items():
        pin_a = pins['pin_a']
        GPIO.setup(pin_a, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(pins['pin_b'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Mapea el pin A al número de motor para identificarlo en el callback
        PIN_TO_MOTOR[pin_a] = motor_num
        
        # Añade la detección de eventos (interrupción) en el pin A
        GPIO.add_event_detect(pin_a, GPIO.BOTH, callback=encoder_callback)
    
    print("Configuración de encoders completada.")

# --- PROGRAMA PRINCIPAL ---
if __name__ == "__main__":
    try:
        setup_gpio_encoders()
        
        print("\n--- LEYENDO VELOCIDADES DE LOS ENCODERS ---")
        print("Mueve los motores manualmente para ver los cambios.")
        print("Presiona CTRL+C para salir.")

        last_counts = encoder_counts.copy()
        last_time = time.time()

        while True:
            # Calcula el tiempo transcurrido
            current_time = time.time()
            dt = current_time - last_time

            if dt >= 1.0: # Actualiza la velocidad cada segundo
                print("\n--- ESTADO ACTUAL ---")
                for motor in [1, 2, 3]:
                    # Calcula la velocidad
                    delta_counts = encoder_counts[motor] - last_counts[motor]
                    velocity_cps = delta_counts / dt  # Velocidad en counts per second
                    rpm = (velocity_cps / ENCODER_CPR) * 60

                    print(f"Motor {motor}:")
                    print(f"  - Conteo Total: {encoder_counts[motor]:7d} pulsos")
                    print(f"  - Velocidad:    {velocity_cps:8.1f} c/s")
                    print(f"  - RPM:          {rpm:7.1f}")

                # Actualiza las variables para el próximo cálculo
                last_counts = encoder_counts.copy()
                last_time = current_time
            
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
    finally:
        # Limpia los pines GPIO al salir
        GPIO.cleanup()
        print("\nGPIO limpiado. Programa finalizado.")