from waitress import serve
from Backend import App, CommandBuilder


def main():
    command = CommandBuilder()
    args = command.parse()

    app = App(args.env, isDebug = args.debug)
    flaskApp = app.initialize()

    if (args.debug):
        app.run()
    else:
        print(f"Serving at port {app.port}...")
        serve(app, port = app.port)


if __name__ == "__main__":
    main()