bl_info = {
    "name": "Blender Project Helper",
    "author": "Blake Rogan",
    "version": (0, 1, "a"),
    "blender": (2, 74, 0),
    "location": "File > Blender Project Helper",
    "description": "Maya Like Project setup",
    "wiki_url": "http://Cethric.github.io/",
    "category": "system"
}

import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
from bpy import context


import os
def run_helper(context, root, suffix, exports, images, source_images, resources, scenes):
    uprefs = context.user_preferences
    fp = uprefs.filepaths
    print("Creating project at %r" % root)
    if not suffix:
        root = root.replace(".blProj")
    os.mkdir(root)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(root, "project.blend"))
    
    if exports:
        dir = os.path.join(root, "exports")
        os.mkdir(dir)
        
    if images:
        dir = os.path.join(root, "images")
        os.mkdir(dir)
        fp.render_output_directory = dir
        
    if source_images:
        dir = os.path.join(root, "source_images")
        os.mkdir(dir)
        fp.texture_directory = dir
        
    if resources:
        dir = os.path.join(root, "resources")
        os.mkdir(dir)
        fp.font_directory = dir
        fp.script_directory = dir
        fp.sound_directory = dir
        
    if scenes:
        os.mkdir(os.path.join(root, "scenes"))
    print("Done")

class ProjectOptions(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "blender_project.helper"
    bl_label = "Blender Project Helper"

    # ImportHelper mixin class uses this
    filename_ext = ".blProj"

    filter_glob = StringProperty(
            default="*.blProj",
            options={'HIDDEN'},
            )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    suffix = BoolProperty(
            name="Add Suffix",
            description="Place the '.blProj' suffic to the file",
            default=True,
            )
            
    exports = BoolProperty(
                name="Export Folder",
                description="Create a folder for the exports",
                default=True,
                )
                
    images = BoolProperty(
                name="Images Folder",
                description="Create a folder for the images",
                default=True,
                )
                
    source_images = BoolProperty(
                name="Source Images folder",
                description="Create a folder for the source images",
                default=True,
                )
                
    resources = BoolProperty(
                    name="Resources folder",
                    description="Create a folder for the misc resources",
                    default=True,
                    )
                    
    scenes = BoolProperty(
                    name="Scenes folder",
                    description="Create a folder for the images scenes",
                    default=True,
                    )

    def execute(self, context):
        run_helper(context, self.filepath, self.suffix, self.exports, self.images, self.source_images, self.resources, self.scenes)
        return {'FINISHED'}


# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ProjectOptions.bl_idname, text="Blender Project Helper")


def register():
    bpy.utils.register_class(ProjectOptions)
    bpy.types.INFO_MT_file.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ProjectOptions)
    bpy.types.INFO_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.blender_project.helper('INVOKE_DEFAULT')
