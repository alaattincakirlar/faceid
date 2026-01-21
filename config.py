import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'Data')
DB_PATH = os.path.join(DATA_DIR, "faceData.pickle")
JSON_PATH = os.path.join(BASE_DIR, "status.json")

CAMERA_ID = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
SCALE_FACTOR = 0.25

TOLERANCE = 0.5
MODEL = "hog"

COLOR_GREEN = (0, 255, 0)
COLOR_RED = (0, 0, 255)