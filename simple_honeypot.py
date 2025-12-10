import asyncio
import random

class SimpleHoneypot:
    def __init__(self, honeypot_id, service_type, port):
        self.id = honeypot_id
        self.type = service_type
        self.port = port
        self.deception_level = 1
        self.attacks_blocked = 0
        self.status = "active"

    def escalate_deception(self):
        if self.deception_level < 3:
            self.deception_level += 1
        return self.deception_level

    def get_status(self):
        return {
            "id": self.id,
            "type": self.type,
            "port": self.port,
            "deception_level": self.deception_level,
            "attacks_blocked": self.attacks_blocked,
            "status": self.status
        }

class HoneypotManager:
    def __init__(self):
        self.honeypots = {}
        self.next_port = 10000

    async def deploy_honeypot(self, service_type):
        port = self.next_port
        self.next_port += 1
        honeypot_id = f"{service_type}_{port}"
        
        honeypot = SimpleHoneypot(honeypot_id, service_type, port)
        self.honeypots[honeypot_id] = honeypot
        
        return honeypot_id

    def escalate_deception(self, honeypot_id):
        if honeypot_id in self.honeypots:
            return self.honeypots[honeypot_id].escalate_deception()
        return None

    def get_status(self, honeypot_id=None):
        if honeypot_id:
            return self.honeypots.get(honeypot_id).get_status() if honeypot_id in self.honeypots else None
        return {hid: honeypot.get_status() for hid, honeypot in self.honeypots.items()}