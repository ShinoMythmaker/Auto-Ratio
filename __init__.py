import bpy

def auto_adjust_resolution(scene):
    if not scene.auto_adjust_enabled or scene.is_swapping_resolution:
        return

    ar_x = scene.aspect_ratio_x
    ar_y = scene.aspect_ratio_y

    if ar_x <= 0 or ar_y <= 0:
        return

    cur_x = scene.render.resolution_x
    cur_y = scene.render.resolution_y

    if scene.last_res_x == 0 and scene.last_res_y == 0:
        scene.last_res_x = cur_x
        scene.last_res_y = cur_y
        return

    if cur_x != scene.last_res_x:
        scene.render.resolution_y = int(cur_x * ar_y / ar_x)
        scene.last_res_x = cur_x
        scene.last_res_y = scene.render.resolution_y
    elif cur_y != scene.last_res_y:
        scene.render.resolution_x = int(cur_y * ar_x / ar_y)
        scene.last_res_y = cur_y
        scene.last_res_x = scene.render.resolution_x

def scene_update_handler(dummy):
    scene = bpy.context.scene
    auto_adjust_resolution(scene)
    
def on_aspect_x_update(self, context):
    scene = context.scene
    ar_x = self.aspect_ratio_x
    ar_y = self.aspect_ratio_y
    if not scene.auto_adjust_enabled or scene.is_swapping_resolution:
        return
    if ar_x > 0 and ar_y > 0:
        self.render.resolution_x = int(self.render.resolution_y * ar_x / ar_y)
        self.last_res_x = self.render.resolution_x
        self.last_res_y = self.render.resolution_y

def on_aspect_y_update(self, context):
    scene = context.scene
    ar_x = self.aspect_ratio_x
    ar_y = self.aspect_ratio_y
    if not scene.auto_adjust_enabled or scene.is_swapping_resolution:
        return
    if ar_x > 0 and ar_y > 0:
        self.render.resolution_y = int(self.render.resolution_x * ar_y / ar_x)
        self.last_res_x = self.render.resolution_x
        self.last_res_y = self.render.resolution_y

class SWAP_RESOLUTION_OT_button(bpy.types.Operator):
    """Switches X and Y Resolution"""
    bl_idname = "render.swap_resolution"
    bl_label = "Swap Resolution"

    def execute(self, context):
        scene = context.scene
        scene.is_swapping_resolution = True
        new_x = scene.render.resolution_y
        new_y = scene.render.resolution_x
        new_ar_x = scene.aspect_ratio_y
        new_ar_y = scene.aspect_ratio_x

        scene.render.resolution_x = new_x
        scene.render.resolution_y = new_y
        scene.aspect_ratio_x = new_ar_x
        scene.aspect_ratio_y = new_ar_y

        scene.last_res_x = scene.render.resolution_x
        scene.last_res_y = scene.render.resolution_y

        scene.is_swapping_resolution = False
        return {'FINISHED'}

class RESOLUTION_TOOLS_PT_panel(bpy.types.Panel):
    bl_label = "Auto Ratio"
    bl_idname = "RESOLUTION_TOOLS_PT_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"
    bl_parent_id = "RENDER_PT_format"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        indent = 0.4
        
        col = layout.column()
        split = col.split(factor=indent)
        split.label(text=" ")
        split.prop(scene, "auto_adjust_enabled", toggle=True, text="Auto Adjust")
        
        
        
        split = col.split(factor=indent)
        col1 = split.column()
        col1.alignment="RIGHT"
        col1.label(text="Aspect Ratio")
        row_split = split.row(align=False)
        row_split.prop(scene, "aspect_ratio_x", text="X")
        row_split.operator("render.swap_resolution", text="", icon="ARROW_LEFTRIGHT")
        row_split.prop(scene, "aspect_ratio_y", text="Y")

def register():
    bpy.utils.register_class(RESOLUTION_TOOLS_PT_panel)
    bpy.utils.register_class(SWAP_RESOLUTION_OT_button)
    bpy.types.Scene.aspect_ratio_x = bpy.props.IntProperty(
        name="Aspect Ratio X", default=16, update=on_aspect_x_update)
    bpy.types.Scene.aspect_ratio_y = bpy.props.IntProperty(
        name="Aspect Ratio Y", default=9, update=on_aspect_y_update)
    bpy.types.Scene.last_res_x = bpy.props.IntProperty(
        name="Last Resolution X", default=0)
    bpy.types.Scene.last_res_y = bpy.props.IntProperty(
        name="Last Resolution Y", default=0)
    bpy.types.Scene.is_swapping_resolution = bpy.props.BoolProperty(
        name="Is Swapping Resolution", default=False)
    bpy.types.Scene.auto_adjust_enabled = bpy.props.BoolProperty(
        name="Auto Adjust Enabled", default=True, description="Enables/Disables automatic Resolution adjustment.")
    for h in list(bpy.app.handlers.depsgraph_update_post):
        if getattr(h, '__name__', None) == 'scene_update_handler':
            bpy.app.handlers.depsgraph_update_post.remove(h)
    bpy.app.handlers.depsgraph_update_post.append(scene_update_handler)

def unregister():
    bpy.utils.unregister_class(RESOLUTION_TOOLS_PT_panel)
    bpy.utils.unregister_class(SWAP_RESOLUTION_OT_button)
    del bpy.types.Scene.aspect_ratio_x
    del bpy.types.Scene.aspect_ratio_y
    del bpy.types.Scene.last_res_x
    del bpy.types.Scene.last_res_y
    del bpy.types.Scene.is_swapping_resolution
    del bpy.types.Scene.auto_adjust_enabled
    for h in list(bpy.app.handlers.depsgraph_update_post):
        if getattr(h, '__name__', None) == 'scene_update_handler':
            bpy.app.handlers.depsgraph_update_post.remove(h)


    
