from filetype.filetype import guess_mime, guess_extension


def check_image(file):
    mime = guess_mime(file)

    if mime is not None and mime.split("/")[0] == "image":
        file.seek(0)
        ext = guess_extension(file)
        file.seek(0)
        return ext
    else:
        return False
