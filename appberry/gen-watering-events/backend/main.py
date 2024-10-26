from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timedelta
from dateutil.rrule import rrule, DAILY, WEEKLY, MONTHLY, YEARLY
import asyncpg
from response_model import APIResponse  # Import the response model


# PostgreSQL connection settings
DB_HOST = "localhost"
DB_NAME = "smart_watering"
DB_USER = "postgres"
DB_PASSWORD = "postgres"


app = FastAPI()

# Frequency mapping for rrule
FREQUENCY_MAP = {
    "daily": DAILY,
    "weekly": WEEKLY,
    "monthly": MONTHLY,
    "yearly": YEARLY,
}


class DeviceResponse(BaseModel):
    id: int
    name: str


class ScheduleRequest(BaseModel):
    start_date: datetime = Field(..., description="Start date of the event")
    end_date: Optional[datetime] = Field(
        None, description="End date to limit occurrences"
    )
    frequency: str = Field(
        ..., description="Recurring frequency (daily, weekly, monthly, yearly)"
    )
    interval: int = Field(1, description="Interval between occurrences")
    count: Optional[int] = Field(None, description="Number of occurrences to generate")
    byweekday: Optional[List[int]] = Field(
        None, description="List of weekdays (0=Monday, 6=Sunday)"
    )
    device_id: int
    duration: int  # Duration in minutes


class ScheduleResponse(BaseModel):
    occurrences: List[str] = Field(
        ..., description="List of scheduled event occurrences as ISO 8601 strings"
    )


async def connect_db():
    """Connect to the PostgreSQL database."""
    return await asyncpg.connect(
        user=DB_USER, password=DB_PASSWORD, database=DB_NAME, host=DB_HOST
    )


@app.get("/devices", response_model=List[DeviceResponse])
async def get_devices():
    """Fetch the list of devices."""
    try:
        conn = await connect_db()
        rows = await conn.fetch("SELECT id, name FROM device")
        await conn.close()
        return [{"id": row["id"], "name": row["name"]} for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/schedules", response_model=APIResponse)
async def get_schedules():
    """Fetch schedules with occurrences and device information."""
    try:
        conn = await connect_db()
        query = """
        SELECT s.start_date, s.end_date,extract(EPOCH from	(end_date - start_date)) / 60 as duration_minutes, d.name as device_name, s.status, d.id as device_id 
        FROM schedule s
        JOIN device d ON s.fk_device_schedule = d.id
        where s.start_date >= CURRENT_DATE - INTERVAL '1 month'
        ORDER BY s.start_date;
        """
        rows = await conn.fetch(query)
        await conn.close()

        schedules = [
            {
                "title": f"{row['device_name']} ({row['duration_minutes']}) min",
                "start": row["start_date"].isoformat(),
                "end": row["end_date"].isoformat(),
                "duration_minutes": row["duration_minutes"],
                "device_name": row["device_name"],
                "status": row["status"],
            }
            for row in rows
        ]
        return APIResponse(
            status="success",
            message="Schedules fetched successfully.",
            result=schedules,
        )
    except Exception as e:
        return APIResponse(
            status="error", message="Failed to fetch schedules.", error_reason=str(e)
        )


@app.post("/generate_schedule", response_model=ScheduleResponse)
async def generate_schedule(request: ScheduleRequest):
    """Generate recurring schedules based on input parameters."""
    if request.frequency not in FREQUENCY_MAP:
        return {
            "error": "Invalid frequency. Choose from: daily, weekly, monthly, yearly."
        }

    rule = rrule(
        freq=FREQUENCY_MAP[request.frequency],
        dtstart=request.start_date,
        until=request.end_date,
        interval=request.interval,
        count=request.count,
        byweekday=request.byweekday,
    )

    # # Convert occurrences to ISO 8601 format strings
    # occurrences = [occurrence.isoformat() for occurrence in rule]

    # Calculate event occurrences and end times
    occurrences = []
    for start in rule:
        end = start + timedelta(minutes=request.duration)
        occurrences.append({"start": start, "end": end})

    print("ocurrences")
    print(occurrences)

    # Store occurrences in the PostgreSQL database
    try:
        conn = await connect_db()
        async with conn.transaction():
            for occ in occurrences:
                await conn.execute(
                    "INSERT INTO schedule (start_date, end_date, fk_device_schedule, duration, status) VALUES ($1, $2, $3, $4,'pending')",
                    occ["start"],
                    occ["end"],
                    request.device_id,
                    timedelta(minutes=request.duration),
                )

        await conn.close()
        # Convert occurrences to ISO 8601 strings for the response
        return APIResponse(
            status="success",
            message="Schedules saved successfully.",
            result="",
        )
    except Exception as e:
        print(f"Database error: {str(e)}")
        return APIResponse(
            status="error", message="Failed to generate schedule.", error_reason=str(e)
        )


# Run the server: uvicorn main:app --reload
