# This file is part of beets.
# Copyright 2010, Adrian Sampson.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

"""Facilities for automatically determining files' correct metadata.
"""

import os
from collections import defaultdict
from beets.autotag import mb
import re
from munkres import Munkres
from beets import library, mediafile, plugins
import logging

# Try 5 releases. In the future, this should be more dynamic: let the
# probability of continuing to the next release be inversely
# proportional to how good our current best is and how long we've
# already taken.
MAX_CANDIDATES = 5

# Distance parameters.
# Text distance weights: proportions on the normalized intuitive edit
# distance.
ARTIST_WEIGHT = 3.0
ALBUM_WEIGHT = 3.0
# The weight of the entire distance calculated for a given track.
TRACK_WEIGHT = 1.0
# These distances are components of the track distance (that is, they
# compete against each other but not ARTIST_WEIGHT and ALBUM_WEIGHT;
# the overall TRACK_WEIGHT does that).
TRACK_TITLE_WEIGHT = 3.0
# Added when the indices of tracks don't match.
TRACK_INDEX_WEIGHT = 1.0
# Track length weights: no penalty before GRACE, maximum (WEIGHT)
# penalty at GRACE+MAX discrepancy.
TRACK_LENGTH_GRACE = 10
TRACK_LENGTH_MAX = 30
TRACK_LENGTH_WEIGHT = 2.0
# MusicBrainz track ID matches.
TRACK_ID_WEIGHT = 5.0

# Recommendation constants.
RECOMMEND_STRONG = 'RECOMMEND_STRONG'
RECOMMEND_MEDIUM = 'RECOMMEND_MEDIUM'
RECOMMEND_NONE = 'RECOMMEND_NONE'
# Thresholds for recommendations.
STRONG_REC_THRESH = 0.04
MEDIUM_REC_THRESH = 0.25
REC_GAP_THRESH = 0.25

# Parameters for string distance function.
# Words that can be moved to the end of a string using a comma.
SD_END_WORDS = ['the', 'a', 'an']
# Reduced weights for certain portions of the string.
SD_PATTERNS = [
    (r'^the ', 0.1),
    (r'[\[\(]?(ep|single)[\]\)]?', 0.0),
    (r'[\[\(]?(featuring|feat|ft)[\. :].+', 0.1),
    (r'\(.*?\)', 0.3),
    (r'\[.*?\]', 0.3),
    (r'(, )?(pt\.|part) .+', 0.2),
]

# Autotagging exceptions.
class AutotagError(Exception):
    pass

# Global logger.
log = logging.getLogger('beets')

def _sorted_walk(path):
    """Like os.walk, but yields things in sorted, breadth-first
    order.
    """
    # Make sure the path isn't a Unicode string.
    path = library._bytestring_path(path)

    # Get all the directories and files at this level.
    dirs = []
    files = []
    for base in os.listdir(path):
        cur = os.path.join(path, base)
        if os.path.isdir(library._syspath(cur)):
            dirs.append(base)
        else:
            files.append(base)

    # Sort lists and yield the current level.
    dirs.sort()
    files.sort()
    yield (path, dirs, files)

    # Recurse into directories.
    for base in dirs:
        cur = os.path.join(path, base)
        # yield from _sorted_walk(cur)
        for res in _sorted_walk(cur):
            yield res

def albums_in_dir(path):
    """Recursively searches the given directory and returns an iterable
    of (path, items) where path is a containing directory and items is
    a list of Items that is probably an album. Specifically, any folder
    containing any media files is an album.
    """
    for root, dirs, files in _sorted_walk(path):
        # Get a list of items in the directory.
        items = []
        for filename in files:
            try:
                i = library.Item.from_path(os.path.join(root, filename))
            except mediafile.FileTypeError:
                pass
            except mediafile.UnreadableFileError:
                log.warn('unreadable file: ' + filename)
            else:
                items.append(i)
        
        # If it's nonempty, yield it.
        if items:
            yield root, items

def _levenshtein(s1, s2):
    """A nice DP edit distance implementation from Wikibooks:
    http://en.wikibooks.org/wiki/Algorithm_implementation/Strings/
    Levenshtein_distance#Python
    """
    if len(s1) < len(s2):
        return _levenshtein(s2, s1)
    if not s1:
        return len(s2)
 
    previous_row = xrange(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
 
    return previous_row[-1]

def _string_dist_basic(str1, str2):
    """Basic edit distance between two strings, ignoring
    non-alphanumeric characters and case. Normalized by string length.
    """
    str1 = re.sub(r'[^a-z0-9]', '', str1.lower())
    str2 = re.sub(r'[^a-z0-9]', '', str2.lower())
    if not str1 and not str2:
        return 0.0
    return _levenshtein(str1, str2) / float(max(len(str1), len(str2)))

def string_dist(str1, str2):
    """Gives an "intuitive" edit distance between two strings. This is
    an edit distance, normalized by the string length, with a number of
    tweaks that reflect intuition about text.
    """
    str1 = str1.lower()
    str2 = str2.lower()
    
    # Don't penalize strings that move certain words to the end. For
    # example, "the something" should be considered equal to
    # "something, the".
    for word in SD_END_WORDS:
        if str1.endswith(', %s' % word):
            str1 = '%s %s' % (word, str1[:-len(word)-2])
        if str2.endswith(', %s' % word):
            str2 = '%s %s' % (word, str2[:-len(word)-2])
    
    # Change the weight for certain string portions matched by a set
    # of regular expressions. We gradually change the strings and build
    # up penalties associated with parts of the string that were
    # deleted.
    base_dist = _string_dist_basic(str1, str2)
    penalty = 0.0
    for pat, weight in SD_PATTERNS:
        # Get strings that drop the pattern.
        case_str1 = re.sub(pat, '', str1)
        case_str2 = re.sub(pat, '', str2)
        
        if case_str1 != str1 or case_str2 != str2:
            # If the pattern was present (i.e., it is deleted in the
            # the current case), recalculate the distances for the
            # modified strings.
            case_dist = _string_dist_basic(case_str1, case_str2)
            case_delta = max(0.0, base_dist - case_dist)
            if case_delta == 0.0:
                continue
            
            # Shift our baseline strings down (to avoid rematching the
            # same part of the string) and add a scaled distance
            # amount to the penalties.
            str1 = case_str1
            str2 = case_str2
            base_dist = case_dist
            penalty += weight * case_delta
    dist = base_dist + penalty
    
    return dist

def _plurality(objs):
    """Given a sequence of comparable objects, returns the object that
    is most common in the set.
    """
    # Calculate frequencies.
    freqs = defaultdict(int)
    for obj in objs:
        freqs[obj] += 1

    # Find object with maximum frequency.
    max_freq = 0
    res = None
    for obj, freq in freqs.items():
        if freq > max_freq:
            max_freq = freq
            res = obj

    return res

def current_metadata(items):
    """Returns the most likely artist and album for a set of Items.
    Each is determined by tag reflected by the plurality of the Items.
    """
    keys = 'artist', 'album'
    likelies = {}
    for key in keys:
        values = [getattr(item, key) for item in items]
        likelies[key] = _plurality(values)
    return likelies['artist'], likelies['album']

def order_items(items, trackinfo):
    """Orders the items based on how they match some canonical track
    information. This always produces a result if the numbers of tracks
    match.
    """
    # Make sure lengths match.
    if len(items) != len(trackinfo):
        return None

    # Construct the cost matrix.
    costs = []
    for cur_item in items:
        row = []
        for i, canon_item in enumerate(trackinfo):
            row.append(track_distance(cur_item, canon_item, i+1))
        costs.append(row)
    
    # Find a minimum-cost bipartite matching.
    matching = Munkres().compute(costs)

    # Order items based on the matching.
    ordered_items = [None]*len(items)
    for cur_idx, canon_idx in matching:
        ordered_items[canon_idx] = items[cur_idx]
    return ordered_items

def track_distance(item, track_data, track_index=None):
    """Determines the significance of a track metadata change. Returns
    a float in [0.0,1.0]. `track_index` is the track number of the
    `track_data` metadata set. If `track_index` is provided and
    item.track is set, then these indices are used as a component of
    the distance calculation.
    """
    # Distance and normalization accumulators.
    dist, dist_max = 0.0, 0.0

    # Check track length.
    if 'length' not in track_data:
        # If there's no length to check, assume the worst.
        dist += TRACK_LENGTH_WEIGHT
    else:
        diff = abs(item.length - track_data['length'])
        diff = max(diff - TRACK_LENGTH_GRACE, 0.0)
        diff = min(diff, TRACK_LENGTH_MAX)
        dist += (diff / TRACK_LENGTH_MAX) * TRACK_LENGTH_WEIGHT
    dist_max += TRACK_LENGTH_WEIGHT
    
    # Track title.
    dist += string_dist(item.title, track_data['title']) * TRACK_TITLE_WEIGHT
    dist_max += TRACK_TITLE_WEIGHT

    # Track index.
    if track_index and item.track:
        if track_index != item.track:
            dist += TRACK_INDEX_WEIGHT
        dist_max += TRACK_INDEX_WEIGHT
    
    # MusicBrainz track ID.
    if item.mb_trackid:
        if item.mb_trackid != track_data['id']:
            dist += TRACK_ID_WEIGHT
        dist_max += TRACK_ID_WEIGHT

    # Plugin distances.
    plugin_d, plugin_dm = plugins.track_distance(item, track_data)
    dist += plugin_d
    dist_max += plugin_dm

    return dist / dist_max

def distance(items, info):
    """Determines how "significant" an album metadata change would be.
    Returns a float in [0.0,1.0]. The list of items must be ordered.
    """
    cur_artist, cur_album = current_metadata(items)
    cur_artist = cur_artist or ''
    cur_album = cur_album or ''
    
    # These accumulate the possible distance components. The final
    # distance will be dist/dist_max.
    dist = 0.0
    dist_max = 0.0
    
    # Artist/album metadata.
    dist += string_dist(cur_artist, info['artist']) * ARTIST_WEIGHT
    dist_max += ARTIST_WEIGHT
    dist += string_dist(cur_album,  info['album']) * ALBUM_WEIGHT
    dist_max += ALBUM_WEIGHT
    
    # Track distances.
    for i, (item, track_data) in enumerate(zip(items, info['tracks'])):
        dist += track_distance(item, track_data, i+1) * TRACK_WEIGHT
        dist_max += TRACK_WEIGHT

    # Plugin distances.
    plugin_d, plugin_dm = plugins.album_distance(items, info)
    dist += plugin_d
    dist_max += plugin_dm

    # Normalize distance, avoiding divide-by-zero.
    if dist_max == 0.0:
        return 0.0
    else:
        return dist/dist_max

def apply_metadata(items, info):
    """Set the items' metadata to match the data given in info. The
    list of items must be ordered.
    """
    for index, (item, track_data) in enumerate(zip(items,  info['tracks'])):
        # Album, artist, track count.
        item.artist = info['artist']
        item.album = info['album']
        item.tracktotal = len(items)
        
        # Release date.
        if 'year' in info:
            item.year = info['year']
        if 'month' in info:
            item.month = info['month']
        if 'day' in info:
            item.day = info['day']
        
        # Title and track index.
        item.title = track_data['title']
        item.track = index + 1
        
        # MusicBrainz IDs.
        item.mb_trackid = track_data['id']
        item.mb_albumid = info['album_id']
        item.mb_artistid = info['artist_id']

def match_by_id(items):
    """If the items are tagged with a MusicBrainz album ID, returns an
    info dict for the corresponding album. Otherwise, returns None.
    """
    # Is there a consensus on the MB album ID?
    albumids = [item.mb_albumid for item in items if item.mb_albumid]
    if not albumids:
        return None
    
    # If all album IDs are equal, look up the album.
    if bool(reduce(lambda x,y: x if x==y else (), albumids)):
        albumid = albumids[0]
        return mb.album_for_id(albumid)
    else:
        return None
    
    #fixme In the future, at the expense of performance, we could use
    # other IDs (i.e., track and artist) in case the album tag isn't
    # present, but that event seems very unlikely.

def recommendation(results):
    """Given a sorted list of result tuples, returns a recommendation
    flag (RECOMMEND_STRONG, RECOMMEND_MEDIUM, RECOMMEND_NONE) based
    on the results' distances.
    """
    if not results:
        # No candidates: no recommendation.
        rec = RECOMMEND_NONE
    else:
        min_dist = results[0][0]
        if min_dist < STRONG_REC_THRESH:
            # Strong recommendation level.
            rec = RECOMMEND_STRONG
        elif len(results) == 1:
            # Only a single candidate. Medium recommendation.
            rec = RECOMMEND_MEDIUM
        elif min_dist <= MEDIUM_REC_THRESH:
            # Medium recommendation level.
            rec = RECOMMEND_MEDIUM
        elif results[1][0] - min_dist >= REC_GAP_THRESH:
            # Gap between first two candidates is large.
            rec = RECOMMEND_MEDIUM
        else:
            # No conclusion.
            rec = RECOMMEND_NONE
    return rec

def validate_candidate(items, tuple_dict, info):
    """Given a candidate info dict, attempt to add the candidate to
    the output dictionary of result tuples. This involves checking
    the track count, ordering the items, checking for duplicates, and
    calculating the distance.
    """
    log.debug('Candidate: %s - %s' % (info['artist'], info['album']))

    # Don't duplicate.
    if info['album_id'] in tuple_dict:
        log.debug('Duplicate.')
        return

    # Make sure the album has the correct number of tracks.
    if len(items) != len(info['tracks']):
        log.debug('Track count mismatch.')
        return

    # Put items in order.
    ordered = order_items(items, info['tracks'])
    if not ordered:
        log.debug('Not orderable.')
        return

    # Get the change distance.
    dist = distance(ordered, info)
    log.debug('Success. Distance: %f' % dist)

    tuple_dict[info['album_id']] = dist, ordered, info

def tag_album(items, search_artist=None, search_album=None):
    """Bundles together the functionality used to infer tags for a
    set of items comprised by an album. Returns everything relevant:
        - The current artist.
        - The current album.
        - A list of (distance, items, info) tuples where info is a
          dictionary containing the inferred tags and items is a
          reordered version of the input items list. The candidates are
          sorted by distance (i.e., best match first).
        - A recommendation, one of RECOMMEND_STRONG, RECOMMEND_MEDIUM,
          or RECOMMEND_NONE; indicating that the first candidate is
          very likely, it is somewhat likely, or no conclusion could
          be reached.
    If search_artist and search_album are provided, then they are used
    as search terms in place of the current metadata.
    May raise an AutotagError if existing metadata is insufficient.
    """
    # Get current metadata.
    cur_artist, cur_album = current_metadata(items)
    log.debug('Tagging %s - %s' % (cur_artist, cur_album))
    
    # The output result tuples (keyed by MB album ID).
    out_tuples = {}
    
    # Try to find album indicated by MusicBrainz IDs.
    id_info = match_by_id(items)
    if id_info:
        validate_candidate(items, out_tuples, id_info)
        if out_tuples:
            # If we have a very good MBID match, return immediately.
            # Otherwise, this match will compete against metadata-based
            # matches.
            rec = recommendation(out_tuples.values())
            if rec == RECOMMEND_STRONG:
                log.debug('ID match.')
                return cur_artist, cur_album, out_tuples.values(), rec
    
    # Search terms.
    if not (search_artist and search_album):
        # No explicit search terms -- use current metadata.
        search_artist, search_album = cur_artist, cur_album
    log.debug('Search terms: %s - %s' % (search_artist, search_album))
    
    # Get candidate metadata from search.
    if search_artist and search_album:
        candidates = mb.match_album(search_artist, search_album,
                                    len(items), MAX_CANDIDATES)
        candidates = list(candidates)
    else:
        candidates = []

    # Get candidates from plugins.
    candidates.extend(plugins.candidates(items))
    
    # Get the distance to each candidate.
    log.debug('Evaluating %i candidates.' % len(candidates))
    for info in candidates:
        validate_candidate(items, out_tuples, info)
    
    # Sort by distance.
    out_tuples = out_tuples.values()
    out_tuples.sort()
    
    rec = recommendation(out_tuples)
    return cur_artist, cur_album, out_tuples, rec
