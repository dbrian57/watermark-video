import cv2
import os
import boto3

from dotenv import load_dotenv
load_dotenv()

# load image and start video


def function(args):
    watermark = cv2.imread(args.watermark)
    yourVideo = cv2.VideoCapture(args.video)

    class FileName:
        name = ''

        def __init__(self, name):
            self.name = name

    fileName = FileName(args.video)

    imageWidth = watermark.shape[1]
    imageHeight = watermark.shape[0]
    vidWidth = yourVideo.get(cv2.CAP_PROP_FRAME_WIDTH)
    vidHeight = yourVideo.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = yourVideo.get(cv2.CAP_PROP_FPS)
    frameSize = (int(vidWidth), int(vidHeight))

    print(frameSize)

    scaleWidth = int(vidWidth * 0.2)
    scaleHeight = int((scaleWidth / imageWidth) * imageHeight)

    scaleDown = (scaleWidth, scaleHeight)

    resized = cv2.resize(watermark, scaleDown, interpolation=cv2.INTER_AREA)

    # position of logo on video
    # the top-left corner of your logo goes here
    position = [int(vidWidth - scaleWidth), int(vidHeight - scaleHeight)]
    xPosition = position[0]  # less yPositionping later
    yPosition = position[1]

    # crop of logo
    left = 0
    right = scaleWidth
    top = 0  # y = 0 is the top of the image
    bottom = scaleHeight

    # calculate width and height of logo crop
    width = right - left
    height = bottom - top

    print(width, height)

    # main loop
    alpha = 0.4

    out = cv2.VideoWriter("output/" + fileName.name,
                          cv2.VideoWriter_fourcc(*'mp4v'), fps, frameSize)
    fileToSend

    while True:
        # read image
        ret, background = yourVideo.read()

        # horizontal flip to create mirror image
        background = cv2.flip(background, 1)

        # quick primer on 2d image slicing:
        # images are [y,x]
        # crop = image[0:100, 300:500] will be a 200x100 image (width x height)
        # the logo slice should give you a decent idea of what's going on

        # WARNING: there are no out-of-bounds checks here, make sure that
        # xPosition + width is less than the width of the background
        # yPosition + height is less than the height of the background
        # right is less than the width of the watermark
        # bottom is less than the height of the watermark

        # get crops of background and logo
        background_slice = background[yPosition:yPosition +
                                      height, xPosition:xPosition+width]
        logo_slice = resized[top:bottom, left:right]
        # since we don't change our crop, we could do the logo slice outside the loop
        # but I'll keep it here for clariyPosition

        # add slice of logo onto slice of background
        added_image = cv2.addWeighted(
            background_slice, alpha, logo_slice, 1-alpha, 0)
        background[yPosition:yPosition+height,
                   xPosition:xPosition+width] = added_image

        fileToSend = out.write(background)

        # show image
        # cv2.imshow('a',background)
        k = cv2.waitKey(30)

        # process keypresses
        # if k == ord('q'):
        #     break
        # if k == ord('a'):
        #     alpha +=0.1
        #     if alpha >=1.0:
        #         alpha = 1.0
        # elif k== ord('d'):
        #     alpha -= 0.1
        #     if alpha <=0.0:
        #         alpha = 0.0

    # close
    yourVideo.release()
    # cv2.destroyAllWindows()

    session = boto3.session.Session()
    client = session.client('s3',
                            # Find your endpoint in the control panel, under Settings. Prepend "https://".
                            endpoint_url='https://nyc3.digitaloceanspaces.com',
                            # Use the region in your endpoint.
                            region_name='nyc3',
                            # Access key pair. You can create access key pairs using the control panel or API.
                            aws_access_key_id='C58A976M583E23R1O00N',
                            aws_secret_access_key=os.getenv('SPACES_SECRET'))  # Secret access key defined through an environment variable.

    # Step 3: Call the put_object command and specify the file to upload.
    client.put_object(Bucket='example-space-name/example-folder/',  # The path to the directory you want to upload the object to, starting with your Space name.
                      # Object key, referenced whenever you want to access this file later.
                      Key='hello-world.txt',
                      Body=b'Hello, World!',  # The object's contents.
                      # Defines Access-control List (ACL) permissions, such as private or public.
                      ACL='private',
                      Metadata={  # Defines metadata tags.
                          'x-amz-meta-my-key': 'your-value'
                      }
                      )
