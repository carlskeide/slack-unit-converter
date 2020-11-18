
<!DOCTYPE html
PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
        <head>
                <title>brage.skeide.se</title>
                <style type="text/css">
                        body {
                            background: #FFFFFF;
                            color: #000000;
                            font-family: arial,verdana,helvetica,sans-serif;
                            font-size: .8em;
                        }
                        img {
                            border: 0px;
                            padding: 0px;
                            margin: 0px;
                        }
                        a {
                            color: #666;
                            text-decoration: none;
                        }
                        a:hover {
                            color: #000;
                            text-decoration: none;
                        }
                        hr {
                            color: #666;
                            background-color: #666;
                            height: 1px;
                            border: 0;
                        }
                        #position {
                            height: 200px;
                            width: 600px;
                            position: absolute;
                            left: 50%;
                            top: 50%;
                            margin-left: -300px;
                            margin-top: -100px;
                            text-align: center;
                        }
                        #position h1 {
                            color: #666;
                            font-size: 2em;
                            margin: .3em;
                        }
                        #list {
                            text-align: left;
                        }
                        .spacer {
                            padding: 0px 5px;
                        }
                </style>
        </head>
        <body>
                <div id="position">
                        <h1>{{ app_title }}</h1>
                       {{ button }}
                </div>
        </body>
</html>