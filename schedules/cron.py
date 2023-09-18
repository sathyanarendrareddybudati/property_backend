from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

def run_command():
    try:
        call_command('property_data')
        logger.info("cron job was called")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

