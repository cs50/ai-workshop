import os as o
import sys as s
from cryptography.fernet import Fernet as f
import hashlib as h
import base64 as b

def a(p: str) -> bytes:
    g = h.sha256(p.encode()).digest()
    return b.urlsafe_b64encode(g[:32])

def d(e: str, p: str) -> str:
    k = a(p)
    c = f(k)
    dm = c.decrypt(e.encode())
    return dm.decode()

def e(m: str, p: str) -> str:
    k = a(p)
    c = f(k)
    em = c.encrypt(m.encode())
    return em.decode()

def m():
    fn = o.path.basename(__file__)

    em = "gAAAAABnB-dRwh__tdpmFkX004j5HW8ywCMeDkL_dHd3JvL7eYPvOFiU0yVATOzD_dsWw3wQmJytf7H2hgTJ49e6nLeZ-7Nfcj06PF3BxGG0PXoWEFzbUW1yqMztpAewNVbTgr4Y7qaLGqGF0nXF3DOdw8IS-SS1UPCe9yNO5ij57RrY8WTepxw4CzrAsZNjOXyDNR7afYQ3-GdzG8IPwz35gRf-r9l6QnHEDBvXFhJuoJaXuwOfvm83_1haCmWsOKWBOQVIWXO72JxNmKkggRLcsQ-Fu7Dhwi4xcKRKFfdhZjOz0wv7Wms="

    p = input("A51C30: ")

    try:
        dm = d(em, p)
        o.system(f'echo "export OPENAI_API_KEY={dm}" >> ~/.bashrc')
        print("🎉 Please create a new terminal by clicking the '+' button on the right side of the terminal.")
        o.system(f"rm {fn}")
    except Exception as e:
        print("Try again, quack! 🦆")
        s.exit(1)

if __name__ == "__main__":
    m()