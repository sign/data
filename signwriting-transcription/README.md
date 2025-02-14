# SignWriting Transcription

Data includes MediaPipe poses of videos from multiple sources, transcribed using SignWriting.

### Examples

(These examples are taken from the DSGS Vokabeltrainer)

|             |                        00004                        |                        00007                        |                        00015                        |
|:-----------:|:---------------------------------------------------:|:---------------------------------------------------:|:---------------------------------------------------:|
|    Video    | <img src="examples/00004.gif" width="150px"> | <img src="examples/00007.gif" width="150px"> | <img src="examples/00015.gif" width="150px"> |
| SignWriting | <img src="examples/00004.png" width="50px">  | <img src="examples/00007.png" width="50px">  | <img src="examples/00015.png" width="50px">  |


### Sources

- `ChicagoFSWild` - About 50,000 fingerspelled signs. Low quality transcriptions. No specific indicator, except for using only hand symbols.
- `dictio` - about 36,000 videos. pose files starts with "dictio". Every sign has two videos, one from a direct angle, and one from a side angle (unmarked).
- `Sign2MINT` - about 5000 isolated signs from Sign2MINT. pose files starts with "s2m".
- `SignSuisse` - about 4000 isolated signs from SignSuisse. pose files starts with "ss".
- `FLEURS-ASL` - about 200, extremely high quality continuous sign language transcriptions with detailed facial expressions. pose files starts with "fasl".
- `19097be0e2094c4aa6b2fdc208c8231e.pose` comes from [Why SignWriting?](https://www.youtube.com/watch?v=Mtl7dmyHgJU), and demonstrates transcription of continuous sign language.

- [Sign2MINT](https://sign2mint.de/) is a lexicon of German Signed Language (DGS) focusing on natural science subjects.
- [SignSuisse](https://signsuisse.sgb-fss.ch/) is a Swiss Signed Languages Lexicon that covers Swiss-German Sign Language (DSGS), 
  French Sign Language (LSF), and Italian Sign Language (LIS). The lexicon includes approximately 4,500 LSF videos
  with [SignWriting transcriptions in SignBank](https://www.signbank.org/signpuddle2.0/index.php?ui=4&sgn=49).

(can also add around 2300 videos from the Vokabeltrainer)

## Poses

Poses are collected using `collect_poses.py` and are available to download from [Cloudflare Storage](https://sign-lanugage-datasets.sign-mt.cloud/poses/holistic/transcription.zip).

It is recommended to pre-process the poses when using them for training. For example:
```python
from pose_format import Pose
from pose_format.utils.generic import pose_normalization_info, correct_wrists, reduce_holistic

# Load full pose video
with open('example.pose', 'rb') as pose_file:
    pose = Pose.read(pose_file.read())

# Or load based on start and end time (faster)
with open('example.pose', 'rb') as pose_file:
    pose = Pose.read(pose_file.read(), start_time=0, end_time=10)
    
# This imo is IDEAL for experimentation, but shouldn't be used for the final model
## Remove legs, simplify face
pose = reduce_holistic(pose)
## Align hand wrists with body wrists
correct_wrists(pose)

# This should be used always
## Adjust pose based on shoulder positions
pose = pose.normalize(pose_normalization_info(pose.header))
```

## Issues to be aware of:

- `.pose` files are not normalized, and are not centered around the origin.

----

Not sure if relevant anymore:

## Automatic Segmentation

Most annotations come from single sign videos with the annotation spanning the entire video. 
However, in real use cases, we would like to transcribe continuous signing, and training on full single-sign videos might not yield correct results.

We automatically segment the single-sign videos using [sign-language-processing/segmentation](https://github.com/sign-language-processing/segmentation)
to extract the sign boundary. Where successful, we record the new sign segments in data_segmentation.csv and use them for additional training data.


---

## Creation Instructions

Data is got from the database using `get_data.py`.
Then, poses are collected using `collect_poses.py`.
The Zip file needs to be manually uploaded to Google Cloud Storage.