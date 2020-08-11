
import os
from pprint import pprint
import typer
import sqlalchemy
from bullet import Bullet, Input
from configobj import ConfigObj
from sqlalchemy.sql import text

app = typer.Typer()
typer.echo("redmine - Simple tool to run common queries\n")

config = ConfigObj(os.environ["PYTHON_SYSTEM_SCRIPT_CONFIG"], stringify=False)
bullet_style = {
    k: config["BULLET"].as_int(k) if k != "bullet" else config["BULLET"]["bullet"]
    for k in config["BULLET"].keys()
}

# Database connection:
engine_str = "{ENGINE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"
engine = sqlalchemy.engine.create_engine(
    engine_str.format(**config["DATABASES"]["REDMINE"])
)

USERS = ["hendrik.huyskens", "christine.kuehnel", "kerstin.landvoigt"]
QUERIES = {
    "user_select": text(
        "SELECT "
        "* "
        "FROM users "
        "JOIN rli_daten.personalnummer ON id = redmine_user_id "
        "WHERE login = :login"
    )
}


def query_users():
    cli = Bullet(prompt="Select user by", choices=["list", "input"], **bullet_style)
    select = cli.launch()
    if select == "list":
        cli = Bullet(prompt="Select user", choices=USERS, **bullet_style)
        login = cli.launch()
    else:
        cli = Input(prompt="Enter user login: ")
        login = cli.launch()
    with engine.connect() as con:
        rows = con.execute(QUERIES["user_select"], login=login)
    for row in rows:
        pprint(dict(row))


TASKS = {"User": query_users}


@app.command()
def redmine():
    main_cli = Bullet(prompt="Select task", choices=list(TASKS.keys()), **bullet_style)
    task = main_cli.launch()

    # Run selected task:
    TASKS[task]()


def main():
    app()

