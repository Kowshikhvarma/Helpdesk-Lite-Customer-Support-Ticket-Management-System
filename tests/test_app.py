import tempfile
import unittest
from pathlib import Path
from app import create_app


class TicketApiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = create_app({'TESTING': True, 'DATABASE': str(Path(self.temp.name) / 'test.db')})
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp.cleanup()

    def test_create_list_update_delete(self):
        created = self.client.post('/api/tickets', json={'title': 'Login issue', 'priority': 'High'})
        self.assertEqual(created.status_code, 201)
        ticket_id = created.json['id']
        self.assertEqual(len(self.client.get('/api/tickets').json), 1)
        changed = self.client.patch(f'/api/tickets/{ticket_id}', json={'status': 'Resolved'})
        self.assertEqual(changed.json['status'], 'Resolved')
        self.assertEqual(self.client.delete(f'/api/tickets/{ticket_id}').status_code, 204)
        self.assertEqual(self.client.get('/api/tickets').json, [])

    def test_validation_and_missing_ticket(self):
        self.assertEqual(self.client.post('/api/tickets', json={'title': ''}).status_code, 400)
        self.assertEqual(self.client.post('/api/tickets', json={'title': 'X', 'priority': 'Urgent'}).status_code, 400)
        self.assertEqual(self.client.patch('/api/tickets/999', json={'status': 'Resolved'}).status_code, 404)
        self.assertEqual(self.client.delete('/api/tickets/999').status_code, 404)


if __name__ == '__main__':
    unittest.main()
