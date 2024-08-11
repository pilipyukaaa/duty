import logging
from database.database_utils import execute_write_query
from templates.duty_configmap import team, duty_calendar


def create_team_table():
    """Create table for team members in the PostgreSQL database."""

    team_ddl = """
        DROP TABLE IF EXISTS duty_team CASCADE;
        CREATE TABLE IF NOT EXISTS public.duty_team (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            telephone TEXT NOT NULL,
            telegram_username TEXT NOT NULL
        );
    """
    if execute_write_query(team_ddl):
        logging.info("Migration: Table team is created or already exists")


def fill_team():
    """Fill data in the team table."""

    query = """
        INSERT INTO public.duty_team (id, name, email, telephone, telegram_username)
        VALUES (%s, %s, %s, %s, %s)
    """
    if execute_write_query(query, params=team, executemany=True):
        logging.info(f"Migration: Table team is filled by {team}")


def create_duty_calendar_table():
    """Create table for duty's mapping by day in the PostgreSQL database."""

    duty_calendar_ddl = """
        DROP TABLE IF EXISTS duty_calendar;
        CREATE TABLE IF NOT EXISTS public.duty_calendar (
            duty_id integer,
            duty_date date,
            CONSTRAINT duty_id
                FOREIGN KEY (duty_id) 
                REFERENCES duty_team (id)
        );
    """
    if execute_write_query(duty_calendar_ddl):
        logging.info("Migration: Table duty_calendar is created or already exists")


def fill_calendar():
    """Fill data in the duty_calendar table."""

    query = """
        INSERT INTO public.duty_calendar (duty_id, duty_date)
        VALUES (%s, %s);
    """
    if execute_write_query(query, duty_calendar, executemany=True):
        logging.info(f"Migration: Table duty_calendar is filled by {duty_calendar}")


def create_duty_view():
    """Create view which join duty_calendar and duty_team tables by duty_id in the PostgreSQL database."""

    duty_view_ddl = """
        CREATE OR REPLACE VIEW public.duty AS
        SELECT
            id,
            name,
            email,
            telephone,
            telegram_username,
            c.duty_date
        FROM
            public.duty_team t
            INNER JOIN public.duty_calendar c ON t.id = c.duty_id;
    """
    if execute_write_query(duty_view_ddl):
        logging.info("Migration: View duty is created or replaced")


def migrate_database():
    logging.info("Migration is True, starting migration process....")
    create_team_table()
    create_duty_calendar_table()
    create_duty_view()
    fill_team()
    fill_calendar()
    logging.info("Migration process is complete....")
