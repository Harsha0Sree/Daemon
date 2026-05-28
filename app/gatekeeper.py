from datetime import date

from app.dependencies import get_db
from app.models import Habit, WebsitesToBlock
from fastapi import Depends
from sqlalchemy import select, true
from sqlalchemy.orm import Session


def block_websites(websites_to_block):

    with open("/etc/hosts", "a") as file:
        for website in websites_to_block:
            file.write(f"127.0.0.1 {website}\n127.0.0.1 www.{website}\n")


def unblock_websites(db: Session = Depends(get_db)):

    with open("/etc/hosts", "r") as file:
        lines = file.readlines()
        result = db.execute(select(WebsitesToBlock)).scalars().all()
    managed_lines = set()
    for website in result:
        managed_lines.add(f"127.0.0.1 {website.url}\n")
        managed_lines.add(f"127.0.0.1 www.{website.url}\n")
    new_lines = [line for line in lines if line not in managed_lines]

    with open("/etc/hosts", "w") as file:
        file.writelines(new_lines)


def sync_blocked_sites(db: Session = Depends(get_db)):
    result = db.execute(select(WebsitesToBlock)).scalars().all()
    with open("/etc/hosts", "r") as file:
        content = file.read()
    for website in result:
        if content.find(f"127.0.0.1 {website.url}") == -1:
            content += f"127.0.0.1 www.{website.url}\n" + f"127.0.0.1 {website.url}\n"

    with open("/etc/hosts", "w") as x:
        x.write(content)
    print("syncing blocked sites")


def check_unlock_status(db: Session = Depends(get_db)) -> bool:
    result = (
        db.execute(select(Habit).where(Habit.is_required is true())).scalars().all()
    )
    if not result:
        return True
    should_unlock = False
    for habit in result:
        if not habit.logs:
            return False
        if habit.logs[-1].logs == str(date.today()):
            should_unlock = True
        else:
            return False
    return should_unlock
