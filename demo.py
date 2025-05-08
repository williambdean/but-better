# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "but-better==0.3.0",
#     "marimo",
#     "ipython",
# ]
# ///

import marimo

__generated_with = "0.13.2"
app = marimo.App(width="medium")


@app.cell
def _(PREDEFINED_VIDEOS, mo):
    mo.md(
        rf"""
        # Your code but better


        ## Installation

        Find the package on [PyPI](https://pypi.org/project/but-better/): 

        ```bash
        uv add but-better
        ```

        ## Usage

        Use the `but_better` decorator to kill the time during long function runs: 

        ```python
        from but_better import but_better

        @but_better("<any-youtube-id-or-url>")
        def your_slow_function(): 
            ...
        ```

        Wrap someone else's function as well:

        ```python
        from their_module import their_function

        their_function_but_butter = but_better("<any-youtube-id-or-url>")(their_function)
        ```

        Can't choose? Use a prefined video:

        ```python
        from but_better import {", ".join(PREDEFINED_VIDEOS.keys())}
        ```
        """
    )
    return


@app.cell
def _():
    from but_better import gotcha, but_better, PREDEFINED_VIDEOS

    return PREDEFINED_VIDEOS, but_better, gotcha


@app.cell
def _(gotcha):
    import time

    @gotcha
    def slow_function_but_better():
        time.sleep(10)  # Simulate a slow function
        return "Function finished!"

    return slow_function_but_better, time


@app.cell
def _(slow_function_but_better):
    slow_function_but_better()
    return


@app.cell
def _(but_better, time):
    youtube_url = "https://www.youtube.com/watch?v=E1bo_G6vncg"
    fire_and_waves = but_better(youtube_url)

    def another_slow_function():
        time.sleep(10)
        return "Another function finished!"

    slow_function_but_calmer = fire_and_waves(another_slow_function)
    return (slow_function_but_calmer,)


@app.cell
def _(slow_function_but_calmer):
    slow_function_but_calmer()
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
