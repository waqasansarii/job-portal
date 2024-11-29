import os
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from dotenv import load_dotenv
load_dotenv()



# Configuration       
cloudinary.config( 
    cloud_name = "dsjylv6kb", 
    api_key = os.getenv('CLOUDINARY_API'), 
    api_secret = os.getenv('CLOUDINARY_SECRET'), 
    secure=True
)

# Upload an image
class CloudinaryImage:
    @staticmethod
    def upload_file(obj,id,resource_type):
        # upload_result = cloudinary.uploader.upload("https://res.cloudinary.com/demo/image/upload/getting-started/shoes.jpg",
        #                                    public_id="shoes")        
        upload_result = cloudinary.uploader.upload(
            obj,
            public_id=id, 
            responsive_breakpoints = { 
                "create_derived": True, 
                "bytes_step": 20000, 
                "min_width": 200, 
                "max_width": 1000 
                },
            resource_type=resource_type
            )
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