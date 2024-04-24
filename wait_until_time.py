import asyncio
import datetime

async def wait_until_time(target_time_str):
    # Convert target_time_str to a datetime object for today
    now = datetime.datetime.now()
    target_time = datetime.datetime.strptime(target_time_str, '%H:%M').replace(year=now.year, month=now.month, day=now.day)

    # Calculate the difference in seconds between now and the target time
    delta_seconds = (target_time - now).total_seconds()

    # If the target time has already passed, check how much time has passed
    if delta_seconds < 0:
        if abs(delta_seconds) > 5:
            print(f"Target time has already passed by more than 5 seconds ({-delta_seconds} seconds ago).")
            return False
        else:
            print(f"Target time was less than 5 seconds ago ({-delta_seconds} seconds).")
            return True

    # If we are before the target time, wait until that time
    print(f"Waiting for {delta_seconds} seconds until the target time...")
    await asyncio.sleep(delta_seconds)

    # After waiting, check the time again to confirm accuracy
    now_after_wait = datetime.datetime.now()
    actual_delta_seconds = (target_time - now_after_wait).total_seconds()

    # Determine if the wake-up happened within 5 seconds of the target time
    if abs(actual_delta_seconds) <= 5:
        print("Woke up on time or within 5 seconds after the target time.")
        return True
    else:
        print(f"Failed to wake up on time (difference: {actual_delta_seconds} seconds).")
        return False