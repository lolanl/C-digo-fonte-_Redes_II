import socket, sys, time, os
from utils.ping_logger import log_rtt

TOTAL_PINGS = 0
SUCESSOS = 0

def ping(dest_host):
    global TOTAL_PINGS, SUCESSOS
    try:
        start = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((dest_host, 8080)) 
        end = time.time()
        rtt = round((end - start) * 1000, 2)
        print(f"({round(end - start, 2)}s, RTT médio: {rtt}ms) -> {dest_host}")
        log_rtt(dest_host, rtt)
        SUCESSOS += 1
    except Exception as e:
        print(f"FALHA -> {dest_host}")
    finally:
        TOTAL_PINGS += 1

def main():
    host_name = sys.argv[1]
    print(f"\nResultados do Host: {host_name}")
    
    hosts = [f"host{i}{letra}" for i in range(1, 6) for letra in ['a', 'b']]
    hosts.remove(host_name)

    for dest in hosts:
        ping(dest)
        time.sleep(1)

    print("\nEstatísticas Gerais - Total de Pings:", TOTAL_PINGS, 
          ", Bem-sucedidos:", SUCESSOS)
    print("Resultados de latência salvos em: performance_results/resultados_<timestamp>.csv")

if __name__ == "__main__":
    main()
