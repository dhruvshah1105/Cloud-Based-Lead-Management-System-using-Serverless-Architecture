const btn = document.querySelector('button');

function sendData( data ) {
  const XHR = new XMLHttpRequest(),
        FD  = new FormData();

  // Push our data into our FormData object
  for( name in data ) {
    FD.append( name, data[ name ] );
  }

  // Define what happens on successful data submission
  XHR.addEventListener( 'load', function( event ) {
    alert( 'Yeah! Data sent and response loaded.' );
  } );

  // Define what happens in case of error
  XHR.addEventListener(' error', function( event ) {
    alert( 'Oops! Something went wrong.' );
  } );

  // Set up our request
  XHR.open( 'POST', 'https://ifdcnhnnoc.execute-api.us-east-1.amazonaws.com/dev/post-json' );

  // Send our FormData object; HTTP headers are set automatically
  XHR.send( FD );
}

btn.addEventListener( 'click', function()
  { sendData( {test:'ok'} );
} )