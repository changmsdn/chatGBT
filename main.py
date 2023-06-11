import _thread
import argparse
import asyncio
import functools
import sys
import json
import xmltodict
import shutil
import time
import wave
from datetime import datetime
from typing import List

import websockets
from flask import request, Flask, render_template, send_file, jsonify
from io import BytesIO
from flask_cors import CORS
from concurrent.futures import ProcessPoolExecutor

from ppasr.predict import PPASRPredictor
from ppasr.utils.logger import setup_logger
from ppasr.utils.utils import add_arguments, print_arguments
from bt_instruction2bt_mapper.instruction2bt import *
from bt_instruction2bt_mapper.bt_tools import *
from bt_language_parser.parser import *

logger = setup_logger(__name__)

parser = argparse.ArgumentParser(description=__doc__)
add_arg = functools.partial(add_arguments, argparser=parser)
add_arg('configs', str, 'third_party/ppasr-zh/configs/conformer.yml', "配置文件")
add_arg("host", str, '0.0.0.0', "监听主机的IP地址")
add_arg("port_server", int, 5000, "普通识别服务所使用的端口号")
add_arg("port_stream", int, 5001, "流式识别服务所使用的端口号")
add_arg("save_path", str, 'bt_language_parser/audio_dataset/upload/', "上传音频文件的保存目录")
add_arg('use_gpu', bool, False, "是否使用GPU预测")
add_arg('use_pun', bool, False, "是否给识别结果加标点符号")
add_arg('is_itn', bool, False, "是否对文本进行反标准化")
add_arg('num_web_p', int, 1, "多少个预测器，这个是Web服务并发的数量，必须大于等于1")
add_arg('num_websocket_p', int, 1, "多少个预测器，这个是WebSocket同时连接的数量，必须大于等于1")
add_arg('model_path', str, 'third_party/ppasr-zh/models/conformer_streaming_fbank/infer', "导出的预测模型文件路径")
add_arg('pun_model_dir', str, 'third_party/ppasr-zh/models/pun_models/', "加标点符号的模型文件夹路径")
args = parser.parse_args()
print_arguments(args=args)

app = Flask('PPASR', template_folder="third_party/ppasr-zh/templates", static_folder="third_party/ppasr-zh/static",
            static_url_path="/")
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


@app.route('/')
def home():
    return render_template("index.html")


dir_bt_temp = "bt_library/family_service/tasks_reuse/temp/"
dir_bt = "bt_library/tasks_reuse/"
dir_bt_img = "bt_library/family_service/tasks_reuse/images/"


@app.route('/bt_save', methods=['POST'])
def bt_save():
    bt_data = request.data.decode('utf-8')  # 获取前端发送的文本信息
    bt_data = json.loads(bt_data)
    save_desc = bt_data['desc']
    print("客户端请求描述：" + save_desc)
    # 将 temp的图片所有文件改名保存到另一个文件中
    # 1 检查目标目录是否存在，如果不存在则创建它
    dest_dir = dir_bt_img + save_desc.replace(" ", "_")
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    # 2 获取源目录中的所有文件
    files = os.listdir(dir_bt_temp)
    # 3 遍历所有文件并重命名复制过去
    for file_name in files:
        source_file = os.path.join(dir_bt_temp, file_name)  # 构造源文件路径和目标文件路径
        if source_file.endswith("dot"):
            dest_file = os.path.join(dest_dir, f"{save_desc.replace(' ', '_')}" + ".dot")
            if dest_file is not None:  # 重命名文件并保存到指定路径
                shutil.copyfile(source_file, dest_file)
        elif source_file.endswith("png"):
            dest_file = os.path.join(dest_dir, f"{save_desc.replace(' ', '_')}" + ".png")
            if dest_file is not None:
                shutil.copyfile(source_file, dest_file)
        elif source_file.endswith("svg"):
            dest_file = os.path.join(dest_dir, f"{save_desc.replace(' ', '_')}" + ".svg")
            if dest_file is not None:
                shutil.copyfile(source_file, dest_file)
        # 重用行为树
        elif source_file.endswith("xml"):
            dest_file = os.path.join(dir_bt, f"{save_desc.replace(' ', '_')}" + ".xml")
            # 重命名文件并保存到指定路径
            if dest_file is not None:
                shutil.copyfile(source_file, dest_file)
            # 读取这个dest_file，将 temp 标签改成用户定义的 name
            tree = ET.parse(dest_file)
            root = tree.getroot()[0]  # 得到根标签
            root.set('name', save_desc.replace(' ', '_'))
            root_name = save_desc.replace("_", " ")
            tree.write(dest_file)
            # 优化 bt_language_parser
            jieba.add_word(root_name)
            if is_chinese(root_name):
                root_vector = nlp_zh_md(root_name).vector
            else:
                root_vector = nlp_en_md(root_name).vector
            dict = {'root_name': save_desc.replace(' ', '_'), "root_vector": root_vector}
            reuses_info.append(dict)
    # 4 图片保存成功，将 XML 可重用保存到 bt_library 库
    return jsonify({"bt": None, "desc": "SUCCESS"})


@app.route('/bt_text2bt', methods=['POST'])
def bt_text2bt():
    bt_data = request.data.decode('utf-8')  # 获取前端发送的文本信息
    bt_data = json.loads(bt_data)
    bt = bt_data['bt']
    text = bt_data['desc']
    if bt is not None:
        tree = ET.parse(dir_bt_temp+"temp.xml")
        root = tree.getroot()[0][0]
        bt = xml2bt(root)
    # 调用text_to_bt函数转化为响应的行为树。
    bt, bt_desc = text_to_bt(text, bt)
    print(bt)
    print(bt_desc)
    bt_xml_dict = None
    if bt is not None:
        # 将 bt 保存到 temp_img中
        save_bt2xml(bt, "temp", dir_bt_temp + 'temp.xml')
        py_trees.display.render_dot_tree(bt, name="temp", target_directory=dir_bt_temp)
        with open(dir_bt_temp + 'temp.xml') as file:
            bt_xml_dict = xmltodict.parse(file.read())
    data = {
        "bt": bt_xml_dict,
        "desc": bt_desc
    }
    return jsonify(data)


@app.route('/bt_image', methods=['GET'])
def bt_image():
    image_data = open(dir_bt_temp + "/temp.png", 'rb').read()
    return send_file(BytesIO(image_data), mimetype='image/png')


@app.route('/help_content', methods=['GET'])
def get_help_content():
    content = "*" * 30 + " 已保存的行为树 " + "*" * 30 + "\n"
    content += "name: " + ", ".join([str(reuse_info['root_name']) for reuse_info in reuses_info]) + "\n"

    content += "\n" + "*" * 30 + " 可用的控制节点 " + "*" * 30 + "\n"
    content += "name: " + ", ".join([str(controller_info['root_name']) for controller_info in controllers_info]) + "\n"
    content += "synonyms:\n"
    for controller_info in controllers_info:
        synonyms_list = []
        for synonyms in controller_info['synonyms']:
            jieba.add_word(synonyms['synonyms_name'])
            synonyms_list.append(synonyms['synonyms_name'])
        content += str(controller_info['root_name']) + ": " + str(synonyms_list) + "\n"

    content += "\n" + "*" * 30 + " 可用的条件节点 " + "*" * 30 + "\n"
    content += "name: " + ", ".join([str(condition_info['root_name']) for condition_info in conditions_info]) + "\n"
    content += "synonyms:\n"
    for condition_info in conditions_info:
        synonyms_list = []
        for synonyms in condition_info['synonyms']:
            jieba.add_word(synonyms['synonyms_name'])
            synonyms_list.append(synonyms['synonyms_name'])
        content += str(condition_info['root_name']) + ": " + str(synonyms_list) + "\n"

    content += "\n" + "*" * 30 + " 可用的行为节点 " + "*" * 30 + "\n"
    content += "name: " + ", ".join([str(action_info['root_name']) for action_info in actions_info]) + "\n"
    content += "synonyms:\n"
    for action_info in actions_info:
        synonyms_list = []
        for synonyms in action_info['synonyms']:
            jieba.add_word(synonyms['synonyms_name'])
            synonyms_list.append(synonyms['synonyms_name'])
        content += str(action_info['root_name']) + ": " + str(synonyms_list) + "\n"
    return jsonify({"code": 0, "msg": "success", "content": content})


# 流式识别 WebSocket服务
async def stream_server_run(websocket, path):
    logger.info(f'有WebSocket连接建立：{websocket.remote_address}')
    # 寻找空闲的预测器
    use_predictor = None
    for predictor2 in predictors:
        if predictor2.running: continue
        use_predictor = predictor2
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
    app.run(host=args.host, port=args.port_server)


if __name__ == '__main__':
    # 实时语音识别所以要这样处理
    for _ in range(args.num_websocket_p - 1):
        predictor1 = PPASRPredictor(configs=args.configs,
                                    model_path=args.model_path,
                                    use_gpu=args.use_gpu,
                                    use_pun=args.use_pun,
                                    pun_model_dir=args.pun_model_dir)
        predictors.append(predictor1)
    # 创建保存路径
    if not os.path.exists(args.save_path):
        os.makedirs(args.save_path)

    # 启动 web 服务
    _thread.start_new_thread(start_server_thread, ())
    logger.warning('因为是多进程，所以第一次访问比较慢是正常，后面速度就会恢复了！')
    # 启动Flask服务
    server = websockets.serve(stream_server_run, args.host, args.port_stream)
    # 启动WebSocket服务
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()
