from PIL import Image
import numpy as np
from collections import deque

img = Image.open("mark-1024.png").convert("RGB")
a = np.asarray(img).astype(int)
H, W = a.shape[:2]
white = (a.sum(axis=2) > 720)  # near-white pixels

# connected components of white (4-connectivity) via BFS on downsampled? do full with scipy-free flood fill using iterative labeling
labels = np.zeros((H, W), dtype=np.int32)
cur = 0
sizes = {}
for y in range(H):
    row = white[y]
    for x in np.nonzero(row & (labels[y] == 0))[0]:
        cur += 1
        q = deque([(y, x)]); labels[y, x] = cur; n = 0
        while q:
            cy, cx = q.popleft(); n += 1
            for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                ny, nx = cy+dy, cx+dx
                if 0 <= ny < H and 0 <= nx < W and white[ny, nx] and labels[ny, nx] == 0:
                    labels[ny, nx] = cur; q.append((ny, nx))
        sizes[cur] = n
ghost_label = max(sizes, key=sizes.get)
print("ghost component size:", sizes[ghost_label])
mask = labels == ghost_label

# dilate mask by ~16px to capture the black outline around the ghost
from PIL import ImageFilter
m = Image.fromarray((mask*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(33))
mask_d = np.asarray(m) > 0
dark = (a.sum(axis=2) < 200)
keep = mask | (mask_d & dark)

out = np.zeros((H, W, 4), dtype=np.uint8)
out[..., :3] = a
out[..., 3] = np.where(keep, 255, 0)
res = Image.fromarray(out, "RGBA")
bbox = res.getbbox()
res = res.crop(bbox)
res.save("ghost.png")
print("ghost.png:", res.size)
