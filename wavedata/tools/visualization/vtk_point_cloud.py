import numpy as np
import vtk
from vtk.util import numpy_support


class VtkPointCloud:
    def __init__(self):

        # References to the converted numpy arrays to avoid seg faults
        self.np_to_vtk_points = None
        self.np_to_vtk_cells = None

        # VTK Data
        self.vtk_poly_data = vtk.vtkPolyData()
        self.vtk_points = vtk.vtkPoints()
        self.vtk_cells = vtk.vtkCellArray()

        # Colours for each point in the point cloud
        self.vtk_colours = vtk.vtkUnsignedCharArray()
        self.vtk_colours.SetNumberOfComponents(3)
        self.vtk_colours.SetName("Colours")

        # Poly Data
        self.vtk_poly_data.SetPoints(self.vtk_points)
        self.vtk_poly_data.SetVerts(self.vtk_cells)

        # Poly Data Mapper
        self.vtk_poly_data_mapper = vtk.vtkPolyDataMapper()
        self.vtk_poly_data_mapper.SetInputData(self.vtk_poly_data)

        # Actor
        self.vtk_actor = vtk.vtkActor()
        self.vtk_actor.SetMapper(self.vtk_poly_data_mapper)

    def set_points(self, points, point_colours=None):
        """
        Sets the point cloud to be visualized

        :param points: point cloud in the form N x [x, y, z]
        :param point_colours: BGR pixel colours corresponding to each point from OpenCV
        """

        num_points = len(points)

        # Set the points
        flattened_points = np.array(points).flatten().astype(np.float32)
        self.np_to_vtk_points = numpy_support.numpy_to_vtk(flattened_points,
                                                           deep=True, array_type=vtk.VTK_TYPE_FLOAT32)
        self.np_to_vtk_points.SetNumberOfComponents(3)
        self.vtk_points.SetData(self.np_to_vtk_points)

        # Create cells, one per point, cells in the form: [length, point index]
        cell_lengths = np.ones(num_points)
        cell_indices = np.arange(0, num_points)
        flattened_cells = np.array([cell_lengths, cell_indices]).transpose().flatten()
        flattened_cells = flattened_cells.astype(np.int32)

        # Convert list of cells to vtk format and set the cells
        self.np_to_vtk_cells = numpy_support.numpy_to_vtk(flattened_cells,
                                                          deep=True, array_type=vtk.VTK_ID_TYPE)
        self.np_to_vtk_cells.SetNumberOfComponents(2)
        self.vtk_cells.SetCells(num_points, self.np_to_vtk_cells)

        if point_colours is not None:
            # Set point colours if provided
            # Rearrange OpenCV BGR into RGB format
            point_colours = np.array(point_colours)[:, [2, 1, 0]]

            # Set the point colours
            flattened_colours = np.array(point_colours).flatten()
            self.vtk_colours = numpy_support.numpy_to_vtk(flattened_colours,
                                                          deep=True, array_type=vtk.VTK_TYPE_UINT8)
            self.vtk_colours.SetNumberOfComponents(3)

        else:
            # Add heights if no colours provided

            y_min = np.amin(points, axis=0)[1]
            y_max = np.amax(points, axis=0)[1]
            y_range = y_max - y_min
            pts_y = (points.transpose()[1] - y_min) / y_range

            height_array = pts_y.astype(np.float32)
            self.vtk_colours = numpy_support.numpy_to_vtk(height_array,
                                                          deep=True, array_type=vtk.VTK_TYPE_FLOAT32)
            self.vtk_colours.SetNumberOfComponents(1)

            # Update PolyDataMapper to display height scalars
            self.vtk_poly_data_mapper.SetColorModeToDefault()
            self.vtk_poly_data_mapper.SetScalarRange(0, 1.0)
            self.vtk_poly_data_mapper.SetScalarVisibility(1)

        # Set point colours in Poly Data
        self.vtk_poly_data.GetPointData().SetScalars(self.vtk_colours)
