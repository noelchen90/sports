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

# def draw_points_on_pitch(
#     config: SoccerPitchConfiguration,
#     xy: np.ndarray,
#     face_color: sv.Color = sv.Color.RED,
#     edge_color: sv.Color = sv.Color.BLACK,
#     radius: int = 10,
#     thickness: int = 2,
#     padding: int = 50,
#     scale: float = 0.1,
#     pitch: Optional[np.ndarray] = None
# ) -> np.ndarray:
#     """
#     Draws points on a soccer pitch.

#     Args:
#         config (SoccerPitchConfiguration): Configuration object containing the
#             dimensions and layout of the pitch.
#         xy (np.ndarray): Array of points to be drawn, with each point represented by
#             its (x, y) coordinates.
#         face_color (sv.Color, optional): Color of the point faces.
#             Defaults to sv.Color.RED.
#         edge_color (sv.Color, optional): Color of the point edges.
#             Defaults to sv.Color.BLACK.
#         radius (int, optional): Radius of the points in pixels.
#             Defaults to 10.
#         thickness (int, optional): Thickness of the point edges in pixels.
#             Defaults to 2.
#         padding (int, optional): Padding around the pitch in pixels.
#             Defaults to 50.
#         scale (float, optional): Scaling factor for the pitch dimensions.
#             Defaults to 0.1.
#         pitch (Optional[np.ndarray], optional): Existing pitch image to draw points on.
#             If None, a new pitch will be created. Defaults to None.

#     Returns:
#         np.ndarray: Image of the soccer pitch with points drawn on it.
#     """
#     if pitch is None:
#         pitch = draw_pitch(
#             config=config,
#             padding=padding,
#             scale=scale
#         )

#     for point in xy:
#         scaled_point = (
#             int(point[0] * scale) + padding,
#             int(point[1] * scale) + padding
#         )
#         cv2.circle(
#             img=pitch,
#             center=scaled_point,
#             radius=radius,
#             color=face_color.as_bgr(),
#             thickness=-1
#         )
#         cv2.circle(
#             img=pitch,
#             center=scaled_point,
#             radius=radius,
#             color=edge_color.as_bgr(),
#             thickness=thickness
#         )

#     return pitch


# def draw_paths_on_pitch(
#     config: SoccerPitchConfiguration,
#     paths: List[np.ndarray],
#     color: sv.Color = sv.Color.WHITE,
#     thickness: int = 2,
#     padding: int = 50,
#     scale: float = 0.1,
#     pitch: Optional[np.ndarray] = None
# ) -> np.ndarray:
#     """
#     Draws paths on a soccer pitch.

#     Args:
#         config (SoccerPitchConfiguration): Configuration object containing the
#             dimensions and layout of the pitch.
#         paths (List[np.ndarray]): List of paths, where each path is an array of (x, y)
#             coordinates.
#         color (sv.Color, optional): Color of the paths.
#             Defaults to sv.Color.WHITE.
#         thickness (int, optional): Thickness of the paths in pixels.
#             Defaults to 2.
#         padding (int, optional): Padding around the pitch in pixels.
#             Defaults to 50.
#         scale (float, optional): Scaling factor for the pitch dimensions.
#             Defaults to 0.1.
#         pitch (Optional[np.ndarray], optional): Existing pitch image to draw paths on.
#             If None, a new pitch will be created. Defaults to None.

#     Returns:
#         np.ndarray: Image of the soccer pitch with paths drawn on it.
#     """
#     if pitch is None:
#         pitch = draw_pitch(
#             config=config,
#             padding=padding,
#             scale=scale
#         )

#     for path in paths:
#         scaled_path = [
#             (
#                 int(point[0] * scale) + padding,
#                 int(point[1] * scale) + padding
#             )
#             for point in path if point.size > 0
#         ]

#         if len(scaled_path) < 2:
#             continue

#         for i in range(len(scaled_path) - 1):
#             cv2.line(
#                 img=pitch,
#                 pt1=scaled_path[i],
#                 pt2=scaled_path[i + 1],
#                 color=color.as_bgr(),
#                 thickness=thickness
#             )

#         return pitch


# def draw_pitch_voronoi_diagram(
#     config: SoccerPitchConfiguration,
#     team_1_xy: np.ndarray,
#     team_2_xy: np.ndarray,
#     team_1_color: sv.Color = sv.Color.RED,
#     team_2_color: sv.Color = sv.Color.WHITE,
#     opacity: float = 0.5,
#     padding: int = 50,
#     scale: float = 0.1,
#     pitch: Optional[np.ndarray] = None
# ) -> np.ndarray:
#     """
#     Draws a Voronoi diagram on a soccer pitch representing the control areas of two
#     teams.

#     Args:
#         config (SoccerPitchConfiguration): Configuration object containing the
#             dimensions and layout of the pitch.
#         team_1_xy (np.ndarray): Array of (x, y) coordinates representing the positions
#             of players in team 1.
#         team_2_xy (np.ndarray): Array of (x, y) coordinates representing the positions
#             of players in team 2.
#         team_1_color (sv.Color, optional): Color representing the control area of
#             team 1. Defaults to sv.Color.RED.
#         team_2_color (sv.Color, optional): Color representing the control area of
#             team 2. Defaults to sv.Color.WHITE.
#         opacity (float, optional): Opacity of the Voronoi diagram overlay.
#             Defaults to 0.5.
#         padding (int, optional): Padding around the pitch in pixels.
#             Defaults to 50.
#         scale (float, optional): Scaling factor for the pitch dimensions.
#             Defaults to 0.1.
#         pitch (Optional[np.ndarray], optional): Existing pitch image to draw the
#             Voronoi diagram on. If None, a new pitch will be created. Defaults to None.

#     Returns:
#         np.ndarray: Image of the soccer pitch with the Voronoi diagram overlay.
#     """
#     if pitch is None:
#         pitch = draw_pitch(
#             config=config,
#             padding=padding,
#             scale=scale
#         )

#     scaled_width = int(config.width * scale)
#     scaled_length = int(config.length * scale)

#     voronoi = np.zeros_like(pitch, dtype=np.uint8)

#     team_1_color_bgr = np.array(team_1_color.as_bgr(), dtype=np.uint8)
#     team_2_color_bgr = np.array(team_2_color.as_bgr(), dtype=np.uint8)

#     y_coordinates, x_coordinates = np.indices((
#         scaled_width + 2 * padding,
#         scaled_length + 2 * padding
#     ))

#     y_coordinates -= padding
#     x_coordinates -= padding

#     def calculate_distances(xy, x_coordinates, y_coordinates):
#         return np.sqrt((xy[:, 0][:, None, None] * scale - x_coordinates) ** 2 +
#                        (xy[:, 1][:, None, None] * scale - y_coordinates) ** 2)

#     distances_team_1 = calculate_distances(team_1_xy, x_coordinates, y_coordinates)
#     distances_team_2 = calculate_distances(team_2_xy, x_coordinates, y_coordinates)

#     min_distances_team_1 = np.min(distances_team_1, axis=0)
#     min_distances_team_2 = np.min(distances_team_2, axis=0)

#     control_mask = min_distances_team_1 < min_distances_team_2

#     voronoi[control_mask] = team_1_color_bgr
#     voronoi[~control_mask] = team_2_color_bgr

#     overlay = cv2.addWeighted(voronoi, opacity, pitch, 1 - opacity, 0)

#     return overlay
