"""Example script doing computations and I/O"""
import time
import json
from pathlib import Path
from urllib.request import urlopen

def p(msg, t_start = time.time()):
    t = time.time() - t_start
    print(f'{t:5.3f} sec :  {msg}')
    
p('starting computation')
data = list(range(int(1e7)))
sum(data)

p('starting network download')
url = 'http://upload.wikimedia.org/wikipedia/commons/5/5f/HubbleDeepField.800px.jpg'
contents = urlopen(url).read()

p('starting more computation')
text = '\n'.join(str(_) for _ in range(int(1e7)))

p('starting disk I/O')
path = Path('compute_and_io.temp')
for _ in range(10):
    path.write_text(text)
path.unlink()

p('done')