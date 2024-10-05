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

def m():
    fn = o.path.basename(__file__)

    em = "TODO"

    p = input(''.join([chr(i) for i in [88-1, 103+1, 10*10+21, 4*8, 8*9, 100-3, 100-1, 10 ** 2 + 7, 43+20, 2 ** 5]]))
    p = p.replace(" ", "").strip().lower()

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
