function resize_image(canvas, maxWidth, maxHeight){
    
        // Calculate the scaling factor to fit within the maximum dimensions
        var scale = Math.min(maxWidth / canvas.width, maxHeight / canvas.height);

        // If the image dimensions are already smaller than the maximum dimensions, don't scale
        if (scale > 1) {
            scale = 1;
        }

          // Calculate the new dimensions of the image
        var newWidth = Math.round(canvas.width * scale);
        var newHeight = Math.round(canvas.height * scale);

        var newCanvas = document.createElement('canvas');
        newCanvas.width = newWidth;
        newCanvas.height = newHeight;

        // Get the 2D context of the new canvas
        var newContext = newCanvas.getContext('2d');

        // Draw the original canvas onto the new canvas with antialiasing
        newContext.drawImage(canvas, 0, 0, newWidth, newHeight);

        return {'newCanvas': newCanvas, 'newContext': newContext}
}