# Part mapping: which video is Part 1 and which is Part 2

Researched 2026-11-17 (agent: part_mapping). British English.

## Verdict
**video1 = "Elfstedentocht Part 1"; video2 = "Elfstedentocht Part 2". Confidence: high** (upgraded from medium).
Three independent lines agree: official track lengths, content/genre description, and our own audio tags.

## Evidence
1. **Official durations (MusicBrainz, release "Elfstedentocht, Parts 1 & 2", digital 2013-11-11 and 7" vinyl, A/B sides).**
   Part 1 recording = 189000 ms (3:09); Part 2 recording = 304000 ms (5:04). MusicBrainz lengths are whole seconds, from submitted data.
   Source: https://musicbrainz.org/ws/2/recording?query=recording:elfstedentocht%20AND%20artist:%22Public%20Service%20Broadcasting%22&fmt=json
   (recording ids 36e96196-cb08-44cd-9249-6592b30d080a and 0e1bb0da-72aa-4df4-ac98-5549f0db29e8; release group 4021a842-fa1e-4e42-82ea-ceda415ac278). Confidence: high.
   - video1 = 188.7 s vs 189 s: match. video2 = 305.9 s vs 304 s: about 1.9 s longer, plausibly trailing black/fade in the video upload (our notes say video2 fades to black at the end). Not a mismatch in ordering terms: the only alternative pairing (video1 as the 304 s track) is impossible by 115 s.
2. **YouTube oEmbed (PSBHQ channel).** https://youtu.be/vrPBTwwnpdc returns title "PUBLIC SERVICE BROADCASTING - Elfstedentocht Part Two", author PSBHQ. https://www.youtube.com/oembed?url=https://youtu.be/vrPBTwwnpdc&format=json . Confidence: high that this id is Part 2. I did not confirm that our video2.mp4 is that exact upload (no duration given by oEmbed). I could not find the Part 1 YouTube id.
3. **Descriptions.** Written In Music, 4 Nov 2013: Part 1 loud and rock-oriented, Part 2 calmer and more electronic. https://writteninmusic.com/nieuws/public-service-broadcasting-doet-hel-van-63-herleven/ (already in existing research). Record Rewind Play, 25 Dec 2013: Part 1 has a "simple blood-pumping guitar riff"; Part 2 is on YouTube at youtu.be/vrPBTwwnpdc. https://www.recordrewindplay.co.uk/tracks/elfstedentocht-part-1/ (fetched; no running times given). MetaFilter, May 2014, confirms two songs/videos, "part 1 and part 2": https://www.metafilter.com/138829/Een-monsterrit-van-ruim-tweehonderd-kilometer (via search snippet). Confidence: high.
4. **Our files (own observation).** video1: b/w, newspaper headlines, rock/guitar; CLAP song_average genre post-rock 0.84, distorted guitar 0.44 top instrument. video2: opens with title card "De winter van 1963 in Friesland", colour, electronic; CLAP genre synth-pop 0.35 / electronic 0.23, drum machine 0.63. Fits the Part 1 rock / Part 2 electronic description. (clap_tags.json in v1/data/video*/music_views/)

## Not found / caveats
- Discogs, Bandcamp and the deluxe-edition track listing page were not retrieved (search returned nothing useful). MusicBrainz lists the 2013-11-11 digital release and 7" with these two tracks; whether the deluxe *Inform - Educate - Entertain* durations are identical was not checked.
- AllMusic has an "Elfstedentocht" album page dated 19 April 2014 (no tracks shown in search): https://www.allmusic.com/album/elfstedentocht-mw0002703103 . Possibly a later release date for a single/EP; unverified.

## Corrections to existing research
- artist_and_tracks.md line 21 says official lengths could not be found and the mapping is "Medium confidence": now found (MusicBrainz 3:09 / 5:04) and mapping is high confidence.
- artist_and_tracks.md line 5 / cultural_context.md line 7 / context.md: "medium on part order" should become high. Note video2 runs about 1.9 s over the official 5:04 (video2 = 5:06 file).
- The Part 2 YouTube link in artist_and_tracks.md "not checked live" is now checked: title is "Part Two".
