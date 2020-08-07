
from flask_login import login_required


@login_required
def need_login():
    pass