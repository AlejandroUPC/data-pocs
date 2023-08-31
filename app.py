import json
import asyncio
from nats.aio.client import Client as NATS
from datetime import datetime
import psycopg2

DATABASE_URL = "postgresql://username:password@localhost:5432/mydatabase"
NATS_SERVER = "nats://localhost:4222"
NATS_TOPIC = "postgres.*.*"

DB_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432",
}


async def run():
    nc = NATS()

    await nc.connect(NATS_SERVER)

    async def message_handler(msg):
        event = json.loads(msg.data.decode())
        operation = event["payload"]["op"]
        event_ts = datetime.fromtimestamp(event["payload"]["ts_ms"] / 1000)
        if operation == "c":
            queries = [
                (
                    f"INSERT INTO department_dim_history (department_id, valid_from, valid_until, department_description) VALUES ({event['payload']['after']['department_id']}, '{event_ts}', NULL, '{event['payload']['after']['department_description']}')"
                ),
            ]
        if operation == "u":
            queries = [
                (
                    f"UPDATE department_dim_history SET valid_until = '{event_ts}' WHERE department_id = {event['payload']['before']['department_id']} AND valid_until IS NULL"
                ),
                (
                    f"INSERT INTO department_dim_history (department_id, valid_from, valid_until, department_description) VALUES ({event['payload']['after']['department_id']}, '{event_ts}', NULL, '{event['payload']['after']['department_description']}')"
                ),
            ]

        if operation == "d":
            queries = [
                (
                    f"UPDATE department_dim_history SET valid_until = '{event_ts}' WHERE department_id = {event['payload']['before']['department_id']} AND valid_until IS NULL"
                )
            ]
        with psycopg2.connect(**DB_PARAMS) as conn:
            with conn.cursor() as cur:
                for query in queries:
                    cur.execute(query)
            conn.commit()

    await nc.subscribe(NATS_TOPIC, cb=message_handler)

    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(run())
