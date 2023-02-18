# kohelper

### Run pip install -r requirements.txt in Command Prompt

### Install tesseract using the Windows installer available at: https://github.com/UB-Mannheim/tesseract/wiki

## python_dir\Lib\site-packages\python_imagesearch\imagesearch.py add func

```
def imagesearch_count_ex(image, precision=0.9):
        img_rgb = pyautogui.screenshot()
        if is_retina:
            img_rgb.thumbnail((round(img_rgb.size[0] * 0.5), round(img_rgb.size[1] * 0.5)))
        img_rgb = np.array(img_rgb)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(image, 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= precision)
        count = []
        for pt in zip(*loc[::-1]):  # Swap columns and rows
            # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2) // Uncomment to draw boxes around found occurrences
            count .append((pt[0], pt[1]))
        # cv2.imwrite('result.png', img_rgb) // Uncomment to write output image with boxes drawn around occurrences
        return count
```
