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
  </head>
  <body>
    <p>Which logo best represents <em>PLSE (pronounced “pulse”)</em>, the
    <em>programming languages and software engineering</em>
    research group at the <em>University of Washington</em>.</p>
    <div>
      <object type="image/svg+xml" data="/imgs/{{id1}}.svg" width="200" height="200">
      </object>
      <a href="/vote/{{id1}}/{{id2}}"> This one! </a>
    </div>
    <div>
      <object type="image/svg+xml" data="/imgs/{{id2}}.svg" width="200" height="200">
      </object>
      <a href="/vote/{{id2}}/{{id1}}"> This one! </a>
    </div>
    <p> Or are <a href="/hate/{{id1}}/{{id2}}">both terrible</a>?
  </body>
</html>
