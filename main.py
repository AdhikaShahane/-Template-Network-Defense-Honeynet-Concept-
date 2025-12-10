from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import random
import time
from simple_honeypot import HoneypotManager
from fake_ai import generate_fake_data, generate_attack

# Create the app
app = FastAPI(title="Chameleon Glass")

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store connections and data
connections = []
honeypot_manager = HoneypotManager()
attacks = []

# WebSocket for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            # Just keep connection alive
            await websocket.receive_text()
    except:
        connections.remove(websocket)

# Send message to all connected clients
async def broadcast(message):
    for connection in connections:
        try:
            await connection.send_text(json.dumps(message))
        except:
            connections.remove(connection)

# API Routes
@app.get("/")
def read_root():
    return {"message": "Chameleon Glass - Baby Simple Version"}

@app.get("/api/status")
def get_status():
    honeypots = honeypot_manager.get_status()
    return {
        "honeypots": honeypots,
        "total_attacks": len(attacks),
        "unique_attackers": len(set(a['attacker_ip'] for a in attacks))
    }

@app.post("/api/deploy/{service_type}")
async def deploy_honeypot(service_type: str):
    honeypot_id = await honeypot_manager.deploy_honeypot(service_type)
    honeypot_status = honeypot_manager.get_status(honeypot_id)
    honeypot_status["fake_data"] = generate_fake_data(service_type)
    
    # Send update to all clients
    await broadcast({
        "type": "honeypot_deployed",
        "honeypot": honeypot_status
    })
    
    # Start simulating attacks for this honeypot
    asyncio.create_task(simulate_attacks(honeypot_id, service_type))
    
    return {"honeypot_id": honeypot_id, "status": "deployed"}

@app.post("/api/honeypot/{honeypot_id}/escalate")
async def escalate_deception(honeypot_id: str):
    new_level = honeypot_manager.escalate_deception(honeypot_id)
    honeypot_status = honeypot_manager.get_status(honeypot_id)
    
    if honeypot_status:
        honeypot_status["fake_data"] = generate_fake_data(honeypot_status["type"])
    
    await broadcast({
        "type": "deception_escalated", 
        "honeypot_id": honeypot_id,
        "new_level": new_level,
        "honeypot": honeypot_status
    })
    
    return {"new_level": new_level}

# Simulate attacks
async def simulate_attacks(honeypot_id, service_type):
    while honeypot_id in honeypot_manager.honeypots:
        # Wait 5-15 seconds between attacks
        await asyncio.sleep(random.randint(5, 15))
        
        # Generate attack
        attack = generate_attack(honeypot_id, service_type)
        attacks.append(attack)
        
        # Update honeypot attack count
        honeypot_manager.honeypots[honeypot_id].attacks_blocked += 1
        
        # Auto-escalate for complex attacks
        if attack["complexity"] == "High" and honeypot_manager.honeypots[honeypot_id].deception_level < 3:
            await escalate_deception(honeypot_id)
        
        # Send attack to all clients
        await broadcast({
            "type": "attack_detected",
            "attack": attack
        })

# Start the server - FIXED VERSION
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)