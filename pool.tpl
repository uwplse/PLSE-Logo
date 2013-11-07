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
    <p>Here is the gene pool for the PLSE logo genetic algorithm.</p>
    % for opt in opts:
    <div>
      <object type="image/svg+xml" data="/imgs/{{opt[0]}}.svg" width="200" height="200">
      </object>
      % if sum(opt[1]):
      {{round(opt[1][0] / sum(opt[1]), 2) * 100}}% ({{sum(opt[1])}} users)
      % else:
      No data
      % end
    </div>
    % end
  </body>
</html>
