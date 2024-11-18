from database.connect_to_db import Task, User, Session, create_db_and_tables
from actions.with_task import select_task, delete_task, create_task
from actions.with_user import select_user, delete_user, create_user

task1 = Task(name="Wake_up", description="TO get out of the bed", owner='admin')
user1 = User(login='admin', password='admin', role='admin')


with Session() as session:
    try:
        #create_task(task1, session)
        #print(select_task("Wake_up", session))
        #print(select_user('string', session))
        create_db_and_tables()
    except:
        session.rollback()
        raise
    else:
        session.commit()
