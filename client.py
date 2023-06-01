import threading, selectors, socket, rsa, sys
from colorama import Fore


with open(f"C:/Users/antonia/Desktop/Project/client_keys/pubKey.pem", "rb") as f:
    pubkey = rsa.PublicKey.load_pkcs1(f.read())
with open("C:/Users/antonia/Desktop/Project/client_keys/privKey.pem", "rb") as f:
    privkey = rsa.PrivateKey.load_pkcs1(f.read())


class ChatClient:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._username = username
        self._pubkey, self._privkey = pubkey, privkey
        self._serverkey = None
        self._threadsend = threading.Thread(target=self._input_and_send_loop)
        self._threadrecv = threading.Thread(target=self.recieve)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._read_selector = selectors.DefaultSelector()

    def _input_and_send_loop(self):
        while True:
            msg = input()
            final = username + ":" + msg
            if msg != "quit":
                try:
                    self._socket.send(
                        (rsa.encrypt(final.encode("ascii"), self._serverkey))
                    )
                except:
                    break
            else:
                print("you exited the chat")
                sys.exit(1)

    def connect(self):
        self._socket.connect((self._host, self._port))
        self._stringkey = self._socket.recv(1024)
        self._serverkey = rsa.PublicKey.load_pkcs1(self._stringkey, format="DER")
        self._threadsend.start()
        self._threadsend.join()
        self._threadrecv.daemon = True
        self._threadrecv.start()
        self._threadrecv.join()

    def recieve(self):
        while True:
            try:
                msg = self._socket.recv(1024).decode("ascii")
                print(msg)
                if msg.split(":", 1)[1] == "KEY":
                    self._socket.send(self._pubKey.save_pkcs1(format="DER"))
                else:
                    print(
                        Fore.GREEN
                        + msg.split(":", 1)[0]
                        + ":"
                        + Fore.WHITE
                        + msg.split(":", 1)[1]
                    )
            except:
                print("an error occured!")
                self._socket.close()
                sys.exit(1)


if __name__ == "__main__":
    username = input("choose your username sir: ")
    client = ChatClient("localhost", 7342)
    client.connect()
    sys.exit(1)
