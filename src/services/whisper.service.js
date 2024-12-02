const { spawn } = require('child_process');
const path = require('path');

/**
 * Run Whisper AI transcription on an audio file
 * @param {string} filename - Path to the audio file
 * @param {Object} options - Whisper options
 * @param {string} options.model - Model to use (tiny, base, small, medium, large)
 * @returns {Promise} - Returns a promise that resolves with the transcription result
 */
exports.runWhisper = (filename, options = {}) => {
    return new Promise((resolve, reject) => {
        // Default to medium model if not specified
        const { model = 'medium' } = options;

        // Create output directory if it doesn't exist
        const outputDir = path.join(process.cwd(), 'output');
        const outputFile = path.join(outputDir, path.basename(filename, path.extname(filename)));

       // Log the command being executed
       const command = `whisper ${filename} --model ${model} --output_dir ${outputDir} --output_format srt`;
       console.log('Executing command:', command);

       // Spawn Whisper process with output options
       const whisperProcess = spawn('whisper', [
           filename,
           '--model', model,
           '--output_dir', outputDir,
           '--output_format', 'srt'
       ]);

        let outputData = '';
        let errorData = '';

        // Collect output data
        whisperProcess.stdout.on('data', (data) => {
            outputData += data;
            console.log(`Whisper progress: ${data}`);
        });

        // Collect error data
        whisperProcess.stderr.on('data', (data) => {
            errorData += data;
            console.error(`Whisper error: ${data}`);
        });

        // Handle process completion
        whisperProcess.on('close', (code) => {
            if (code !== 0) {
                reject(new Error(`Whisper process failed with code ${code}: ${errorData}`));
                return;
            }

            resolve({
                success: true,
                output: outputData,
                inputFile: filename,
                outputFiles: {
                    srt: `${outputFile}.srt`,
                    txt: `${outputFile}.txt`
                }
            });
        });

        // Handle process errors
        whisperProcess.on('error', (error) => {
            reject(new Error(`Failed to start Whisper process: ${error.message}`));
        });
    });
};