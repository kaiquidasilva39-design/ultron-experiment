import time
from app.agent import agent
from app.state import save


def main():
    print("ULTRON-EXPERIMENT SERVICE")
    print("Serviço iniciado.")

    agent.start()

    save({
        "agent": agent.name,
        "running": True,
        "service": True,
        "version": "0.1-local",
    })

    while True:
        time.sleep(30)


if __name__ == "__main__":
    main()
