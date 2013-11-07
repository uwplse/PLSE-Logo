<!doctype html>
<html>
  <head>
    <meta charset="utf8" />
    <title>Decide the next PLSE Logo</title>
    <style>
/* Style goes here */
body {
max-width: 550px;
margin: 10px auto;
padding: 0;
}

object {
display: block;
}

div {
width: 200px;
text-align: center;
margin: 35px;
float: left;
}

p {
hyphens: auto;
text-align: justify;
}
    </style>
    <script>
document.onkeydown = function(e) {
    e = e || event;
    switch (e.keyCode) {
        case 37:
            window.location.href = document.getElementById("im1").href;
            break;
        case 39:
            window.location.href = document.getElementById("im2").href;
            break;
        default:
            return true;
    }
}
    </script>
  </head>
  <body>
    <p>Which logo best represents <em>PLSE (pronounced “pulse”)</em>, the
    <em>programming languages and software engineering</em>
    research group at the <em>University of Washington</em>.</p>
    <div>
      <object type="image/svg+xml" data="/imgs/{{id1}}.svg" width="200" height="200">
      </object>
      <a id="im1" href="/vote/{{id1}}/{{id2}}"> This one! </a>
    </div>
    <div>
      <object type="image/svg+xml" data="/imgs/{{id2}}.svg" width="200" height="200">
      </object>
      <a id="im2" href="/vote/{{id2}}/{{id1}}"> This one! </a>
    </div>
    <p> You can also use the <em>left and right arrow keys</em> to select a logo.
  </body>
</html>
