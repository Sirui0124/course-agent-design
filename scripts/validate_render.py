#!/usr/bin/env python3
"""Validate course-agent JSON and optionally render its exact five-column table."""
import argparse,json,re
from pathlib import Path

def validate(d):
    def require(ok,msg):
        if not ok: raise ValueError(msg)
    require(d.get('schema_version')=='course-agent-design-v1','schema_version不匹配')
    require(bool(d.get('course')) and bool(d.get('scope')),'缺课程名或范围')
    sources=d.get('source_facts',[]); ids=[s.get('id') for s in sources]
    require(bool(ids) and len(set(ids))==len(ids),'来源为空或ID重复')
    for s in sources: require(bool(re.match(r'https?://',s.get('url',''))),'来源URL无效')
    rows=d.get('domains',[]); require(bool(rows),'domains为空')
    require(len({r.get('id') for r in rows})==len(rows),'领域ID重复')
    require(len({r.get('name') for r in rows})==len(rows),'领域名称重复')
    for r in rows:
        label=r.get('id','未知领域')
        for k in ['id','name','definition']:require(bool(r.get(k)),f'{label}: 缺{k}')
        rub=r.get('rubric',[])
        require([x.get('level') for x in rub]==[f'L{i}' for i in range(1,7)],f'{label}: rubric须按L1-L6恰好六项')
        require(all(isinstance(x.get('standard'),str) and x['standard'].strip() for x in rub),f'{label}: 空评价标准')
        require(len({x['standard'] for x in rub})==6,f'{label}: 六级标准重复')
        require(r.get('initial_level') in [f'L{i}' for i in range(7)],f'{label}: 初始级别无效')
        require(r.get('target_level') in ['L3','L4','L5','L6'],f'{label}: 目标级别无效')
        require(r.get('initial_basis',{}).get('type') in ['planning_assumption','diagnostic_evidence'],f'{label}: 缺初始依据类型')
        require(bool(r.get('initial_basis',{}).get('note')),f'{label}: 缺初始依据')
        require(r.get('target_basis',{}).get('type') in ['ai_design_suggestion','teacher_explicit','user_configuration'],f'{label}: 缺目标依据类型')
        require(bool(r.get('target_basis',{}).get('note')),f'{label}: 缺目标依据')
        mapping=r.get('source_mapping',[]);require(bool(mapping),f'{label}: 缺来源映射')
        for m in mapping:
            require(m.get('source_id') in ids and bool(m.get('section')),f'{label}: 来源映射不可解析')
            require(m.get('coverage') in ['required','optional','purpose'],f'{label}: coverage无效')
    return len(rows)

def render(d):
    def cell(x): return str(x).replace('&','&amp;').replace('|','&#124;').replace('\n','<br>')
    lines=[f"# {d['course']}：课程Agent五列表格",'',d['scope'],'',d.get('interpretation_note',''),'']
    for s in d['source_facts']:
        lines.append(f"来源：[{s['institution']}·{s['title']}]({s['url']})；{s['hours']}学时；核验日期{s['accessed_at']}。")
    lines+=['','初始级别均按每行initial_basis解释；本示例没有学生实测。目标以上标准为扩展，不表示本学期全部必达。L0是本技能的规划扩展，非布鲁姆原始等级。','','| 知识领域 | 定义 | L1-L6评估标准（json数组） | 初始级别 | 目标级别 |','|---|---|---|---|---|']
    for r in d['domains']:
        v=[r['name'],r['definition'],json.dumps(r['rubric'],ensure_ascii=False,separators=(',',':')),r['initial_level'],r['target_level']]
        lines.append('| '+' | '.join(cell(x) for x in v)+' |')
    lines+=['','未核实事项：'+'；'.join(d.get('uncertainties',[])),'']
    return '\n'.join(lines)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('--markdown');a=p.parse_args()
    try:
        d=json.loads(Path(a.input).read_text());n=validate(d)
        if a.markdown:Path(a.markdown).write_text(render(d))
    except (ValueError,KeyError,TypeError) as e:p.exit(1,f'校验失败: {e}\n')
    print(f'通过：{d["course"]}，{n}领域，{n*6}条标准。结构校验不代表教学效度验证。')
