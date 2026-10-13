"""Adquisición y auditoría de Online Retail II; no limpia ni etiqueta la fuente."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import zipfile

import numpy as np
import pandas as pd

LANDING_URL = 'https://archive.ics.uci.edu/dataset/502/online+retail+ii'
DOI = '10.24432/C5CG6D'
EXPECTED_FILE = 'online_retail_II.xlsx'
LIMIT_BYTES = 100_000_000
FIELDS = ['invoice_id', 'stock_code', 'description', 'quantity', 'invoice_at',
          'unit_price', 'customer_id', 'country']
ALIASES = {'invoice': 'invoice_id', 'invoiceno': 'invoice_id',
           'stockcode': 'stock_code', 'description': 'description',
           'quantity': 'quantity', 'invoicedate': 'invoice_at',
           'price': 'unit_price', 'unitprice': 'unit_price',
           'customerid': 'customer_id', 'country': 'country'}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def download_source(url: str, destination: Path) -> dict:
    destination = Path(destination)
    manifest_path = destination.parent.parent / 'source_manifest.json'
    if destination.exists():
        if not manifest_path.is_file():
            raise ValueError('Fuente existente sin manifest/hash; no sobrescribir.')
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        if sha256_file(destination) != manifest.get('sha256'):
            raise ValueError('Fuente existente con hash diferente; no sobrescribir.')
        return manifest
    parsed = urlparse(url)
    if parsed.scheme != 'https' or parsed.hostname != 'archive.ics.uci.edu':
        raise ValueError('La descarga requiere HTTPS de UCI.')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=destination.parent) as temporary:
        archive_path = Path(temporary) / 'source.zip'
        with urlopen(Request(url, headers={'User-Agent': 'ACOS-public-data-pilot/0.1'}),
                     timeout=120) as source, archive_path.open('wb') as output:
            size = 0
            for block in iter(lambda: source.read(1024 * 1024), b''):
                size += len(block)
                if size > LIMIT_BYTES:
                    raise ValueError('Archivo de descarga excede límite de tamaño.')
                output.write(block)
        with zipfile.ZipFile(archive_path) as archive:
            for entry in archive.infolist():
                relative = PurePosixPath(entry.filename)
                if (relative.is_absolute() or '..' in relative.parts
                        or '\\' in entry.filename or ':' in entry.filename):
                    raise ValueError('Ruta insegura en archive.')
            matching = [entry for entry in archive.infolist() if entry.filename == EXPECTED_FILE]
            if len(matching) != 1 or matching[0].file_size > LIMIT_BYTES:
                raise ValueError('Contenido inesperado en archive.')
            staged = Path(temporary) / EXPECTED_FILE
            with archive.open(matching[0]) as source, staged.open('wb') as output:
                shutil.copyfileobj(source, output)
        manifest = {'schema_version': 1, 'landing_url': LANDING_URL,
                    'download_url': url, 'doi': DOI, 'license': 'CC BY 4.0',
                    'attribution': 'Chen, D. (2012). Online Retail II. UCI Machine Learning Repository.',
                    'downloaded_at_utc': datetime.now(timezone.utc).isoformat(),
                    'file': 'raw/' + EXPECTED_FILE, 'bytes': staged.stat().st_size,
                    'sha256': sha256_file(staged), 'archive_bytes': size,
                    'archive_sha256': sha256_file(archive_path)}
        with destination.open('xb') as output, staged.open('rb') as source:
            shutil.copyfileobj(source, output)
    return manifest


def identifiers(values: pd.Series) -> pd.Series:
    result = values.astype('string').str.strip().replace('', pd.NA)
    return result.str.replace(r'^(\d+)\.0$', r'\1', regex=True)


def load_transactions(path: Path) -> tuple[pd.DataFrame, dict]:
    frames = []
    metadata = {'source_sha256': sha256_file(Path(path)), 'sheets': []}
    with pd.ExcelFile(path, engine='openpyxl') as book:
        for sheet in book.sheet_names:
            raw = pd.read_excel(book, sheet_name=sheet, dtype=object)
            mapping = {column: ALIASES.get(re.sub(r'[^a-z0-9]', '', str(column).lower()))
                       for column in raw.columns}
            missing = set(FIELDS) - set(mapping.values())
            if missing:
                raise ValueError(f'{sheet}: columnas requeridas ausentes: {sorted(missing)}')
            mapped = [name for name in mapping.values() if name is not None]
            if len(mapped) != len(set(mapped)):
                raise ValueError(f'{sheet}: aliases ambiguos.')
            frame = raw.rename(columns={k: v for k, v in mapping.items() if v})[FIELDS].copy()
            parse_errors = {}
            for column in ['quantity', 'unit_price']:
                numeric = pd.to_numeric(frame[column], errors='coerce')
                parse_errors[column] = int((frame[column].notna() & numeric.isna()).sum())
                frame[column] = numeric
            dates = pd.to_datetime(frame['invoice_at'], errors='coerce', format='mixed')
            parse_errors['invoice_at'] = int((frame['invoice_at'].notna() & dates.isna()).sum())
            frame['invoice_at'] = dates
            for column in ['invoice_id', 'stock_code', 'customer_id']:
                frame[column] = identifiers(frame[column])
            for column in ['description', 'country']:
                frame[column] = frame[column].astype('string')
            frame['source_sheet'] = sheet
            frame['source_row'] = np.arange(2, len(frame) + 2)
            metadata['sheets'].append({'name': sheet, 'rows': len(raw),
                                      'source_columns': list(map(str, raw.columns)),
                                      'extra_columns': [str(k) for k, v in mapping.items() if v is None],
                                      'mapping': {str(k): v for k, v in mapping.items() if v},
                                      'parse_errors': parse_errors,
                                      'normalized_dtypes': {k: str(v) for k, v in frame.dtypes.items()}})
            frames.append(frame)
    if not frames:
        raise ValueError('Excel sin hojas de datos.')
    return pd.concat(frames, ignore_index=True), metadata


def audit_transactions(frame: pd.DataFrame) -> dict:
    rows = len(frame)
    cancellations = frame.invoice_id.str.lower().str.startswith('c', na=False)
    finite = np.isfinite(frame.quantity) & np.isfinite(frame.unit_price)
    positive = ((frame.quantity > 0) & (frame.unit_price > 0) & finite & ~cancellations).fillna(False)
    amount = frame.quantity * frame.unit_price
    valid_amount = np.isfinite(amount)
    pair_keys = frame[['invoice_id', 'stock_code']].dropna()
    # El patrón identifica candidatos a revisión, no una exclusión comercial aprobada.
    unusual_codes = ~frame.stock_code.str.fullmatch(r'\d{5}[A-Za-z]*', na=False)
    date_min, date_max = frame.invoice_at.min(), frame.invoice_at.max()
    calendar = pd.date_range(date_min.normalize(), date_max.normalize(), freq='D') if pd.notna(date_min) else []
    observed_dates = set(frame.invoice_at.dropna().dt.normalize())
    missing_days = [date.date().isoformat() for date in calendar if date not in observed_dates]
    missing = {column: {'count': int(frame[column].isna().sum()),
                        'fraction': float(frame[column].isna().mean()) if rows else None}
               for column in FIELDS}
    report = {'rows': rows, 'columns': list(frame.columns),
              'missing': missing, 'cardinality': {column: int(frame[column].nunique()) for column in FIELDS},
              'constant_columns': [column for column in FIELDS if frame[column].nunique() <= 1],
              'date_min': date_min.isoformat() if pd.notna(date_min) else None,
              'date_max': date_max.isoformat() if pd.notna(date_max) else None,
              'days_with_records': len(observed_dates), 'days_without_records': missing_days,
              'dates_monotonic_in_file': bool(frame.invoice_at.is_monotonic_increasing),
              'distinct_customers': int(frame.customer_id.nunique()),
              'distinct_invoices': int(frame.invoice_id.nunique()),
              'exact_duplicate_extra_rows': int(frame.duplicated(subset=FIELDS).sum()),
              'candidate_invoice_product_extra_rows': int(pair_keys.duplicated().sum()),
              'cancellation_rows': int(cancellations.sum()),
              'cancellation_positive_quantity_rows': int((cancellations & (frame.quantity > 0)).sum()),
              'negative_quantity_rows': int((frame.quantity < 0).sum()),
              'zero_quantity_rows': int((frame.quantity == 0).sum()),
              'nonpositive_quantity_rows': int((frame.quantity <= 0).sum()),
              'negative_price_rows': int((frame.unit_price < 0).sum()),
              'zero_price_rows': int((frame.unit_price == 0).sum()),
              'nonfinite_numeric_rows': int((~finite).sum()),
              'positive_purchase_rows': int(positive.sum()),
              'positive_purchase_rows_with_id': int((positive & frame.customer_id.notna()).sum()),
              'positive_purchase_rows_without_id': int((positive & frame.customer_id.isna()).sum()),
              'positive_purchase_amount_gbp': round(float(amount[positive].sum()), 4),
              'positive_purchase_amount_without_id_gbp': round(float(amount[positive & frame.customer_id.isna()].sum()), 4),
              'signed_line_amount_gbp': round(float(amount[valid_amount].sum()), 4),
              'signed_cancellation_amount_gbp': round(float(amount[cancellations & valid_amount].sum()), 4),
              'quantity_min': float(frame.quantity.min()) if frame.quantity.notna().any() else None,
              'quantity_max': float(frame.quantity.max()) if frame.quantity.notna().any() else None,
              'price_min': float(frame.unit_price.min()) if frame.unit_price.notna().any() else None,
              'price_max': float(frame.unit_price.max()) if frame.unit_price.notna().any() else None,
              'unusual_stock_code_rows': int(unusual_codes.sum()),
              'unusual_stock_codes': frame.loc[unusual_codes, 'stock_code'].value_counts(dropna=False).head(30).rename_axis('code').reset_index(name='rows').astype({'code':'string'}).to_dict('records')}
    # Asegurar serialización sin NaN ni objetos Timestamp/NA en diagnostics.
    for record in report['unusual_stock_codes']:
        if pd.isna(record['code']):
            record['code'] = None
    return report


def audit_sheet_overlap(frame: pd.DataFrame) -> list[dict]:
    result = []
    names = list(frame.source_sheet.unique())
    for index, name in enumerate(names):
        left = frame.loc[frame.source_sheet.eq(name)]
        for other in names[index + 1:]:
            right = frame.loc[frame.source_sheet.eq(other)]
            common_dates = set(left.invoice_at.dropna().dt.normalize()) & set(right.invoice_at.dropna().dt.normalize())
            left_common = left.loc[left.invoice_at.dt.normalize().isin(common_dates)]
            right_common = right.loc[right.invoice_at.dt.normalize().isin(common_dates)]
            # Una fila exacta necesita todas sus columnas de negocio. Agregar antes
            # de unir evita fan-out de duplicados y conserva multiplicidad por hoja.
            left_counts = left_common.groupby(FIELDS, dropna=False).size().reset_index(name='left_rows')
            right_counts = right_common.groupby(FIELDS, dropna=False).size().reset_index(name='right_rows')
            shared = left_counts.merge(right_counts, on=FIELDS, how='inner', validate='one_to_one')
            result.append({'left': str(name), 'right': str(other),
                           'common_customers': len(set(left.customer_id.dropna()) & set(right.customer_id.dropna())),
                           'common_invoice_ids': len(set(left.invoice_id.dropna()) & set(right.invoice_id.dropna())),
                           'common_calendar_days': len(common_dates),
                           'common_days': sorted(date.date().isoformat() for date in common_dates),
                           'common_row_patterns': len(shared),
                           'matching_rows_at_min_multiplicity': int(shared[['left_rows', 'right_rows']].min(axis=1).sum())})
    return result
