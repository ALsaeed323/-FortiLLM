import unittest
from unittest.mock import patch, MagicMock
from fortillm_ui import app

class FortiLLMTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Perform login to obtain auth_token cookie
        response = self.app.post('/login', data=dict(
            email='kopylopum@mailinator.com',
            password='Pa$$w0rd!',
            verify_human='on'
        ))

        set_cookie = response.headers.get('Set-Cookie', '')
        self.auth_cookie = None
        if 'auth_token=' in set_cookie:
            self.auth_cookie = set_cookie.split('auth_token=')[1].split(';')[0]

    def cookie_header(self):
        return {'Cookie': f'auth_token={self.auth_cookie}'} if self.auth_cookie else {}

    def print_result(self, case_id, description, expected, actual, passed):
        print(f"\n[{'✅' if passed else '❌'}] {case_id} - {description}")
        print(f"   Expected: {expected}")
        print(f"   Actual:   {actual}")

    def test_TC03_authenticate_researcher(self):
        """Check successful login returns auth_token cookie"""
        self.assertIsNotNone(self.auth_cookie)
        print("\n✅ TC03 - Login successful, auth_token cookie set")

    def test_TC07_fetch_attack_results(self):
        """Check if results endpoint returns 200 or 404"""
        response = self.app.get('/get_results', headers=self.cookie_header())
        self.assertIn(response.status_code, [200, 404])
        print(f"✅ TC07 - /get_results responded with {response.status_code} (expected 200 or 404)")

    @patch('controllers.attack_controller.subprocess.run')
    def test_TC05_launch_attack_authenticated(self, mock_subprocess):
        """Launch attack with mocked subprocess"""
        mock_result = MagicMock()
        mock_result.stdout = b"Mocked attack output"
        mock_result.stderr = b""
        mock_result.returncode = 0
        mock_subprocess.return_value = mock_result

        description = "Launch attack with cookie-based auth"
        response = self.app.post('/run-attack', headers=self.cookie_header(), data=dict(
            intention='injection',
            target_app='LLM_API'
        ))
        passed = response.status_code == 200
        self.print_result("TC05", description, "200 OK", response.status_code, passed)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
