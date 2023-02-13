$(document).ready(function(){
    const apiUrl = 'http://' + location.hostname + ':5000/submit_song';
    let query_data = {}
    $('form').submit(function(event) {
        event.preventDefault();
        let songTitle = $('#song_title').val();
        let artistName = $('#artist_name').val();
        console.log(songTitle)
        console.log(artistName)
        query_data['song_name'] = songTitle;
        query_data['artist'] = artistName;
        console.log(query_data)

        $.ajax({
            type: 'POST',
            url: apiUrl,
            contentType: 'application/json',
            data: JSON.stringify(query_data),
            success: function(response) {
                $('section.recommendations').empty();
                let tracks = response['tracks'];
                let message = `<h4>Here are some songs we think you might like!</h4>`;
                $('section.recommendations').append(message);
                for (track of tracks) {
                    let recommendations = `
                    <li>${track}</li>`;
                    $('section.recommendations').append(recommendations);
                }
            },
            error: function(tokenErr, textStatus, errorThrown) {
                if (tokenErr.status === 400) {
                // handle error
                let message = `<h4>oops something went wrong, please try again some other time</h4>`;
                $('section.recommendations').append(message);
                } else if (tokenErr.status === 500) {
                    let message = `<h4>oops something went wrong, please check your spellings</h4>`;
                    $('section.recommendations').append(message);
                }
            }
        });
    });
});