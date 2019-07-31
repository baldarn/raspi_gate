from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from raspi_gate.auth import login_required
from raspi_gate.db import get_db

from gpiozero import LED
from time import sleep
import datetime

bp = Blueprint('gate', __name__)

LAST_OPEN_KEY = 'LAST_OPEN'
GATE_OPEN_SECONDS = 50

@bp.route('/')
def index():
    """index page."""
    print(session.get(LAST_OPEN_KEY))
    last_open = session.get(LAST_OPEN_KEY)
    is_open = False
    if last_open is not None:
        is_open = (datetime.datetime.now() - datetime.timedelta(seconds=GATE_OPEN_SECONDS)) < last_open

    return render_template('gate/index.html', is_open=is_open)


@bp.route('/open')
@login_required
def open():
    """Open the gate."""

    led = LED(11)
    led.off()
    sleep(1)
    led.on()

    session[LAST_OPEN_KEY] = datetime.datetime.now()

    return redirect(url_for('gate.index'))

