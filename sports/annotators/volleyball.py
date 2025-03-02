from typing import Optional, List

import cv2
import supervision as sv
import numpy as np

from sports.configs.volleyball import VolleyballCourtConfiguration

def draw_volleyball_court(
    config: VolleyballCourtConfiguration,
    inside_color: sv.Color = sv.Color(245, 161, 66),  # Orange
    outside_color: sv.Color = sv.Color(66, 161, 245),  # Blue 
    line_color: sv.Color = sv.Color.WHITE,
    padding: int = 20,
    line_thickness: int = 1,
    scale: float = 0.1
) -> np.ndarray:
    """
    Draws a volleyball court with specified dimensions, colors, and scale.

    Args:
        config (VolleyballCourtConfiguration): Configuration object containing the
            dimensions and layout of the court.
        inside_color (sv.Color, optional): Color of the court inside the boundaries.
            Defaults to sv.Color(245, 161, 66) (orange).
        outside_color (sv.Color, optional): Color of the court outside the boundaries.
            Defaults to sv.Color(66, 161, 245) (blue).
        line_color (sv.Color, optional): Color of the court lines.
            Defaults to sv.Color.WHITE.
        padding (int, optional): Padding around the court in pixels.
            Defaults to 20.
        line_thickness (int, optional): Thickness of the court lines in pixels.
            Defaults to 1.
        scale (float, optional): Scaling factor for the court dimensions.
            Defaults to 0.1.

    Returns:
        np.ndarray: Image of the volleyball court.
    """
    scaled_width = int(config.width * scale)
    scaled_length = int(config.length * scale)

    court_image = np.ones(
        (scaled_width + 2 * padding, scaled_length + 2 * padding, 3),
        dtype=np.uint8
    ) * np.array(outside_color.as_bgr(), dtype=np.uint8)

    # color the inside of the court 
    court_boundaries = []
    for start, end in [config.vertices[i-1] for i in config.boundary_vertices_indices]:
        scaled_point = [int(start * scale) + padding,
                        int(end * scale) + padding]
        court_boundaries.append(scaled_point)

    cv2.fillPoly(court_image, pts=[np.array(court_boundaries)], color=inside_color.as_bgr())

    for start, end in config.edges:
        point1 = (int(config.vertices[start - 1][0] * scale) + padding,
                  int(config.vertices[start - 1][1] * scale) + padding)
        point2 = (int(config.vertices[end - 1][0] * scale) + padding,
                  int(config.vertices[end - 1][1] * scale) + padding)
        cv2.line(
            img=court_image,
            pt1=point1,
            pt2=point2,
            color=line_color.as_bgr(),
            thickness=line_thickness
        )

    return court_image

def draw_points_on_court(
    config: VolleyballCourtConfiguration,
    xy: np.ndarray,
    face_color: sv.Color = sv.Color.RED,
    edge_color: sv.Color = sv.Color.BLACK,
    radius: int = 1,
    thickness: int = 1,
    padding: int = 20,
    scale: float = 0.1,
    court: Optional[np.ndarray] = None
) -> np.ndarray:
    """
    Draws points on a volleyball court.

    Args:
        config (VolleyballCourtConfiguration): Configuration object containing the
            dimensions and layout of the court.
        xy (np.ndarray): Array of points to be drawn, with each point represented by
            its (x, y) coordinates.
        face_color (sv.Color, optional): Color of the point faces.
            Defaults to sv.Color.RED.
        edge_color (sv.Color, optional): Color of the point edges.
            Defaults to sv.Color.BLACK.
        radius (int, optional): Radius of the points in pixels.
            Defaults to 10.
        thickness (int, optional): Thickness of the point edges in pixels.
            Defaults to 2.
        padding (int, optional): Padding around the court in pixels.
            Defaults to 50.
        scale (float, optional): Scaling factor for the court dimensions.
            Defaults to 0.1.
        court (Optional[np.ndarray], optional): Existing court image to draw points on.
            If None, a new court will be created. Defaults to None.

    Returns:
        np.ndarray: Image of the volleyball court with points drawn on it.
    """
    if court is None:
        court = draw_volleyball_court(
            config=config,
            padding=padding,
            scale=scale
        )

    for point in xy:
        scaled_point = (
            int(point[0] * scale) + padding,
            int(point[1] * scale) + padding
        )
        cv2.circle(
            img=court,
            center=scaled_point,
            radius=radius,
            color=face_color.as_bgr(),
            thickness=-1
        )
        cv2.circle(
            img=court,
            center=scaled_point,
            radius=radius,
            color=edge_color.as_bgr(),
            thickness=thickness
        )

    return court