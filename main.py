from fastapi import FastAPI, HTTPException, UploadFile, File, Response
from fastapi.responses import HTMLResponse
import matplotlib.pyplot as plt
import cv2
import numpy as np
from io import BytesIO
from PIL import Image

app = FastAPI()

def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image

def convert_to_cv2(image):
    image = np.array(image)
    return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

def load_image(image_file):
    image = read_imagefile(image_file)
    if image is None:
        raise IOError("Error loading image")
    cv2_image = convert_to_cv2(image)
    return cv2_image

@app.post("/uploadfiles/")
async def create_upload_files(imageA: UploadFile = File(...), imageB: UploadFile = File(...)):
    try:
        contentsA = await imageA.read()
        contentsB = await imageB.read()
        
        imgA = load_image(contentsA)
        imgB = load_image(contentsB)
        
        orb = cv2.ORB_create(nfeatures=1000)
        kpA, desA = orb.detectAndCompute(imgA, None)
        kpB, desB = orb.detectAndCompute(imgB, None)
        
        if desA is None or desB is None:
            raise IOError("No keypoints found")
        
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(desA, desB)
        matches = sorted(matches, key=lambda x: x.distance)
        
        avg_distance = np.mean([m.distance for m in matches]) if matches else 9999
        
        colors = [
            (255, 89, 94),
            (255, 202, 58),
            (138, 201, 38),
            (25, 130, 196),
            (106, 76, 147)
        ]
        
        matched_img = np.zeros(
            (max(imgA.shape[0], imgB.shape[0]), imgA.shape[1] + imgB.shape[1], 3),
            dtype=np.uint8
        )
        
        matched_img[:imgA.shape[0], :imgA.shape[1]] = imgA
        matched_img[:imgB.shape[0], imgA.shape[1]:imgA.shape[1] + imgB.shape[1]] = imgB
        
        for idx, match in enumerate(matches):
            color = colors[idx % len(colors)]
            pt1 = tuple(map(int, kpA[match.queryIdx].pt))
            pt2 = (int(kpB[match.trainIdx].pt[0] + imgA.shape[1]), int(kpB[match.trainIdx].pt[1]))
            cv2.circle(matched_img, pt1, 3, color, 1)
            cv2.circle(matched_img, pt2, 3, color, 1)
            cv2.line(matched_img, pt1, pt2, color, 1)
        
        fig = plt.figure(figsize=(20, 8), facecolor='#1E1E1E')
        fig.patch.set_facecolor('#1E1E1E')
        
        ax = plt.gca()
        ax.imshow(cv2.cvtColor(matched_img, cv2.COLOR_BGR2RGB))
        ax.set_title(
            f'Image Comparison (Average distance: {avg_distance:.2f})',
            color='white',
            fontsize=18,
            pad=15
        )
        ax.axis('off')
        
        plt.tight_layout()
        img_buf = BytesIO()
        plt.savefig(img_buf, format='png', dpi=300)
        img_buf.seek(0)
        plt.close(fig)
        
        return Response(content=img_buf.read(), media_type="image/png")
    
    except IOError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def main():
    content = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #1E1E1E;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background-color: #2D2D2D;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
        }
        h1 {
            text-align: center;
            color: #00FF9D;
            margin-bottom: 25px;
        }
        .input-group {
            margin: 15px 0;
        }
        input[type="file"] {
            background-color: #3D3D3D;
            color: white;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #4D4D4D;
            width: 100%;
        }
        input[type="submit"] {
            background-color: #00FF9D;
            color: #1E1E1E;
            padding: 12px 25px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
            font-weight: bold;
            margin-top: 20px;
        }
        input[type="submit"]:hover {
            background-color: #00CC7A;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Image Comparison</h1>
        <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
            <div class="input-group">
                <input name="imageA" type="file" accept="image/*">
            </div>
            <div class="input-group">
                <input name="imageB" type="file" accept="image/*">
            </div>
            <input type="submit" value="Compare">
        </form>
    </div>
</body>
</html>
    """
    return HTMLResponse(content=content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
