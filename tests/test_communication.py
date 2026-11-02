
import io
import json
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from http.server import ThreadingHTTPServer
from unittest.mock import patch

import numpy as np
from scipy.io import wavfile

import resqlink_server


class TestResQLinkCommunication(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create temporary storage for test audio and message information.
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.temp_path = Path(cls.temp_dir.name)

        cls.audio_path = cls.temp_path / "test_received.wav"
        cls.info_path = cls.temp_path / "test_info.json"

        # Replace the real output paths with temporary test paths.
        cls.audio_patch = patch.object(
            resqlink_server, "LATEST_AUDIO", cls.audio_path
        )
        cls.info_patch = patch.object(
            resqlink_server, "LATEST_INFO", cls.info_path
        )

        cls.audio_patch.start()
        cls.info_patch.start()

        # Start a local HTTP server without HTTPS certificates.
        cls.server = ThreadingHTTPServer(
            ("127.0.0.1", 0),
            resqlink_server.ResQLinkHandler
        )

        cls.port = cls.server.server_address[1]
        cls.base_url = f"http://127.0.0.1:{cls.port}"

        cls.server_thread = threading.Thread(
            target=cls.server.serve_forever,
            daemon=True
        )
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

        cls.audio_patch.stop()
        cls.info_patch.stop()

        cls.temp_dir.cleanup()

    def get_request(self, path):
        with urlopen(self.base_url + path) as response:
            return response.status, response.read()

    def post_audio(self, audio_data):
        request = Request(
            self.base_url + "/upload",
            data=audio_data,
            headers={"Content-Type": "audio/wav"},
            method="POST"
        )

        with urlopen(request) as response:
            return response.status, json.loads(response.read())

    def create_wav(self, sample_rate=16000):
        # Generate a short test audio signal.
        samples = np.zeros(1600, dtype=np.int16)

        buffer = io.BytesIO()
        wavfile.write(buffer, sample_rate, samples)

        return buffer.getvalue()

    def test_sender_page(self):
        status, content = self.get_request("/")

        self.assertEqual(status, 200)
        self.assertIn(b"ResQLink", content)
        self.assertIn(b"Sender", content)

    def test_receiver_page(self):
        status, content = self.get_request("/receiver")

        self.assertEqual(status, 200)
        self.assertIn(b"Receiver", content)

    def test_status_before_upload(self):
        status, content = self.get_request("/status")

        self.assertEqual(status, 200)
        self.assertEqual(json.loads(content), {})

    def test_latest_audio_before_upload(self):
        with self.assertRaises(HTTPError) as error:
            self.get_request("/latest.wav")

        self.assertEqual(error.exception.code, 404)

    def test_upload_valid_audio(self):
        audio_data = self.create_wav()

        status, result = self.post_audio(audio_data)

        self.assertEqual(status, 200)
        self.assertTrue(result["ok"])
        self.assertEqual(result["samples"], 1600)
        self.assertIn("bit_errors", result)
        self.assertIn("ber", result)

        self.assertTrue(self.audio_path.exists())
        self.assertTrue(self.info_path.exists())

    def test_status_after_upload(self):
        self.post_audio(self.create_wav())

        status, content = self.get_request("/status")
        result = json.loads(content)

        self.assertEqual(status, 200)
        self.assertIn("id", result)
        self.assertIn("samples", result)
        self.assertEqual(result["samples"], 1600)

    def test_latest_audio_after_upload(self):
        self.post_audio(self.create_wav())

        status, content = self.get_request("/latest.wav")

        self.assertEqual(status, 200)

        sample_rate, recovered_audio = wavfile.read(
            io.BytesIO(content)
        )

        self.assertEqual(sample_rate, 16000)
        self.assertEqual(recovered_audio.dtype, np.int16)
        self.assertEqual(len(recovered_audio), 1600)

    def test_reject_wrong_sample_rate(self):
        audio_data = self.create_wav(sample_rate=8000)

        with self.assertRaises(HTTPError) as error:
            self.post_audio(audio_data)

        self.assertEqual(error.exception.code, 400)

    def test_reject_unknown_endpoint(self):
        with self.assertRaises(HTTPError) as error:
            self.get_request("/unknown")

        self.assertEqual(error.exception.code, 404)


if __name__ == "__main__":
    unittest.main()

