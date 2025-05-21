import socket
import json
import time
import threading
import os
from utils.algoritmo_de_roteamento import processa_lsa, atualiza_lsdb
from utils.graph import Graph


ROUTER_ID = os.environ.get("ROUTER_ID")
PORT = 5000 + int(ROUTER_ID[-1])  
LSDB = {}
graph = Graph()

def load_neighbors():
    try:
        with open(f"config/{ROUTER_ID}/vizinhos.json") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[{ROUTER_ID}] Arquivo de vizinhos não encontrado.")
        return {}

def send_lsa(neighbor_ip, lsa_data):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            message = json.dumps(lsa_data).encode()
            sock.sendto(message, (neighbor_ip, PORT))
            print(f"[{ROUTER_ID}] Enviou LSA para {neighbor_ip}")
    except Exception as e:
        print(f"[{ROUTER_ID}] Erro ao enviar LSA para {neighbor_ip}: {e}")

def receive_loop():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", PORT))
    print(f"[{ROUTER_ID}] Escutando na porta {PORT}...")
    while True:
        try:
            data, addr = sock.recvfrom(4096)
            lsa = json.loads(data.decode())
            print(f"[{ROUTER_ID}] Recebeu LSA de {lsa['origin']}")
            updated = processa_lsa(LSDB, lsa)
            if updated:
                atualiza_lsdb(ROUTER_ID, LSDB)
                graph.load_lsdb(LSDB)
                rotas = graph.dijkstra(ROUTER_ID)
                print(f"[{ROUTER_ID}] Tabela de roteamento atualizada: {rotas}")
        except Exception as e:
            print(f"[{ROUTER_ID}] Erro no recebimento: {e}")

def start_router():
    neighbors = load_neighbors()
    if not neighbors:
        print(f"[{ROUTER_ID}] Nenhum vizinho configurado.")
        return

    # Atualiza LSDB local
    LSDB[ROUTER_ID] = neighbors

    # Thread de recebimento
    threading.Thread(target=receive_loop, daemon=True).start()

    # Loop de envio periódico de LSAs
    while True:
        lsa = {
            "origin": ROUTER_ID,
            "timestamp": time.time(),
            "neighbors": neighbors
        }
        for ip in neighbors.values():
            send_lsa(ip, lsa)
        time.sleep(10)

if __name__ == "__main__":
    print(f"[{ROUTER_ID}] Roteador iniciado com porta {PORT}")
    start_router()
