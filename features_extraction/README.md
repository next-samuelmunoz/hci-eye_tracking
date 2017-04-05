# Eye Tracking

## Features Extraction
### Extract features
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
