import _thread  # 创建线程用的
import argparse  # 解析参数
import asyncio
import functools
import sys
import time
import wave
from datetime import datetime
from typing import List
from ppasr.predict import PPASRPredictor
import websockets
from flask import request, Flask, render_template, send_file
from io import BytesIO
from flask_cors import CORS
from concurrent.futures import ProcessPoolExecutor
from ppasr.utils.logger import setup_logger
from ppasr.utils.utils import add_arguments, print_arguments

from text_to_bt import *

BT_SAVE_DIR = "primitives/task_base/"
IMG_BT_SAVE_DIR = "primitives/task_base/images/"
BT_SAVE_DIR_TEMP = "primitives/task_base/temp/"

BT = None

logger = setup_logger(__name__)

parser = argparse.ArgumentParser(description=__doc__)
add_arg = functools.partial(add_arguments, argparser=parser)
add_arg('configs', str, 'asrs/ppasr/configs/conformer_chatgbt.yml', "配置文件")
add_arg("host", str, '0.0.0.0', "监听主机的IP地址")
add_arg("port_server", int, 5000, "普通识别服务所使用的端口号")
add_arg("port_stream", int, 5001, "流式识别服务所使用的端口号")
add_arg("save_path", str, 'asrs/ppasr/dataset/upload/', "上传音频文件的保存目录")
add_arg('use_gpu', bool, True, "是否使用GPU预测")
add_arg('use_pun', bool, True, "是否给识别结果加标点符号")
add_arg('is_itn', bool, False, "是否对文本进行反标准化")
add_arg('num_web_p', int, 2, "多少个预测器，这个是Web服务并发的数量，必须大于等于1")
add_arg('num_websocket_p', int, 2, "多少个预测器，这个是WebSocket同时连接的数量，必须大于等于1")
add_arg('model_path', str, 'asrs/ppasr/models/conformer_streaming_fbank/infer', "导出的预测模型文件路径")
add_arg('pun_model_dir', str, 'asrs/ppasr/models/pun_models/', "加标点符号的模型文件夹路径")
args = parser.parse_args()
print_arguments(args=args)

app = Flask('PPASR', template_folder="asrs/ppasr/templates", static_folder="asrs/ppasr/static", static_url_path="/")
# 允许跨越访问
CORS(app)

assert args.num_web_p >= 1, f'Web服务的预测器数量必须大于等于1，当前为：{args.num_web_p}'
assert args.num_websocket_p >= 1, f'WebSocket服务的预测器数量必须大于等于1，当前为：{args.num_websocket_p}'

# 多进程
executor = ProcessPoolExecutor(max_workers=args.num_web_p)
# 创建预测器，是实时语音的第一个对象和创建多进程时使用
predictor = PPASRPredictor(configs=args.configs,
                           model_path=args.model_path,
                           use_gpu=args.use_gpu,
                           use_pun=args.use_pun,
                           pun_model_dir=args.pun_model_dir)
# 创建多个预测器，实时语音识别所以要这样处理
predictors: List[PPASRPredictor] = [predictor]


# 多进行推理需要用到的
def run_model_recognition(file_path, is_long_audio=False):
    if is_long_audio:
        result = predictor.predict_long(audio_data=file_path, use_pun=args.use_pun, is_itn=args.is_itn)
    else:
        result = predictor.predict(audio_data=file_path, use_pun=args.use_pun, is_itn=args.is_itn)
    return result


# 语音识别接口
@app.route("/recognition", methods=['POST'])
def recognition():
    f = request.files['audio']
    if f:
        # 保存路径
        save_dir = os.path.join(args.save_path, datetime.now().strftime('%Y-%m-%d'))
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, f'{int(time.time() * 1000)}{os.path.splitext(f.filename)[-1]}')
        f.save(file_path)
        try:
            start = time.time()
            # 执行识别
            result = executor.submit(run_model_recognition, file_path, is_long_audio=False).result()
            score, text = result['score'], result['text']
            end = time.time()
            print("识别时间：%dms，识别结果：%s， 得分: %f" % (round((end - start) * 1000), text, score))
            result = str({"code": 0, "msg": "success", "result": text, "score": round(score, 3)}).replace("'", '"')
            return result
        except Exception as e:
            print(f'[{datetime.now()}] 短语音识别失败，错误信息：{e}', file=sys.stderr)
            return str({"error": 1, "msg": "audio read fail!"})
    return str({"error": 3, "msg": "audio is None!"})


# 长语音识别接口
@app.route("/recognition_long_audio", methods=['POST'])
def recognition_long_audio():
    f = request.files['audio']
    if f:
        # 保存路径
        save_dir = os.path.join(args.save_path, datetime.now().strftime('%Y-%m-%d'))
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, f'{int(time.time() * 1000)}{os.path.splitext(f.filename)[-1]}')
        f.save(file_path)
        try:
            start = time.time()
            result = executor.submit(run_model_recognition, file_path, is_long_audio=True).result()
            score, text = result['score'], result['text']
            end = time.time()
            print("识别时间：%dms，识别结果：%s， 得分: %f" % (round((end - start) * 1000), text, score))
            result = str({"code": 0, "msg": "success", "result": text, "score": score}).replace("'", '"')
            return result
        except Exception as e:
            print(f'[{datetime.now()}] 长语音识别失败，错误信息：{e}', file=sys.stderr)
            return str({"error": 1, "msg": "audio read fail!"})
    return str({"error": 3, "msg": "audio is None!"})


@app.route('/generate_bt_img', methods=['POST'])
def generate_bt_img():
    global BT  # 多线程可能有点问题
    # 获取前端发送的文本信息
    task_description = request.data.decode('utf-8')
    print(task_description)
    # 调用text_to_BT服务转化为响应的行为树，并且保存响应的图片。过度图片也要存
    BT = text_to_BT(task_description, BT)
    # 将BT保存到temp_img中
    tree_to_xml_file(BT, "temp", BT_SAVE_DIR_TEMP + 'temp.xml')
    py_trees.display.render_dot_tree(BT, name="temp", target_directory=BT_SAVE_DIR_TEMP)
    # 读取图片
    image_data = open(BT_SAVE_DIR_TEMP + "/temp.png", 'rb').read()
    return send_file(BytesIO(image_data), mimetype='image/png')


@app.route('/generate_and_reuse_bt_img', methods=['POST'])
def generate_and_reuse_bt_img():
    global BT
    # 获取前端发送的文本信息
    task_name = request.data.decode('utf-8')
    # 将BT保存到temp_img中
    tree_to_xml_file(BT, task_name, BT_SAVE_DIR + task_name + '.xml')
    # 创建任务存放目录
    dir_path = IMG_BT_SAVE_DIR + task_name
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    py_trees.display.render_dot_tree(BT, name=task_name, target_directory=dir_path)
    BT = None
    # 读取图片
    image_data = open(dir_path +"/"+ task_name + ".png", 'rb').read()
    return send_file(BytesIO(image_data), mimetype='image/png')


@app.route('/')
def home():
    return render_template("index.html")


# 流式识别WebSocket服务
async def stream_server_run(websocket, path):
    logger.info(f'有WebSocket连接建立：{websocket.remote_address}')
    # 寻找空闲的预测器
    use_predictor = None
    for predictor in predictors:
        if predictor.running: continue
        use_predictor = predictor
        use_predictor.running = True
        break
    if use_predictor is not None:
        frames = []
        score, text = 0, ""
        while not websocket.closed:
            try:
                data = await websocket.recv()
                frames.append(data)
                if len(data) == 0: continue
                is_end = False
                # 判断是不是结束预测
                if b'end' == data[-3:]:
                    is_end = True
                    data = data[:-3]
                # 开始预测
                result = use_predictor.predict_stream(audio_data=data, use_pun=args.use_pun, is_itn=args.is_itn,
                                                      is_end=is_end)
                if result is not None:
                    score, text = result['score'], result['text']
                send_data = str({"code": 0, "result": text}).replace("'", '"')
                logger.info(f'向客户端发生消息：{send_data}')
                await websocket.send(send_data)
                # 结束了要关闭当前的连接
                if is_end: await websocket.close()

            except Exception as e:
                logger.error(f'识别发生错误：错误信息：{e}')
                try:
                    await websocket.send(str({"code": 2, "msg": "recognition fail!"}).replace("'", '"'))
                except:
                    pass

        # 重置流式识别
        use_predictor.reset_stream()
        use_predictor.running = False
        # 保存录音
        save_dir = os.path.join(args.save_path, datetime.now().strftime('%Y-%m-%d'))
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, f'{int(time.time() * 1000)}.wav')
        audio_bytes = b''.join(frames)
        wf = wave.open(file_path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(audio_bytes)
        wf.close()
    else:
        logger.error(f'语音识别失败，预测器不足')
        await websocket.send(str({"code": 1, "msg": "recognition fail, no resource!"}).replace("'", '"'))
        await websocket.close()


# 因为有多个服务需要使用线程启动
def start_server_thread():
    # host: 127.0.0.1   port:5000
    app.run(host=args.host, port=args.port_server)


if __name__ == '__main__':
    # 创建多个语音识别器
    # num_websocket_p: WebSocket同时连接的数量， 创建多个预测器用于并发语音识别
    for _ in range(args.num_websocket_p - 1):
        predictor = PPASRPredictor(configs=args.configs,
                                   model_path=args.model_path,
                                   use_gpu=args.use_gpu,
                                   use_pun=args.use_pun,
                                   pun_model_dir=args.pun_model_dir)
        predictors.append(predictor)
    # 语音识别后，创建保存路径
    if not os.path.exists(args.save_path):
        os.makedirs(args.save_path)

    # 启动web服务   127.0.0.1:5000
    _thread.start_new_thread(start_server_thread, ())
    logger.warning('因为是多进程，所以第一次访问比较慢是正常，后面速度就会恢复了！')
    # 启动Flask服务   127.0.0.1:5001
    server = websockets.serve(stream_server_run, args.host, args.port_stream)
    # 启动WebSocket服务
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()
