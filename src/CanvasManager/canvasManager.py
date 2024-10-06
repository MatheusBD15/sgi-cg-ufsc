from tkinter import *
from tkinter import ttk, filedialog, messagebox
from CanvasManager.objFileManager import export_as_obj_file, import_obj_file
from CanvasManager.screenObject import ScreenObject
from vars import *
from CanvasManager.viewport import Viewport
from CanvasManager.window import Window
from Math.transformations import (
    translate,
    scale,
    rotate_around_point,
    rotate_around_world,
    normalized_coordinate_transform
)
from Math.helpers import get_center_of_object
from CanvasManager.world import World
from CanvasManager.clipping import cohen_sutherland_clip
import numpy as np

class CanvasManager:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.movement_speed = 25
        self.mouseXw = 0
        self.mouseYw = 0
        self.clip_xmin = VIEWPORT_OFFSET
        self.clip_ymin = VIEWPORT_OFFSET
        self.clip_xmax = CANVAS_WIDTH - VIEWPORT_OFFSET
        self.clip_ymax = CANVAS_HEIGHT - VIEWPORT_OFFSET

        self.viewport = Viewport(
            self.clip_xmin,
            self.clip_ymin,
            self.clip_xmax,
            self.clip_ymax,
        )

        self.window = Window(
            self.clip_xmin,
            self.clip_ymin,
            self.clip_xmax,
            self.clip_ymax,
        )

        self.world = World((1, 0), (0, 1))
        self.display_file = STARTING_DISPLAY_FILE
        self.objects_var = StringVar(value=self.get_all_object_names())

        self.selected_objects = []
        self.objects_list = None

        self.setup_bindings()
        self.repaint()

    # Setup and initialization methods
    def setup_bindings(self):
        self.canvas.bind("<Button-4>", self.handle_zoom_in)
        self.canvas.bind("<Button-5>", self.handle_zoom_out)
        self.canvas.bind_all("<KeyPress>", self.handle_key_press)
        self.canvas.bind("<Motion>", self.handle_mouse_movement)
        self.canvas.bind_all("<Delete>", self.delete_selected_objects)

    def set_objects_list(self, listbox):
        self.objects_list = listbox
        self.objects_list.bind("<<ListboxSelect>>", self.on_select)
        self.objects_list.config(selectmode=MULTIPLE)

    # Event handling methods
    def handle_key_press(self, event: Event):
        movement_speed = self.movement_speed

        if event.keysym == "Right":
            self.window.move(-movement_speed, 0)
        elif event.keysym == "Left":
            self.window.move(movement_speed, 0)
        elif event.keysym == "Up":
            self.window.move(0, -movement_speed)
        elif event.keysym == "Down":
            self.window.move(0, movement_speed)

        self.repaint()

    def handle_mouse_movement(self, event: Event):
        self.mouseXw = event.x
        self.mouseYw = event.y
        self.repaint()

    def handle_zoom_in(self, event: Event):
        self.zoom(-0.1)

    def handle_zoom_out(self, event: Event):
        self.zoom(0.1)

    def on_select(self, event):
        selected_indices = self.objects_list.curselection()
        self.selected_objects = [self.display_file[i] for i in selected_indices]
        for obj in self.display_file:
            obj.selected = obj in self.selected_objects
        self.repaint()

    # Object management methods
    def add_object(self, obj: ScreenObject):
        self.display_file.append(obj)
        self.objects_var.set(self.get_all_object_names())
        self.repaint()

    def delete_selected_objects(self, event=None):
        if self.selected_objects:
            object_names = ", ".join([obj.name for obj in self.selected_objects])
            confirm = messagebox.askyesno(
                "Confirmar deleção",
                f"Tem certeza que deseja deletar os objetos selecionados: {object_names}?"
            )
            if confirm:
                for obj in self.selected_objects:
                    self.display_file.remove(obj)
                self.selected_objects = []
                self.objects_var.set(self.get_all_object_names())
                self.repaint()
                messagebox.showinfo("Deleção bem sucedida", "Objetos deletados.")
        else:
            messagebox.showinfo("No Selection", "Nenhum objeto está selecionado.")

    def get_all_object_names(self):
        return [f"{obj.name} - {obj.type}" for obj in self.display_file]

    def get_objects_list(self):
        return self.objects_var

    def clear_selected(self):
        for obj in self.selected_objects:
            obj.selected = False
        self.selected_objects = []
        self.repaint()

    # Transformation methods
    def rotate_selected(self, direction):
        if self.selected_objects:
            angle = float(self.rotate_entry.get() or 10)
            if direction == "clockwise":
                angle = angle * -1

            rotation_type = self.rotate_type.get() or "world"

            for obj in self.selected_objects:
                if rotation_type == "world":
                    obj.apply_transformation(rotate_around_world, angle)
                elif rotation_type == "object":
                    (xCenter, yCenter) = get_center_of_object(obj.world_coords)
                    obj.apply_transformation(rotate_around_point, xCenter, yCenter, angle)
                elif rotation_type == "arbitrary_point":
                    [tx, ty] = list(eval(self.rotate_point_entry.get() or "0, 0"))
                    obj.apply_transformation(rotate_around_point, tx, ty, angle)
            self.repaint()

    def translate_selected(self, dx, dy):
        for obj in self.selected_objects:
            obj.apply_transformation(translate, dx, dy)
        self.repaint()

    def translate_selected_right(self):
        translation_distance = float(self.translation_entry.get() or 10)
        angle_rad = np.radians(self.window.world_rotation_angle)
        dx = translation_distance * np.cos(angle_rad)
        dy = translation_distance * np.sin(angle_rad)
        self.translate_selected(dx, dy)

    def translate_selected_left(self):
        translation_distance = float(self.translation_entry.get() or 10)
        angle_rad = np.radians(self.window.world_rotation_angle)
        dx = -translation_distance * np.cos(angle_rad)
        dy = -translation_distance * np.sin(angle_rad)
        self.translate_selected(dx, dy)

    def translate_selected_up(self):
        translation_distance = float(self.translation_entry.get() or 10)
        angle_rad = np.radians(self.window.world_rotation_angle)
        dx = -translation_distance * np.sin(angle_rad)
        dy = translation_distance * np.cos(angle_rad)
        self.translate_selected(dx, dy)

    def translate_selected_down(self):
        translation_distance = float(self.translation_entry.get() or 10)
        angle_rad = np.radians(self.window.world_rotation_angle)
        dx = translation_distance * np.sin(angle_rad)
        dy = -translation_distance * np.cos(angle_rad)
        self.translate_selected(dx, dy)

    def scale_selected(self, magnitude):
        for obj in self.selected_objects:
            (xCenter, yCenter) = get_center_of_object(obj.world_coords)
            obj.apply_transformation(scale, magnitude, magnitude, xCenter, yCenter)
        self.repaint()

    # Window and viewport methods
    def zoom(self, percentage: float = 0.1):
        self.window.scale_window(percentage)
        self.repaint()

    def rotate_window_clockwise(self):
        self.window.set_world_rotation(-5)  # Note the negative sign
        self.repaint()

    def rotate_window_counter_clock_wise(self):
        self.window.set_world_rotation(5)
        self.repaint()

    def viewport_transform_2d(self, coords: tuple[float]):
        (xw, yw) = coords
        viewport = self.viewport

        xvp = ((xw + 1) / 2) * (viewport.xMax - viewport.xMin) + viewport.xMin
        yvp = ((1 - yw) / 2) * (viewport.yMax - viewport.yMin) + viewport.yMin
        return (xvp, yvp)

    # Drawing methods
    def repaint(self):
        self.canvas.delete("all")
        self.draw_clip_box()
        self.draw_all_objects()
        self.draw_text()

    def draw_clip_box(self):
        self.canvas.create_rectangle(
            self.clip_xmin,
            self.clip_ymin,
            self.clip_xmax,
            self.clip_ymax,
            outline="red",
            width=3,
        )

    def draw_text(self):
        self.canvas.create_text(
            10,
            10,
            text="Controle com scroll do mouse e setas do teclado",
            font=("tkMenuFont", 7),
            fill="white",
            anchor="nw",
        )

        self.canvas.create_text(
            CANVAS_WIDTH - 50,
            CANVAS_HEIGHT - 20,
            anchor="se",
            font=("tkMenuFont", 7),
            text=f"Xwmin: {round(self.window.xMin, 2)}\n"
                 f"Xwmax: {round(self.window.xMax, 2)}\n"
                 f"Ywmin: {round(self.window.yMin, 2)}\n"
                 f"Ywmax: {round(self.window.yMax, 2)}",
            fill="white",
            )

        self.canvas.create_text(
            CANVAS_WIDTH - 40,
            10,
            anchor="ne",
            fill="white",
            font=("tkMenuFont", 7),
            text=f"Mouse xw: {round(self.mouseXw, 2)}\n"
                 f"Mouse yw: {round(self.mouseYw, 2)}",
            )

    def draw_all_objects(self):
        self.draw_view_up()

        for obj in self.display_file:
            self.draw_object(obj)

    def draw_view_up(self):
        [x, y] = self.window.view_up_vector

        (xvp1, yvp1) = self.viewport_transform_2d((x, y))
        (xvp2, yvp2) = self.viewport_transform_2d((0, 0))

        self.canvas.create_line(
            (xvp1, yvp1, xvp2, yvp2),
            width=2,
            fill="pink",
        )

    def draw_object(self, obj: ScreenObject):
        obj.normalize_coords(self.window)
        if obj.type == "point":
            [(x, y)] = obj.normalized_coords
            clipped_point = cohen_sutherland_clip(x, y, x, y)
            if clipped_point:
                width = 0.01
                if obj in self.selected_objects:
                    width = 0.02
                (xvp1, yvp1) = self.viewport_transform_2d((x - width, y - width))
                (xvp2, yvp2) = self.viewport_transform_2d((x + width, y + width))
                self.canvas.create_oval(xvp1, yvp1, xvp2, yvp2, fill=obj.color)
        else:
            for index, _el in enumerate(obj.normalized_coords):
                if index == 0:
                    continue
                start = obj.normalized_coords[index - 1]
                end = obj.normalized_coords[index]
                clipped_line = cohen_sutherland_clip(start[0], start[1], end[0], end[1])
                if clipped_line:
                    width = 2
                    if obj in self.selected_objects:
                        width = 10
                    (x1, y1), (x2, y2) = clipped_line
                    (xvp1, yvp1) = self.viewport_transform_2d((x1, y1))
                    (xvp2, yvp2) = self.viewport_transform_2d((x2, y2))
                    self.canvas.create_line(
                        xvp1, yvp1, xvp2, yvp2,
                        width=width,
                        fill=obj.color,
                    )

    # File operations methods
    def export_obj_file(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".obj", filetypes=[("Wavefront OBJ", "*.obj")]
        )
        if filename:
            try:
                export_as_obj_file(filename, self.display_file)
                messagebox.showinfo(
                    "Exportação bem sucedida", f"Objetos exportados para {filename}"
                )
            except Exception as e:
                messagebox.showerror(
                    "Erro de exportação", f"Erro ao exportar objetos: {str(e)}"
                )

    def import_obj_file(self, filename: str):
        new_objects = import_obj_file(filename)
        self.display_file.extend(new_objects)
        self.objects_var.set(self.get_all_object_names())
        self.repaint()