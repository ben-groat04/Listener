#!/bin/bash
# Download Internet Archive videos and re-encode to 480p mp4 in testvideos/. Usage: fetch_archive.sh "identifier|file name|slug|licence" ...
cd "$(dirname "$0")/../.."; mkdir -p testvideos/.tmp
for spec in "$@"; do
  IFS='|' read -r id file slug lic <<< "$spec"
  [ -f testvideos/$slug.mp4 ] && continue
  curl -sSL -m 600 -o "testvideos/.tmp/$slug.src" "https://archive.org/download/$id/$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$file")" || continue
  ffmpeg -loglevel error -y -i "testvideos/.tmp/$slug.src" -vf "scale=-2:480" -c:v libx264 -crf 28 -preset veryfast -c:a aac -b:a 128k testvideos/$slug.mp4 && rm "testvideos/.tmp/$slug.src"
  echo "- \`$slug.mp4\`: archive.org/details/$id · licence: $lic" >> testvideos/SOURCES.md; echo ok $slug
done
