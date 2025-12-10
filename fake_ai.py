import random
import json
from faker import Faker

fake = Faker()

def generate_fake_data(service_type):
    if service_type == "ssh":
        return {
            "users": [
                {"username": "admin", "password": "admin123"},
                {"username": "root", "password": "toor"}
            ],
            "files": ["/etc/passwd", "/var/log/auth.log"],
            "hostname": f"server-{random.randint(1,100)}"
        }
    else:  # http
        return {
            "pages": ["/", "/login", "/admin"],
            "users": [
                {"username": "admin", "email": "admin@company.com"},
                {"username": "user1", "email": "user1@company.com"}
            ],
            "company": fake.company()
        }

def generate_attack(honeypot_id, service_type):
    attacks = [
        {"type": "Port Scan", "complexity": "Low", "color": "green"},
        {"type": "Brute Force", "complexity": "Medium", "color": "yellow"},
        {"type": "SQL Injection", "complexity": "High", "color": "red"}
    ]
    
    attack = random.choice(attacks)
    return {
        "id": random.randint(1000, 9999),
        "honeypot_id": honeypot_id,
        "attacker_ip": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
        "attack_type": attack["type"],
        "complexity": attack["complexity"],
        "color": attack["color"],
        "timestamp": fake.iso8601()
    }