# Gallery

## Image processing

Use ImageMagick to compress JPEG, resizing longest side to 2000 pixels (maintains aspect ratio):

    convert Shrouded.jpg -sampling-factor 4:2:0 -strip -quality 85 -interlace JPEG -resize '2000x2000' image_converted.jpg

Or do the same thing but modify files in place:

    cd images/to/convert
    mogrify -sampling-factor 4:2:0 -strip -quality 85 -interlace JPEG -resize '2000x2000' *.jpg

This does a decent job of compressing PNGs (only tested on a stylized graphic):

    pngquant -o out.png teton_splash_resized.png  --force --quality=0-20

## CSS

### Why `height` needs to be set on parents for `max-height` to do the sensible thing in child elements

Basically, `max-height` as a percentage is a percentage of the parent's _actual_ height (not max-height).
If the parent has set only `max-height` and not `height`, `max-height` of the child becomes `none`,
which allows it to be as tall as possible.

https://stackoverflow.com/a/14263416
