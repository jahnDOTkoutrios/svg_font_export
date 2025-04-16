from mojo.roboFont import CurrentFont
from fontTools.pens.svgPathPen import SVGPathPen
import os

def glyphToSVGPath(glyph):
    """Convert a glyph to an SVG path string."""
    svgPen = SVGPathPen(glyph.getParent())
    glyph.draw(svgPen)
    return svgPen.getCommands()

def exportSVGFont(font, savePath):
    fontName = font.info.familyName or "Unnamed"
    svg = []
    svg.append('<?xml version="1.0" standalone="no"?>')
    svg.append('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"')
    svg.append('"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">')
    svg.append('<svg xmlns="http://www.w3.org/2000/svg">')
    svg.append(f'  <defs>')
    svg.append(f'    <font id="{fontName}" horiz-adv-x="{int(font.info.unitsPerEm)}">')
    svg.append(f'      <font-face font-family="{fontName}" units-per-em="{int(font.info.unitsPerEm)}" ascent="{int(font.info.ascender)}" descent="{int(font.info.descender)}" />')

    for glyph in font:
        if glyph.unicode is None:
            continue
        svgPath = glyphToSVGPath(glyph)
        unicodeChar = f'&#x{glyph.unicode:X};'
        svg.append(f'      <glyph unicode="{unicodeChar}" d="{svgPath}" horiz-adv-x="{glyph.width}" />')

    svg.append('    </font>')
    svg.append('  </defs>')
    svg.append('</svg>')

    with open(savePath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(svg))

    print(f"SVG font exported to: {savePath}")


font = CurrentFont()
if font:
    desktopPath = os.path.expanduser("~/Desktop")
    svgFontPath = os.path.join(desktopPath, f"{font.info.familyName or 'ExportedFont'}.svg")
    exportSVGFont(font, svgFontPath)
else:
    print("No font is open in RoboFont.")
