from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()

class Table(Base):

    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

def first_page():
    print("1) Today's tasks")
    print("2) Add task")
    print("0) Exit")

    choice = int(input())
    print()

    if choice == 1:
        rows = session.query(Table).all()

        if len(rows) == 0:
            print("Nothing to do!")
        else:
            print("Today:")
            for i, row in enumerate(rows, 1):
                print(i, '. ', row, sep='')

        print()

    elif choice == 2:
        print("Enter task")
        new_task = input()
        new_row = Table(task=new_task)
        session.add(new_row)
        session.commit()
        print("The task has been added!")
        print()

    else:
        return 0

    return 1

page = 1
while True:
    if page == 1:
        page = first_page()

    if page == 0:
        break
