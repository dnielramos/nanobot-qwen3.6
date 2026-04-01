from apscheduler.schedulers.asyncio import AsyncIOScheduler
from agents.workers import code_reviewer
from memory.long_term import long_term_memory
import logging
import asyncio

logger = logging.getLogger(__name__)

async def scheduled_code_review():
    """Background task to review code automatically every hour."""
    logger.info("Running scheduled code review...")
    # Simulated review of a repo file
    result = await code_reviewer.execute_task("Review the python file src/main.py for security vulnerabilities.")

    # Store output to long-term memory for orchestrator review later
    long_term_memory.store_memory(
        session_id="system_cron",
        text=f"Cron Job Output:\n{result}",
        metadata={"type": "cron_job", "job_name": "scheduled_code_review"}
    )
    logger.info("Scheduled code review completed and stored in long-term memory.")

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(scheduled_code_review, 'interval', hours=1, id='code_review_job')
    scheduler.start()
    logger.info("Cron scheduler started.")
