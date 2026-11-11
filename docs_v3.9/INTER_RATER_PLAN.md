# 评判者信度实验方案（Inter-Rater Reliability Study）

**目的**：补上心秩学目前最大的硬伤——**172/172 只证明内部一致性，不证明外部有效性**。
**版本**：v3.9 · **日期**：2026-09-02

---

## 一、为什么必须做这个实验

评审的硬伤说得准确：

> 每个案例的慈秩博工定级是人工预先写进 JSON 的，预期结论也是人工预设的。
> 输入就是结论，算法只是给预判做了层算术包装。

消融实验和敏感性分析缓解了这个问题（它们确实推翻过我们自己的规则），但**没有解决它**。
维度定级这个输入依然是作者自己给的。

**唯一的补救办法**：让不了解这套体系的人独立给同一批案例定级，看他们和体系、以及彼此之间，
能在多大程度上达成一致。这就是评判者信度（inter-rater reliability）。

**它同时补三处**：

| 用途      | 补什么                         |
| ------- | --------------------------- |
| 北核论文    | 外部有效性                       |
| AI 对齐论文 | 标注一致性（annotation agreement） |
| 体系本身    | **可证伪性**——这是从"自洽"走到"有效"的唯一桥 |

---

## 二、关键设计：双组对照（这一步让实验价值翻倍）

**不要只做一组。** 做两组，给的材料不同：

| 组            | 给什么材料                  | 预期    |
| ------------ | ---------------------- | ----- |
| **A 组**（实验组） | 四维定义 + 五步法 + 公理 + 判定规则 | 一致性较高 |
| **B 组**（对照组） | **只给四个维度的定义**，不给判定规则   | 一致性较低 |

### 这个对照证明了什么

如果 A 组一致性显著高于 B 组，说明：

> **降低评价任意性的不是"分了四个维度"，而是这套判定规则本身。**

这比单纯报告"kappa = 0.7"有力得多。它把一个可能被质疑为循环验证的实验，
变成了**对规则有效性的检验**：

- 如果规则没用，A 组和 B 组应该差不多 → 规则是装饰性的，体系的核心主张（五步法有效）被推翻
- 如果 A 组显著更高 → 规则确实在降低任意性，且效应可量化

**这正是预印本 §8.1 里写的第一个可证伪条件。**

---

## 三、评判者不需要懂哲学

### 关键认知

**实验测的不是评判者的哲学水平，而是"不同人按同一套规则能否得出相同定级"。**

所以评判者只需要：

1. 对历史人物有基本了解（高中以上通识水平即可）
2. 愿意认真读 15 分钟规则
3. 能独立判断（不查资料、不讨论）

**工程师其实很合适**——他们习惯了按规格说明（spec）执行。

### 招募渠道（按推荐度）

| 渠道                              | 可得人数 | 成本  | 说明                                      |
| ------------------------------- | ---- | --- | --------------------------------------- |
| **工程师 / 技术社群**                  | 3–5  | 0   | 最容易启动。发内部群或技术社区，附网页链接                   |
| **LessWrong / Alignment Forum** | 5–10 | 0   | 对齐社区，对"可计算的价值框架"本身感兴趣，反馈质量最高            |
| **知乎 / Reddit 定向**              | 不定   | 0   | r/philosophy、r/AskHistorians；知乎历史话题活跃答主 |
| **Prolific**                    | 20+  | 付费  | 学术界标准平台，数据最干净，适合正式论文                    |

**建议起步配置**：A 组 5 人 + B 组 5 人 = 10 人。
样本量小也能出结果（配合 bootstrap 置信区间），正式论文再考虑扩到 20+。

---

## 四、实验材料

### 4.1 案例集：20–25 个，约 20 分钟填完

**选取原则**（不是随便挑，要覆盖不同的判定难度）：

| 类别        | 数量  | 例子                 | 为什么选                       |
| --------- | --- | ------------------ | -------------------------- |
| **争议度低**  | 5   | 孔子、董卓、释迦牟尼         | 基线——这些应该高度一致，用来测"实验本身是否正常" |
| **争议度中**  | 8   | 隋炀帝、王安石、乔布斯、商鞅     | 主体战场——能看出规则是否真的在起作用        |
| **争议度高**  | 7   | 成吉思汗、美国制宪先贤、马克思、尼采 | 最锋利的部分——如果这里都能有中等一致，说服力最强  |
| **触底线案例** | 5   | 纳粹德国、奴隶种植园、华盛顿     | **测 A2 是否真的不随视角改变**        |

**注意**：争议度低的案例如果一致性反而低，说明材料写得有问题（规则没讲清楚），
这时应该修材料重做，而不是硬着头皮报告结果。

### 4.2 需要收集的数据

每个案例，评判者填：

1. **四维定级**：慈 / 秩 / 博 / 工 各选一档（无 / 普世以下 / 普世 / 精英 / 至圣）
2. **是否有确凿的主动背离善意证据**（是/否）——用于测 Ci 归零判据
3. **是否触发绝对人道底线**（是/否）——**这是最关键的，用于测不变量**
4. **贡献与破坏的粗略量级**（0–10 滑块）
5. **置信度**（0–1）
6. **填写耗时**（自动记录）

### 4.3 不需要收集的

- 不要问"你觉得这个人好不好"——那是综合打分，正是体系反对的
- 不要问开放式理由——开放式文本无法算 kappa，且会大幅增加填写负担
  （可以 optional 加一栏，但不用于统计）

---

## 五、统计方法

### 5.1 主指标

**加权 Cohen's kappa**（定级是有序分档，用线性加权 kappa 比普通 kappa 更合适）

- 逐对计算（pairwise），取平均
- 或直接用 **Krippendorff's alpha**（更适合多评判者 + 有序数据，是内容分析的标准做法）

**报告格式**（学术界惯例）：

| 维度           | A 组 α | B 组 α | 差值    |
| ------------ | ----- | ----- | ----- |
| 慈            |       |       |       |
| 秩            |       |       |       |
| 博            |       |       |       |
| 工            |       |       |       |
| **底线判定（二值）** |       |       | ← 最关键 |

### 5.2 判读标准

Krippendorff's alpha 的通行门槛：

| α         | 判读                  |
| --------- | ------------------- |
| ≥ 0.80    | 可靠（reliable）        |
| 0.67–0.80 | 可用于探索性结论（tentative） |
| < 0.67    | 不可靠                 |

**我们的预期与应对**：

- **底线判定 α 应该最高**——因为 A2 的判据是明确的（是否治理性/制度性剥夺），且它不依赖视角
- **四维定级 α 可能只有中等**（0.4–0.6）——这不要紧，**重要是 A > B**
- **如果底线判定 α 也低**——那 A2 的定义有问题，必须回去改公理，这是重大发现

### 5.3 补充分析

1. **A vs B 的差异显著性**：bootstrap 或 Mann-Whitney U
2. **逐维度看**：哪个维度最难达成一致？（我猜是"秩"，因为"有效性"最容易和"正当性"混淆）
3. **与体系输出的一致率**：评判者定级的众数 vs 体系输出
4. **置信度校准**：高置信度的判断是否真的更一致？

---

## 六、实施步骤

| 步骤  | 内容                             | 周期            |
| --- | ------------------------------ | ------------- |
| 1   | 定稿实验材料（两份说明书：A 组完整版、B 组仅维度定义版） | 1 天           |
| 2   | 做成网页表单或问卷（可嵌进现有网页，或用腾讯文档/问卷星）  | 1 天           |
| 3   | 招募（发渠道 + 等待）                   | **3–14 天，最长** |
| 4   | 数据清理（剔除明显乱填的：耗时过短、全部选同一档）      | 0.5 天         |
| 5   | 统计（脚本已附在下面）                    | 0.5 天         |
| 6   | 写进预印本 §6.3                     | 1 天           |

**关键路径是第 3 步**——所以这个实验要**最早启动**，让它在后台跑着，同时做别的事。

---

## 七、招募文案（可直接用）

### 版本 A：技术社群

> **招募：一个价值评判实验的参与者（20 分钟）**
> 
> 我做了一套"历史人物价值评判"的可计算框架（四维三层五步法），现在需要验证一件事：
> **不同人按同一套规则，能否得出相同的定级？**
> 
> 你不需要懂哲学，也不需要同意这套框架。只需要：
> 读 15 分钟规则说明 → 给 20 个历史人物定级 → 提交（约 20 分钟）
> 
> 你的数据会用于计算评判者间一致性系数，结果会公开在预印本里。
> 参与链接：[链接]
> 
> 补充：有一半参与者会拿到"简化版规则"（只有维度定义，没有判定流程）——
> 这是对照组，用来测判定规则本身有没有用。分到哪组是随机的。

### 版本 B：LessWrong / Alignment Forum（英文）

> **Call for participants: inter-rater reliability study on a pluralistic value
> assessment framework (20 min)**
> 
> I've built a computational framework for evaluating agents (persons, institutions,
> laws) across four independent dimensions, with a hard invariant constraint that
> priors may not override. I need to test whether independent raters, given the rules,
> converge.
> 
> You don't need to endorse the framework — you need to apply a spec.
> Read the rules (15 min) → grade 20 historical subjects (20 min) → submit.
> 
> Half of participants receive a reduced rule set (dimension definitions only, no
> adjudication procedure) as a control — this tests whether the procedure itself does
> any work, or whether the four dimensions alone explain the result.
> 
> Results (Krippendorff's alpha, per dimension) will be published in the preprint,
> including if they're unfavorable.

**最后那句很重要**——"结果不利也会公开"。

---

## 八、统计脚本（可直接使用）

```python
# -*- coding: utf-8 -*-
"""
评判者信度统计：Krippendorff's alpha + Cohen's kappa
用法：python irr_stats.py ratings.csv
ratings.csv 格式：rater,case,dimension,value
"""
import csv, itertools, math
from collections import defaultdict

LEVELS = ['无', '普世以下', '普世', '精英', '至圣']
IDX = {lv: i for i, lv in enumerate(LEVELS)}


def load(path):
    """返回 {dimension: {case: {rater: value}}}"""
    data = defaultdict(lambda: defaultdict(dict))
    with open(path, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row['value'] in IDX:
                data[row['dimension']][row['case']][row['rater']] = row['value']
    return data


def observed_disagreement(pairs):
    """序数数据的观测不一致度（平方差）"""
    if not pairs:
        return float('nan')
    return sum((a - b) ** 2 for a, b in pairs) / len(pairs)


def expected_disagreement(values):
    """期望不一致度：所有可能配对的平方差均值"""
    if len(values) < 2:
        return float('nan')
    ps = list(itertools.combinations(values, 2))
    return sum((a - b) ** 2 for a, b in ps) / len(ps)


def krippendorff_alpha(unit_ratings):
    """
    unit_ratings: {case: {rater: value}}，value 为整数等级
    返回 alpha（序数差的平方版）
    """
    Do = 0.0
    De = 0.0
    n_total = 0
    for case, rmap in unit_ratings.items():
        vals = [IDX[v] if isinstance(v, str) else v for v in rmap.values()]
        if len(vals) < 2:
            continue
        Do += observed_disagreement(list(itertools.combinations(vals, 2))) * len(vals)
        n_total += len(vals)
    if n_total == 0:
        return float('nan')
    Do /= n_total

    all_vals = [IDX[v] if isinstance(v, str) else v
                for rmap in unit_ratings.values() for v in rmap.values()]
    De = expected_disagreement(all_vals)
    if De == 0:
        return 1.0
    return 1.0 - Do / De


def cohens_kappa(r1, r2):
    """两个评判者之间的加权 kappa（线性权重）"""
    keys = sorted(set(r1) & set(r2))
    if not keys:
        return float('nan')
    a = [IDX[r1[k]] for k in keys]
    b = [IDX[r2[k]] for k in keys]
    maxv = len(LEVELS) - 1
    po = 1.0 - (sum(abs(x - y) for x, y in zip(a, b)) / (maxv * len(keys)))
    # 期望一致率
    from collections import Counter
    ca, cb = Counter(a), Counter(b)
    n = len(keys)
    pe = 1.0 - (sum(ca[i] * cb[j] * abs(i - j)
                    for i in range(maxv + 1) for j in range(maxv + 1))
                / (maxv * n * n))
    if pe == 1.0:
        return 1.0
    return (po - pe) / (1 - pe)


def report(data, group_name):
    print('=' * 72)
    print('%s · 评判者信度' % group_name)
    print('=' * 72)
    print('%-14s %10s %10s %10s' % ('维度', 'alpha', '平均kappa', 'n(案例)'))
    for dim in ['慈', '秩', '博', '工', '底线判定']:
        if dim not in data:
            continue
        ur = {c: {r: (int(v) if dim == '底线判定' else v) for r, v in rm.items()}
              for c, rm in data[dim].items()}
        if dim == '底线判定':
            # 二值：用简单 alpha（0/1 时平方差 = 0/1，等价于名义差异）
            pass
        a = krippendorff_alpha(ur)
        raters = sorted({r for rm in ur.values() for r in rm})
        ks = []
        for r1, r2 in itertools.combinations(raters, 2):
            common = {c: rm[r1] for c, rm in ur.items() if r1 in rm and r2 in rm}
            other = {c: rm[r2] for c, rm in ur.items() if r1 in rm and r2 in rm}
            if common:
                k = cohens_kappa(common, other)
                if not math.isnan(k):
                    ks.append(k)
        avg_k = sum(ks) / len(ks) if ks else float('nan')
        print('%-14s %10.3f %10.3f %10d'
              % (dim, a, avg_k, len(ur)))
    print()


def interpret(a):
    if math.isnan(a):
        return '数据不足'
    if a >= 0.80:
        return '可靠 (reliable)'
    if a >= 0.67:
        return '可用于探索性结论 (tentative)'
    return '不可靠 — 需修规则或材料'


if __name__ == '__main__':
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else 'ratings.csv'
    data = load(path)
    print()
    print('判读标准:  alpha >= 0.80 可靠 | 0.67-0.80 探索性 | < 0.67 不可靠')
    print()
    report(data, '全组')
    print('提示：把 A 组 / B 组数据分成两个 csv 分别跑，比较 alpha 差值。')
    print('      若 A 组 alpha 显著高于 B 组 → 判定规则确实在降低任意性。')
```

---

## 九、结果如何写进论文

### 9.1 如果结果好（A 组 α ≥ 0.67，且 A > B）

> Independent raters (n=X), applying the framework's rules without author involvement,
> achieved Krippendorff's alpha of α_A on dimensional grading. Raters given only the
> dimension definitions — without the adjudication procedure — achieved α_B.
> The gap (α_A − α_B) indicates that the reduction in arbitrariness is attributable to
> the procedure, not merely to the dimensional decomposition.

### 9.2 如果结果不好（两组差不多，或 α 都低）

**不要藏。** 这是真正的发现，而且它直接指向体系该怎么改：

> The procedure did not improve agreement over dimensional decomposition alone.
> This indicates either (a) the adjudication rules are under-specified at the point of
> dimensional grading, or (b) dimensional grading is irreducibly standpoint-dependent,
> in which case the framework's claim to reduce arbitrariness via procedure is refuted
> and must be reconceived as a tool for making disagreement explicit rather than
> resolving it.

第二种写法反而更诚实，而且它**依然有价值**——"让分歧可见"本来就是你的核心主张之一。
预印本 §8.1 已经写明了"如果规则加不了分，说明规则是装饰性的"，所以结果不好也在预期内。
