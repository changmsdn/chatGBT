import argparse
import functools
import time

from ppasr.trainer import PPASRTrainer
from ppasr.utils.utils import add_arguments, print_arguments
from ppasr.infer_utils.pun_predictor import PunctuationPredictor

parser = argparse.ArgumentParser(description=__doc__)
add_arg = functools.partial(add_arguments, argparser=parser)
add_arg('configs',          str,   'configs/conformer.yml',     "配置文件")
add_arg("use_gpu",          bool,  True,                        "是否使用GPU评估模型")
add_arg("use_pun",          bool,  True,                        "是否使用标点符号")
add_arg('resume_model',     str,   'models/conformer_streaming_fbank/best_model/',  "模型的路径")
args = parser.parse_args()
print_arguments(args=args)


# 获取训练器
trainer = PPASRTrainer(configs=args.configs, use_gpu=args.use_gpu)

# 开始评估
start = time.time()
loss, error_result = trainer.evaluate(resume_model=args.resume_model, display_result=True)
end = time.time()
print('评估消耗时间：{}s，错误率：{:.5f}'.format(int(end - start), error_result))

pun_predictor = PunctuationPredictor(model_dir='models/pun_models')
result = pun_predictor('近几年不但我用书给女儿儿压岁也劝说亲朋不要给女儿压岁钱而改送压岁书')
print(result)
