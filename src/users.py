import os
import time
import physicsLab as pl
from utils import constants
from utils import db_guard

if not os.path.exists(os.path.join(constants.DB_DIR, "users.db")):
    raise FileExistsError("users.db already exists")

if __name__ == "__main__":
    with db_guard.SqliteGuard(os.path.join(constants.DB_DIR, "users.db")) as guard:
        conn = guard.conn
        cursor = guard.cursor

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_table (
                UserID TEXT PRIMARY KEY,
                UserNickname TEXT,
                UserSignature TEXT,
                UserVerification TEXT,
                UserAvatar INTEGER,
                UserAvatarRegion INTEGER,
                UserDecoration INTEGER,
                UserGold INTEGER,
                UserDiamond INTEGER,
                UserFragment INTEGER,
                UserLevel INTEGER,
                UserExperience INTEGER,
                UserPrestige INTEGER,
                UserSubscription INTEGER,
                UserSubscriptionUntil TEXT,
                UserIsBinded BOOLEAN,
                UserRegions TEXT,
                UserSocials TEXT,
                Statistic TEXT,
                Backpack TEXT,
                Bonuses TEXT,
                UserToken TEXT,
                TargetLink TEXT
            )
        """
        )

        cursor.execute("SELECT UserID FROM user_table")
        all_user_id: set[str] = {row[0] for row in cursor.fetchall()}

        for i, a_user_id in enumerate(all_user_id):
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} :: i/{len(all_user_id)}: {a_user_id}")
            user = constants.user.get_user(a_user_id, pl.GetUserMode.by_id)["Data"]
            cursor.execute(
                """
                INSERT OR IGNORE INTO user_table (
                    UserID,
                    UserNickname,
                    UserSignature,
                    UserVerification,
                    UserAvatar,
                    UserAvatarRegion,
                    UserDecoration,
                    UserGold,
                    UserDiamond,
                    UserFragment,
                    UserLevel,
                    UserExperience,
                    UserPrestige,
                    UserSubscription,
                    UserSubscriptionUntil,
                    UserIsBinded,
                    UserRegions,
                    UserSocials,
                    Statistic,
                    Backpack,
                    Bonuses,
                    UserToken,
                    TargetLink
                ) VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            """,
                (
                    user["User"]["ID"],
                    user["User"]["Nickname"],
                    user["User"]["Signature"],
                    user["User"]["Verification"],
                    user["User"]["Avatar"],
                    user["User"]["AvatarRegion"],
                    user["User"]["Decoration"],
                    user["User"]["Gold"],
                    user["User"]["Diamond"],
                    user["User"]["Fragment"],
                    user["User"]["Level"],
                    user["User"]["Experience"],
                    user["User"]["Prestige"],
                    user["User"]["Subscription"],
                    user["User"]["SubscriptionUntil"],
                    user["User"]["IsBinded"],
                    str(user["User"]["Regions"]),
                    str(user["User"]["Socials"]),
                    str(user["Statistic"]),
                    user["Backpack"],
                    user["Bonuses"],
                    user["UserToken"],
                    user["TargetLink"],
                ),
            )
