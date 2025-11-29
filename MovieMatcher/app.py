from flask import Flask, render_template, request

app = Flask(__name__)

# After MOVIES and SEARCH_FIELDS definitions...

@app.route("/", methods=["GET", "POST"])
def search():
    query = ""
    field = "title"
    results = []

    if request.method == "POST":
        field = request.form.get("field") or "title"
        query = (request.form.get("query") or "").strip()

        if query and field in SEARCH_FIELDS:
            lower_query = query.lower()
            for movie in MOVIES:
                value = movie.get(field)
                if value is None:
                    continue
                # Convert to string (handles ints like year/rating)
                text_value = str(value)
                if lower_query in text_value.lower():
                    results.append(movie)

    return render_template(
        "index.html",
        fields=SEARCH_FIELDS,
        selected_field=field,
        query=query,
        results=results,
    )


import os

def parse_movie_block(lines):
    """
    lines: list of non-empty lines for one movie.
    Expected format:
      0: title
      1: lead actor
      2: supporting actor
      3: genre
      4: alternate genre
      5: year
      6: rating
      7: description (optional but usually present)
    """
    if len(lines) < 7:
        # Not enough data for a full movie, skip it
        return None

    title = lines[0].strip()
    lead = lines[1].strip()
    support = lines[2].strip()
    genre = lines[3].strip()
    alt_genre = lines[4].strip()
    if alt_genre == genre:
        alt_genre = " "
    year_raw = lines[5].strip()
    rating_raw = lines[6].strip()
    description = lines[7].strip() if len(lines) >= 8 else ""

    # Try to convert year & rating to int, but don't crash if they’re weird
    try:
        year = int(year_raw)
    except ValueError:
        year = None

    try:
        rating = int(rating_raw)
    except ValueError:
        rating = None

    return {
        "title": title,
        "lead": lead,
        "support": support,
        "genre": genre,
        "alt_genre": alt_genre,
        "year": year,
        "rating": rating,
        "description": description,
    }


def load_movies_from_file(filename="infile.txt"):
    """
    Reads the text file and returns a list of movie dicts.
    Uses blank lines to separate movie records.
    """
    movies = []

    if not os.path.exists(filename):
        print(f"[WARN] {filename} not found. No movies loaded.")
        return movies

    with open(filename, "r", encoding="utf-8") as f:
        block = []
        for line in f:
            # Detect blank line = end of one movie block
            if line.strip() == "":
                if block:
                    movie = parse_movie_block(block)
                    if movie:
                        movies.append(movie)
                    block = []
            else:
                # Non-empty line, part of current movie
                block.append(line.rstrip("\n"))

        # Handle last block if file doesn’t end with a blank line
        if block:
            movie = parse_movie_block(block)
            if movie:
                movies.append(movie)

    print(f"[INFO] Loaded {len(movies)} movies from {filename}")
    return movies

MOVIES = load_movies_from_file("infile.txt")

SEARCH_FIELDS = {
    "title": "Title",
    "lead": "Leading Actor",
    "support": "Supporting Actor",
    "genre": "Genre",
    "alt_genre": "Alternate Genre",
    "year": "Year",
    "rating": "Rating",
    "description": "Description",
}

# List of moods the user can choose from
MOODS = [
    "cozy",
    "sad",
    "stressed",
    "excited",
    "motivated",
    "nostalgic",
    "creative",
    "intense",
    "focused",
    "whimsical",
    "coming-of-age",
]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)