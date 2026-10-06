import sys

from branch_command import (
    create_branch,
    run_migrations,
    cleanup_branch,
    delete_branch
)


command = sys.argv[1]

if command == "create":
    create_branch()

elif command == "migrate":
    revision = sys.argv[2]
    run_migrations(revision)

elif command == "cleanup":
    cleanup_branch()

elif command == "delete":
    branch_id = sys.argv[2]
    delete_branch(branch_id)

else:
    raise ValueError(f"Unknown command: {command}")