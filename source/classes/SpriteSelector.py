from tkinter import filedialog, messagebox, Button, Canvas, Label, LabelFrame, Frame, PhotoImage, Scrollbar, Toplevel, ALL, LEFT, BOTTOM, X, RIGHT, TOP, EW, NS
from glob import glob
import json
import os
import random
import shutil
import ssl
from urllib.parse import urlparse
from urllib.request import urlopen
import webbrowser
from GuiUtils import ToolTips, set_icon, BackgroundTaskProgress
from Rom import Sprite
from Utils import is_bundled, local_path, output_path, open_file


class SpriteSelector(object):
    def __init__(self, parent, callback, adjuster=False):
        if is_bundled():
            self.deploy_icons()
        self.parent = parent
        self.window = Toplevel(parent)
        self.window.geometry("800x650")
        self.sections = []
        self.callback = callback
        self.adjuster = adjuster

        self.window.wm_title("TAKE ANY ONE YOU WANT")
        self.window['padx'] = 5
        self.window['pady'] = 5
        self.all_sprites = []

        def open_official_sprite_listing(_evt):
            webbrowser.open("http://alttpr.com/sprite_preview")

        def open_official_sprite_dir(_evt):
            if not os.path.isdir(self.official_sprite_dir):
                os.makedirs(self.official_sprite_dir)
            open_file(self.official_sprite_dir)

        def open_unofficial_sprite_dir(_evt):
            if not os.path.isdir(self.unofficial_sprite_dir):
                os.makedirs(self.unofficial_sprite_dir)
            open_file(self.unofficial_sprite_dir)

        # Open SpriteSomething directory for Link sprites
        def open_spritesomething_listing(_evt):
            webbrowser.open("https://miketrethewey.github.io/SpriteSomething-collections/snes/zelda3/link/")

        official_frametitle = Frame(self.window)
        official_title_text = Label(official_frametitle, text="Official Sprites")
        official_title_text.pack(side=LEFT)
        official_local_title_link = Label(official_frametitle, text="(open local)", fg="blue", cursor="hand2")
        official_local_title_link.pack(side=LEFT)
        official_local_title_link.bind("<Button-1>", open_official_sprite_dir)
        official_title_link = Label(official_frametitle, text="(ALttPR)", fg="blue", cursor="hand2")
        official_title_link.pack(side=LEFT)
        official_title_link.bind("<Button-1>", open_official_sprite_listing)

        unofficial_frametitle = Frame(self.window)
        unofficial_title_text = Label(unofficial_frametitle, text="Unofficial Sprites")
        unofficial_title_link = Label(unofficial_frametitle, text="(open local)", fg="blue", cursor="hand2")
        unofficial_title_text.pack(side=LEFT)
        unofficial_title_link.pack(side=LEFT)
        unofficial_title_link.bind("<Button-1>", open_unofficial_sprite_dir)
        # Include hyperlink to SpriteSomething directory for Link sprites
        spritesomething_title_link = Label(unofficial_frametitle, text="(SpriteSomething)", fg="blue", cursor="hand2")
        spritesomething_title_link.pack(side=LEFT)
        spritesomething_title_link.bind("<Button-1>", open_spritesomething_listing)

        self.icon_section(official_frametitle, os.path.join(self.official_sprite_dir,"*"), 'Official sprites not found. Click "Update official sprites" to download them.')
        self.icon_section(unofficial_frametitle, os.path.join(self.unofficial_sprite_dir,"*"), 'Put sprites in the unofficial sprites folder (see open link above) to have them appear here.')

        frame = Frame(self.window)
        frame.pack(side=BOTTOM, fill=X, pady=5)

        button = Button(frame, text="Browse for file...", command=self.browse_for_sprite)
        button.pack(side=RIGHT, padx=(5, 0))

        button = Button(frame, text="Update official sprites", command=self.update_official_sprites)
        button.pack(side=RIGHT, padx=(5, 0))

        button = Button(frame, text="Default Link sprite", command=self.use_default_link_sprite)
        button.pack(side=LEFT, padx=(0, 5))

        button = Button(frame, text="Random sprite", command=self.use_random_sprite)
        button.pack(side=LEFT, padx=(0, 5))

        if adjuster:
            button = Button(frame, text="Current sprite from rom", command=self.use_default_sprite)
            button.pack(side=LEFT, padx=(0, 5))

        set_icon(self.window)
        self.window.focus()

    def icon_section(self, frame_label, path, no_results_label):
        frame = LabelFrame(self.window, labelwidget=frame_label, padx=5, pady=5)
        canvas = Canvas(frame, borderwidth=0)
        y_scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
        y_scrollbar.pack(side="right", fill="y")
        content_frame = Frame(canvas)
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((4, 4), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=y_scrollbar.set)

        def onFrameConfigure(canvas):
            """Reset the scroll region to encompass the inner frame"""
            canvas.configure(scrollregion=canvas.bbox("all"))

        content_frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
        frame.pack(side=TOP, fill=X)

        sprites = []

        for file in glob(path):
            sprites.append(Sprite(file))

        sprites.sort(key=lambda s: str.lower(s.name or "").strip())

        i = 0
        for sprite in sprites:
            image = get_image_for_sprite(sprite)
            if image is None:
                continue
            self.all_sprites.append(sprite)
            button = Button(content_frame, image=image, command=lambda spr=sprite: self.select_sprite(spr))
            ToolTips.register(button, sprite.name + ("\nBy: %s" % sprite.author_name if sprite.author_name else ""))
            button.image = image
            button.grid(row=i // 16, column=i % 16)
            i += 1

        if i == 0:
            label = Label(content_frame, text=no_results_label)
            label.pack()

    def update_official_sprites(self):
        # need to wrap in try catch. We don't want errors getting the json or downloading the files to break us.
        self.window.destroy()
        self.parent.update()
        def work(task):
            resultmessage = ""
            successful = True

            def finished():
                task.close_window()
                if successful:
                    messagebox.showinfo("Sprite Updater", resultmessage)
                else:
                    messagebox.showerror("Sprite Updater", resultmessage)
                SpriteSelector(self.parent, self.callback, self.adjuster)

            try:
                task.update_status("Downloading official sprites list")
                with urlopen('https://alttpr.com/sprites', context=ssl._create_unverified_context()) as response:
                    sprites_arr = json.loads(response.read().decode("utf-8"))
            except Exception as e:
                resultmessage = "Error getting list of official sprites. Sprites not updated.\n\n%s: %s" % (type(e).__name__, e)
                successful = False
                task.queue_event(finished)
                return

            try:
                task.update_status("Determining needed sprites")
                current_sprites = [os.path.basename(file) for file in glob(os.path.join(self.official_sprite_dir,"*"))]
                official_sprites = [(sprite['file'], os.path.basename(urlparse(sprite['file']).path)) for sprite in sprites_arr]
                needed_sprites = [(sprite_url, filename) for (sprite_url, filename) in official_sprites
                                  if filename not in current_sprites and filename != "001.link.1.zspr"]
                bundled_sprites = [os.path.basename(file) for file in glob(os.path.join(self.unofficial_sprite_dir,"*"))]
                # todo: eventually use the above list to avoid downloading any sprites that we already have cached in the bundle.

                official_filenames = [filename for (_, filename) in official_sprites]
                obsolete_sprites = [sprite for sprite in current_sprites if sprite not in official_filenames]
            except Exception as e:
                resultmessage = "Error Determining which sprites to update. Sprites not updated.\n\n%s: %s" % (type(e).__name__, e)
                successful = False
                task.queue_event(finished)
                return

            updated = 0
            for (sprite_url, filename) in needed_sprites:
                try:
                    task.update_status("Downloading needed sprite %g/%g" % (updated + 1, len(needed_sprites)))
                    target = os.path.join(self.official_sprite_dir, filename)
                    with urlopen(sprite_url) as response, open(target, 'wb') as out:
                        shutil.copyfileobj(response, out)
                except Exception as e:
                    resultmessage = "Error downloading sprite. Not all sprites updated.\n\n%s: %s" % (type(e).__name__, e)
                    successful = False
                updated += 1

            deleted = 0
            for sprite in obsolete_sprites:
                try:
                    task.update_status("Removing obsolete sprite %g/%g" % (deleted + 1, len(obsolete_sprites)))
                    os.remove(os.path.join(self.official_sprite_dir, sprite))
                except Exception as e:
                    resultmessage = "Error removing obsolete sprite. Not all sprites updated.\n\n%s: %s" % (type(e).__name__, e)
                    successful = False
                deleted += 1

            if successful:
                resultmessage = "official sprites updated successfully"

            task.queue_event(finished)

        BackgroundTaskProgress(self.parent, work, "Updating Sprites")

    def browse_for_sprite(self):
        sprite = filedialog.askopenfilename(
            filetypes=[("All Sprite Sources", (".zspr", ".spr", ".sfc", ".smc")),
                       ("ZSprite files", ".zspr"),
                       ("Sprite files", ".spr"),
                       ("Rom Files", (".sfc", ".smc")),
                       ("All Files", "*")])
        try:
            self.callback(Sprite(sprite))
        except Exception:
            self.callback(None)
        self.window.destroy()

    def use_default_sprite(self):
        self.callback(None, False)
        self.window.destroy()

    def use_default_link_sprite(self):
        self.callback(Sprite.default_link_sprite(), False)
        self.window.destroy()

    def use_random_sprite(self):
        self.callback(random.choice(self.all_sprites) if self.all_sprites else None, True)
        self.window.destroy()

    def select_sprite(self, spritename):
        self.callback(spritename, False)
        self.window.destroy()

    def deploy_icons(self):
        if not os.path.exists(self.unofficial_sprite_dir):
            os.makedirs(self.unofficial_sprite_dir)
        if not os.path.exists(self.official_sprite_dir):
            shutil.copytree(self.local_official_sprite_dir, self.official_sprite_dir)

    @property
    def official_sprite_dir(self):
        return self.local_official_sprite_dir

    @property
    def local_official_sprite_dir(self):
        return local_path(os.path.join("data","sprites","official"))

    @property
    def unofficial_sprite_dir(self):
        return self.local_unofficial_sprite_dir

    @property
    def local_unofficial_sprite_dir(self):
        return local_path(os.path.join("data","sprites","unofficial"))


def get_image_for_sprite(sprite):
    if not sprite.valid:
        return None
    height = 24
    width = 16

    def draw_sprite_into_gif(add_palette_color, set_pixel_color_index):

        def drawsprite(spr, pal_as_colors, offset):
            for y, row in enumerate(spr):
                for x, pal_index in enumerate(row):
                    if pal_index:
                        color = pal_as_colors[pal_index - 1]
                        set_pixel_color_index(x + offset[0], y + offset[1], color)

        add_palette_color(16, (40, 40, 40))
        shadow = [
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        ]

        drawsprite(shadow, [16], (2, 17))

        palettes = sprite.decode_palette()
        for i in range(15):
            add_palette_color(i + 1, palettes[0][i])

        body = sprite.decode16(0x4C0)
        drawsprite(body, list(range(1, 16)), (0, 8))
        head = sprite.decode16(0x40)
        drawsprite(head, list(range(1, 16)), (0, 0))

    def make_gif(callback):
        gif_header = b'GIF89a'

        gif_lsd = bytearray(7)
        gif_lsd[0] = width
        gif_lsd[2] = height
        gif_lsd[4] = 0xF4  # 32 color palette follows.  transparant + 15 for sprite + 1 for shadow=17 which rounds up to 32 as nearest power of 2
        gif_lsd[5] = 0  # background color is zero
        gif_lsd[6] = 0  # aspect raio not specified
        gif_gct = bytearray(3 * 32)

        gif_gce = bytearray(8)
        gif_gce[0] = 0x21  # start of extention blocked
        gif_gce[1] = 0xF9  # identifies this as the Graphics Control extension
        gif_gce[2] = 4  # we are suppling only the 4 four bytes
        gif_gce[3] = 0x01  # this gif includes transparency
        gif_gce[4] = gif_gce[5] = 0  # animation frrame delay (unused)
        gif_gce[6] = 0  # transparent color is index 0
        gif_gce[7] = 0  # end of gif_gce
        gif_id = bytearray(10)
        gif_id[0] = 0x2c
        # byte 1,2 are image left. 3,4 are image top both are left as zerosuitsamus
        gif_id[5] = width
        gif_id[7] = height
        gif_id[9] = 0  # no local color table

        gif_img_minimum_code_size = bytes([7])  # we choose 7 bits, so that each pixel is represented by a byte, for conviennce.

        clear = 0x80
        stop = 0x81

        unchunked_image_data = bytearray(height * (width + 1) + 1)
        # we technically need a Clear code once every 125 bytes, but we do it at the start of every row for simplicity
        for row in range(height):
            unchunked_image_data[row * (width + 1)] = clear
        unchunked_image_data[-1] = stop

        def add_palette_color(index, color):
            gif_gct[3 * index] = color[0]
            gif_gct[3 * index + 1] = color[1]
            gif_gct[3 * index + 2] = color[2]

        def set_pixel_color_index(x, y, color):
            unchunked_image_data[y * (width + 1) + x + 1] = color

        callback(add_palette_color, set_pixel_color_index)

        def chunk_image(img):
            for i in range(0, len(img), 255):
                chunk = img[i:i + 255]
                yield bytes([len(chunk)])
                yield chunk

        gif_img = b''.join([gif_img_minimum_code_size] + list(chunk_image(unchunked_image_data)) + [b'\x00'])

        gif = b''.join([gif_header, gif_lsd, gif_gct, gif_gce, gif_id, gif_img, b'\x3b'])

        return gif

    gif_data = make_gif(draw_sprite_into_gif)
    image = PhotoImage(data=gif_data)

    return image.zoom(2)
