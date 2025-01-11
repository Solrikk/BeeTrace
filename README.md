![Logo](https://github.com/Solrikk/BeeTrace/blob/main/assets/photo/photo_2025-01-11_18-26-53.jpg)
 
<div align="center">
  <h3>
    <a href="https://github.com/Solrikk/BeeTrace/blob/main/README.md">✦ English ✦</a> |
    <a href="https://github.com/Solrikk/BeeTrace/blob/main/docs/readme/README_RU.md">Russian</a> |
    <a href="https://github.com/Solrikk/BeeTrace/blob/main/docs/readme/README_GE.md">German</a> |
    <a href="https://github.com/Solrikk/BeeTrace/blob/main/docs/readme//README_JP.md">Japanese</a> |
    <a href="https://github.com/Solrikk/BeeTrace/blob/main/docs/readme/README_KR.md">Korean</a> |
    <a href="https://github.com/Solrikk/BeeTrace/blob/main/docs/readme/README_CN.md">Chinese</a>
  </h3>
</div>

-----------------

# BeeTrace 🔍

BeeTrace is a web-based application that uses computer vision techniques to detect and match features between pairs of images using the ORB (Oriented FAST and Rotated BRIEF) algorithm.

## Features

- **Real-time Image Preview**: Instantly preview uploaded images before processing
- **Feature Detection**: Utilizes OpenCV's ORB algorithm for robust feature detection
- **Visual Matching**: Displays matched features between images with colored connecting lines
- **User-friendly Interface**: Clean, modern UI with responsive design
- **Fast Processing**: Efficient image processing and feature matching

## Technology Stack

- **Backend**:
  - FastAPI (Python web framework)
  - OpenCV (Computer vision library)
  - NumPy (Numerical computing)
  - Uvicorn (ASGI server)

- **Frontend**:
  - HTML5
  - CSS3
  - Vanilla JavaScript
  - Fetch API for asynchronous requests

## How It Works

1. **Image Upload**: Users can upload two images through the intuitive interface
2. **Feature Detection**: The ORB algorithm detects key features in both images
3. **Feature Matching**: The application matches similar features between the images
4. **Visualization**: Matched features are displayed with connecting lines and circles

## Installation and Setup

1. Clone the repository:
```bash
git clone https://github.com/solrikk/beetrace.git
cd beetrace
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

4. Open your browser and navigate to `http://localhost:8000`

## API Endpoints

- `GET /`: Serves the main application interface
- `POST /match-features/`: Processes uploaded images and returns matched features

## Technical Details

### ORB Algorithm
The application uses ORB (Oriented FAST and Rotated BRIEF) algorithm which:
- Is rotation invariant and resistant to noise
- Detects keypoints using FAST
- Computes descriptors using BRIEF
- Performs well for real-time applications

### Feature Matching Process
1. Detect keypoints and compute descriptors for both images
2. Use Brute Force Matcher with Hamming distance
3. Sort matches by distance
4. Visualize top 30 matches with unique colors

## Usage Examples

1. Upload two images that have common elements
2. Wait for the processing to complete
3. View the matched features highlighted in the result image
4. The connecting lines show corresponding features between images

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenCV community for computer vision tools
- FastAPI framework for efficient API development
- Contributors and testers who helped improve the application
