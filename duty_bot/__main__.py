import logging
import os
from database.database_migration import migrate_database


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)


def main():
    if os.getenv('MIGRATION').lower() == 'true':
        migrate_database()
    from app.app import telegram_bot
    logging.info("Starting telegram duty bot....")
    telegram_bot()


if __name__ == '__main__':
    main()
