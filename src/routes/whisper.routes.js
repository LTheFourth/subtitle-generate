const express = require('express');
const multer = require('multer');
const path = require('path');
const whisperController = require('../controllers/whisper.controller');

// Configure multer for audio file uploads
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/');
    },
    filename: (req, file, cb) => {
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));
    }
});

const fileFilter = (req, file, cb) => {
    // Accept audio files
    if (file.mimetype.startsWith('audio/') || 
        file.originalname.match(/\.(wav|mp3|ogg|m4a|flac)$/)) {
        cb(null, true);
    } else {
        cb(new Error('Only audio files are allowed!'), false);
    }
};

const upload = multer({ 
    storage: storage,
    fileFilter: fileFilter,
    limits: {
        fileSize: 50 * 1024 * 1024 // 50MB limit
    }
});

const router = express.Router();

// Routes
router.post('/transcribe', 
    upload.single('audio'), 
    whisperController.transcribeAudio
);

router.get('/status/:id',
    whisperController.getTranscriptionStatus
);

module.exports = router;
