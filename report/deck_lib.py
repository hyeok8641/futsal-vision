from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION

FONT = "맑은 고딕"
MONO = "Consolas"
DARK = RGBColor(0x17, 0x26, 0x1F)     # 짙은 잔디색 (제목·마무리 배경)
INK = RGBColor(0x1F, 0x29, 0x33)      # 본문 글자
MUTED = RGBColor(0x5F, 0x6B, 0x76)    # 보조 글자
TINT = RGBColor(0xEE, 0xF4, 0xF0)     # 카드 배경
LINE = RGBColor(0xD3, 0xDC, 0xD6)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREEN = RGBColor(0x2E, 0x8B, 0x57)    # 검출
ORANGE = RGBColor(0xE8, 0x83, 0x1F)   # 추정
RED = RGBColor(0xD1, 0x43, 0x43)      # 놓침
GRAY = RGBColor(0xB8, 0xC2, 0xBC)

W, H = Inches(13.333), Inches(7.5)


class Deck:
    def __init__(self, footer):
        self.prs = Presentation()
        self.prs.slide_width, self.prs.slide_height = W, H
        self.blank = self.prs.slide_layouts[6]
        self.footer = footer
        self.n = 0

    def slide(self, title=None, dark=False, notes=None):
        s = self.prs.slides.add_slide(self.blank)
        self.n += 1
        bg = s.background.fill
        bg.solid()
        bg.fore_color.rgb = DARK if dark else WHITE
        if title:
            text(s, 0.6, 0.38, 12.1, 0.8, title, 30, WHITE if dark else INK, bold=True)
        if self.n > 1:
            col = GRAY if dark else MUTED
            text(s, 0.6, 7.0, 8, 0.3, self.footer, 10, col)
            text(s, 11.7, 7.0, 1.0, 0.3, str(self.n), 10, col, align=PP_ALIGN.RIGHT)
        if notes:
            s.notes_slide.notes_text_frame.text = notes
        return s

    def save(self, path):
        self.prs.save(path)


def _style(run, size, color, bold=False, font=FONT, italic=False):
    f = run.font
    f.name, f.size, f.bold, f.italic = font, Pt(size), bold, italic
    f.color.rgb = color
    rpr = run._r.get_or_add_rPr()                     # 한글 글꼴도 같은 글꼴로 지정
    for tag in ("a:ea",):
        el = rpr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}ea")
        if el is None:
            from pptx.oxml.ns import qn
            el = rpr.makeelement(qn(tag), {})
            rpr.append(el)
        el.set("typeface", font)


def text(slide, x, y, w, h, content, size=16, color=INK, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, font=FONT, space=6, bullets=False, italic=False):
    """content: 문자열, 또는 줄 목록. 줄은 문자열이거나 [(글자, {옵션}), ...] 묶음."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    lines = content if isinstance(content, list) else [content]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(space)
        runs = line if isinstance(line, list) else [(line, {})]
        if bullets:
            runs = [("•  ", {"color": GREEN, "bold": True})] + list(runs)
        for t, o in runs:
            r = p.add_run()
            r.text = t
            _style(r, o.get("size", size), o.get("color", color), o.get("bold", bold),
                   o.get("font", font), o.get("italic", italic))
    return tb


def box(slide, x, y, w, h, fill=TINT, line=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06):
    sh = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.shadow.inherit = False
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(1.25)
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        sh.adjustments[0] = radius
    return sh


def chip(slide, x, y, w, h, label, fill, size=13):
    b = box(slide, x, y, w, h, fill=fill, radius=0.5)
    tf = b.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = label
    _style(r, size, WHITE, True)
    return b


def stat(slide, x, y, w, big, label, color=GREEN, big_size=40, label_size=13):
    text(slide, x, y, w, 0.8, big, big_size, color, bold=True)
    text(slide, x, y + big_size / 72 + 0.15, w, 0.7, label, label_size, MUTED)


def image(slide, path, x, y, w=None, h=None):
    kw = {}
    if w: kw["width"] = Inches(w)
    if h: kw["height"] = Inches(h)
    return slide.shapes.add_picture(path, Inches(x), Inches(y), **kw)


def table(slide, x, y, w, rows, col_w, size=13, row_h=0.42, header_fill=DARK, first_col_bold=False):
    shp = slide.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y), Inches(w),
                                 Inches(row_h * len(rows)))
    tbl = shp.table
    for j, cw in enumerate(col_w):
        tbl.columns[j].width = Inches(cw)
    for i, row in enumerate(rows):
        tbl.rows[i].height = Inches(row_h)
        for j, val in enumerate(row):
            cell = tbl.cell(i, j)
            opts = {}
            if isinstance(val, tuple):
                val, opts = val
            cell.margin_left = cell.margin_right = Inches(0.1)
            cell.margin_top = cell.margin_bottom = Inches(0.04)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = header_fill if i == 0 else (TINT if i % 2 == 0 else WHITE)
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = opts.get("align", PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER)
            r = p.add_run()
            r.text = str(val)
            _style(r, opts.get("size", size),
                   WHITE if i == 0 else opts.get("color", INK),
                   i == 0 or opts.get("bold", False) or (first_col_bold and j == 0))
    return tbl


def bar_chart(slide, x, y, w, h, cats, series, colors, title=None, maxv=1.0, fmt='0.000'):
    cd = CategoryChartData()
    cd.categories = cats
    for name, vals in series:
        cd.add_series(name, vals)
    gf = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(x), Inches(y),
                                Inches(w), Inches(h), cd)
    ch = gf.chart
    ch.font.name, ch.font.size = FONT, Pt(12)
    ch.font.color.rgb = MUTED
    ch.has_title = bool(title)
    if title:
        ch.chart_title.text_frame.text = title
        _style(ch.chart_title.text_frame.paragraphs[0].runs[0], 13, INK, True)
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.TOP
    ch.legend.include_in_layout = False
    va = ch.value_axis
    va.maximum_scale, va.minimum_scale = maxv, 0
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = LINE
    va.format.line.fill.background()
    va.tick_labels.font.size = Pt(11)
    ch.category_axis.format.line.color.rgb = LINE
    ch.category_axis.tick_labels.font.size = Pt(12)
    plot = ch.plots[0]
    plot.gap_width = 70
    plot.overlap = -10
    plot.has_data_labels = True
    dl = plot.data_labels
    dl.number_format, dl.number_format_is_linked = fmt, False
    dl.position = XL_LABEL_POSITION.OUTSIDE_END
    dl.font.size, dl.font.color.rgb = Pt(11), INK
    for s, c in zip(plot.series, colors):
        s.format.fill.solid()
        s.format.fill.fore_color.rgb = c
    return ch


def arrow(slide, x, y, w=0.35, h=0.4, color=GRAY):
    a = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x), Inches(y), Inches(w), Inches(h))
    a.fill.solid()
    a.fill.fore_color.rgb = color
    a.line.fill.background()
    a.shadow.inherit = False
    return a
