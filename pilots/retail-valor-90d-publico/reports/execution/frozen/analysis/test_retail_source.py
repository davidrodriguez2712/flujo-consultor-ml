import hashlib
import io
import json
import zipfile

import pandas as pd
import pytest
from openpyxl import Workbook

from retail_source import audit_transactions, download_source, load_transactions


def workbook(path, missing_column=False):
    book = Workbook()
    first = book.active
    first.title = 'Year 2009-2010'
    names = ['Invoice', 'StockCode', 'Description', 'Quantity', 'InvoiceDate',
             'Price', 'Customer ID', 'Country']
    if missing_column:
        names[5] = 'Unknown'
    first.append(names)
    first.append(['100', 'A1', 'Gift', 2, '2009-12-01 10:00:00', 3.5, 12345, 'United Kingdom'])
    first.append(['C101', 'A1', None, -1, '2009-12-02 10:00:00', 3.5, None, 'United Kingdom'])
    second = book.create_sheet('Year 2010-2011')
    second.append(['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate',
                   'UnitPrice', 'CustomerID', 'Country'])
    second.append(['102', 'A2', 'Gift 2', 1, '2010-12-01 11:00:00', 2, 12345, 'United Kingdom'])
    book.save(path)


def test_load_both_sheets_and_preserve_missing_id(tmp_path):
    path = tmp_path / 'source.xlsx'
    workbook(path)
    frame, metadata = load_transactions(path)
    assert len(frame) == 3
    assert set(frame.source_sheet) == {'Year 2009-2010', 'Year 2010-2011'}
    assert list(frame.source_row) == [2, 3, 2]
    assert pd.isna(frame.customer_id.iloc[1])
    assert frame.customer_id.iloc[0] == '12345'
    assert metadata['sheets'][0]['rows'] == 2
    assert str(frame.invoice_at.dtype).startswith('datetime64')


def test_missing_required_column_is_rejected(tmp_path):
    path = tmp_path / 'source.xlsx'
    workbook(path, missing_column=True)
    with pytest.raises(ValueError, match='unit_price'):
        load_transactions(path)


def test_existing_source_with_different_hash_is_never_replaced(tmp_path, monkeypatch):
    path = tmp_path / 'data/raw/online_retail_II.xlsx'
    path.parent.mkdir(parents=True)
    path.write_bytes(b'preserve-me')
    (tmp_path / 'data/source_manifest.json').write_text(json.dumps({'sha256':'different'}))
    monkeypatch.setattr('retail_source.urlopen', lambda *args, **kwargs: pytest.fail('No network'))
    with pytest.raises(ValueError, match='hash'):
        download_source('https://archive.ics.uci.edu/example.zip', path)
    assert path.read_bytes() == b'preserve-me'


def test_download_extracts_only_expected_file_and_can_verify_without_network(tmp_path, monkeypatch):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as archive:
        archive.writestr('online_retail_II.xlsx', b'fixture-data')
    monkeypatch.setattr('retail_source.urlopen', lambda *args, **kwargs: io.BytesIO(buffer.getvalue()))
    path = tmp_path / 'data/raw/online_retail_II.xlsx'
    manifest = download_source('https://archive.ics.uci.edu/example.zip', path)
    assert path.read_bytes() == b'fixture-data'
    assert manifest['sha256'] == hashlib.sha256(b'fixture-data').hexdigest()
    (tmp_path / 'data/source_manifest.json').write_text(json.dumps(manifest))
    monkeypatch.setattr('retail_source.urlopen', lambda *args, **kwargs: pytest.fail('No network'))
    assert download_source(manifest['download_url'], path)['sha256'] == manifest['sha256']


def test_archive_escape_is_rejected(tmp_path, monkeypatch):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as archive:
        archive.writestr('../online_retail_II.xlsx', b'bad')
    monkeypatch.setattr('retail_source.urlopen', lambda *args, **kwargs: io.BytesIO(buffer.getvalue()))
    with pytest.raises(ValueError, match='archive'):
        download_source('https://archive.ics.uci.edu/example.zip', tmp_path/'data/raw/online_retail_II.xlsx')
    assert not (tmp_path/'data/raw/online_retail_II.xlsx').exists()


def test_audit_reports_quality_without_dropping_rows(tmp_path):
    path = tmp_path / 'source.xlsx'
    workbook(path)
    frame, _ = load_transactions(path)
    before = frame.copy(deep=True)
    report = audit_transactions(frame)
    assert report['rows'] == 3
    assert report['missing']['customer_id']['count'] == 1
    assert report['cancellation_rows'] == 1
    assert report['nonpositive_quantity_rows'] == 1
    assert report['positive_purchase_rows_with_id'] == 2
    assert report['date_min'].startswith('2009-12-01')
    assert report['distinct_customers'] == 1
    pd.testing.assert_frame_equal(frame, before)


def test_exact_duplicates_ignore_sheet_provenance_and_are_not_removed(tmp_path):
    path = tmp_path / 'source.xlsx'
    workbook(path)
    frame, _ = load_transactions(path)
    duplicate = frame.iloc[[0]].copy()
    duplicate['source_sheet'] = 'Other'
    duplicate['source_row'] = 99
    frame = pd.concat([frame, duplicate], ignore_index=True)
    report = audit_transactions(frame)
    assert report['exact_duplicate_extra_rows'] == 1
    assert report['candidate_invoice_product_extra_rows'] == 1
    assert report['rows'] == 4


def test_sheet_overlap_counts_multiplicity_without_cartesian_join(tmp_path):
    from retail_source import audit_sheet_overlap
    path = tmp_path / 'source.xlsx'
    workbook(path)
    frame, _ = load_transactions(path)
    row = frame.iloc[[0]].copy()
    left = pd.concat([row, row], ignore_index=True)
    right = pd.concat([row, row, row], ignore_index=True)
    right['source_sheet'] = 'Other'
    combined = pd.concat([left, right], ignore_index=True)
    result = audit_sheet_overlap(combined)[0]
    assert result['common_row_patterns'] == 1
    assert result['matching_rows_at_min_multiplicity'] == 2
    assert result['common_invoice_ids'] == 1
    assert len(combined) == 5


def test_overlap_compares_missing_values_and_does_not_equate_different_lines(tmp_path):
    from retail_source import audit_sheet_overlap
    path = tmp_path / 'source.xlsx'
    workbook(path)
    frame, _ = load_transactions(path)
    left = frame.iloc[[1]].copy()
    right = pd.concat([left, left], ignore_index=True)
    right['source_sheet'] = 'Other'
    right.loc[1, 'quantity'] = -2
    result = audit_sheet_overlap(pd.concat([left, right], ignore_index=True))[0]
    assert result['common_row_patterns'] == 1
    assert result['matching_rows_at_min_multiplicity'] == 1
