from pymysql import connect
from app_init import get_settings


settings = get_settings()
conn = connect(
    user=settings['mysql']['user'],
    password=settings['mysql']['password'],
    host=settings['mysql']['host'],
    database=settings['mysql']['database']
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM subscriber")
subscribers = cursor.fetchall()
channels = {}

for subscriber in subscribers:
    if not subscriber[1] in channels:
        channels.update({
            subscriber[1]: [
                subscriber[2],
            ]
        })
    else:
        if not subscriber[2] in channels[subscriber[1]]:
            channels[subscriber[1]].append(subscriber[2])
        else:
            cursor.execute("DELETE FROM subscriber WHERE id = %s", subscriber[0])
conn.commit()

