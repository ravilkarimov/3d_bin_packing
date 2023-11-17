import plotly.graph_objects as go
from src.types import Box


def plot_boxes(bounds: tuple[int, int, int], boxes: list[Box]):
    data = []

    for box in boxes:
        data.append(
            go.Mesh3d(
                # 8 vertices of a cube
                x=box.get_x_vertices(),
                y=box.get_y_vertices(),
                z=box.get_z_vertices(),
                # color='blue',
                # opacity=0,
                # i, j and k give the vertices of triangles
                i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
                j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
                k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
                # facecolor=['blue'] * 12,
                flatshading=True
            )
        )

    fig = go.Figure(data=data)
    fig.update_layout(
        autosize=False,
        height=650,
        scene=dict(
            xaxis=dict(nticks=4, range=[0, bounds[0]]),
            yaxis=dict(nticks=4, range=[0, bounds[0]]),
            zaxis=dict(nticks=4, range=[0, bounds[0]]),
        )
    )
    return fig
