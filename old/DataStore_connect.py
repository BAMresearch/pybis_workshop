import marimo

__generated_with = "0.10.14"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Using openBIS via `pyBIS`""")
    return


@app.cell(hide_code=True)
def con_settings(getuser, mo, pat_stored):
    _top = mo.md('## Connecting to an openBIS server')
    _help = mo.accordion({'Fill in form and press button to connect! Get more help here!': mo.md("""
    If the _PAT_ field is filled, the connection is made by a Personal Access Token. If not,e _username_ and _password_ will be used. The connection will be established or renewed when pressing the button, you should see a success message below. Pelase be patient, this may need a couple of seconds.
    """)})
    url_i = mo.ui.text(value='https://main.datastore.bam.de/', kind='url', label='openBIS URL: ', full_width=True)
    pat_i = mo.ui.text(value=pat_stored, kind='password', label='PAT: ', placeholder='[if empty, password authentication will be used](hidden)', full_width=True)
    username_i = mo.ui.text(value=getuser(), label='Username: ')
    password_i = mo.ui.text(kind='password', label=' with Password: ', placeholder='PASSWORD (hidden)')
    connect_b = mo.ui.run_button(label='(Re)Connect')
    mo.vstack([_top, _help,
        mo.hstack((url_i, pat_i), justify='start', align='stretch', widths=[1,2]),
        mo.hstack((username_i, password_i, connect_b), justify='start'),
    ], align='stretch')
    return connect_b, password_i, pat_i, url_i, username_i


@app.cell(hide_code=True)
def connect(
    Openbis,
    connect_b,
    mo,
    password_i,
    pat_i,
    pybis_installed,
    url_i,
    username_i,
):
    o = None
    pat = None
    if not pybis_installed:
        _content = mo.md('Package `pyBIS` is not installed, please use `pip install pybis` to install')
        _kind    = 'danger'
    elif not connect_b.value:
        _content = mo.md('Please enter credentails above and press __(Re)Connect__!')
        _kind = 'neutral'
    else:
        if pat_i.value:
            pat = pat_i.value
            o = Openbis(url_i.value, token=pat)
            userid = o.token.split('-')[1]
        else:
            o = Openbis(url_i.value)
            userid = username_i.value
            o.login(userid, password_i.value)
        server_info = o.get_server_information()
        person = o.get_person(userid)
        home_space = person.space
        _content = mo.md(f"""__Connected!__

        * Server: `{o.hostname}`, version {server_info.openbis_version}, API version: {server_info.api_version}
        * UserId: `{person.userId}`, {person.firstName} {person.lastName} ({person.email})
        * Space: `{home_space}`
        * PAT: {pat is not None}

        _Now use object `o` to interact with openBIS (also available: `person`, `server_info`, `home_space` and `pat`!_
        """)
        _kind = 'success'

    mo.output.replace(mo.callout(_content, kind=_kind))
    return home_space, o, pat, person, server_info, userid


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Using the connection""")
    return


@app.cell
def use_openbis(home_space, mo, o):
    mo.stop(o is None, 'Please connect before running code like this!')
    # try to run something like
    home_space.get_objects(type='EXPERIMENTAL_STEP')
    # or
    # o.get_spaces()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Helpers""")
    return


@app.cell(hide_code=True)
def create_pat(mo, o, pat):
    import datetime

    _out = [
        mo.md("""### Create and Store a Personal Access Token (PAT)""")
    ]
    new_pat_ready = False
    if o is None:
        _out.append(mo.md("""Please connect first"""))
    elif not pat:
        _out.append(mo.md("""Check the forms and press the button to create and store a new _PAT_. After that you may re-run this notebook or enter the _PAT_ in the form to reconnect using your new _PAT_.
        """))
        new_pat_session_name = mo.ui.text(label='Session name: ', value='default')
        new_pat_valid_from = mo.ui.datetime(label='Valid from: ')
        _max = datetime.datetime.now() + datetime.timedelta(days=365)
        new_pat_valid_to = mo.ui.datetime(label='to: ', value=_max, stop=_max)
        new_pat_b = mo.ui.run_button(label='Create PAT')
        _out.append(mo.hstack([new_pat_session_name, new_pat_valid_from, new_pat_valid_to, new_pat_b], justify='start'))
        new_pat_ready = True
    else:
        _out.append(mo.md("""Looks like you are already connected using a _PAT_. For security reasons this connection can not be used to create a new _PAT_. You have to delete the _PAT_ from the connection settings form above, enter a _password_ and reconnect. After that you can try again creating a new _PAT_.
        """))
    mo.vstack(_out)
    return (
        datetime,
        new_pat_b,
        new_pat_ready,
        new_pat_session_name,
        new_pat_valid_from,
        new_pat_valid_to,
    )


@app.cell(hide_code=True)
def new_pat(
    mo,
    new_pat_b,
    new_pat_ready,
    new_pat_session_name,
    new_pat_valid_from,
    new_pat_valid_to,
    o,
    pat,
):
    def createPAT():
        """create and store a PAT, connection must be established using a password"""
        if pat is not None:
            return mo.md("__ERROR:__ You must login with a password instead of a _PAT_ to create a _PAT_!")
        sessionName = new_pat_session_name.value
        validFrom = new_pat_valid_from.value
        validTo   = new_pat_valid_to.value
        token = o.get_or_create_personal_access_token(sessionName, validFrom, validTo)
        from os import environ
        with open(environ.get('OPENBIS_PAT_FILE', 'OPENBIS_PAT.txt'), 'w') as pat_file:
            pat_file.write(token.permId)
        return token.permId

    if not pat and new_pat_ready and new_pat_b.value:
        new_pat = createPAT()
    else:
        new_pat = None
    new_pat
    return createPAT, new_pat


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Appendix""")
    return


@app.cell(hide_code=True)
def startup():
    import marimo as mo
    from getpass import getuser
    try:
        from pybis import Openbis
        pybis_installed = True
    except:
        Openbis = None
        pybis_installed = False
    try:
        from os import environ
        pat_stored = open(environ.get('OPENBIS_PAT_FILE', 'OPENBIS_PAT.txt'), 'r').read().strip()
    except:
        pat_stored = ''
    return Openbis, environ, getuser, mo, pat_stored, pybis_installed


if __name__ == "__main__":
    app.run()
