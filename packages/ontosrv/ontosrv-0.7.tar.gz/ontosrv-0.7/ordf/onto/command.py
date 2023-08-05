from paste.script.command import Command as PasteCommand, BadCommand
from paste.deploy import appconfig
from glob import glob
from getpass import getuser
from ordf.graph import Graph
from ordf.vocab.opmv import Agent, Process
from ordf.handler import init_handler

import os

class Command(PasteCommand):
    group_name = "ontosrv"
    package_name = "ordf.onto"
    def parse_args(self, *av, **kw):
        super(Command, self).parse_args(*av, **kw)
        if not self.args:
            raise BadCommand("please specify a configuration file")
        config = self.args[0]
        self.args = self.args[1:]
        self.parse_config(config)
        self.housekeeping()

    def parse_config(self, config_file):
        ### parse the config file
        if not config_file.startswith("/"):
            context = { "relative_to": os.getcwd() }
        else:
            context = {}
        self.logging_file_config(config_file)
        self.config = appconfig('config:' + config_file, **context)

        envmod = self.package_name + ".config.environment"
        env = __import__(envmod, globals(), locals(), ["load_environment"])
        env.load_environment(self.config.global_conf, self.config.local_conf)
        self.handler = init_handler(self.config)

    def housekeeping(self):
        self.agent = Agent()
        self.agent.nick(getuser())

class Fresnel(Command):
    summary = "Load Fresnel Data"
    usage = "config.ini"
    parser = Command.standard_parser(verbose=True)
    parser.add_option("-b", "--base",
        dest="base",
        default="http://ordf.org/lens/",
        help="Base URI (default http://ordf.org/lens/)")
    def command(self):
        ontoroot = os.path.dirname(__file__)
        n3data = os.path.join(ontoroot, "n3")

        ctx = self.handler.context(getuser(), "ontosrv fixture import")
        for fpath in glob("%s/*.n3" % n3data):
            fname, ext = os.path.basename(fpath).rsplit(".", 1)
            graph = Graph(identifier=self.options.base + fname)
            graph.parse(fpath, format="n3")
            proc = Process()
            proc.use("file://" + fpath)
            proc.result(graph)
            ctx.add(graph)
        ctx.commit()
