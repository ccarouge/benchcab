from user_options import repo2
from setup.machine_inits import date

#
## Repositories to test, default is head of the trunk against personal repo.
## But if trunk is false, repo1 could be anything
#
trunk = False
repo1 = f"integration"
share_branch = True
repos = [repo1, repo2]
