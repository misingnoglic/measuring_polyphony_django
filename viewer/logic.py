# Files for dealing with verovio library logic
# Github links from questions I've asked from verovio:
# https://github.com/rism-ch/verovio/issues/523
# https://github.com/rism-ch/verovio/issues/491
# https://github.com/rism-ch/verovio/issues/490

import verovio
import secrets
import base64
import xml.etree.ElementTree as ET


def svg_size(svg_string: str):
    root = ET.fromstring(svg_string)
    return root.attrib['width'].strip("px"), root.attrib['height'].strip("px")


def load_mei_tk(mensural=True):
    """
    Loads the verovio toolkit
    :param mensural: If the piece is mensural or not
    :return: Toolkit
    """
    tk = verovio.toolkit(False)
    # The path for my resource folder - probably will change on server
    tk.setResourcePath(secrets.font_path)
    # Suggested by developer on github for mensural MEI files
    if mensural:
        tk.setNoLayout(True)

    else:
        tk.setPageHeight(2000)
        tk.setPageWidth(1500)
        tk.redoLayout()

    tk.setFormat("mei")
    return tk


def mei_to_svg(file_path: str, mensural=True):
    """
    Takes the path for an MEI, and returns the SVG file. 
    :param file_path: Path to the MEI
    :return: SVG
    """
    tk = load_mei_tk(mensural=mensural)
    tk.loadFile(file_path)
    svg_string = tk.renderToSvg(1)
    return svg_string

def mei_to_midi(file_path: str, bpm: int):
    """
    Turns an MEI file to a midi file - adds the bpm as 800
    :param file_path: Path to mei
    :param bpm: BPM of the midi
    :return: MIDI file (list of bytes)
    """

    # Add the BPM
    mei = open(file_path).read()
    s = "scoreDef"
    i = mei.find(s)
    mei = mei[:i+len(s)] + f''' midi.bpm="{bpm}" '''+mei[i+len(s):]

    # load it into verovio and make it a midi file
    tk = load_mei_tk()
    tk.loadData(mei)
    midi = tk.renderToMidi()

    data = base64.b64decode(midi)
    return data
