# For now this is where I am just putting a scratch pad for my progress
# Github links from questions I've asked from verovio:
# https://github.com/rism-ch/verovio/issues/523
# https://github.com/rism-ch/verovio/issues/491
# https://github.com/rism-ch/verovio/issues/490

import verovio
from django.conf import settings
import secrets
import base64



def load_mei_tk(mensural=True):
    tk = verovio.toolkit(False)
    # The path for my resource folder - probably will change on server
    tk.setResourcePath(secrets.font_path)
    # Suggested by developer on github for mensural MEI files
    if mensural:
        tk.setNoLayout(True)
        #tk.setPageHeight(800)
        #tk.setPageWidth(2)
    tk.setFormat("mei")
    return tk



def mei_to_svg(file_path: str):
    tk = load_mei_tk()
    tk.loadFile(file_path)
    svg_string = tk.renderToSvg(1)
    return svg_string

def mei_to_midi(file_path: str):
    tk = load_mei_tk()
    mei = open(file_path).read()
    s = "scoreDef"
    i = mei.find(s)
    mei = mei[:i+len(s)] + ''' midi.bpm="800" '''+mei[i+len(s):]
    tk.loadData(mei)
    midi = tk.renderToMidi()

    data = base64.b64decode(midi)

    return data