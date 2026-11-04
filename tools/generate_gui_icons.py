"""Regenerate the original packaged SVG/PNG GUI icons (requires the shared Qt environment)."""
from pathlib import Path
from PySide6 import QtCore,QtGui,QtWidgets
app=QtWidgets.QApplication([])
root=Path(__file__).resolve().parents[1]
for package,project in [('bullet_view','bullet_view'),('flight_lens','flight_lens')]:
    directory=root/'projects'/project/'src'/package/'assets';directory.mkdir(exist_ok=True)
    common='<rect x="12" y="12" width="232" height="232" rx="54" fill="#142233"/><rect x="21" y="21" width="214" height="214" rx="46" fill="none" stroke="#30485f" stroke-width="3"/>'
    if package=='bullet_view':
        art='<g fill="none" stroke="#70d6ad" stroke-width="10" stroke-linecap="round"><path d="M83 83L173 173M83 173L173 83"/>'+''.join(f'<circle cx="{x}" cy="{y}" r="27"/>' for x,y in [(74,74),(182,74),(74,182),(182,182)])+'</g><circle cx="128" cy="128" r="24" fill="#142233" stroke="#58b8f5" stroke-width="7"/><path d="M128 113v30M113 128h30" stroke="#d9e6f4" stroke-width="5" stroke-linecap="round"/>'
    else:
        art='<circle cx="112" cy="109" r="61" fill="none" stroke="#58b8f5" stroke-width="13"/><path d="M157 154L205 202" stroke="#58b8f5" stroke-width="22" stroke-linecap="round"/><path d="M65 127L92 127L108 91L125 137L144 106L162 106" fill="none" stroke="#70d6ad" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"/>'
    (directory/'icon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 256 256">'+common+art+'</svg>\n')
    for size in (256,512):
        image=QtGui.QImage(size,size,QtGui.QImage.Format.Format_ARGB32_Premultiplied);image.fill(QtCore.Qt.GlobalColor.transparent)
        p=QtGui.QPainter(image);p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing);p.scale(size/256,size/256)
        p.setPen(QtCore.Qt.PenStyle.NoPen);p.setBrush(QtGui.QColor('#142233'));p.drawRoundedRect(QtCore.QRectF(12,12,232,232),54,54)
        p.setBrush(QtCore.Qt.BrushStyle.NoBrush);p.setPen(QtGui.QPen(QtGui.QColor('#30485f'),3));p.drawRoundedRect(QtCore.QRectF(21,21,214,214),46,46)
        def pen(color,width):
            p.setPen(QtGui.QPen(QtGui.QColor(color),width,QtCore.Qt.PenStyle.SolidLine,QtCore.Qt.PenCapStyle.RoundCap,QtCore.Qt.PenJoinStyle.RoundJoin))
        if package=='bullet_view':
            pen('#70d6ad',10)
            p.drawLine(83,83,173,173);p.drawLine(83,173,173,83)
            for x,y in [(74,74),(182,74),(74,182),(182,182)]:p.drawEllipse(QtCore.QPointF(x,y),27,27)
            pen('#58b8f5',7);p.setBrush(QtGui.QColor('#142233'));p.drawEllipse(QtCore.QPointF(128,128),24,24)
            pen('#d9e6f4',5);p.drawLine(128,113,128,143);p.drawLine(113,128,143,128)
        else:
            pen('#58b8f5',13);p.drawEllipse(QtCore.QPointF(112,109),61,61)
            pen('#58b8f5',22);p.drawLine(157,154,205,202)
            pen('#70d6ad',8);p.drawPolyline([QtCore.QPointF(x,y) for x,y in [(65,127),(92,127),(108,91),(125,137),(144,106),(162,106)]])
        p.end();assert image.save(str(directory/f'icon-{size}.png'))
