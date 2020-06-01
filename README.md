# Bookmarks Content Section
Bookmarks content section for the Academic theme (Hugo framework).


## Installation

1. Put all the files/directories of this repository in the root your Hugo Academic website
1. Fill the file `data/bookmakrs.yaml` with your bookmarks
1. Run the code code below **before** the static content generation:
`./generate_bookmarks_data.py \
    --bookmarks_filename data/bookmarks.yaml \
    --bookmarks_by_tags_filename data/bookmarks_by_tags.json \
    --tags_directory content/bookmarks/tags/`
