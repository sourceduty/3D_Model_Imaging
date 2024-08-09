require 'sketchup.rb'
require 'fileutils'

module VisualizeAndCaptureViews
  unless file_loaded?(__FILE__)
    toolbar = UI::Toolbar.new "Capture Views"

    cmd = UI::Command.new("Capture Views") {
      model = Sketchup.active_model
      view = model.active_view
      
      # Prompt user for distance from the model
      distance_input = UI.inputbox(["Distance from model:"], [10], "Set Camera Distance")
      distance = distance_input[0]

      # Define the standard views with relative directions
      views = {
        "top" => Geom::Vector3d.new(0, 0, distance),
        "bottom" => Geom::Vector3d.new(0, 0, -distance),
        "left" => Geom::Vector3d.new(-distance, 0, 0),
        "right" => Geom::Vector3d.new(distance, 0, 0),
        "front" => Geom::Vector3d.new(0, distance, 0),
        "back" => Geom::Vector3d.new(0, -distance, 0)
      }

      # Ask the user where to save the images
      output_dir = UI.select_directory(title: "Select output directory")
      if output_dir.nil?
        UI.messagebox("Output directory not selected!")
        next
      end

      # Set the image size
      width = 1920
      height = 1080

      # Loop through each view, set the camera to the specified distance, and save the image
      views.each do |name, vector|
        target = Geom::Point3d.new(0, 0, 0) # Assume model is centered at origin
        eye = target + vector
        up = vector.z.abs > 0 ? Geom::Vector3d.new(0, 1, 0) : Geom::Vector3d.new(0, 0, 1)

        # Set the camera with the calculated eye, target, and up vector
        camera = Sketchup::Camera.new(eye, target, up)
        model.active_view.camera = camera

        # Save the view as an image
        file_path = File.join(output_dir, "#{name}.png")
        view.write_image(file_path, width, height, false, 1)
      end

      UI.messagebox("Views captured and saved successfully!")
    }

    # Add the command to the toolbar
    cmd.small_icon = "capture_views_icon.png"
    cmd.large_icon = "capture_views_icon.png"
    cmd.tooltip = "Capture views and save as images"
    cmd.status_bar_text = "Capture views and save as images"
    cmd.menu_text = "Capture Views"
    toolbar = toolbar.add_item cmd
    toolbar.show

    file_loaded(__FILE__)
  end
end
