import sys

from branch_command import (
    create_database,
    run_migrations,
    cleanup_database,
    delete_database
)


command = sys.argv[1]

if command == "create":
    create_database()

elif command == "migrate":
    revision = sys.argv[2]
    run_migrations(revision)

elif command == "cleanup":
    cleanup_database()

elif command == "delete":
    branch_id = sys.argv[2]
    delete_database(branch_id)

else:
    raise ValueError(f"Unknown command: {command}")