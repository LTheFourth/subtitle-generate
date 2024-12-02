const whisperService = require('../services/whisper.service');

exports.transcribeAudio = async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({
                success: false,
                error: 'No audio file provided'
            });
        }

        const model = req.body.model || 'base';
        const language = req.body.language || null;

        const result = await whisperService.runWhisper(req.file.path, {
            model,
            language
        });

        res.json({
            success: true,
            data: result
        });
    } catch (error) {
        console.error('Transcription error:', error);
        res.status(500).json({
            success: false,
            error: error.message || 'Failed to transcribe audio'
        });
    }
};

exports.getTranscriptionStatus = async (req, res) => {
    try {
        const { id } = req.params;
        const status = await whisperService.getStatus(id);
        
        res.json({
            success: true,
            data: status
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
};
