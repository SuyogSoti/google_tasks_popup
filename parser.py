from dataclasses import dataclass, field
import datetime
import re


@dataclass
class Task:
    title: str
    description: str = field(default="")
    duedate: str = field(default="")


re_date = re.compile("(^|\s)date:\w")
re_title = re.compile('".*"')
today = datetime.datetime.today()


def on_day(day: str):
    return today + datetime.timedelta(days=(day - today.weekday() + 7) % 7)


datetime_dict = {
    "today": lambda: today,
    "tomorrow": lambda: today + datetime.timedelta(days=1),
    "monday": lambda: on_day(0),
    "tuesday": lambda: on_day(1),
    "wednesday": lambda: on_day(2),
    "thursday": lambda: on_day(3),
    "friday": lambda: on_day(4),
    "saturday": lambda: on_day(5),
    "sunday": lambda: on_day(6),
    # "every_monday":
    # "every_tuesday":
    # "every_wednesday":
    # "every_thursday":
    # "every_friday":
    # "every_saturday":
    # "every_sunday":
}


def parse_date(date: str) -> datetime.datetime:
    date = date.lower()
    if date not in datetime_dict:
        return today
    func = datetime_dict[date]
    return func()


def parse_text(text: str) -> Task:
    duedate_match = re_date.search(text)
    duedate = ""
    if duedate_match:
        section = text[duedate_match.start():duedate_match.endpos].strip()
        duedate = section.split(":")[1]
        duedate = duedate.split(" ")[0].strip().lower()
        end = duedate_match.start() + 6 + len(duedate)
        text = text[:duedate_match.start()] + text[end:]

    title_match = re_title.search(text)
    title = text
    description = ""
    if title_match:
        end = text.find('"', title_match.start() + 1)
        section = text[title_match.start():end]
        title = section.replace('"', "")
        text = text[:title_match.start()] + text[end + 1:]
        description = text.replace("  ", " ")
    return Task(title=title, description=description, duedate=duedate.lower())


def test_parse_text():
    text = 'start description date:tomorrow end "some title" end description'
    task = parse_text(text)
    print(task)
    assert task.title == "some title"
    assert task.duedate == "tomorrow"
    assert task.description == "start description end end description"
