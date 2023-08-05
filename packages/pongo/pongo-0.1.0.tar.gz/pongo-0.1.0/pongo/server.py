import bottle
import controller

app = bottle.default_app()

if __name__ == '__main__':
    from bottle import run
    run(host='localhost', port=8000)

