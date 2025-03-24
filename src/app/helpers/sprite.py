""" Sprite utils """

import PIL.Image
from PIL import ImageOps
from arcade import TextureAnimationSprite, TextureKeyframe, TextureAnimation
from arcade.resources import resolve
from arcade.texture import Texture


def load_animated_gif(
        resource_name: str,
        flip_horizontally: bool = False
) -> TextureAnimationSprite:
    """
    Attempt to load an animated GIF as a :class:`TextureAnimationSprite`.

    .. note::

        Many older GIFs will load with incorrect transparency for every
        frame but the first. Until the Pillow library handles the quirks of
        the format better, loading animated GIFs will be pretty buggy. A
        good workaround is loading GIFs in another program and exporting them
        as PNGs, either as sprite sheets or a frame per file.

    Args:
        resource_name: A path to a GIF as either a :py:class:`pathlib.Path`
            or a :py:class:`str` which may include a
            :param flip_horizontally:
            :ref:`resource handle <resource_handles>`.

    """

    file_name = resolve(resource_name)
    image_object = PIL.Image.open(file_name)

    # Pillow doc recommends testing for the is_animated attribute as of 10.0.0
    # https://pillow.readthedocs.io/en/stable/deprecations.html#categories
    if not getattr(image_object, "is_animated", False) or not (
            n_frames := getattr(image_object, "n_frames", 0)
    ):
        raise TypeError(f"The file {resource_name} is not an animated gif.")

    sprite = TextureAnimationSprite()
    keyframes = []
    for frame in range(n_frames):
        image_object.seek(frame)
        frame_duration = image_object.info["duration"]
        image = image_object

        if flip_horizontally:
            image = ImageOps.mirror(image)

        image = image.convert("RGBA")

        texture = Texture(image)
        texture.file_path = file_name
        # sprite.textures.append(texture)
        keyframes.append(TextureKeyframe(texture, frame_duration))

    animation = TextureAnimation(keyframes=keyframes)
    sprite.animation = animation
    return sprite
