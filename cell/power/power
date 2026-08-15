import os
import time
import subprocess

# Configuración
CHECK_INTERVAL = 0.5  # Revisión cada medio segundo
LOG_FILE = "/var/log/power_monitor.log"

def flash_sync():
    """Fuerza la escritura de datos pendientes al disco."""
    try:
        subprocess.run(["sync"], check=True)
    except Exception as e:
        pass

def emergency_shutdown():
    """Intenta salvar todo y apagar."""
    flash_sync()
    # Enviamos la señal de apagado inmediato
    os.system("sudo shutdown -h now")

def check_power_events():
    """
    Busca señales de 'Under-voltage' en el log del kernel (dmesg).
    Común en sistemas donde la fuente empieza a flaquear.
    """
    try:
        # Buscamos alertas de voltaje o errores críticos de bus
        result = subprocess.check_output(["dmesg", "|", "tail", "-n", "20"], shell=True).decode()
        if "Under-voltage detected" in result or "Voltage normalised" in result:
            return True
    except:
        return False
    return False

print("Monitor de energía activo...")
try:
    while True:
        if check_power_events():
            with open(LOG_FILE, "a") as f:
                f.write(f"[{time.ctime()}] Inestabilidad detectada. Iniciando protocolo de emergencia.\n")
            emergency_shutdown()
            break
        
        # Opcional: Ejecutar sync preventivo cada cierto tiempo
        # flash_sync() 
        
        time.sleep(CHECK_INTERVAL)
except KeyboardInterrupt:
    print("Monitor detenido manualmente.")
