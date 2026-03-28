import unittest
import sys
import os

# Adjuct the system path to allow importing from the src directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from scanner import parse_port_range, parse_ip_range

class TestScannerFunctions(unittest.TestCase):
    
    def test_parse_single_ip(self):
        ips = parse_ip_range("192.168.1.1")
        self.assertEqual(ips, ["192.168.1.1"])

    def test_parse_multiple_ips(self):
        ips = parse_ip_range("10.0.0.1, 192.168.1.200")
        self.assertEqual(ips, ["10.0.0.1", "192.168.1.200"])

    def test_parse_single_port(self):
        start, end = parse_port_range("80")
        self.assertEqual(start, 80)
        self.assertEqual(end, 80)

    def test_parse_port_range(self):
        start, end = parse_port_range("1-65535")
        self.assertEqual(start, 1)
        self.assertEqual(end, 65535)

if __name__ == '__main__':
    unittest.main()
