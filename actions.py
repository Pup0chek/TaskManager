from connect_to_db import Task, Session, create_task, get_by_name




task1 = Task(name="Wake_up", description="TO get out of the bed")
with Session() as session:
    try:
        #create_task(task1, session)
        print(get_by_name("Wake_up", session))
    except:
        session.rollback()
        raise
    else:
        session.commit()
