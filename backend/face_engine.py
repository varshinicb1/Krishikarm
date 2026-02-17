"""
Kisan-Eye V6 — Face Recognition Engine
InsightFace-based face detection, embedding, and matching.
Uses buffalo_l model for SOTA accuracy on Indian faces.
"""

import numpy as np
import cv2
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Lazy load InsightFace (heavy import)
_app = None


def _get_app():
    global _app
    if _app is None:
        try:
            from insightface.app import FaceAnalysis
            _app = FaceAnalysis(
                name='buffalo_l',
                root=str(Path(__file__).parent / "models"),
                providers=['CUDAExecutionProvider', 'CPUExecutionProvider']
            )
            _app.prepare(ctx_id=0, det_size=(640, 640))
            logger.info("✅ InsightFace loaded with GPU")
        except Exception as e:
            logger.warning(f"InsightFace GPU failed, trying CPU: {e}")
            try:
                from insightface.app import FaceAnalysis
                _app = FaceAnalysis(
                    name='buffalo_l',
                    root=str(Path(__file__).parent / "models"),
                    providers=['CPUExecutionProvider']
                )
                _app.prepare(ctx_id=-1, det_size=(640, 640))
                logger.info("✅ InsightFace loaded with CPU")
            except Exception as e2:
                logger.error(f"❌ InsightFace failed completely: {e2}")
                _app = "FAILED"
    return _app if _app != "FAILED" else None


def detect_faces(image_bytes):
    """Detect faces in image bytes. Returns list of face dicts with bbox + embedding."""
    app = _get_app()
    if app is None:
        return []

    # Decode image
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        return []

    faces = app.get(img)
    results = []
    for face in faces:
        results.append({
            'bbox': face.bbox.tolist(),
            'embedding': face.embedding,  # 512-dim float32
            'det_score': float(face.det_score),
            'age': int(face.age) if hasattr(face, 'age') else None,
            'gender': 'M' if (hasattr(face, 'gender') and face.gender == 1) else 'F',
        })
    return results


def compute_similarity(embed1, embed2):
    """Cosine similarity between two face embeddings."""
    if embed1 is None or embed2 is None:
        return 0.0
    e1 = embed1 / np.linalg.norm(embed1)
    e2 = embed2 / np.linalg.norm(embed2)
    return float(np.dot(e1, e2))


def identify_farmer(face_embedding, farmer_embeddings, threshold=0.45):
    """
    Match a face embedding against all stored farmer embeddings.
    Returns (farmer_id, similarity, name) or (None, 0, None) if no match.
    """
    best_match = None
    best_score = 0.0
    best_name = None

    for farmer in farmer_embeddings:
        if farmer['embedding'] is None:
            continue
        score = compute_similarity(face_embedding, farmer['embedding'])
        if score > best_score:
            best_score = score
            best_match = farmer['id']
            best_name = farmer['name']

    if best_score >= threshold:
        return best_match, best_score, best_name
    return None, best_score, None


def extract_face_crop(image_bytes, bbox, padding=30):
    """Extract and return a cropped face image for display."""
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        return None

    h, w = img.shape[:2]
    x1 = max(0, int(bbox[0]) - padding)
    y1 = max(0, int(bbox[1]) - padding)
    x2 = min(w, int(bbox[2]) + padding)
    y2 = min(h, int(bbox[3]) + padding)

    crop = img[y1:y2, x1:x2]
    _, buffer = cv2.imencode('.jpg', crop, [cv2.IMWRITE_JPEG_QUALITY, 90])
    return buffer.tobytes()


def is_available():
    """Check if InsightFace is available."""
    return _get_app() is not None
