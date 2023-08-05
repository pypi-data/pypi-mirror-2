def extra1(event):
    print event.args[0].etc.arguments

def extra2(event):
    print event

def extra3(event):
    char = event.args[0]
    verb = event.uargs[0]
    print char.id + ' ' + verb + ' the name..'

def main():
    action('beforesystemstart', extra1)
    action('beforegamestart', extra2)
    action('beforecharacteradd', extra3, 'is')
