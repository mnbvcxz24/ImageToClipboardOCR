import re
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageGrab, ImageTk
import numpy as np
from rapidocr_onnxruntime import RapidOCR


APP_TITLE = "ImageToClipboardOCR"
NUMBER_PATTERN = re.compile(r"[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?")


class ImageToClipboardOCR:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("360x190")
        self.root.resizable(False, False)
        self.root.configure(bg="#172033")
        self.ocr = None

        tk.Label(
            root, text="ImageToClipboardOCR", font=("Segoe UI", 16, "bold"),
            fg="#f2f6ff", bg="#172033"
        ).pack(pady=(20, 6))
        tk.Label(
            root, text="Capture a screen area and copy numbers only.",
            font=("Segoe UI", 9), fg="#c1cbe0", bg="#172033"
        ).pack(pady=(0, 16))
        tk.Button(
            root, text="START SELECTION", command=self.start_selection,
            font=("Segoe UI", 10, "bold"), bg="#32c5d2", fg="#101827",
            activebackground="#68dce4", relief="flat", padx=18, pady=9
        ).pack()
        tk.Label(
            root, text="Drag around the number you want. Press Esc to cancel.",
            font=("Segoe UI", 8), fg="#9eabc4", bg="#172033"
        ).pack(pady=12)

    def start_selection(self):
        self.root.withdraw()
        self.root.after(250, self.capture_screen)

    def capture_screen(self):
        try:
            self.screenshot = ImageGrab.grab()
        except Exception as exc:
            self.root.deiconify()
            messagebox.showerror("Screenshot failed", str(exc), parent=self.root)
            return

        self.overlay = tk.Toplevel(self.root)
        self.overlay.overrideredirect(True)
        self.overlay.attributes("-topmost", True)
        width, height = self.screenshot.size
        self.overlay.geometry(f"{width}x{height}+0+0")

        self.canvas = tk.Canvas(
            self.overlay, width=width, height=height,
            cursor="crosshair", highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        self.screen_image = ImageTk.PhotoImage(self.screenshot)
        self.canvas.create_image(0, 0, image=self.screen_image, anchor="nw")
        self.rect = None
        self.start_x = self.start_y = 0

        self.canvas.bind("<ButtonPress-1>", self.begin_crop)
        self.canvas.bind("<B1-Motion>", self.drag_crop)
        self.canvas.bind("<ButtonRelease-1>", self.finish_crop)
        self.overlay.bind("<Escape>", self.cancel_selection)
        self.overlay.focus_force()

    def begin_crop(self, event):
        self.start_x, self.start_y = event.x, event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            event.x, event.y, event.x, event.y,
            outline="#31d5e1", width=3
        )

    def drag_crop(self, event):
        if self.rect:
            self.canvas.coords(
                self.rect, self.start_x, self.start_y, event.x, event.y
            )

    def finish_crop(self, event):
        left, right = sorted((self.start_x, event.x))
        top, bottom = sorted((self.start_y, event.y))
        self.overlay.destroy()
        self.root.deiconify()

        if right - left < 3 or bottom - top < 3:
            return

        cropped = self.screenshot.crop((left, top, right, bottom))
        self.root.after(100, lambda: self.read_numbers(cropped))

    def cancel_selection(self, _event=None):
        if self.overlay and self.overlay.winfo_exists():
            self.overlay.destroy()
        self.root.deiconify()

    def read_numbers(self, cropped):
        try:
            if self.ocr is None:
                self.ocr = RapidOCR()
            result, _ = self.ocr(np.asarray(cropped.convert("RGB")))
            recognized_lines = []
            if result:
                for item in result:
                    if len(item) >= 2 and item[1]:
                        recognized_lines.append(str(item[1]))

            raw_text = " ".join(recognized_lines)
            numbers = NUMBER_PATTERN.findall(raw_text)
            if not numbers:
                messagebox.showinfo(
                    "No numbers found",
                    "I couldn't recognize a number in that selection. Try a tighter, clearer crop.",
                    parent=self.root
                )
                return

            clipboard_text = "\n".join(numbers)
            self.root.clipboard_clear()
            self.root.clipboard_append(clipboard_text)
            self.root.update()
            messagebox.showinfo(
                "Copied to clipboard",
                f"Copied {len(numbers)} number(s):\n\n{clipboard_text}",
                parent=self.root
            )
        except Exception as exc:
            messagebox.showerror(
                "OCR failed",
                f"Couldn't read that selection.\n\n{exc}",
                parent=self.root
            )


def main():
    root = tk.Tk()
    ImageToClipboardOCR(root)
    root.mainloop()


if __name__ == "__main__":
    main()
