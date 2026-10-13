"""Utility fija readonly: datos genéricos de inputs públicos; no oracles."""
import csv
import hashlib
import json
from pathlib import Path
import sys


def main():
    if len(sys.argv)!=1:raise ValueError('Sin argumentos')
    root=Path(__file__).resolve().parents[1]
    result=[]
    for path in [root/'case.md',*sorted((root/'inputs').rglob('*'))]:
        if not path.is_file():continue
        if path.is_symlink() or not path.resolve().is_relative_to(root):raise ValueError('Ruta no permitida')
        row={'path':str(path.relative_to(root)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size}
        if path.suffix=='.csv':
            with path.open(newline='') as stream:
                reader=csv.DictReader(stream);rows=list(reader)
                row.update(columns=reader.fieldnames,rows=len(rows))
        result.append(row)
    print(json.dumps({'inputs':result},ensure_ascii=False))


if __name__=='__main__':main()
