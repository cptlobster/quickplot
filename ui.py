import PySimpleGUI as sg
from math import comb

n = 3
v = 3

minx = -20
miny = -20
maxx = 20
maxy = 20

draw_axes = True
draw_lines = False

sg.theme("dark2")

fr_layout = [[sg.Text("X"), sg.Push(), sg.Text("Y")],
             [sg.Input("-10", s=6, justification="right", enable_events=True, key="px0"),
              sg.Input("-10", s=6, justification="right", enable_events=True, key="py0")],
             [sg.Input("0", s=6, justification="right", enable_events=True, key="px1"),
              sg.Input("-10", s=6, justification="right", enable_events=True, key="py1")],
             [sg.Input("0", s=6, justification="right", enable_events=True, key="px2"),
              sg.Input("10", s=6, justification="right", enable_events=True, key="py2")],
             [sg.Input("10", s=6, justification="right", enable_events=True, key="px3"),
              sg.Input("10", s=6, justification="right", enable_events=True, key="py3")]]

ctl_layout = [[sg.Button("+", button_color="green", key="-ADD-", expand_x=True),
               sg.Button("-", button_color="dark red", key="-DEL-", expand_x=True)],
              [sg.Checkbox("Lines", key="lines")],
              [sg.Checkbox("Axes", key="axes", default=True)],
              [sg.Text("Coordinate Plane")],
              [sg.Push(), sg.Input("20", s=4, justification="right", enable_events=True, key="maxx"), sg.Input("20", s=4, justification="right", enable_events=True, key="maxy")],
              [sg.Input("-20", s=4, justification="right", enable_events=True, key="minx"), sg.Input("-20", s=4, justification="right", enable_events=True, key="miny"), sg.Push()]]

layout = [[sg.Column([[sg.Frame("Control", ctl_layout, expand_x=True)],
                      [sg.Frame("Points", fr_layout, expand_x=True, expand_y=True, key="-PTS-")]], expand_y=True),
           sg.Graph(background_color=sg.theme_button_color()[1], canvas_size=(600, 600), graph_bottom_left=(-20, -20),
                    graph_top_right=(20, 20), key="plot")
           ]]

window = sg.Window('Bezier Curve Plotter', layout)

c = window['plot']


def create_pt():
    global n, v
    if n > v:
        v += 1
        window[f"px{v}"].update(visible=True)
        window[f"py{v}"].update(visible=True)
    else:
        n += 1
        v += 1
        window.extend_layout(window['-PTS-'], [[sg.Input("0", s=6, justification="right", enable_events=True, key=f"px{n}"),
                             sg.Input("0", s=6, justification="right", enable_events=True, key=f"py{n}")]])


def destroy_pt():
    global n, v
    if v > 1:
        window[f"px{v}"].update(visible=False)
        window[f"py{v}"].update(visible=False)
        v -= 1


def draw(vx, vy):
    c.change_coordinates((maxx, maxy), (minx, miny))
    c.erase()
    deg = len(vx) - 1
    # draw plane axes
    if draw_axes:
        c.draw_line((minx, 0), (maxx, 0), color=sg.theme_slider_color())
        c.draw_line((0, miny), (0, maxy), color=sg.theme_slider_color())

    # draw lines between bezier points
    if draw_lines:
        x = float(vx[0])
        y = float(vy[0])
        for d in range(1, deg + 1):
            px = x
            py = y
            x = float(vx[d])
            y = float(vy[d])
            c.draw_line((px, py), (x, y), color=sg.theme_slider_color())

    # draw bezier curve
    x = float(vx[0])
    y = float(vy[0])
    for u in range(1, 101):
        t = u / 100
        px = x
        py = y
        x = 0
        y = 0
        for d in range(0, deg + 1):
            ptx = vx[d]
            pty = vy[d]
            x += comb(deg, d) * (float(ptx) * ((1 - t) ** (deg - d)) * (t ** d))
            y += comb(deg, d) * (float(pty) * ((1 - t) ** (deg - d)) * (t ** d))
        c.draw_line((px, py), (x, y), color=sg.theme_text_color(), width=2)


def update(vr):
    draw_axes = vr["axes"]
    draw_lines = vr["lines"]
    vx = [vr[x] for x in vr.keys() if "px" in x][:(v + 1)]
    vy = [vr[y] for y in vr.keys() if "py" in y][:(v + 1)]
    if all([str(vr[i]).lstrip().isdigit() for i in ["maxx", "minx", "maxy", "miny"]]):
        maxx = int(vr["maxx"])
        minx = int(vr["minx"])
        maxy = int(vr["maxy"])
        miny = int(vr["miny"])
    if all(str(val).lstrip("-").isdigit() for val in vx) and all(str(val).lstrip("-").isdigit() for val in vy):
        draw(vx, vy)

while True:
    event, vr = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == "-ADD-":
        create_pt()
        window.visibility_changed()
        update(vr)
    if event == "-DEL-":
        destroy_pt()
        window.visibility_changed()
        update(vr)
    update(vr)

window.close()
