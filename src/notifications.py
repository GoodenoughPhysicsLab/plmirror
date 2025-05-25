import os
import physicsLab as pl

from utils import db_guard
from utils import constants

if __name__ == "__main__":
    user = pl.web.token_login(
        token="dqQXBDflrOYV4a82HMbNjFtz9k3C5hWL",
        auth_code="aUKltj1Nq7JOz0EWHDnXoYP6fk3G4rRd",
    )

    with db_guard.SqliteGuard(os.path.join(constants.DB_DIR, "notifications.db")) as guard:
        conn = guard.conn
        cursor = guard.cursor

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS notification_table (
            NotificationID TEXT,
            CategoryID INTEGER,
            TemplateID TEXT,
            TargetID TEXT,
            UserID TEXT,
            UserName TEXT,
            UserAvatar INTEGER,
            Timestamp INTEGER,
            TimestampInitial INTEGER,
            Unread INTEGER,
            Handled INTEGER,
            Fields TEXT
        )""")

        for i, msg in enumerate(pl.web.NotificationsIter(user, category_id=5, max_retry=3)):
            sql = f"""
                INSERT INTO notification_table (
                    NotificationID, CategoryID, TemplateID, TargetID,
                    UserID, UserName, UserAvatar, Timestamp,
                    TimestampInitial, Unread, Handled, Fields
                ) VALUES (
                    '{msg['ID']}', {msg['CategoryID']}, '{msg['TemplateID']}', '{msg['TargetID']}',
                    '{msg['Users'][0]}', '{msg['UserNames'][0]}', {msg['UserAvatar']}, {msg['Timestamp']},
                    {msg['TimestampInitial']}, {msg['Unread']}, {msg['Handled']}, \"{str(msg['Fields'])}\"
            )"""
            cursor.execute(sql)
