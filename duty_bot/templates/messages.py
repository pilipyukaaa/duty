import logging
from textwrap import dedent
from database.database_utils import execute_read_query


def get_duty():
    query = '''select telegram_username from public.duty where duty_date = CURRENT_DATE;'''
    today_duty = execute_read_query(query)
    logging.info(f"Today's duty officer from the database is {today_duty}")
    return " ".join(today_duty[0])


def generate_reply_message(message):
    return dedent(message).strip("\n")


def reply_message():
    message = generate_reply_message(f"""
    Today's duty officer is {get_duty()}
    Do you have any questions? Let us know! 🤌
    """)
    return message


def reply_message_weekend():
    message = generate_reply_message(f"""
        Today is a weekend, and no duty officers are available. We can assist on weekdays
        from 10:00 to 19:00 🌚
    """)
    return message


def reply_message_out_time():
    message = generate_reply_message(f"""
        Unfortunately, support is only available from 10:00 to 19:00 on weekdays.
        There's no one available to respond right now, but if your question is urgent,
        you can call +44444444444; maybe someone will pick up. 🌚
    """)
    return message