
from flask import Flask, render_template_string

app = Flask(__name__)

# HTML template with mobile-first design
template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mobile Optimized App</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            padding: 1rem;
            max-width: 100%;
        }
        .container {
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
        }
        .card {
            background: #fff;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }
        @media (max-width: 768px) {
            body {
                padding: 0.5rem;
            }
            .card {
                padding: 0.8rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>Mobile Optimized App</h1>
            <p>This page is optimized for mobile devices with responsive design.</p>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
