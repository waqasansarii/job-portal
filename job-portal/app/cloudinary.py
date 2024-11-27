import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

# Configuration       
cloudinary.config( 
    cloud_name = "dsjylv6kb", 
    api_key = "671799984497613", 
    api_secret = "", # Click 'View API Keys' above to copy your API secret
    secure=True
)

# Upload an image
class CloudinaryImage:
    @staticmethod
    def upload_image(obj,id):
        # upload_result = cloudinary.uploader.upload("https://res.cloudinary.com/demo/image/upload/getting-started/shoes.jpg",
        #                                    public_id="shoes")        
        upload_result = cloudinary.uploader.upload(obj,public_id=id)
        print(upload_result["secure_url"])

        # Optimize delivery by resizing and applying auto-format and auto-quality
        optimize_url, _ = cloudinary_url("shoes", fetch_format="auto", quality="auto")
        print(optimize_url)
        return {
            'result':upload_result,
            'optimize_url':optimize_url
        }

# Transform the image: auto-crop to square aspect_ratio
# auto_crop_url, _ = cloudinary_url("shoes", width=500, height=500, crop="auto", gravity="auto")
# print(auto_crop_url)