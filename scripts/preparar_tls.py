"""Provide the missing intermediate, retaining certificate/hostname checks."""
from pathlib import Path
import certifi,hashlib,subprocess,sys
root=Path(__file__).resolve().parents[1]
intermediate=root/'scripts/certs/sectigo-ov-r36.pem'
# Certificate from the CA URL advertised by the official server certificate.
# It is an intermediate, NOT a new trust root: verify against certifi first.
subprocess.run(['openssl','verify','-CAfile',certifi.where(),str(intermediate)],check=True)
target=root/'data/ca-completa.pem';target.parent.mkdir(exist_ok=True)
target.write_bytes(Path(certifi.where()).read_bytes()+intermediate.read_bytes())
print(str(target.resolve()))
