$(document).ready(function(){
    const apiUrl = 'http://' + location.hostname + ':5006/submit_song';
    let query_data = {}
    $('form#submit_songs').submit(function(event) {
        event.preventDefault();
        let songTitle = $('#song_title').val();
        let artistName = $('#artist_name').val();
        query_data['song_name'] = songTitle;
        query_data['artist'] = artistName;
        console.log(query_data)

        $.ajax({
            type: 'POST',
            url: apiUrl,
            contentType: 'application/json',
            data: JSON.stringify(query_data),
            success: function(response) {
                $('section.welcome').empty();
                $('section.submission').empty();
                $('section.recommendations').empty();
                let tracks = response['tracks'];
                console.log(tracks)
                let thankYouNote = `<h2>Thank you for using FlairVibes Tailor</h2>`
                let message = `<h4>Based on your favourite song, <b>${songTitle}</b>, here are some songs we think you might like!</h4>`;
                let goagainButton = `<form>
                    <input type="submit" value="ouu i wanna go again!" id="goagainButton">
                </form>`
                $('section.welcome').append(thankYouNote);
                $('section.recommendations').append(message);
                for (track of tracks) {
                    parsedTrack = JSON.parse(track)
                    let recommendations = `
                    <li><b>${parsedTrack['title']}</b> by ${parsedTrack['artist']}
                    <p class="listtext"> listen to <a href="${parsedTrack['link']}" target="_blank"> ${parsedTrack['title']}</a> on spotify</p>
                    </li>`;
                    $('section.recommendations').append(recommendations);
                }
                $('section.recommendations').append(goagainButton);
            },
            error: function(tokenErr, textStatus, errorThrown) {
                $('section.recommendations').empty();
                if (tokenErr.status === 400) {
                // handle error
                let message = `<h4>oops something went wrong, please try again some other time</h4>`;
                $('section.recommendations').append(message);
                } else if (tokenErr.status === 500) {
                    let message = `<h4>oops something went wrong, please check your submitted details</h4>
                                    <p>note: the song submited might not be present on major streaming services like apple music and/or spotify</p>`;
                    $('section.recommendations').append(message);
                }
            }
        });
    });
    $('form#goagainButton').submit(function(event) {
        event.preventDefault();
        location.reload(true);
    });
});