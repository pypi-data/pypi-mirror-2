/**
 * PaPyDVD scripts
 */

$.PapyDVD = {
	params: {
		curr_page: 0,
		b_size: 30,
		autocomplete_min_chars: 2
	}
};

$(document).ready(function() {
	
	/**
	 * Prepare all features for the movie dialog
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
	}; // end of prepareMovieDialog


	/**
	 * Prepare all features for the director dialog
	 */
	var prepareDirectorDialog = function(dialog, command, actionLabel, id) {

		// Form action
		$('form', dialog).attr('action', $('form', dialog).attr('action') + command);
		// Submit label
		$(':submit', dialog).attr('value', actionLabel);		
		
		if (id) {
			$("input[name=director_id]").val(id);
		}
        
	}; // end of prepareDirectorDialog


	/**
	 * Prepare all features for the genre dialog
	 */
	var prepareGenreDialog = function(dialog, command, actionLabel, id) {

		// Form action
		$('form', dialog).attr('action', $('form', dialog).attr('action') + command);
		// Submit label
		$(':submit', dialog).attr('value', actionLabel);		
		
		if (id) {
			$("input[name=genre_id]").val(id);
		}
        
	}; // end of prepareGenreDialog

	
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
    var editMovieCommandEventHandler = function(event) {
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
    };
	
	$(".editMovieCommand").click(editMovieCommandEventHandler);
    
    // Confirm movie deletion dialog
    var deleteMovieCommandEventHandler = function(event) {
        var confirmDialog = $("#models .confirmDeleteMovieDialog").clone();
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
    };

	/**
	 * Edit director
	 */
    var editDirectorCommandEventHandler = function(event) {
        event.preventDefault();
        var dialog = $("#models .directorDialog").clone();
		var href = $(this).attr('href');
		var id = href.substring(href.indexOf('director_id=') + 12);
		
		// Fill dialog DOM with director's data
		$.getJSON('/loadDirector', {director_id: id}, function(data) {
			$(":input[name=name]", dialog).val(data.name);
	        dialog.dialog(
	            {modal:true,
	             title:'Modifica il Regista',
	             width: 550
	             }
	        );
			prepareDirectorDialog(dialog, 'updateDirector', 'Salva', id);
		});		
    };
	
	$(".editDirectorCommand").click(editDirectorCommandEventHandler);


	/**
	 * Edit genre
	 */
    var editGenreCommandEventHandler = function(event) {
        event.preventDefault();
        var dialog = $("#models .genreDialog").clone();
		var href = $(this).attr('href');
		var id = href.substring(href.indexOf('genre_id=') + 9);
		
		// Fill dialog DOM with director's data
		$.getJSON('/loadGenre', {genre_id: id}, function(data) {
			$(":input[name=name]", dialog).val(data.name);
	        dialog.dialog(
	            {modal:true,
	             title:'Modifica il Genere',
	             width: 550
	             }
	        );
			prepareGenreDialog(dialog, 'updateGenre', 'Salva', id);
		});		
    };
	
	$(".editGenreCommand").click(editDirectorCommandEventHandler);


    // Confirm director deletion dialog	
	$('.deleteDirectorCommand').click(function(event) {
        var confirmDialog = $("#models .confirmDeleteDirectorDialog").clone();
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

    // Confirm genre deletion dialog	
	$('.deleteGenreCommand').click(function(event) {
        var confirmDialog = $("#models .confirmDeleteGenreDialog").clone();
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

	var lastSearchQuery = '';
	var searchField = $('#search');
	searchField.keyup(function(event) {
		if (searchField.val().length>=$.PapyDVD.params.autocomplete_min_chars && searchField.val()!==lastSearchQuery || searchField.val().length<lastSearchQuery.length) {
			$('#main').trigger('PapyDVD.updateTable', [searchField.val(), $.PapyDVD.params.curr_page, $.PapyDVD.params.b_size]);
		}
	});
	searchField.keydown(function(event) {
		lastSearchQuery = searchField.val();
	});
	
	// First thing to do when the page is loaded
	var loadingRow = $('#loading');
	$('#movieList #main').bind('PapyDVD.updateTable', function(event, search, b_start, b_size) {
		b_start = b_start || 0;
		b_size = b_size || 30;
		$this = $(this);
		$this.find('tr:not(:first)').remove();
		loadingRow.show();
		$.getJSON('/loadMovies', {'search': search, 'b_start': b_start, 'b_size': b_size}, function(data) {
			loadingRow.hide();
			$.each(data.movies, function(index, value) {
				var rowClass = index % 2 == 0 ? 'even' : 'odd';
				var newRow = $('#rowModel tr').clone(false).addClass(rowClass);
				// Cell 1: commands
				$('.movieCommands a:first', newRow).attr('href', $('.movieCommands a:first', newRow).attr('href')+value.id);
				$('.movieCommands a:eq(1)', newRow).attr('href', $('.movieCommands a:eq(1)', newRow).attr('href')+value.id);
				// Cell 2: id
				$('td:eq(1)', newRow).text(value.primary_number+(value.secondary_number?'/'+value.secondary_number:''));
				// Cell 2: title
				$('td:eq(2)', newRow).text(value.title);
				// Cell 3: genre
				$('td:eq(3)', newRow).text(value.genre);
				// Cell 4: year
				$('td:eq(4)', newRow).text(value.year);
				// Cell 5: director
				$('td:eq(5)', newRow).text(value.director);
				// Events
				$('.deleteMovieCommand', newRow).click(deleteMovieCommandEventHandler);
				$('.editMovieCommand', newRow).click(editMovieCommandEventHandler);

				// Batching
				if (data.canGoLeft) {
					$('#pageBack').show();
				} else {
					$('#pageBack').hide();
				}
				if (data.canGoRight) {
					$('#pageForward').show();
				} else {
					$('#pageForward').hide();
				}

				$this.append(newRow);
			});	
		});
	}).trigger('PapyDVD.updateTable', ['', 0, $.PapyDVD.params.b_size]);
	
	$('#pageBack a').click(function(event) {
		event.preventDefault();
		$.PapyDVD.params.curr_page = $.PapyDVD.params.curr_page-=1;
		$('#main').trigger('PapyDVD.updateTable', [searchField.val(),
		                                           $.PapyDVD.params.curr_page*$.PapyDVD.params.b_size,
												   $.PapyDVD.params.b_size]);
	});
	$('#pageForward a').click(function(event) {
		event.preventDefault();
		$.PapyDVD.params.curr_page = $.PapyDVD.params.curr_page+=1;
		$('#main').trigger('PapyDVD.updateTable', [searchField.val(),
		                                           $.PapyDVD.params.curr_page*$.PapyDVD.params.b_size,
												   $.PapyDVD.params.b_size]);
	});
	
	if ($('.portalMessage').length>0) {
		$.jGrowl($('.portalMessage').text(),{ life: 10000, theme: 'error' });
	}
	

});
