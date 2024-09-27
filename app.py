# app.py
from flask import Flask, render_template, request, jsonify, Response, send_from_directory
import subprocess
import os
import argparse
import threading
import queue
import time

# 在 app.py 的顶部添加这行
OUTPUT_DIR = os.environ.get('OUTPUT_DIR', '/app/output')

app = Flask(__name__)

# 全局队列用于存储日志消息
log_queue = queue.Queue()


def enqueue_output(out, queue):
    for line in iter(out.readline, ''):
        queue.put(line)
    out.close()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.png')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    output_path = os.path.join(OUTPUT_DIR, request.form['output_path'])
    template_file_playlist = request.form['template_file_playlist']
    print_exceptions = 'print_exceptions' in request.form
    save_playlist = 'save_playlist' in request.form

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    command = ['gamdl', '-o', output_path, '--template-file-playlist', template_file_playlist, '--ffmpeg-path', '/app/ffmpeg']

    if print_exceptions:
        command.append('--print-exceptions')
    if save_playlist:
        command.append('--save-playlist')

    command.append(url)

    # 清空队列
    while not log_queue.empty():
        log_queue.get_nowait()

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1,
                               universal_newlines=True)

    # 在新线程中读取输出
    t = threading.Thread(target=enqueue_output, args=(process.stdout, log_queue))
    t.daemon = True
    t.start()

    return jsonify({'status': 'started', 'message': 'Download started.'})


@app.route('/stream')
def stream():
    def generate():
        while True:
            try:
                # 非阻塞方式获取日志
                message = log_queue.get_nowait()
                yield f"data: {message}\n\n"
            except queue.Empty:
                time.sleep(0.1)

    return Response(generate(), mimetype='text/event-stream')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GAMDL Web UI')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')
    args = parser.parse_args()

    app.run(debug=True, host='0.0.0.0', port=args.port, threaded=True)