import sys
from epio.commands import AppCommand, CommandError

class Command(AppCommand):
    help = 'Run an arbitary command.'

    def handle_app(self, app, command=None, *args, **options):
        client = self.get_client(options)

        # Send the command request
        response, content = client.post("app/%s/run_command/" % app, {
            "cmdline": " ".join(args),
            "stdin": "",
        })

        # What came back?
        if response.status in (200, ):
            print content['output']
            sys.exit(content['returncode'])
        else:
            raise CommandError("Unknown error, %s: %s" % (response.status, content))


