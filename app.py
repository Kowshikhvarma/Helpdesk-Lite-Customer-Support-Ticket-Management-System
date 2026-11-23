"""Helpdesk Lite: a small Flask + SQLite ticket tracker."""
import os
import sqlite3
from pathlib import Path
from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
STATUSES = ('Open', 'In Progress', 'Resolved')
PRIORITIES = ('Low', 'Medium', 'High')


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(DATABASE=str(BASE_DIR / 'tickets.db'))
    if test_config:
        app.config.update(test_config)

    def connect():
        conn = sqlite3.connect(app.config['DATABASE'])
        conn.row_factory = sqlite3.Row
        return conn

    def init_db():
        with connect() as db:
            db.execute('''CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                priority TEXT NOT NULL DEFAULT 'Medium',
                status TEXT NOT NULL DEFAULT 'Open',
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )''')

    init_db()

    @app.get('/')
    def index():
        return render_template('index.html')

    @app.get('/api/tickets')
    def list_tickets():
        with connect() as db:
            tickets = [dict(row) for row in db.execute('SELECT * FROM tickets ORDER BY id DESC')]
        return jsonify(tickets)

    @app.post('/api/tickets')
    def create_ticket():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify(error='Send a JSON object.'), 400
        title = data.get('title')
        description = data.get('description', '')
        priority = data.get('priority', 'Medium')
        if not isinstance(title, str) or not title.strip() or len(title.strip()) > 120:
            return jsonify(error='Title must be 1–120 characters.'), 400
        if not isinstance(description, str) or len(description) > 2000:
            return jsonify(error='Description must be at most 2000 characters.'), 400
        if priority not in PRIORITIES:
            return jsonify(error='Invalid priority.'), 400
        with connect() as db:
            cursor = db.execute('INSERT INTO tickets (title, description, priority) VALUES (?, ?, ?)',
                                (title.strip(), description.strip(), priority))
            ticket = dict(db.execute('SELECT * FROM tickets WHERE id = ?', (cursor.lastrowid,)).fetchone())
        return jsonify(ticket), 201

    @app.patch('/api/tickets/<int:ticket_id>')
    def update_ticket(ticket_id):
        data = request.get_json(silent=True)
        if not isinstance(data, dict) or data.get('status') not in STATUSES:
            return jsonify(error='Provide a valid status.'), 400
        with connect() as db:
            cursor = db.execute('UPDATE tickets SET status = ? WHERE id = ?', (data['status'], ticket_id))
            if cursor.rowcount == 0:
                return jsonify(error='Ticket not found.'), 404
            ticket = dict(db.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,)).fetchone())
        return jsonify(ticket)

    @app.delete('/api/tickets/<int:ticket_id>')
    def delete_ticket(ticket_id):
        with connect() as db:
            cursor = db.execute('DELETE FROM tickets WHERE id = ?', (ticket_id,))
            if cursor.rowcount == 0:
                return jsonify(error='Ticket not found.'), 404
        return '', 204

    return app


if __name__ == '__main__':
    create_app().run(debug=os.environ.get('FLASK_DEBUG') == '1')
