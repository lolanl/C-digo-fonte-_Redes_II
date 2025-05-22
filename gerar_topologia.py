import os
import time

def start_docker():
    print("Subindo containers com Docker Compose...")
    os.system("docker-compose up --build -d")
    print("Containers iniciados.")
    print("Aguardando 15 segundos para estabilizar a rede...")
    time.sleep(15)

def testar_ping_hosts():
    hosts = [f"host{i}{letra}" for i in range(1, 6) for letra in ['a', 'b']]
    for host in hosts:
        print(f"\n Rodando testes de ping a partir de {host}...")
        os.system(f"docker exec {host} python3 hosts.py {host}")
        time.sleep(1)

if __name__ == "__main__":
    start_docker()
    testar_ping_hosts()

