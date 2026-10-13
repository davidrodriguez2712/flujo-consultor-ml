"""Runner portable del ensayo; crea outputs nuevos y no reescribe un run existente."""
import argparse,csv,gzip,hashlib,json,platform,sys
from pathlib import Path
from forecast import build_weekly,forecasts,metrics,choose_method,METHODS


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def persist_read(path,rows):
    with path.open('x',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader()
        for row in rows:
            writer.writerow({k:format(v,'.17g') if isinstance(v,float) else v for k,v in row.items()})
    with path.open(encoding='utf-8',newline='') as stream:
        return [{k:int(v) if k=='actual' else float(v) if k=='prediction' else v for k,v in r.items()} for r in csv.DictReader(stream)]


def run_pipeline(project,output):
    project,output=Path(project),Path(output)
    protocol_path=project/'analysis/protocol.json'
    protocol=json.loads(protocol_path.read_text(encoding='utf-8'))
    source=project/'data/raw/transactions_normalized.csv.gz'
    if sha(source)!=protocol['source_expected_sha256']:
        raise ValueError('Hash de fuente distinto del protocolo.')
    output.mkdir(parents=True,exist_ok=False)
    with gzip.open(source,'rt',encoding='utf-8',newline='') as stream:
        weekly,audit=build_weekly(csv.DictReader(stream))
    weekly=persist_read(output/'weekly_counts.csv',weekly)
    development=forecasts(weekly,protocol['development_start'],protocol['development_end_exclusive'],list(METHODS))
    development=persist_read(output/'development_predictions.csv',development)
    comparisons={method:metrics([r for r in development if r['method']==method]) for method in METHODS}
    selected=choose_method(comparisons)
    # Cerrar la decisión antes de generar/evaluar final; releer la estrategia persistida.
    save_json(output/'strategy.json',{'selected_method':selected,'rule':'Development WAPE; tie retains baseline','development':comparisons,'protocol_sha256':sha(protocol_path)})
    strategy=json.loads((output/'strategy.json').read_text())
    final=forecasts(weekly,protocol['final_start'],protocol['final_end_exclusive'],[strategy['selected_method']])
    final=persist_read(output/'final_predictions.csv',final)
    result={'selected_method':selected,'development':comparisons,'final':metrics(final),'last_complete_final':max(final,key=lambda r:r['cutoff']),'audit':audit}
    save_json(output/'result.json',result)
    save_json(output/'environment.json',{'python':platform.python_version(),'platform':platform.platform(),'dependencies':'Python standard library only','source_sha256':sha(source),'protocol_sha256':sha(protocol_path),'code':{name:sha(project/'analysis'/name) for name in ['forecast.py','run_forecast.py']},'serialization':{'source':'gzip CSV UTF-8, Decimal quantities/prices, naive ISO timestamp','weekly':'CSV writer/reader; actual int; cutoffs str','predictions':'CSV float .17g then float reader; actual int','strategy':'JSON saved and reread before final'},'seeds':'No randomness','ingestion_delay':'Zero assumed retrospectively, unverified'})
    save_json(output/'outputs-manifest.json',{'files':[{'path':p.name,'sha256':sha(p)} for p in sorted(output.iterdir()) if p.is_file()]})
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--project',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(run_pipeline(args.project,args.output),ensure_ascii=False,indent=2))
