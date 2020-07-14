import json
from time import sleep

import psycopg2
from flask import Flask, request, Response


MAX_RADIUS_DEG = 1.0
MAX_RADIUS_ARCSEC = 3600.0 * MAX_RADIUS_DEG


CONNECTION = psycopg2.connect(host='catalog-sql', user='app', dbname='catalog')


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def index():
    return '''
    <p>
        Welcome to <a href="//snad.space">SNAD</a>
        <a href="http://variables.cn:88/ztf/">ZTF Catalog of Periodic Variable Stars</a>
        mirror
    </p>
    <p>
        See API details on <a href="/api/v1/help">/api/v1/help</a>
    </p>
    <p>
        See source code <a href="http://github.com/snad-space/ztf-periodic-catalog-db">on GitHub</a>
    </p>
    '''


@app.route('/api/v1/help')
def help():
    return f'''
    <h1>Available resources</h1>
    <h2><font face='monospace'>/api/v1/circle</font></h2>
        <p> Get objects in the circle</p>
        <p> Query parameters:</p>
        <ul>
            <li><font face='monospace'>ra</font> &mdash; right ascension of the circle center, degrees. Mandatory</li>
            <li><font face='monospace'>dec</font> &mdash; declination of the circle center, degrees. Mandatory</li>
            <li><font face='monospace'>radius_arcsec</font> &mdash; circle radius, arcseconds. Mandatory, should be positive and less than {MAX_RADIUS_ARCSEC}</li>
        </ul>
    '''


def to_str(x):
    return '' if x is None else str(x).strip()


def strip(x):
    try:
        return x.strip()
    except AttributeError:
        return x


def table_response(query, var=()):
    with CONNECTION.cursor() as cur:
        try:
            cur.execute(query, var)
        except psycopg2.errors.InternalError as e:
            return str(e), 404
        items = []
        columns = [c.name for c in cur.description]
        for row in cur:
            items.append(dict(zip(columns, map(strip, row))))
        message = json.dumps(items)
    return Response(message, mimetype='application/json')


@app.route('/api/v1/circle')
def select_in_circle():
    query = '''
        SELECT *
        FROM table2
        WHERE coord @ scircle %s
        ;
    '''
    try:
        ra = float(request.args['ra'])
        dec = float(request.args['dec'])
        radius_deg = float(request.args['radius_arcsec']) / 3600.0
    except KeyError:
        return 'ra, dec and radius_arcsec parameters are required', 404
    except ValueError:
        return 'ra, dec and radius_arcsec should be float numbers', 404
    if radius_deg > MAX_RADIUS_DEG:
        return f'radius should be less than {MAX_RADIUS_ARCSEC}', 404
    scircle = f'<({ra}d, {dec}d), {radius_deg}d>'
    return table_response(query, var=[scircle])
