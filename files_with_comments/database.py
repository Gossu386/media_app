import databases
import sqlalchemy

from src.config import (
    config,  # Import configuration settings, including environment variables.
)

# Metadata object to hold information about the database schema.
metadata = sqlalchemy.MetaData()

# Define the "posts" table schema.
post_table = sqlalchemy.Table(
    "posts",  # Table name
    metadata,  # Metadata object to associate the table with
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),  # Primary key column
    sqlalchemy.Column("body", sqlalchemy.String),  # Column to store the post content
)

# Define the "comments" table schema.
comment_table = sqlalchemy.Table(
    "comments",  # Table name
    metadata,  # Metadata object to associate the table with
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),  # Primary key column
    sqlalchemy.Column("body", sqlalchemy.String),  # Column to store the comment content
    sqlalchemy.Column(
        "post_id",  # Foreign key column to associate the comment with a post
        sqlalchemy.ForeignKey(
            "posts.id"
        ),  # References the "id" column in the "posts" table
        nullable=False,  # Ensures that every comment must be linked to a post
    ),
)

# Create a SQLAlchemy engine to connect to the database.
# The database URL is retrieved from the environment variable `DATABASE_URL` via the `config` object.
engine = sqlalchemy.create_engine(
    config.DATABASE_URL,  # Database connection string (e.g., SQLite, PostgreSQL)
    connect_args={
        "check_same_thread": False
    },  # SQLite-specific argument to allow multithreading
)

# Create all tables defined in the metadata object in the database.
metadata.create_all(engine)

# Create a `databases.Database` instance for asynchronous database operations.
# The `DATABASE_URL` and `DB_FORCE_ROLL_BACK` are retrieved from environment variables via the `config` object.
database = databases.Database(
    config.DATABASE_URL,  # Database connection string
    force_rollback=config.DB_FORCE_ROLL_BACK,  # Enables rollback for test environments to avoid persisting changes
)
