%#template to generate the dynamic HTML for Fresh Tomatoes Movie Trailers
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes Movie Trailers</title>
    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }
        #trailer .modal-dialog {
            margin-top: 70px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
            min-height: 360px;
        }
        .movie-tile {
            margin-bottom: 20px;
            padding-top: 20px;
        }
        .movie-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }
        .scale-media {
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
        #trailer-video-container .description{
			padding: 20px;
			padding-top: 0px;
        }

    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile', function (event) {
            var movie = $(this).data();
            var sourceUrl = 'http://www.youtube.com/embed/' + movie.trailerYoutubeId + '?autoplay=1&html5=1';
            var buttonEdit = '<a href="#" data-id="'+movie.id+'" class="btn btn-sm btn-primary edit-movie pull-right" data-dismiss="modal" data-toggle="modal" data-target="#add-update-movie-modal">Edit</a>';
            var buttonDelete  = '<a href="/delete/'+movie.id+ '"class="btn btn-sm btn-danger pull-right" style="margin-left: 5px;">Delete</a>';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            })).append('<div class="description"><h2>'+movie.title+buttonDelete+buttonEdit+'</h2><p>'+movie.storyLine+'</p></div>');
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
        // Add new movie
        $(document).on('click', '#add-movie', function (event) {
            event.preventDefault();
            var modal = $("#add-update-movie-modal")
            modal.find('form').attr("action", "/");
            modal.find('.modal-title').text('Add New Movie')
            modal.find('button[type="submit"]').text('Save Movie')
            modal.find('input[name="title"]').attr('value', '');
            modal.find('textarea[name="story"]').val('');
            modal.find('input[name="poster"]').attr('value', '');
            modal.find('input[name="trailer"]').attr('value', '');
        })
        // Update movie
        $(document).on('click', '.edit-movie', function (event) {
            event.preventDefault();
            var movie = $('div[data-id="'+$(this).data('id')+'"]').data();
            var modal = $("#add-update-movie-modal");
            modal.find('form').attr("action", "/edit/"+movie.id);
            modal.find('.modal-title').html('Edit <b>' + movie.title + '</b>');
            modal.find('button[type="submit"]').text('Save Movie');
            modal.find('input[name="title"]').attr('value', movie.title);
            modal.find('textarea[name="story"]').val(movie.storyLine);
            modal.find('input[name="poster"]').attr('value', movie.poster);
            modal.find('input[name="trailer"]').attr('value', movie.trailerYoutubeId);
        })
    </script>

</head>

  <body>

    <!-- Nav bar -->
    <div class="container">
        <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
            <div class="container">
                <div class="navbar-header">
                    <a class="navbar-brand" href="/">Fresh Tomatoes Movie Trailers</a>
                </div>
                <p class="navbar-text">by Daniel Yovchev</p>

                <ul class="nav navbar-nav navbar-right">
                    <li>
                        <a href="#" id="add-movie" data-toggle="modal" data-target="#add-update-movie-modal">
                            <span class="glyphicon glyphicon-plus"></span> Add New
                        </a>
                    </li>
                </ul>

            </div>
        </div>
    </div>

    <!-- Main Page Content -->
    <div class="container">
    	%for movie in movies:
			<div class="col-md-6 col-lg-4 movie-tile text-center" data-id="{{movie.id}}" data-trailer-youtube-id="{{movie.trailer_youtube_id}}" data-story-line="{{movie.storyline}}" data-title="{{movie.title}}" data-toggle="modal" data-target="#trailer" data-poster="{{movie.poster_image_url}}">
			    <img src="{{movie.poster_image_url}}" width="220" height="342">
			    <h2>{{movie.title}}</h2>
			</div>
		%end
    </div>

    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Trailer Video Modal -->
    <div class="modal fade bs-example-modal-lg" id="add-update-movie-modal" role="dialog" aria-labelledby="myLargeModalLabel">
        <form action method="POST" class="modal-dialog" role="document">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h4 class="modal-title">Add New Movie</h4>
              </div>
              <div class="modal-body">

                <div class="form-group">
                    <label for="newMovieTitle">Title</label>
                    <input name="title" type="text" class="form-control" id="newMovieTitle" placeholder="Movie Name">
                </div>
                <div class="form-group">
                    <label for="newMovieDescription">Description</label>
                    <textarea name="story" class="form-control" rows="3"></textarea>
                </div>
                <div class="form-group">
                    <label for="newMovieImageUrl">Image Url</label>
                    <input name="poster" type="text" class="form-control" id="newMovieImageUrl" placeholder="https://image.tmdb.org/t/p/w640/xfWac8MTYDxujaxgPVcRD9yZaul.jpg">
                </div>
                <div class="form-group">
                    <label for="newMovieTrailer">Youtube ID</label>
                    <input name="trailer" type="text" class="form-control" id="newMovieTrailer" placeholder="3xoxeCWpZyU">
                </div>

              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                <button type="submit" class="btn btn-primary">Save Movie</button>
              </div>
            </div><!-- /.modal-content -->
        </form><!-- /.modal-dialog -->
    </div>


  </body>
</html>