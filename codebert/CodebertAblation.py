import os
import tqdm
import random
import pandas as pd
from util.io_util import *
from util.github_util import *
from transformers import RobertaTokenizer

tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")

def count_tokens(text):
    tokens = tokenizer.encode(text)
    return len(tokens)


class CodeBertAblation:

    def __init__(self, module_root_path: str, cve_data_all: dict, candidates: dict, correct_commits: dict):
        self.module_root_path = module_root_path
        self.cve_data_all = cve_data_all
        self.correct_commits = correct_commits

        os.makedirs(module_root_path, exist_ok = True)

        os.makedirs(f'{module_root_path}/file_content', exist_ok = True)
        self.pos_content_path = f'{module_root_path}/file_content/pos'
        os.makedirs(self.pos_content_path, exist_ok = True)
        self.neg_content_path = f'{module_root_path}/file_content/neg'
        os.makedirs(self.neg_content_path, exist_ok = True)

        positive_label_list_path = f'{self.module_root_path}/positive_label_list'
        if not os.path.exists(f'{positive_label_list_path}.pkl'):
            self.positive_label_list = [
                (cve, repo, file)
                for cve, v in candidates.items()
                for repo, files in v.items()
                if len(files) > 1 and cve in correct_commits and repo in correct_commits[cve]
                for file in files
                if file == correct_commits[cve][repo]
            ]
            save_text(f'{self.module_root_path}/positive_label_list', self.positive_label_list)
            save_pickle(f'{self.module_root_path}/positive_label_list.pkl', self.positive_label_list)
        else:
            self.positive_label_list = load_pickle(f'{positive_label_list_path}.pkl')
        
        negtive_label_list_path = f'{self.module_root_path}/negtive_label_list'
        if not os.path.exists(f'{negtive_label_list_path}.pkl'):
            self.negtive_label_list = [
                (cve, repo, file)
                for cve, v in candidates.items()
                for repo, files in v.items()
                if len(files) > 1
                for file in files
                if not (cve in correct_commits and repo in correct_commits[cve]) or file != correct_commits[cve][repo]
            ]
            save_text(f'{self.module_root_path}/negtive_label_list', self.negtive_label_list)
            save_pickle(f'{self.module_root_path}/negtive_label_list.pkl', self.negtive_label_list)
        else:
            self.negtive_label_list = load_pickle(f'{negtive_label_list_path}.pkl')

        print(len(self.positive_label_list))
        print(len(self.negtive_label_list))


    def start(self):
        # self.scrapy_file_content()

        # self.select_training_and_test_set()
        # for i in range(5):
        #     print(f'round {i}')
        #     self.generate_data_set(
        #         load_pickle(f'{self.module_root_path}/tmp/training_set_{i}.pkl'),
        #         f'{self.module_root_path}/training_set_{i}.csv'
        #     )
        #     self.generate_data_set(
        #         load_pickle(f'{self.module_root_path}/tmp/test_set_{i}.pkl'),
        #         f'{self.module_root_path}/test_set_{i}.csv'
        #     )
        # self.check_result()

        self.check_recall()


    def scrapy_file_content(self):
        def get_gt_file_sub(to_scrapy_list_sub: list, token: str):
            for (cve, repo, file) in tqdm.tqdm(to_scrapy_list_sub):
                dir = f'{target_path}/{cve}'
                tp1 = repo.replace('/', '\\')
                tp2 = file.replace('/', '\\')
                save_path = f'{dir}/{tp1}____{tp2}'
                if os.path.exists(save_path):
                    continue
                sha = ''
                for repo2, sha2 in self.cve_data_all[cve]['collected_commit']:
                    if repo2 == repo:
                        sha = sha2
                        break
                if not sha:
                    print('error4321', cve, repo)
                res = get_file_content(repo, sha, file, token)
                if res:
                    # print(save_path)
                    os.makedirs(dir, exist_ok = True)
                    save_text(save_path, res)
                else:
                    print('error233', cve, repo, file)

        target_path = self.pos_content_path
        multi_thread(self.positive_label_list, get_gt_file_sub, tokens = github_tokens)
        
        target_path = self.neg_content_path
        multi_thread(self.negtive_label_list, get_gt_file_sub, tokens = github_tokens)


    def select_training_and_test_set(self):
        print('start select training and test set')
        os.makedirs(f'{self.module_root_path}/tmp', exist_ok = True)
        res = self.random_split(self.positive_label_list, 5)
        for i in range(5):
            print(f'round {i}')
            # res[i]作为测试集
            test_set_pos = res[i]
            training_set_pos = []
            for j in range(5):
                if i != j:
                    training_set_pos += res[j]
            print(len(test_set_pos), len(training_set_pos))
            training_set_neg = set()
            print('start select training_set_neg')
            tp = [ (cve, file.split('____')[0].replace('\\', '/'), file.split('____')[1].replace('\\', '/'))
                for cve, _, _ in training_set_pos
                if os.path.exists(f'{self.neg_content_path}/{cve}')
                for file in os.listdir(f'{self.neg_content_path}/{cve}')
                if file not in ['.DS_Store']
            ]
            print(f'training_set_neg total size: {len(tp)}')
            training_set_neg = random.sample(tp, len(training_set_pos))
            print('end select training_set_neg')

            print('start select test_set_neg')
            # 这里没有100倍数量的负样本，所有都用上
            test_set_neg = [ (cve, file.split('____')[0].replace('\\', '/'), file.split('____')[1].replace('\\', '/'))
                for cve, _, _ in test_set_pos
                if os.path.exists(f'{self.neg_content_path}/{cve}')
                for file in os.listdir(f'{self.neg_content_path}/{cve}')
                if file not in ['.DS_Store']
            ]
            print(f'test_set_neg total size: {len(test_set_neg)}')
            print('end select test_set_neg')
            training_set_pos = [
                (cve, repo, file, 1)
                for cve, repo, file in training_set_pos
            ]
            training_set_neg = [
                (cve, repo, file, 0)
                for cve, repo, file in training_set_neg
            ]
            test_set_pos = [
                (cve, repo, file, 1)
                for cve, repo, file in test_set_pos
            ]
            test_set_neg = [
                (cve, repo, file, 0)
                for cve, repo, file in test_set_neg
            ]
            training_set = training_set_pos + training_set_neg
            test_set = test_set_pos + test_set_neg
            save_text(f'{self.module_root_path}/tmp/training_set_{i}', training_set)
            save_pickle(f'{self.module_root_path}/tmp/training_set_{i}.pkl', training_set)
            save_text(f'{self.module_root_path}/tmp/test_set_{i}', test_set)
            save_pickle(f'{self.module_root_path}/tmp/test_set_{i}.pkl', test_set)
        print('end select training and test set')


    def random_split(self, data: list, parts: int):
        random.shuffle(data)
        block_size = int(len(data) / parts)
        res = []
        for i in range(parts):
            l = i * block_size
            r = l + block_size
            if i == parts - 1:
                r = len(data)
            res.append(data[l:r])
        return res


    def generate_data_set(self, data_set: list, target: str):
        df = pd.DataFrame({
            'sentence': [],
            'label': [],
        })
        for cve, repo, file, label in tqdm.tqdm(data_set):
            file_name = repo.replace('/', '\\') + '____' + file.replace('/', '\\')
            file_path = f'{self.pos_content_path}/{cve}/{file_name}' if label == 1 else f'{self.neg_content_path}/{cve}/{file_name}'
            if not os.path.exists(file_path):
                print(f'file not exist: {file_path}')
                continue
            
            desc = self.cve_data_all[cve]['complete_description'] if 'complete_description' in self.cve_data_all[cve] else self.cve_data_all[cve]['original_description']
            desc = desc[:400]   # 大约100个token
            try:
                content = load_file(file_path)
            except Exception as e:
                print(f'load {file_path} failure, {e}')
            # content = clear_comment(format_text(content, ' '))
            content = format_text(content, ' ')
            simplified_file_path = file_path.split('/')[-1].split('____')[1].replace('\\', '/')
            tp = f'{repo} <|endoftext|> {simplified_file_path} <|endoftext|> {desc} <|endoftext|> '
            rest_token = 500 - count_tokens(tp)
            r = 800
            step = 50
            content_len = len(content)
            while count_tokens(content[:r]) > rest_token:
                r -= step
                if r < 0:
                    r = 0
                    break
            while count_tokens(content[:r + step]) < rest_token:
                r += step
                if r > content_len:
                    break
            # print(f'real r: {r}')
            content = content[:r]
            df.loc[len(df)] = [
                f'{tp}{content}',
                label
            ]
        
        df.to_csv(
            target,
            index = False,
        )

    
    def check_result(self):
        print('start check')
        pos_cnt1 = 0
        pos_cnt2 = 0

        for i in range(5):
            df_training = pd.read_csv(f'{self.module_root_path}/training_set_{i}.csv')
            df_test = pd.read_csv(f'{self.module_root_path}/test_set_{i}.csv')
            print(f'round {i}: training size: {len(df_training)}, test size: {len(df_test)}')
            if len(df_training.columns) != 2 or len(df_test.columns) != 2:
                print('error! column != 2')
                sys.exit()
            for index, row in df_test.iterrows():
                if row.label == 1:
                    pos_cnt1 += 1
                tokens = count_tokens(row.sentence)
                if tokens > 505:
                    print(f'test_set_{i} {index} {tokens}')
            for index, row in df_training.iterrows():
                if row.label == 1:
                    pos_cnt2 += 1
                tokens = count_tokens(row.sentence)
                if tokens > 505:
                    print(f'training_set_{i} {index} {tokens}')

        print(f'positive cnt1: {pos_cnt1}')     # 应该等于1763
        print(f'positive cnt2: {pos_cnt2}')     # 应该等于1763 * 4
        print('end check')


    def check_recall(self):
        desc_to_cve_path = f'{self.module_root_path}/result/desc_to_cve.json'
        if os.path.exists(desc_to_cve_path):
            desc_to_cve = load_json(desc_to_cve_path)
        else:
            desc_to_cve = {}
            for cve in self.cve_data_all:
                desc = self.cve_data_all[cve]['complete_description'] if 'complete_description' in self.cve_data_all[cve] else self.cve_data_all[cve]['original_description']
                if desc[:400] not in desc_to_cve:
                    desc_to_cve[desc[:400]] = [cve]
                else:
                    desc_to_cve[desc[:400]].append(cve)
                    # print('error:', desc_to_cve[desc[:400]], cve)
            save_json(desc_to_cve_path, desc_to_cve)

        rank_path = f'{self.module_root_path}/result/rank.json'
        if os.path.exists(rank_path):
            rank = load_json(rank_path)
        else:
            rank = {}
            for i in range(5):
                df = pd.read_csv(f'{self.module_root_path}/test_set_{i}.csv')
                socres = load_file(f'{self.module_root_path}/result/codebert{i}/test_prob')
                socres = socres.strip().split('\n')

                for index, (_, row) in enumerate(df.iterrows()):
                    repo = row.sentence.split(' <|endoftext|> ')[0]
                    file = row.sentence.split(' <|endoftext|> ')[1]
                    desc = row.sentence.split(' <|endoftext|> ')[2]
                    cves = desc_to_cve[desc]
                    if len(cves) == 1:
                        cve = cves[0]
                    else:
                        cve = 'CVE-2015-1812'
                    if cve not in rank:
                        rank[cve] = {}
                    if repo not in rank[cve]:
                        rank[cve][repo] = [(file, socres[index].split(' ')[1])]
                    else:
                        rank[cve][repo].append((file, socres[index].split(' ')[1]))
            
            for cve, v in rank.items():
                for repo, files in v.items():
                    rank[cve][repo] = sorted(files, key = lambda x: x[1], reverse = True)

            save_json(f'{self.module_root_path}/result/rank.json', rank)

        totoal_cnt = 0
        correct_cnt = [0] * 20
        for cve, v in rank.items():
            totoal_cnt += 1
            f = False
            for repo, files in v.items():
                if f: break
                if repo not in self.correct_commits[cve]: continue
                vul_file = self.correct_commits[cve][repo].lower()
                for index, (file, _) in enumerate(files):
                    if file.lower() == vul_file:
                        # print(cve, repo, index, file)
                        correct_cnt[index] += 1
                        f = True
                        break
        
        sum = 0
        for index in range(20):
            cnt = correct_cnt[index]
            sum += cnt / (index + 1)
            print(f'k = {index + 1}', '{:.2f}%'.format(sum / totoal_cnt * 100), f'({sum}/{totoal_cnt})')