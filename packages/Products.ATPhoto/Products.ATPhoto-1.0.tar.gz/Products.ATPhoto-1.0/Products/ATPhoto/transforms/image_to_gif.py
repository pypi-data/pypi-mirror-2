from Products.ATPhoto.transforms.PILTransforms import PILTransforms

class image_to_gif(PILTransforms):
    __name__  = "image_to_gif"
    inputs    = ('image/*', )
    output   = 'image/gif'
    format  = 'gif'


def register():
    return image_to_gif()
