from database.connect_to_db import Task, Session, select_task, delete_task

task1 = Task(name="Wake_up", description="TO get out of the bed")
with Session() as session:
    try:
        #create_task(task1, session)
        print(select_task("Wake_up", session))
    except:
        session.rollback()
        raise
    else:
        session.commit()
