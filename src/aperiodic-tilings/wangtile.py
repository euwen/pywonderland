"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Draw Wang Tile with Pyglet and GLSL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Code exported from srtuss's shadertoy project at

    "https://www.shadertoy.com/view/Wds3z7"

"""
import sys
sys.path.append("../glslhelpers")

import time
import ctypes
from PIL import Image

import pyglet
pyglet.options["debug_gl"] = False
import pyglet.gl as gl
import pyglet.window.key as key

from shader import Shader
from texture import create_cubemap_texture


CUBEMAP_IMAGES = ["../glslhelpers/textures/st_peters_blurred{}.png".format(i) for i in range(6)]


class WangTile(pyglet.window.Window):

    def __init__(self, width, height, zoom):
        """
        :param width & height: size of the main window in pixels.

        :param zoom: zoom factor of the scene.

        Keyboard control:
            1. press `Enter` to save screenshots.
            2. press `Esc` to exit.
        """
        pyglet.window.Window.__init__(self,
                                      width,
                                      height,
                                      caption="Wang-Tile",
                                      resizable=True,
                                      visible=False,
                                      vsync=False)
        self._start_time = time.clock()
        self.shader = Shader(["./glsl/wang.vert"], ["./glsl/wang.frag"])

        cubemap = create_cubemap_texture(CUBEMAP_IMAGES)
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_CUBE_MAP, cubemap)
        with self.shader:
            self.shader.vertex_attrib("position", [-1, -1, 1, -1, -1, 1, 1, 1])
            self.shader.uniformf("iResolution", width, height, 0.0)
            self.shader.uniformf("iTime", 0.0)
            self.shader.uniformf("zoom", zoom)
            self.shader.uniformi("cubemap", 0)

    def on_draw(self):
        gl.glClearColor(0, 0, 0, 0)
        self.clear()
        gl.glViewport(0, 0, self.width, self.height)
        with self.shader:
            self.shader.uniformf("iTime", time.clock() - self._start_time)
            gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, 4)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ENTER:
            self.save_screenshot()

        if symbol == key.ESCAPE:
            pyglet.app.exit()

    def save_screenshot(self):
        buff = pyglet.image.get_buffer_manager().get_color_buffer()
        buff.save("wangtile.png")

    def run(self, fps=None):
        self.set_visible(True)
        if fps is None:
            pyglet.clock.schedule(lambda dt: None)
        else:
            pyglet.clock.schedule_interval(lambda dt: None, 1.0/fps)
        pyglet.app.run()


if __name__ == "__main__":
    app = WangTile(width=800, height=600, zoom=10.0)
    app.run(fps=60)