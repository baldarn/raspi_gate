from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

from gpiozero import LED
from time import sleep

bp = Blueprint('gate', __name__)


@bp.route('/')
def index():
    """index page."""

    led = LED(11)
    led.on()
    sleep(1)
    led.off()

    return render_template('gate/index.html')


@bp.route('/open')
@login_required
def open():
    """Open the gate."""


    return redirect(url_for('gate.index'))

