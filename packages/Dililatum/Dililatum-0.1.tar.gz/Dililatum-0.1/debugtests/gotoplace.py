def goto(event):
    game = event.args[0]
    sys = game.sys
    sys.signalactions.clear('beforeworldrun')
    try:
        plcnum = int(sys.etc.arguments[0])
    except IndexError:
        plcnum = 0
    try:
        pos = eval('[' + sys.etc.arguments[1] + ']')
    except Exception:
        pos = None
    game.world.set_place(plcnum, pos)

def main():
    action('beforegamerun', goto)
