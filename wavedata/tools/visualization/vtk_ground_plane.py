import numpy as np
import vtk

from wavedata.tools.core import geometry_utils


class VtkGroundPlane:
    """
    VtkPlane is used to display a plane
    """

    def __init__(self):

        # Plane Source
        self.vtk_plane_source = vtk.vtkPlaneSource()
        self.vtk_plane_mapper = vtk.vtkPolyDataMapper()
        self.vtk_actor = vtk.vtkActor()

    def set_plane(self, ground_plane, xz_extents):
        """
        Calculates 3 points for plane visualization
        based on the provided ground plane

        :param ground_plane: Plane equation coefficients (a, b, c, d)
        :param xz_extents: Extents along the xz plane for visualization
        """
        min_x = xz_extents[0][0]
        max_x = xz_extents[0][1]
        min_z = xz_extents[1][0]
        max_z = xz_extents[1][1]

        plane_point0 = geometry_utils.calculate_plane_point(ground_plane, (min_x, None, min_z))
        plane_point1 = geometry_utils.calculate_plane_point(ground_plane, (max_x, None, min_z))
        plane_point2 = geometry_utils.calculate_plane_point(ground_plane, (min_x, None, max_z))

        self.vtk_plane_source.SetOrigin(*plane_point0)
        self.vtk_plane_source.SetPoint1(*plane_point1)
        self.vtk_plane_source.SetPoint2(*plane_point2)

        self.vtk_plane_source.Update()

        vtk_plane_poly_data = self.vtk_plane_source.GetOutput()
        self.vtk_plane_mapper.SetInputData(vtk_plane_poly_data)

        self.vtk_actor.SetMapper(self.vtk_plane_mapper)
