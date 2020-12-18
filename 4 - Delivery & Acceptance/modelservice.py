import os
import pandas as pd
from io import StringIO 
from flask import Flask, request, render_template, url_for, redirect, send_file, make_response

app = Flask(__name__)


@app.route("/")
def fileFrontPage():
    return """
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

    <title>Forest Cover Type Prediction</title>
    <meta name="theme-color" content="#563d7c">


    <style>
      .bd-placeholder-img {
        font-size: 1.125rem;
        text-anchor: middle;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
      }

      @media (min-width: 768px) {
        .bd-placeholder-img-lg {
          font-size: 3.5rem;
        }
      }
    </style>
  </head>
  <body>
  <nav class="navbar navbar-dark bg-primary">
  <a class="navbar-brand" href="#">Forest Cover Type Prediction</a>
</nav>
<div class="jumbotron">
  <h3>Please upload the test dataset:</h3>
    <form action="/handleUpload" method="post" enctype="multipart/form-data">
  <div class="col">
        <input type="file" name="data_file" />
        <input class="btn btn-primary btn-lg" type="submit" />
    </div>
    </form>
</div>
    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
  </body>
</html>    
    """

import joblib
@app.route("/handleUpload", methods=['GET','POST'])
def handleFileUpload():
    print(request.files)
    from io import StringIO
    if 'data_file' in request.files:
        fs = request.files['data_file']
        test_df = df = pd.read_csv(fs.stream)
        model_filename = 'forestcover.joblib'
        newmodel = joblib.load(model_filename)
        y_submission = newmodel.predict(test_df).round(0).astype(int)
        w = [list(test_df['Id']),list(y_submission)]
        dataset_submission = pd.DataFrame({'Id':list(test_df['Id']), 'Cover_Type':list(y_submission)})
        resp = make_response(dataset_submission.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp

    return redirect(url_for('fileFrontPage'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)