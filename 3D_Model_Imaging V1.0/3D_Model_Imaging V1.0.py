# 3D_Model_Imaging V1.0

# 📷 Visualize 3D model files and capture images from six distinct views.

#Copyright (C) 2023,  Sourceduty - All Rights Reserved.
#THE CONTENTS OF THIS PROJECT ARE PROPRIETARY.

import vtk
import os

# Directory paths
input_dir = 'input_stl'
output_dir = 'output_images'

# Check if input directory exists
if not os.path.exists(input_dir):
    print(f'Error: Directory {input_dir} does not exist.')
    exit()

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# List all STL files in the input directory
stl_files = [f for f in os.listdir(input_dir) if f.endswith('.stl')]

if not stl_files:
    print(f'Error: No STL files found in {input_dir}.')
    exit()

for stl_file in stl_files:
    print(f'Processing {stl_file}...')

    # Read the STL file
    reader = vtk.vtkSTLReader()
    reader.SetFileName(os.path.join(input_dir, stl_file))

    # Map to a color
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    # Create an actor and set its color to light blue
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(0.53, 0.81, 0.98)  # Light blue

    # Create a renderer and set its background to white
    ren = vtk.vtkRenderer()
    ren.SetBackground(1, 1, 1)  # White
    ren_win = vtk.vtkRenderWindow()
    ren_win.AddRenderer(ren)

    # Add the actor to the renderer
    ren.AddActor(actor)
    ren.ResetCamera()

    # Set up the camera views for 6 sides
    views = ['1', '2', '3', '4', '5', '6']
    camera_orientations = [
        (0, 0, 1, 0, 1, 0),
        (0, 0, -1, 0, 1, 0),
        (-1, 0, 0, 0, 1, 0),
        (1, 0, 0, 0, 1, 0),
        (0, 1, 0, 0, 0, 1),
        (0, -1, 0, 0, 0, -1)
    ]

    for view, orientation in zip(views, camera_orientations):
        # Set camera orientation
        ren.GetActiveCamera().SetPosition(orientation[0], orientation[1], orientation[2])
        ren.GetActiveCamera().SetFocalPoint(0, 0, 0)  # Center of the model
        ren.GetActiveCamera().SetViewUp(orientation[3], orientation[4], orientation[5])
        ren.ResetCamera()

        # Update the render window
        ren_win.Render()

        # Capture the image
        w2if = vtk.vtkWindowToImageFilter()
        w2if.SetInput(ren_win)
        w2if.Update()

        writer = vtk.vtkPNGWriter()
        base_name = os.path.splitext(stl_file)[0]
        writer.SetFileName(os.path.join(output_dir, f'{base_name}_{view}.png'))
        writer.SetInputConnection(w2if.GetOutputPort())
        writer.Write()

    print(f'{stl_file} processed successfully!')

print('All images captured successfully!')