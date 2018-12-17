from . import app, is_authed
from flask import request, redirect, render_template, url_for, flash, make_response

@app.route('/registerServer', methods=['POST'])
def registerServer():
    """Register a new server with TheArk