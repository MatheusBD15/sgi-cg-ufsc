from tkinter import *
from tkinter import filedialog, messagebox
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
)
from Math.helpers import get_center_of_object
from CanvasManager.world import World
from CanvasManager.clipping import should_draw_point
import numpy as np


class CanvasManager:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.movement_speed = 25
        self.canvas.bind("<Button-4>", self.handle_zoom_in)
        self.canvas.bind("<Button-5>", self.handle_zoom_out)
        self.canvas.bind_all("<KeyPress>", self.handle_key_press)
        self.canvas.bind("<Motion>", self.handle_mouse_movement)
        self.canvas.bind_all("<Delete>", self.delete_selected_object)
        self.mouseXw = 0
        self.mouseYw = 0

        ## Representa o canvas em si
        self.viewport = Viewport(
            VIEWPORT_OFFSET,
            VIEWPORT_OFFSET,
            CANVAS_WIDTH - VIEWPORT_OFFSET,
            CANVAS_HEIGHT - VIEWPORT_OFFSET,
        )

        # Representa um recorte do mundo
        self.window = Window(
            VIEWPORT_OFFSET,
            VIEWPORT_OFFSET,
            CANVAS_WIDTH - VIEWPORT_OFFSET,
            CANVAS_HEIGHT - VIEWPORT_OFFSET,
        )
        self.world = World((1, 0), (0, 1))
        self.display_file = STARTING_DISPLAY_FILE
        self.objects_var = StringVar(value=self.get_all_object_names())

        self.selected_object = None
        self.objects_list = None

        self.repaint()

    def set_objects_list(self, listbox):
        self.objects_list = listbox
        self.objects_list.bind("<<ListboxSelect>>", self.on_select)

    def on_select(self, event):
        if self.objects_list.curselection():
            index = self.objects_list.curselection()[0]
            self.selected_object = self.display_file[index]
            self.selected_object.selected = True
            self.repaint()
        else:
            self.clearSelected()

    def clear_selected(self):
        if self.selected_object:
            self.selected_object.selected = False
            self.selected_object = None
            self.repaint()

    def rotate_selected(self, direction):
        if self.selected_object:
            angle = float(self.rotate_entry.get() or 10)
            if direction == "clockwise":
                angle = angle * -1

            rotation_type = self.rotate_type.get() or "world"

            if rotation_type == "world":
                self.selected_object.apply_transformation(rotate_around_world, angle)
            elif rotation_type == "object":
                (xCenter, yCenter) = get_center_of_object(
                    self.selected_object.world_coords
                )

                self.selected_object.apply_transformation(
                    rotate_around_point, xCenter, yCenter, angle
                )
            elif rotation_type == "arbitrary_point":
                [tx, ty] = list(eval(self.rotate_point_entry.get() or "0, 0"))
                self.selected_object.apply_transformation(
                    rotate_around_point, tx, ty, angle
                )
            self.repaint()

    def transform_selected(self, transformation, *args):
        if self.selected_object:
            if transformation == "translate":
                self.selected_object.apply_transformation(translate, *args)
            self.repaint()

    def translate_selected_right(self):
        if self.selected_object:
            window_view_up = self.window.view_up_vector
            right_vector = np.array([window_view_up[1], -window_view_up[0]])

            translation_distance = float(self.translation_entry.get() or 10)
            translation_vector = translation_distance * right_vector

            self.selected_object.apply_transformation(
                translate, translation_vector[0], translation_vector[1]
            )
            self.repaint()

    def translate_selected_left(self):
        if self.selected_object:
            window_view_up = self.window.view_up_vector
            left_vector = np.array([-window_view_up[1], window_view_up[0]])

            translation_distance = float(self.translation_entry.get() or 10)
            translation_vector = translation_distance * left_vector

            self.selected_object.apply_transformation(
                translate, translation_vector[0], translation_vector[1]
            )
            self.repaint()

    def translate_selected_up(self):
        if self.selected_object:
            window_view_up = self.window.view_up_vector

            translation_distance = float(self.translation_entry.get() or 10)
            translation_vector = translation_distance * window_view_up

            self.selected_object.apply_transformation(
                translate, translation_vector[0], translation_vector[1]
            )
            self.repaint()

    def translate_selected_down(self):
        if self.selected_object:
            window_view_up = self.window.view_up_vector

            translation_distance = float(self.translation_entry.get() or 10)
            translation_vector = (
                -translation_distance * window_view_up
            )  # Downward translation

            self.selected_object.apply_transformation(
                translate, translation_vector[0], translation_vector[1]
            )
            self.repaint()

    def handle_mouse_movement(self, event: Event):
        self.mouseXw = event.x
        self.mouseYw = event.y

        self.repaint()

    def handle_zoom_in(self, event: Event):
        self.zoom(-0.1)

    def handle_zoom_out(self, event: Event):
        self.zoom(0.1)

    def handle_key_press(self, event: Event):
        movement_speed = self.movement_speed

        window_center = np.array(self.window.center)
        window_view_up = self.window.view_up_vector

        if event.keysym == "Right":
            right_view_up = np.array([window_view_up[1], -window_view_up[0]])
            self.window.center = (window_center) + (movement_speed * right_view_up)

        if event.keysym == "Left":
            left_view_up = np.array([-window_view_up[1], window_view_up[0]])
            self.window.center = (window_center) + (movement_speed * left_view_up)

        if event.keysym == "Down":
            self.window.center = (window_center) + (-movement_speed * window_view_up)

        if event.keysym == "Up":
            self.window.center = (window_center) + (movement_speed * window_view_up)

        self.repaint()

    def viewport_transform_2d(self, coords: tuple[float]):
        (xw, yw) = coords
        viewport = self.viewport

        xMin = -1
        xMax = 1
        yMin = -1
        yMax = 1
        xvp = ((xw - xMin) / (xMax - xMin)) * (viewport.xMax - viewport.xMin)
        yvp = (1 - ((yw - yMin) / (yMax - yMin))) * (viewport.yMax - viewport.yMin)
        return (xvp, yvp)

    def add_object(self, obj: ScreenObject):
        self.display_file.append(obj)
        self.objects_var.set(self.get_all_object_names())
        self.repaint()

    def repaint(self):
        self.canvas.delete("all")
        self.draw_clip_box()
        self.draw_all_objects()
        self.draw_text()

    def draw_clip_box(self):
        height = CANVAS_HEIGHT - VIEWPORT_OFFSET / 2
        width = CANVAS_WIDTH - VIEWPORT_OFFSET / 2
        offset = VIEWPORT_OFFSET / 2

        self.canvas.create_line(
            offset,
            offset,
            width,
            offset,
            width=3,
            fill="red",
        )
        self.canvas.create_line(
            width,
            offset,
            width,
            height,
            width=3,
            fill="red",
        )
        self.canvas.create_line(
            width,
            height,
            offset,
            height,
            width=3,
            fill="red",
        )
        self.canvas.create_line(
            offset,
            height,
            offset,
            offset,
            width=3,
            fill="red",
        )

    def rotate_window_clockwise(self):
        self.window.set_rotation(5)
        self.repaint()

    def rotate_window_counter_clock_wise(self):
        self.window.set_rotation(-5)
        self.repaint()

    def draw_all_objects(self):
        self.draw_view_up()

        for obj in self.display_file:
            self.draw_object(obj)

    def draw_view_up(self):
        [x, y] = self.window.view_up_vector

        (xvp1, yvp1) = self.viewport_transform_2d((x, y))
        (xvp2, yvp2) = self.viewport_transform_2d((0, 0))

        # criar oval para representar um ponto
        self.canvas.create_line(
            (xvp1, yvp1, xvp2, yvp2),
            width=2,
            fill="pink",
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
            text="Xwmin: "
            + str(round(self.window.xMin, 2))
            + "\n"
            + "Xwmax: "
            + str(round(self.window.xMax, 2))
            + "\n"
            + "Ywmin: "
            + str(round(self.window.yMin, 2))
            + "\n"
            + "Ywmax: "
            + str(round(self.window.yMax, 2)),
            fill="white",
        )

        self.canvas.create_text(
            CANVAS_WIDTH - 40,
            10,
            anchor="ne",
            fill="white",
            font=("tkMenuFont", 7),
            text="Mouse xw: "
            + str(round(self.mouseXw, 2))
            + "\n"
            + "Mouse yw: "
            + str(round(self.mouseYw, 2)),
        )

    def draw_object(self, obj: ScreenObject):
        obj.normalize_coords(self.window)
        if obj.type == "point":
            if should_draw_point(obj):
                width = 0.01
                if self.selected_object and self.selected_object.name == obj.name:
                    width = 0.02

                [(xw, yw)] = obj.normalized_coords
                (xvp1, yvp1) = self.viewport_transform_2d((xw - width, yw - width))
                (xvp2, yvp2) = self.viewport_transform_2d((xw + width, yw + width))

                # criar oval para representar um ponto
                self.canvas.create_oval(xvp1, yvp1, xvp2, yvp2, fill=obj.color)
        else:
            for index, _el in enumerate(obj.normalized_coords):
                if index == 0:
                    pass
                else:
                    (xvp1, yvp1) = self.viewport_transform_2d(
                        obj.normalized_coords[index - 1]
                    )
                    (xvp2, yvp2) = self.viewport_transform_2d(
                        obj.normalized_coords[index]
                    )

                    width = 2
                    if self.selected_object and self.selected_object.name == obj.name:
                        width = 10

                    self.canvas.create_line(
                        (xvp1, yvp1, xvp2, yvp2),
                        width=width,
                        fill=obj.color,
                    )

    def zoom(self, percentage: float = 0.1):
        self.window.scale_window(percentage)
        self.repaint()

    def get_objects_list(self):
        return self.objects_var

    def get_all_object_names(self):
        acc = []
        for obj in self.display_file:
            acc.append(obj.name + " - " + obj.type)
        return acc

    def transform_selected_object(self, transformation, *args):
        selected_index = self.objects_list.curselection()
        if selected_index:
            obj = self.display_file[selected_index[0]]
            getattr(obj, transformation)(*args)
            self.repaint()

    def scale_selected(self, magnitude):
        if self.selected_object:
            (xCenter, yCenter) = get_center_of_object(self.selected_object.world_coords)

            self.selected_object.apply_transformation(
                scale, magnitude, magnitude, xCenter, yCenter
            )
            self.repaint()

    def delete_selected_object(self, event=None):
        if self.selected_object:
            confirm = messagebox.askyesno(
                "Confirmar deleção",
                f"Tem certeza que deseja deletar o objeto '{self.selected_object.name}'?",
            )
            if confirm:
                self.display_file.remove(self.selected_object)
                self.selected_object = None
                self.objects_var.set(self.get_all_object_names())
                self.repaint()
                messagebox.showinfo("Deleção bem sucedida", "Objeto deletado.")
        else:
            messagebox.showinfo("No Selection", "Nenhum objeto está selecionado.")

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
