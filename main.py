from cleanvision import Imagelab
from cleanvision.video_sampler.video_exporter import video_exporter_main

# Specify path to folder containing the image files in your dataset
file = "/Users/samet/Desktop/temporal_consistency/data/video1.mp4"
folder = f"{file}_images/"

video_exporter_main(file)
imagelab = Imagelab(data_path=folder)

# Automatically check for a predefined list of issues within your dataset
imagelab.find_issues({"near_duplicates": {}, "exact_duplicates": {}})

# Produce a neat report of the issues found in your dataset
imagelab.report()
