"""Restore compressed initial snapshot, checking archive integrity and paths."""
import hashlib,io,zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
payload=b''.join(p.read_bytes() for p in sorted((root/'.baseline').glob('snapshot.part*')))
expected='69f9a5546df733ed57a3408aa9c0baba8e108c4ebde19cdafc60f9ee28c87765'
if hashlib.sha256(payload).hexdigest()!=expected:
    raise ValueError('Snapshot inicial incompleto ou alterado')
target=root/'dist'; target.mkdir(exist_ok=True)
with zipfile.ZipFile(io.BytesIO(payload)) as z:
    if any(not (target/n).resolve().is_relative_to(target.resolve()) for n in z.namelist()):
        raise ValueError('Caminho fora do diretório da base')
    z.extractall(target)
print('Versão inicial restaurada com hash verificado.')

import shutil
for asset in (root/"web").glob("*.js"):
    shutil.copy2(asset,target/asset.name)
