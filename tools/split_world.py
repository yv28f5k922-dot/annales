# Split the published single-file game back into source + data so it can be edited and rebuilt.
# usage: python3 tools/split_world.py annales-world.html  -> src/world.src.html, src/gamedata.json, src/flags.b64
import sys, re, os
s = open(sys.argv[1] if len(sys.argv) > 1 else 'annales-world.html').read()
out = sys.argv[2] if len(sys.argv) > 2 else 'src'
m = re.search(r'<script>window\.GAMEDATA=(.*?);</script>', s, re.S); open(os.path.join(out, 'gamedata.json'), 'w').write(m.group(1))
s = s[:m.start()] + '<script>/*__GAMEDATA__*/</script>' + s[m.end():]
m = re.search(r'<script>window\.FLAGSPRITE="(.*?)";</script>', s, re.S); open(os.path.join(out, 'flags.b64'), 'w').write(m.group(1))
s = s[:m.start()] + '<script>/*__FLAGS__*/</script>' + s[m.end():]
open(os.path.join(out, 'world.src.html'), 'w').write(s); print('ok', len(s))
