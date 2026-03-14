# DeepCheck - Project Documentation

## Student Information
- **Name**: Aziz Ali
- **Email**: alyyaziz45@gmail.com
- **Supervisor**: Mr. Hassan
- **Institution**: [Your University Name]
- **Program**: [Your Program]
- **Year**: [Current Year]

## Project Overview
DeepCheck is a deepfake detection system developed as a final year project. It uses advanced machine learning techniques to identify manipulated videos and images.

## System Architecture
1. **Frontend**: React.js with Tailwind CSS
2. **Backend**: FastAPI (Python)
3. **ML Model**: Xception CNN + Bi-directional GRU
4. **Database**: MongoDB Atlas
5. **Deployment**: Local/Cloud ready

## Features Implemented
- ✅ User authentication system
- ✅ Video upload and processing
- ✅ Deepfake detection using AI
- ✅ Confidence scoring
- ✅ User history tracking
- ✅ Responsive web interface

## How It Works
1. User uploads a video
2. System extracts frames (10 frames per video)
3. Xception CNN processes spatial features
4. Bi-GRU analyzes temporal inconsistencies
5. Final classification with confidence score

## Performance
- **Processing Time**: 2-4 seconds per video
- **Accuracy**: ~85% (can be improved with more training)
- **Model Size**: 24M parameters

## Future Improvements
- Train with larger dataset
- Implement real-time detection
- Add support for images
- Improve accuracy with ensemble methods

## References
- FaceForensics++ Dataset
- Celeb-DF Dataset
- Xception: Deep Learning with Depthwise Separable Convolutions

---
**Submitted by**: Aziz Ali
**Supervised by**: Mr. Hassan
**Date**: [Current Date]
