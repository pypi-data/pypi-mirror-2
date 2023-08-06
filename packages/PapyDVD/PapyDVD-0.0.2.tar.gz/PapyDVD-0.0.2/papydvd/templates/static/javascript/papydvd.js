/**
 * PaPyDVD scripts
 */

$(document).ready(function() {
	
	/**
	 * Prepare al features for the movie dialog
	 */
	var prepareMovieDialog = function(dialog, command, actionLabel, id) {

		// Form action
		$('form', dialog).attr('action', $('form', dialog).attr('action') + command);
		// Submit label
		$(':submit', dialog).attr('value', actionLabel);		
		
		if (id) {
			$("input[name=movie_id]").val(id);
		}

        /**
         * Popup for adding a new genre 
         */
        $(".newGenreCommand", dialog).click(function(event) {
            event.preventDefault();
            var genreDialog = $("#models .genreDialog").clone();

            genreDialog.dialog(
                {modal:true,
                 title:'Aggiunta di un Genere',
                 width: 500
                 }
            );
            $(":submit", genreDialog).click(function(event) {
                event.preventDefault();
                $.getJSON('/addGenre', {name: $(":input[name=name]", genreDialog).val(),
                                        description: $(":input[name=description]", genreDialog).val()},
                          /**
                           * Add the new genre, then load all genres from server and update the opening
                           * genre selection, selecting the new ones
                           * @param {Object} data json server genres response
                           */
                          function(data, textStatus) {
                              var genreSelect = $(":input[name=genre_id]", dialog);
                            genreSelect.children(":not(:first)").remove();
                            $.each(data, function() {
                                genreSelect.append('<option value="'+this.id+'"'+(this.selected?' selected="selected"':'')+'>'+this.name+'</option>');
                            });
                            genreDialog.dialog('close');
                });
            });
        });
        
        /**
         * Popup for adding a new director 
         */
        $(".newDirectorCommand", dialog).click(function(event) {
            event.preventDefault();
            var directorDialog = $("#models .directorDialog").clone();
            directorDialog.dialog(
                {modal:true,
                 title:'Aggiunta di un Regista',
                 width: 500
                 }
            );
            $(":submit", directorDialog).click(function(event) {
                event.preventDefault();
                $.getJSON('/addDirector', {name: $(":input[name=name]", directorDialog).val()},
                          /**
                           * Add the new director, then load all from server and update the opening
                           * director selection, selecting the new ones
                           * @param {Object} data json server directors response
                           */
                          function(data, textStatus) {
                              var directorSelect = $(":input[name=director_id]", dialog);
                            directorSelect.children(":not(:first)").remove();
                            $.each(data, function() {
                                directorSelect.append('<option value="'+this.id+'"'+(this.selected?' selected="selected"':'')+'>'+this.name+'</option>');
                            });
                            directorDialog.dialog('close');
                });
            });
        });
	};
	
	/**
	 * Add new movie
	 */
    $("#addMovieCommand").click(function(event) {
        event.preventDefault();
        var dialog = $("#models .movieDialog").clone();
        dialog.dialog(
            {modal:true,
             title:'Aggiunta di un Film',
             width: 550
             }
        );
		prepareMovieDialog(dialog, 'addMovie', 'Aggiungi');
    });

	/**
	 * Edit movie
	 */
    $(".editMovieCommand").click(function(event) {
        event.preventDefault();
        var dialog = $("#models .movieDialog").clone();
		var href = $(this).attr('href');
		var id = href.substring(href.indexOf('movie_id=')+9);
		
		// Fill dialog DOM with movie data
		$.getJSON('/loadMovie', {movie_id: id}, function(data) {
			$(":input[name=title]", dialog).val(data.title);
			$(":input[name=primary_number]", dialog).val(data.primary_number);
			$(":input[name=secondary_number]", dialog).val(data.secondary_number);
			$(":input[name=year]", dialog).val(data.year);
			$(":input[name=genre_id]", dialog).val(data.genre_id);
			$(":input[name=director_id]", dialog).val(data.director_id);
	        dialog.dialog(
	            {modal:true,
	             title:'Modifica il Film',
	             width: 550
	             }
	        );
			prepareMovieDialog(dialog, 'updateMovie', 'Salva', id);
		});		
    });
    
    // Confirm movie deletion
    $(".deleteCommand").click(function(event) {
        var confirmDialog = $("#models .confirmDialog").clone();
        var link = $(this);
        event.preventDefault();
        confirmDialog.dialog({
            resizable: false,
            width: 500,
            modal: true,
            title: 'Conferma cancellazione',
            buttons: {
                Conferma: function() {
                    $(this).dialog( "close" );
                    window.location.href = link.attr('href');
                },
                Annulla: function() {
                    $(this).dialog( "close" );
                }
            }
        });
    });

});
