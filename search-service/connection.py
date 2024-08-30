"""This module creates a database connection that is reused across the service."""

import os

import pymysql

connection = pymysql.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    db=os.getenv("DB_DBNAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)
