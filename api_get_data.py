import time


def write_stream_streamlit(text: str):
    for i in text:
        yield i
        # time.sleep(0.01)
