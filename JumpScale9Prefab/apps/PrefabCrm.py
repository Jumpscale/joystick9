from js9 import j

app = j.tools.prefab._getBaseAppClass()


class PrefabCrm(app):
    NAME = "crm"

    def _init(self):
        self.git_url = "https://github.com/incubaid/crm"
        self.crm_dir = self.replace("$CODEDIR/github/incubaid/crm")

    def build(self):
        """
        Clone the crm repo and install postgresql, caddy, python requirements
        """
        if self.doneGet('build') or self.isInstalled():
            return

        # Install and start Postgres
        self.prefab.apps.postgresql.install()
        self.prefab.apps.postgresql.start()

        # Clone the repository and install python requirements
        self.prefab.development.git.pullRepo(self.git_url, dest=self.crm_dir, branch="production")
        self.prefab.package.multiInstall(["python3-dev", "libffi-dev"])
        requirements = j.sal.fs.readFile("{}/requirements.pip".format(self.crm_dir))
        self.prefab.development.pip.multiInstall(requirements)

        # Install Caddy
        self.prefab.apps.caddy.build(plugins=['iyo', 'git', 'mailout'], reset=True)
        self.prefab.apps.caddy.install(reset=True)

        self.doneSet('build')

    def install(self, reset=False, start=False, domain="localhost", caddy_port=80, db_name="crm", demo=False,
                client_id=None, client_secret=None):
        if reset is False and self.isInstalled():
            return
        if not self.doneGet('build'):
            self.build()

        if not self.doneGet('configure'):
            self.configure(domain=domain, caddy_port=caddy_port, db_name=db_name,
                           demo=demo, client_id=client_id, client_secret=client_secret)

        if start:
            self.start()

    def configure(self, caddy_port, db_name, demo, client_id, client_secret, domain):
        """
        Configure
        """

        # Configure Caddy
        log_dir = self.replace("{{LOGDIR}}/caddy/log")
        caddy_cfg = """
        #tcpport:{PORT}
        :{PORT}
        gzip
        log {LOGDIR}/access.log
        proxy / localhost:5000 {{
            header_upstream Host "{DOMAIN}"
        }}
        errors {{
            * {LOGDIR}/errors.log
        }}
        """.format(PORT=caddy_port, LOGDIR=log_dir, DOMAIN=domain)

        if client_id and client_secret:
            caddy_cfg += """
            oauth {{
                client_id                       {CLIENT_ID}
                client_secret                   {CLIENT_SECRET}
                redirect_url                    http://{DOMAIN}/iyo_callback
                extra_scopes                    user:address,user:email,user:phone
                allow_extension                 api
                allow_extension                 graphql
                authentication_required         /
            }}
            """.format(CLIENT_ID=client_id, CLIENT_SECRET=client_secret, DOMAIN=domain)
        self.prefab.core.dir_ensure(log_dir)
        self.prefab.core.file_write(self.replace("$CFGDIR/caddy.cfg"), caddy_cfg)

        # Configure Database
        if not self.prefab.apps.postgresql.isStarted():
            self.prefab.apps.postgresql.start()

        cmd = """
        cd {src_dir}
        export POSTGRES_DATABASE_URI="postgresql://postgres:postgres@localhost:5432/{db_name}"
        export ENV=prod
        export FLASK_APP=app.py
        flask createdb
        flask db migrate
        flask db upgrade
        """
        if demo:
            cmd += "flask loadfixtures"
        cmd = cmd.format(src_dir=self.crm_dir, db_name=db_name)
        self.prefab.core.run(cmd, profile=True)

        self.doneSet('configure')

    def start(self, db_name="crm"):
        """
        Start postgres, caddy, crm
        """
        if not self.prefab.apps.postgresql.isStarted():
            self.prefab.apps.postgresql.start()

        if not self.prefab.apps.caddy.isStarted():
            self.prefab.apps.caddy.start()

        cmd = "cd {src_dir};"
        cmd += "export POSTGRES_DATABASE_URI=postgresql://postgres:postgres@localhost:5432/{db_name};"
        cmd += "export ENV=prod;flask db upgrade; uwsgi --ini uwsgi.ini"
        cmd = cmd.format(src_dir=self.crm_dir, db_name=db_name)
        self.prefab.processmanager.ensure(name="crm", cmd=cmd, autostart=True)
