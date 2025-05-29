import os
import time
import physicsLab as pl
from physicsLab.web._threadpool import ThreadPool
from utils import constants
from utils import db_guard

if not os.path.exists(os.path.join(constants.DB_DIR, "users.db")):
    raise FileExistsError("users.db already exists")

if __name__ == "__main__":
    if os.path.exists(os.path.join(constants.SRC_DIR, "user_index.ignore")):
        with open(os.path.join(constants.SRC_DIR, "user_index.ignore")) as f:
            index = int(f.read())
    else:
        index = 0

    with db_guard.SqliteGuard(os.path.join(constants.DB_DIR, "users.db")) as guard:
        conn = guard.conn
        cursor = guard.cursor

        # This table must exists
        # Only to show you the table structure
        # cursor.execute(
        #     """
        #     CREATE TABLE IF NOT EXISTS user_table (
        #         UserID TEXT PRIMARY KEY,
        #         UserNickname TEXT,
        #         UserSignature TEXT,
        #         UserVerification TEXT,
        #         UserAvatar INTEGER,
        #         UserAvatarRegion INTEGER,
        #         UserDecoration INTEGER,
        #         UserGold INTEGER,
        #         UserDiamond INTEGER,
        #         UserFragment INTEGER,
        #         UserLevel INTEGER,
        #         UserExperience INTEGER,
        #         UserPrestige INTEGER,
        #         UserSubscription INTEGER,
        #         UserSubscriptionUntil TEXT,
        #         UserIsBinded BOOLEAN,
        #         UserRegions TEXT,
        #         UserSocials TEXT,
        #         Statistic TEXT,
        #         Backpack TEXT,
        #         Bonuses TEXT,
        #         UserToken TEXT,
        #         TargetLink TEXT
        #     )
        # """
        # )

        cursor.execute("SELECT UserID FROM user_table")
        all_user_id: list[str] = [row[0] for row in cursor.fetchall()]
        increment = []

        print("$$ getting increasing user-id", flush=True)

        def _append_following(user_id: str) -> None:
            for a_user in pl.web.RelationsIter(
                constants.user,
                user_id=user_id,
                display_type="Following",
                max_retry=3,
            ):
                if a_user["User"]["ID"] not in all_user_id:
                    increment.append(a_user["User"]["ID"])

        def _append_follower(user_id: str) -> None:
            for a_user in pl.web.RelationsIter(
                constants.user,
                user_id=user_id,
                display_type="Follower",
                max_retry=3,
            ):
                if a_user["User"]["ID"] not in all_user_id:
                    increment.append(a_user["User"]["ID"])

        i = 0
        try:
            with ThreadPool(max_workers=4) as executor:
                tasks = []
                for a_user_id in all_user_id[index:]:
                    tasks.append(executor.submit(_append_following, a_user_id))
                    tasks.append(executor.submit(_append_follower, a_user_id))

                for a_task in tasks:
                    a_task.result()
                    if i % 2 == 0:
                        print(
                            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]"
                            f" index: {index + i // 2}, amount: {len(all_user_id)}",
                            flush=True,
                        )
                    i += 1
        except Exception as e:
            with open(os.path.join(constants.SRC_DIR, "user_index.ignore"), "w") as f:
                f.write(str(index + i - 1))
            raise e
        del i

        print(f"$$ Done, find {len(increment)} new users", flush=True)

        def _insert_user(user_id: str) -> None:
            user = constants.user.get_user(user_id, pl.GetUserMode.by_id)["Data"]
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

        with ThreadPool(max_workers=4) as executor:
            tasks = []
            for a_user_id in all_user_id:
                tasks.append(executor.submit(_insert_user, a_user_id))

            for i, a_task in enumerate(tasks):
                a_task.result()
                print(
                    f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"index: {i + 1}, amount: {len(all_user_id)}",
                    flush=True,
                )

        if os.path.exists(os.path.join(constants.SRC_DIR, "user_index.ignore")):
            os.remove(os.path.join(constants.SRC_DIR, "user_index.ignore"))
