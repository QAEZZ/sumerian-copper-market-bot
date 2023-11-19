
def google_makersuit() -> str:
    with open('client_secrets/makersuite.key', 'r') as file_ms:
        return file_ms.read()

def bard_cookies() -> dict:
    try:
        with open('client_secrets/bard/Secure-1PSID.key', 'r') as file_1psid:
            Secure_1PSID = file_1psid.read().strip()

        with open('client_secrets/bard/Secure-1PSIDTS.key', 'r') as file_1psidts:
            Secure_1PSIDTS = file_1psidts.read().strip()

        with open('client_secrets/bard/Secure-1PSIDCC.key', 'r') as file_1psidcc:
            Secure_1PSIDCC = file_1psidcc.read().strip()

        cookies = {
            "__Secure-1PSID": Secure_1PSID,
            "__Secure-1PSIDTS": Secure_1PSIDTS,
            "__Secure-1PSIDCC": Secure_1PSIDCC,
        }

        return cookies
    except FileNotFoundError as e:
        print(f"Error: {e.filename} not found.")
        return {}
    except Exception as e:
        print(f"Error: {e}")
        return {}
