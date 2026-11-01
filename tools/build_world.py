# Put the data back into the source and write the playable single file.
# usage: python3 tools/build_world.py  -> annales-world.html
import os
d = os.path.join(os.path.dirname(__file__), '..', 'src')
src = open(os.path.join(d, 'world.src.html')).read()
data = open(os.path.join(d, 'gamedata.json')).read()
flags = open(os.path.join(d, 'flags.b64')).read().strip()
out = src.replace('/*__GAMEDATA__*/', 'window.GAMEDATA=' + data + ';').replace('/*__FLAGS__*/', 'window.FLAGSPRITE="' + flags + '";')
open('annales-world.html', 'w').write(out)
print(len(out))
