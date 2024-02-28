import requests
import json
import urllib.request
from PIL import Image

# Step 1: Download the image
def get_png(inputt):
    postt = ('https://e1kf0882p7.execute-api.us-east-1.amazonaws.com/default/latex2image')
    #get = 
    payload = {"latexInput":inputt,
            "outputFormat":"PNG",
            "outputScale":"150%"}
    #r = requests.post(postt,payload)
    r = requests.post(postt,json=payload)

    idk = r.text
    res = json.loads(idk)
    url = res["imageUrl"]
    print(url)
    urllib.request.urlretrieve(url, "downloaded_image.png")

    # Step 2: Remove transparency and save as JPG
    png_image = Image.open("downloaded_image.png").convert("RGBA")
    background = Image.new("RGBA", png_image.size, (255, 255, 255))
    result_image = Image.alpha_composite(background, png_image)
    result_image.save("result_image.jpg", "PNG", quality=80)

    print("Image saved as result_image.jpg")
    return True

test = r'''
So,
 let's break it down:

1. **What Is Ampere’s Law?**
   Ampere’s law is all about
 the connection between **magnetic fields** and **electric currents**. Imagine a dance between these two – they're like partners
 in crime! The law says that the magnetic field created by an electric current is **proportional** to the size of
 that electric current. And guess what? There's a fancy constant of proportionality called the **permeability of free space
** that comes into play. Basically, it's like saying, "Hey, magnetic field, you're chill, but you
 gotta groove with the current!" 🕺💡

   The official equation for Ampere’s law (which is also one of **
Maxwell’s equations**) goes like this:
   $$\oint_C \mathbf{B} \cdot d\math
started
bf{l} = \mu_0 I$$
   - Here, $$\oint_C$$ represents a **line integral
** around a closed loop (like a hula hoop of magnetic vibes).
   - $$\mathbf{B}$$
 is the magnetic field vector.
   - $$d\mathbf{l}$$ is a tiny chunk of the loop's path
 (think of it as a little magnetic breadcrumb).
   - $$\mu_0$$ is the permeability of free space
 (a cosmic constant that keeps things in check).
   - And $$I$$? That's the electric current doing its thing
! ⚡

2. **Ampere’s Circuital Law in Simple Terms**
   Imagine you've got a **
conductor** (like a wire) carrying a current $$I$$. Well, that current creates a magnetic field that wraps
 around the wire like a cozy scarf. 🧣 Now, if you draw an imaginary path around the wire (kinda like tracing
 the wire's outline), the total magnetic field along that path is equal to the **current enclosed** by that route. Yep
, it's like saying, "Hey, magnetic field, you're the sum of all currents in this loop!" 🌀


   So, in a nutshell:
   - **Line integral of magnetic field** around a closed loop = $$I_{\
ok. m gonna execute something.
text{enclosed}}$$

3. **Why André-Marie Ampère Is the Cool Cat Behind This Law**
'''

get_png(test)