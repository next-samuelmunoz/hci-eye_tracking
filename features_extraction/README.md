# Eye Tracking

## Features Extraction

### Extract features
- We use Microsoft Cognitive Face API. Try [demo](https://www.microsoft.com/cognitive-services/en-us/face-api)
- Free tier allows 20 calls/minute. 30,000 per month. View [pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/face-api/)
- Landmarks include 5 points for each eye. View [details](https://www.microsoft.com/cognitive-services/en-us/face-api/documentation/face-api-how-to-topics/HowtoDetectFacesinImage#step3)

```
python face-detect-ms-cognitive.py
```

### Validate responses
Remove wrong files
```
grep -l -r -v faceR $OUTPUT_PATH > files_to_remove.txt
cat files_to_remove.txt | xargs rm -f
rm files_to_remote.txt
```
Count number of faces
```
grep -or faceR $OUTPUT_PATH | uniq --count | grep -v "1\s"
```
