import asyncio
from aiohttp import ClientSession
from flask import Flask, render_template, jsonify

app = Flask(__name__)

SNMP_DEVICES = [
    {"ip": "192.168.1.1", "community_string": "public"},
    {"ip": "192.168.1.2", "community_string": "public"},
    # Add more SNMP devices as needed
]

async def check_printer_status(ip, community_string):
    # Implement your SNMP check logic here
    # For demonstration purposes, we'll assume printers are up
    # Replace this with your actual SNMP logic
    return {"ip": ip, "status": "Up"}

async def fetch_printer_statuses():
    tasks = []
    async with ClientSession() as session:
        for device in SNMP_DEVICES:
            tasks.append(check_printer_status(device["ip"], device["community_string"]))
        return await asyncio.gather(*tasks)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/printers')
def get_printer_statuses():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    printer_statuses = loop.run_until_complete(fetch_printer_statuses())
    return jsonify(printer_statuses)

if __name__ == '__main__':
    app.run(debug=True)
