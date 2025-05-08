from IPython import get_ipython
from IPython.display import display, YouTubeVideo
from IPython.core.display import Javascript
import re
import random
from functools import wraps
from urllib import parse
import warnings


def parse_youtube_url(url: str) -> str:
    """Get the YouTube video ID from a URL.

    Reference: https://stackoverflow.com/questions/4356538/how-can-i-extract-video-id-from-youtubes-link-in-python

    Args:
        url (str): The YouTube URL.

    Returns:
        str: The YouTube video ID.

    Examples:
        Get the video ID from a URL.

        ```python
        parse_youtube_url("https://www.youtube.com/watch?v=z3SEc70eQYE")
        # "z3SEc70eQYE"
        ```

    """
    url_data = parse.urlparse(url)
    query = parse.parse_qs(url_data.query)
    return query["v"][0]


def in_jupyter_notebook() -> bool:
    return get_ipython().__class__.__name__ == "ZMQInteractiveShell"


def in_marimo_notebook() -> bool:
    try:
        import marimo as mo

        return mo.running_in_notebook()
    except ImportError:
        return False


def is_url(url_string):
    """Checks if a string is a valid URL using regular expressions.

    Args:
      url_string: The string to check.

    Returns:
      True if the string is a valid URL, False otherwise.
    """
    regex = r"^(https?://)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/\S*)?$"
    match = re.match(regex, url_string)
    return bool(match)


def but_better(video: str, stop_on_completion: bool = True, **youtube_kwargs):
    """Wrap any function with this decorator to play a YouTube video while it runs.

    Args:
        video (str): The YouTube video ID or URL.
        stop_on_completion (bool): Whether to stop the video when the function completes.
        **youtube_kwargs: Additional keyword arguments to pass to `IPython.display.YouTubeVideo`.

    Returns:
        function: The decorated function that plays the YouTube video
            while the original function runs.

    Examples:
        Use as a decorator to play a YouTube video while a function runs.

        ```python
        @but_better("z3SEc70eQYE")
        def phillies_hype_song():
            print("Let's go Phillies!")
        ```

        Return a new function from an existing function.

        ```python
        from my_module import my_function

        my_function_but_better = but_better("z3SEc70eQYE")(my_function)
        ```

    """
    if not in_jupyter_notebook() and not in_marimo_notebook():
        warnings.warn(
            "This decorator only works in Jupyter or marimo notebooks.",
            UserWarning,
        )
        return lambda func: func

    if "allow_autoplay" not in youtube_kwargs:
        youtube_kwargs["allow_autoplay"] = True

    video_id = video if not is_url(video) else parse_youtube_url(video)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            display(YouTubeVideo(video_id, **youtube_kwargs))
            result = func(*args, **kwargs)
            if not stop_on_completion:
                return result

            stop_video_js = f"""
            var iframe = document.querySelector('iframe[src*="{video_id}"]');
            if (iframe) {{
                var url = new URL(iframe.src);
                url.searchParams.set('autoplay', '0');
                iframe.src = url.toString();
            }}
            """
            display(Javascript(stop_video_js))
            return result

        return wrapper

    return decorator


PREDEFINED_VIDEOS = {
    "elevator": "xNjyG8S4_kI",
    "favorite_customer": "mwgcK4E_RU0",
    "gasolina": "3tw2P65wv5E",
    "gotcha": "dQw4w9WgXcQ",
    "phillies_hype_song": "z3SEc70eQYE",
    "ten_hour_fireplace": "L_LUpnjgPso",
}


def random_video():
    """Return a random video from the predefined list.

    Examples:
        Get a random video from the predefined list.

        ```python
        from but_better import random_video

        @random_video
        def your_function():
            ...
        ```
    """
    return but_better(random.choice(list(PREDEFINED_VIDEOS.values())))


elevator = but_better(PREDEFINED_VIDEOS["elevator"])
favorite_customer = but_better(PREDEFINED_VIDEOS["favorite_customer"])
gasolina = but_better(PREDEFINED_VIDEOS["gasolina"])
gotcha = but_better(PREDEFINED_VIDEOS["gotcha"])
phillies_hype_song = but_better(PREDEFINED_VIDEOS["phillies_hype_song"])
ten_hour_fireplace = but_better(PREDEFINED_VIDEOS["ten_hour_fireplace"])
