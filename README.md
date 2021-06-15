

Bugs

Cover filename issue

During the development of the add_book functionality, an issue arose with the image files showing. Uploading the images was fine, and worked thanks to the ever helpful advice of [Miguel Grinberg](https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask), but as the files were saved under the file path "/static/images/file_name.png", it was a struggle to get the file path to add to the database.
In the end, this was solved by turning it into an f string, adding the file path before it, then adding the "uploaded_file.filename" which was established in the image upload section above. This solved the issue outright, and I am seriously bloody chuffed with solving it!

However, getting it to stay when using the edit_book function is an ongoing problem. This would probably be easily fixed if image files weren't being saved to the static file but instead were hosted somewhere else as then this could be a link or something. In future updates, this will probably be the way, but until then books that need editing would be better sorted through the MongoDB Atlas webpage instead.


Getting the cover to stay if not updated in Edit Book page

```
        new_cov_check = request.form.to_dict('new_cover_check')
        if new_cov_check is True:
            # uploads file
            uploaded_file = request.files['cover']
            # sanitizes filename provided by client
            filename = secure_filename(uploaded_file.filename)
            if filename != '':
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in app.config["UPLOAD_EXTENSIONS"]:
                    abort(400)
                uploaded_file.save(
                    os.path.join(app.config["UPLOAD_PATH"], filename))
                book_cover = f"/static/images/{uploaded_file.filename}"
        else:
            book_cover = request.form.get("book.cover"),
```


[Big Shoulders Font](https://fonts.google.com/specimen/Big+Shoulders+Display?preview.text=ROBERT%20CLARK&preview.text_type=custom)

[Remix Icons](https://remixicon.com/)

[Navbar](https://www.youtube.com/watch?v=At4B7A4GOPg)

[Slick Slider Carousel](http://kenwheeler.github.io/slick/)

[Contact form tutorial](https://www.youtube.com/watch?v=6VGu1CwCN2Y)