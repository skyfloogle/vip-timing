from PIL import Image

bg = Image.open("background.png")
hl = Image.open("highlighted.png")
fn = Image.open("final.png")

frames = [bg]
frame = bg.copy()
for tr in range(2):
    for t in range(6):
        for r in range((3,5)[tr]):
            frame.alpha_composite(hl, (t*8, (5,8)[tr] + r), (t*8, (5,8)[tr] + r, t*8+8, (5,8)[tr] + r + 1))
            frames.append(frame.copy())
            frame.alpha_composite(fn, (t*8, (5,8)[tr] + r), (t*8, (5,8)[tr] + r, t*8+8, (5,8)[tr] + r + 1))
        frames.append(frame.copy())
    frames.append(frame.copy())
for i in range(5): frames.append(frame)

bg.save("anim.gif", save_all=True, optimize=True, append_images=frames, disposal=1, duration=300, loop=0)