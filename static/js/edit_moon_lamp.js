function edit_moon_img(is_text) {
    // Load the image
    let src = cv.imread('img');
    let background = cv.imread('background');
    
    // Convert to grayscale
    let grayscale = new cv.Mat();
    cv.cvtColor(src, grayscale, cv.COLOR_BGR2GRAY);


    // Threshold
    let thresholded = new cv.Mat();
    cv.threshold(grayscale, thresholded, 0, 255, cv.THRESH_OTSU);

    // Get bounding box
    let bbox = new cv.Rect();
    bbox = cv.boundingRect(thresholded);

    // Extract foreground
    let foreground = new cv.Mat();
    let x = bbox.x, y = bbox.y, w = bbox.width, h = bbox.height;
    foreground = src.roi(new cv.Rect(x, y, w, h));

    img = foreground

    // Define aspect ratio
    const aspect_ratio = 2/1;

    // Create a black image with the desired aspect ratio
    let bigger_frame_ratio = 3.5;
    let y_offset_ratio = 1.6;
    var img_cols = img.cols
    var img_rows = img.rows

    if (is_text) {
    bigger_frame_ratio = 4.45;
    y_offset_ratio = 2;
    }

    var size;
    if(img_rows < img_cols){
        size = img_rows
    }
    else{
        size = img_cols
    }
    
    var black_img = new cv.Mat.zeros(size * bigger_frame_ratio, size * aspect_ratio * bigger_frame_ratio, cv.CV_8UC4);

    // Copy the image into the black image
    const x_offset = Math.floor((black_img.cols - img.cols) / 2);
    const y_offset = Math.floor((black_img.rows - img.rows) / y_offset_ratio);
    const roi = black_img.roi(new cv.Rect(x_offset, y_offset, img.cols, img.rows));
    img.copyTo(roi);
    img = black_img

    // Resize the second image to match the size of the first image
    cv.resize(background, background, new cv.Size(img.cols, img.rows));

    const alpha_s = new cv.Mat();
    const rgba_channels = new cv.MatVector();
    cv.split(img, rgba_channels);
    cv.threshold(rgba_channels.get(3), alpha_s, 254, 255, cv.THRESH_BINARY_INV);

    const alpha_l = new cv.Mat();
    cv.bitwise_not(alpha_s, alpha_l);
    
    let fg = new cv.Mat();
    let bk = new cv.Mat();
    let result = new cv.Mat();

    img.copyTo(result, alpha_l)
    background.copyTo(result, alpha_s)
    /*
    cv.bitwise_or(img, img, fg, alpha_l)
    cv.bitwise_or(background, background, bk, alpha_s)
    cv.bitwise_or(fg, bk, result)
    */
    cv.imshow('output', result);

    // Free memory
    src.delete();
    grayscale.delete();
    thresholded.delete();
    foreground.delete();
    roi.delete();
    alpha_s.delete();
    alpha_l.delete();
    fg.delete();
    bk.delete();
}
