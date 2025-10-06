from pathlib import Path
import cv2
import numpy as np

def add_black_dot_noise_cv2(src, dst, n_dots=5, radius=(10,20), seed=None, jpeg_quality=95):
    rng = np.random.default_rng(seed)
    img = cv2.imread(src)                  # BGR
    h, w = img.shape[:2]
    rmin, rmax = radius
    for _ in range(n_dots):
        x = int(rng.integers(0, w))
        y = int(rng.integers(0, h))
        r = int(rng.integers(rmin, rmax + 1))
        cv2.circle(img, (x, y), r, (0, 0, 0), -1)  # 검정색 점
    cv2.imwrite(dst, img, [cv2.IMWRITE_JPEG_QUALITY, jpeg_quality])

# 사용 예
# add_black_dot_noise_cv2("in.jpg", "out.jpg", n_dots=800, radius=(1,4), seed=42)


if __name__ == '__main__':
    input_dir = Path('frames') / 'frame_0.jpg'
    output_dir = Path('noisy_imgs') / 'noisy_image.jpg'

    add_black_dot_noise_cv2(input_dir, output_dir)
    # for p in input_dir.rglob("*"):
    #     if p.is_file() and p.suffix.lower() in (".jpg", ".jpeg"):
    #         rel = p.relative_to(input_dir)
    #         out = (output_dir / rel).with_suffix(".jpg")
    #         output_dir.mkdir(exist_ok=True)
    #         with Image.open(p) as img:
    #             img = noisy('gauss', img)     
    #             print(type(img))   # 필요시
    #             im = im.resize((256, 256))         # 필요시
    #             img.save(out, format="JPEG", quality=95, optimize=True)

    