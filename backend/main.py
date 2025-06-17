from waitress import serve
from src import App, CommandBuilder


command = CommandBuilder()
args = command.parse()

app = App(args.env)
flaskApp = app.initialize()

if (args.debug):
    app.run(debug = True)
else:
    print(f"Serving at port {app.port}...")
    serve(app, port = app.port)