# Gallery

## Image processing

Use ImageMagick to compress JPEG, resizing longest side to 2000 pixels (maintains aspect ratio):

    convert Shrouded.jpg -sampling-factor 4:2:0 -strip -quality 85 -interlace JPEG -resize '2000x2000' image_converted.jpg

Or do the same thing but modify files in place:

    cd images/to/convert
    mogrify -sampling-factor 4:2:0 -strip -quality 85 -interlace JPEG -resize '2000x2000' *.jpg

This does a decent job of compressing PNGs (only tested on a stylized graphic):

    pngquant -o out.png teton_splash_resized.png  --force --quality=0-20
