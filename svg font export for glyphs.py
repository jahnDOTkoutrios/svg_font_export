import GlyphsApp
from fontTools.pens.svgPathPen import SVGPathPen
import os


def glyphToSVGPath(glyph, font):
    """Convert a glyph to an SVG path string using fontTools SVGPathPen."""
    try:
        # Glyphs glyphs do not have getParent(), so we pass the font
        svgPen = SVGPathPen(font)
        glyph.draw(svgPen)
        return svgPen.getCommands()
    except Exception as e:
        print(f"Error converting glyph {glyph.name} to SVG path: {e}")
        return ""


def exportSVGFont(font, savePath):
    try:
        fontName = font.familyName or "Unnamed"
        unitsPerEm = font.upm or 1000
        ascender = font.masters[0].ascender if font.masters else 800
        descender = font.masters[0].descender if font.masters else -200
        svg = []
        svg.append('<?xml version="1.0" standalone="no"?>')
        svg.append('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"')
        svg.append('"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">')
        svg.append('<svg xmlns="http://www.w3.org/2000/svg">')
        svg.append(f'  <defs>')
        svg.append(f'    <font id="{fontName}" horiz-adv-x="{int(unitsPerEm)}">')
        svg.append(f'      <font-face font-family="{fontName}" units-per-em="{int(unitsPerEm)}" ascent="{int(ascender)}" descent="{int(descender)}" />')

        for glyph in font.glyphs:
            # Use the first layer of the first master
            layer = glyph.layers[font.masters[0].id]
            if not glyph.unicode:
                continue
            try:
                unicode_int = int(str(glyph.unicode), 16) if isinstance(glyph.unicode, str) else int(glyph.unicode)
                unicodeChar = f'&#x{unicode_int:X};'
            except Exception as e:
                print(f"Error processing unicode for glyph {glyph.name}: {e}")
                continue
            svgPath = glyphToSVGPath(layer, font)
            svg.append(f'      <glyph unicode="{unicodeChar}" d="{svgPath}" horiz-adv-x="{layer.width}" />')

        svg.append('    </font>')
        svg.append('  </defs>')
        svg.append('</svg>')

        with open(savePath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(svg))

        print(f"SVG font exported to: {savePath}")
    except Exception as e:
        print(f"Error exporting SVG font: {e}")


def main():
    font = Glyphs.font
    if font is None:
        print("No font is open in Glyphs.")
        return
    try:
        desktopPath = os.path.expanduser("~/Desktop")
        svgFontPath = os.path.join(desktopPath, f"{font.familyName or 'ExportedFont'}.svg")
        exportSVGFont(font, svgFontPath)
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main() 