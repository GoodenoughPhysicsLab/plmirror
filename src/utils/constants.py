import os
import physicsLab as pl

SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(os.path.dirname(SRC_DIR), "db")

user = pl.web.token_login(
    token="dqQXBDflrOYV4a82HMbNjFtz9k3C5hWL",
    auth_code="aUKltj1Nq7JOz0EWHDnXoYP6fk3G4rRd",
)
