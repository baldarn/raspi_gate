from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from raspi_gate.auth import login_required
from raspi_gate.db import get_db

from gpiozero import LED
from time import sleep

bp = Blueprint('gate', __name__)


@bp.route('/')
def index():
    """index page."""
    return render_template('gate/index.html')


@bp.route('/open')
@login_required
def open():
    """Open the gate."""

    led = LED(11)
    led.off()
    sleep(1)
    led.on()

    return redirect(url_for('gate.index'))

