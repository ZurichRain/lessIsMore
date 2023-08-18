#!/usr/bin/env python3
import os
import openai
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import time

if False:
    openai.api_base = "http://localhost:5000/v1"
else:
    openai.api_base = "http://openai.group-megvii-aic-research-hardware.megvii-aic.svc.hh-d.brainpp.local:5000/v1"
# openai.api_key = os.environ['OPENAI_API_KEY']
openai.api_key = 'sk-ZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSVV6STFOaUo5LmV5SjFjMlZ5Ym1GdFpTSTZJbmRoYm1kbVpXNW5NRGdpZlEuSWluWkRTRUtQa3hZclIxSm4ybklBNHU2YTlQQ2I4NXpkcGZ5bXkxdlFjWQ=='


CUR_ROOT="/data/lessIsMore/"
DATA_ROOT="/data/public/sharpwang/dataset/"

# def main(prompt):
#     sys_prompt = '''
#     You are an assistant who is very good at judging whether the information in a description is needed to answer a question
#     '''
    
#     try:
#         s = openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "system", "content": sys_prompt},
#                 {"role": "user", "content": prompt},
#             ]
#         )
#     except:
#         return main(prompt)
#     # print(s)
#     # print(s['choices'][0]['message']['content'])
#     return s

def main(prompt,id):
    sys_prompt = '''you are a helpful assistant'''
    
    try:
        s = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": prompt},
            ]
        )
    except:
        print("retry!")
        time.sleep(1)
        return main(prompt,id)
    # print(s)
    # print(s['choices'][0]['message']['content'])
    return {
        "gpt4" : s,
        "id" : id
    }


def run_main(workers, count):
    tasks = []
    with open('/data/dataset/LLaVA-Instruct-150K/conversation_58k.json','r') as f:
        data = json.load(f)
    description_lis = dict()
    for des_file in os.listdir('/data/lessIsMore/llava_descriptions/llava_descriptions_13b/conversation_58k'):
        # print(des_file)
        if description_lis.get(des_file.split('.')[0]):
            raise False
        with open('/data/lessIsMore/llava_descriptions/llava_descriptions_13b/conversation_58k/'+des_file,'r') as f:
            cdata=json.load(f)
        description_lis[des_file.split('.')[0]] = cdata['llava_description'].split('\n')[0]
        # import ipdb;ipdb.set_trace()
        # with open()
    # with open('/data/public/sharpwang/lessIsMore/llava_descriptions/complex_reasoning_77k','r')
    with open(CUR_ROOT+'instanceScore/openai-proxy/Clear_LLaVa/curid_conversation_check_accuary.txt','r') as f:
        sid = int(f.read().strip())
    with ThreadPoolExecutor(workers) as pool:
        for Pid in tqdm(range(sid,len(data),workers)):
            # if(len(os.listdir('/data/lessIsMore/clearDataLLaVa150k/LLaVA13b/Accuracy/conversation'))>=10000):
            #     break
            with open(CUR_ROOT+'instanceScore/openai-proxy/Clear_LLaVa/curid_conversation_check_accuary.txt','w') as f:
                f.write(str(Pid))
            print(Pid)
            tasks = []
            for ci in range(workers):
                i = Pid + ci
                if description_lis.get(data[i]['id']):
                    description = description_lis[data[i]['id']]
                else:
                    continue
                qas = ""
                for senidx in range(0,len(data[i]['conversations']),2):
                    question = data[i]['conversations'][senidx]['value'].replace('<image>','').replace('\n','')
                    answer = data[i]['conversations'][senidx+1]['value']
                    qas+='USER: '
                    qas+=question
                    qas+=' ASSISTANT: '
                    qas+=answer
                
                    
                    
                prompt = '''We would like to request your feedback on the performance of AI assistant in response to the instruction and the given input displayed following.
If you have an image described as follows:{}
And then you have some questions and answers like:{}
Please rate according to the accuracy of the response to the instruction and the input Each assistant receives a score on a scale of 0 to 5, where a higher score indicates higher level of the accuracy. Please first output a single line containing the value indicating the scores. In the subsequent line, please provide a comprehensive explanation of your evaluation, avoiding any potential bias.
                '''.format(description, qas)
                # import ipdb; ipdb.set_trace()
                print(prompt)
                main_param = {"prompt" : prompt,
                                "id" : data[i]['id']}
                tasks.append(pool.submit(main, **main_param))
                    # for task in tqdm(as_completed(tasks), total=len(tasks)):
            
            for task in tqdm(as_completed(tasks), total=len(tasks)):
                try:
                    print(task.result()['gpt4']['choices'][0]['message']['content'])
                except Exception as e:
                    print(e)
                    with open('/data/lessIsMore/instanceScore/openai-proxy/Clear_LLaVa/output_err/err_conversation_check_accuary.txt','w') as f:
                        f.write(str(e))
                    exit()

                output_path = CUR_ROOT+'clearDataLLaVa150k/LLaVA13b/Accuracy/conversation/'+task.result()['id']+'.json'
                print(output_path)
                with open(output_path,'w') as f:
                    f.write(json.dumps({
                        'id' : task.result()['id'],
                        'gpt4' : task.result()['gpt4']['choices'][0]['message']['content']
                    }))


def test_request():
    run_main(1, 1)



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--count", type=int, default=1)
    args = parser.parse_args()

    run_main(args.workers, args.count)

# vim: ts=4 sw=4 sts=4 expandtab
