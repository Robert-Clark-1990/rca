

Bugs

Cover filename issue

During the development of the add_book functionality, an issue arose with the image files showing. Uploading the images was fine, and worked thanks to the ever helpful advice of [Miguel Grinberg](https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask), but as the files were saved under the file path "/static/images/file_name.png", it was a struggle to get the file path to add to the database.
In the end, this was solved by turning it into an f string, adding the file path before it, then adding the "uploaded_file.filename" which was established in the image upload section above. This solved the issue outright, and I am seriously bloody chuffed with solving it!



[Big Shoulders Font](https://fonts.google.com/specimen/Big+Shoulders+Display?preview.text=ROBERT%20CLARK&preview.text_type=custom)

[Remix Icons](https://remixicon.com/)

[Navbar](https://www.youtube.com/watch?v=At4B7A4GOPg)

[Slick Slider Carousel](http://kenwheeler.github.io/slick/)

[Contact form tutorial](https://www.youtube.com/watch?v=6VGu1CwCN2Y)