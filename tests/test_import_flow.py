import sys
import os
import json
import sqlite3
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient

from api.sqlite_api_clean import app


class DummyResponse:
    def __init__(self, data, status=200):
        self._data = data
        self.status_code = status

    def json(self):
        return self._data


def seed_db(client: TestClient):
    r = client.post('/api/seed')
    assert r.status_code == 200


def db_rows(query, params=()):
    BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    DB = os.path.join(BASE, 'api', 'gjb_dev.db')
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def test_import_insert_and_audit(monkeypatch):
    client = TestClient(app)

    # Reset DB to known state
    seed_db(client)

    fake_payload = {
        'status': 'OK',
        'nome': 'ACME ENERGIA SOLAR LTDA',
        'cnpj': '11.111.111/1111-11',
        'situacao': 'ATIVA',
        'municipio': 'São Paulo',
        'uf': 'SP',
        'atividade_principal': [{'code': '3511', 'text': 'Geração de energia elétrica'}],
        'atividades_secundarias': [],
        'porte': 'PEQUENA',
        'natureza_juridica': '',
        'capital_social': '10000.00'
    }

    import requests

    monkeypatch.setattr(requests, 'get', lambda *a, **k: DummyResponse(fake_payload))

    resp = client.post('/api/empresas/import-receita', json={'cnpj': '11.111.111/1111-11'})
    assert resp.status_code == 200
    body = resp.json()
    assert body.get('created') is True

    # Check empresa inserted
    rows = db_rows('SELECT * FROM empresas_esg WHERE cnpj = ?', ('11.111.111/1111-11',))
    assert len(rows) == 1

    # Check audit entry
    audits = db_rows('SELECT * FROM import_audit WHERE cnpj = ? ORDER BY imported_at DESC', ('11.111.111/1111-11',))
    assert len(audits) >= 1
    assert audits[0]['action'] == 'insert'


def test_import_update_and_audit(monkeypatch):
    client = TestClient(app)

    # Ensure DB seeded
    seed_db(client)

    # First import to create
    first_payload = {
        'status': 'OK',
        'nome': 'EMPRESA A',
        'cnpj': '22.222.222/2222-22',
        'atividade_principal': [{'code': '7490', 'text': 'Consultoria ambiental'}],
    }

    import requests

    monkeypatch.setattr(requests, 'get', lambda *a, **k: DummyResponse(first_payload))
    r1 = client.post('/api/empresas/import-receita', json={'cnpj': '22.222.222/2222-22'})
    assert r1.status_code == 200 and r1.json().get('created') is True

    # Now update with different payload (simulate new data)
    second_payload = {
        'status': 'OK',
        'nome': 'EMPRESA A - ATUALIZADA',
        'cnpj': '22.222.222/2222-22',
        'atividade_principal': [{'code': '3511', 'text': 'Geração de energia elétrica'}],
    }

    monkeypatch.setattr(requests, 'get', lambda *a, **k: DummyResponse(second_payload))
    r2 = client.post('/api/empresas/import-receita', json={'cnpj': '22.222.222/2222-22'})
    assert r2.status_code == 200 and r2.json().get('created') is False

    # Check an audit 'update' exists for this CNPJ (order may vary depending on timestamps)
    audits = db_rows('SELECT * FROM import_audit WHERE cnpj = ? ORDER BY imported_at DESC', ('22.222.222/2222-22',))
    assert len(audits) >= 1
    assert any(a['action'] == 'update' for a in audits), f"expected at least one update audit, got: {audits}"
